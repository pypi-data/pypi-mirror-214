'''
# AWS Identity and Access Management Construct Library

Define a role and add permissions to it. This will automatically create and
attach an IAM policy to the role:

```python
role = Role(self, "MyRole",
    assumed_by=ServicePrincipal("sns.amazonaws.com")
)

role.add_to_policy(PolicyStatement(
    resources=["*"],
    actions=["lambda:InvokeFunction"]
))
```

Define a policy and attach it to groups, users and roles. Note that it is possible to attach
the policy either by calling `xxx.attachInlinePolicy(policy)` or `policy.attachToXxx(xxx)`.

```python
user = User(self, "MyUser", password=cdk.SecretValue.unsafe_plain_text("1234"))
group = Group(self, "MyGroup")

policy = Policy(self, "MyPolicy")
policy.attach_to_user(user)
group.attach_inline_policy(policy)
```

Managed policies can be attached using `xxx.addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))`:

```python
group = Group(self, "MyGroup")
group.add_managed_policy(ManagedPolicy.from_aws_managed_policy_name("AdministratorAccess"))
```

## Granting permissions to resources

Many of the AWS CDK resources have `grant*` methods that allow you to grant other resources access to that resource. As an example, the following code gives a Lambda function write permissions (Put, Update, Delete) to a DynamoDB table.

```python
# fn: lambda.Function
# table: dynamodb.Table


table.grant_write_data(fn)
```

The more generic `grant` method allows you to give specific permissions to a resource:

```python
# fn: lambda.Function
# table: dynamodb.Table


table.grant(fn, "dynamodb:PutItem")
```

The `grant*` methods accept an `IGrantable` object. This interface is implemented by IAM principlal resources (groups, users and roles) and resources that assume a role such as a Lambda function, EC2 instance or a Codebuild project.

You can find which `grant*` methods exist for a resource in the [AWS CDK API Reference](https://docs.aws.amazon.com/cdk/api/latest/docs/aws-construct-library.html).

## Roles

Many AWS resources require *Roles* to operate. These Roles define the AWS API
calls an instance or other AWS service is allowed to make.

Creating Roles and populating them with the right permissions *Statements* is
a necessary but tedious part of setting up AWS infrastructure. In order to
help you focus on your business logic, CDK will take care of creating
roles and populating them with least-privilege permissions automatically.

All constructs that require Roles will create one for you if don't specify
one at construction time. Permissions will be added to that role
automatically if you associate the construct with other constructs from the
AWS Construct Library (for example, if you tell an *AWS CodePipeline* to trigger
an *AWS Lambda Function*, the Pipeline's Role will automatically get
`lambda:InvokeFunction` permissions on that particular Lambda Function),
or if you explicitly grant permissions using `grant` functions (see the
previous section).

### Opting out of automatic permissions management

You may prefer to manage a Role's permissions yourself instead of having the
CDK automatically manage them for you. This may happen in one of the
following cases:

* You don't like the permissions that CDK automatically generates and
  want to substitute your own set.
* The least-permissions policy that the CDK generates is becoming too
  big for IAM to store, and you need to add some wildcards to keep the
  policy size down.

To prevent constructs from updating your Role's policy, pass the object
returned by `myRole.withoutPolicyUpdates()` instead of `myRole` itself.

For example, to have an AWS CodePipeline *not* automatically add the required
permissions to trigger the expected targets, do the following:

```python
role = iam.Role(self, "Role",
    assumed_by=iam.ServicePrincipal("codepipeline.amazonaws.com"),
    # custom description if desired
    description="This is a custom role..."
)

codepipeline.Pipeline(self, "Pipeline",
    # Give the Pipeline an immutable view of the Role
    role=role.without_policy_updates()
)

# You now have to manage the Role policies yourself
role.add_to_policy(iam.PolicyStatement(
    actions=[],
    resources=[]
))
```

### Using existing roles

If there are Roles in your account that have already been created which you
would like to use in your CDK application, you can use `Role.fromRoleArn` to
import them, as follows:

```python
role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::123456789012:role/MyExistingRole",
    # Set 'mutable' to 'false' to use the role as-is and prevent adding new
    # policies to it. The default is 'true', which means the role may be
    # modified as part of the deployment.
    mutable=False
)
```

## Configuring an ExternalId

If you need to create Roles that will be assumed by third parties, it is generally a good idea to [require an `ExternalId`
to assume them](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_create_for-user_externalid.html).  Configuring
an `ExternalId` works like this:

```python
role = iam.Role(self, "MyRole",
    assumed_by=iam.AccountPrincipal("123456789012"),
    external_ids=["SUPPLY-ME"]
)
```

## Principals vs Identities

When we say *Principal*, we mean an entity you grant permissions to. This
entity can be an AWS Service, a Role, or something more abstract such as "all
users in this account" or even "all users in this organization". An
*Identity* is an IAM representing a single IAM entity that can have
a policy attached, one of `Role`, `User`, or `Group`.

## IAM Principals

When defining policy statements as part of an AssumeRole policy or as part of a
resource policy, statements would usually refer to a specific IAM principal
under `Principal`.

IAM principals are modeled as classes that derive from the `iam.PolicyPrincipal`
abstract class. Principal objects include principal type (string) and value
(array of string), optional set of conditions and the action that this principal
requires when it is used in an assume role policy document.

To add a principal to a policy statement you can either use the abstract
`statement.addPrincipal`, one of the concrete `addXxxPrincipal` methods:

* `addAwsPrincipal`, `addArnPrincipal` or `new ArnPrincipal(arn)` for `{ "AWS": arn }`
* `addAwsAccountPrincipal` or `new AccountPrincipal(accountId)` for `{ "AWS": account-arn }`
* `addServicePrincipal` or `new ServicePrincipal(service)` for `{ "Service": service }`
* `addAccountRootPrincipal` or `new AccountRootPrincipal()` for `{ "AWS": { "Ref: "AWS::AccountId" } }`
* `addCanonicalUserPrincipal` or `new CanonicalUserPrincipal(id)` for `{ "CanonicalUser": id }`
* `addFederatedPrincipal` or `new FederatedPrincipal(federated, conditions, assumeAction)` for
  `{ "Federated": arn }` and a set of optional conditions and the assume role action to use.
* `addAnyPrincipal` or `new AnyPrincipal` for `{ "AWS": "*" }`

If multiple principals are added to the policy statement, they will be merged together:

```python
statement = iam.PolicyStatement()
statement.add_service_principal("cloudwatch.amazonaws.com")
statement.add_service_principal("ec2.amazonaws.com")
statement.add_arn_principal("arn:aws:boom:boom")
```

Will result in:

```json
{
  "Principal": {
    "Service": [ "cloudwatch.amazonaws.com", "ec2.amazonaws.com" ],
    "AWS": "arn:aws:boom:boom"
  }
}
```

The `CompositePrincipal` class can also be used to define complex principals, for example:

```python
role = iam.Role(self, "MyRole",
    assumed_by=iam.CompositePrincipal(
        iam.ServicePrincipal("ec2.amazonaws.com"),
        iam.AccountPrincipal("1818188181818187272"))
)
```

The `PrincipalWithConditions` class can be used to add conditions to a
principal, especially those that don't take a `conditions` parameter in their
constructor. The `principal.withConditions()` method can be used to create a
`PrincipalWithConditions` from an existing principal, for example:

```python
principal = iam.AccountPrincipal("123456789000").with_conditions({"StringEquals": {"foo": "baz"}})
```

> NOTE: If you need to define an IAM condition that uses a token (such as a
> deploy-time attribute of another resource) in a JSON map key, use `CfnJson` to
> render this condition. See [this test](./test/integ.condition-with-ref.ts) for
> an example.

The `WebIdentityPrincipal` class can be used as a principal for web identities like
Cognito, Amazon, Google or Facebook, for example:

```python
principal = iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
    "StringEquals": {"cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"},
    "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "unauthenticated"}
})
```

If your identity provider is configured to assume a Role with [session
tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html), you
need to call `.withSessionTags()` to add the required permissions to the Role's
policy document:

```python
iam.Role(self, "Role",
    assumed_by=iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
        "StringEquals": {
            "cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"
        },
        "ForAnyValue:StringLike": {
            "cognito-identity.amazonaws.com:amr": "unauthenticated"
        }
    }).with_session_tags()
)
```

## Parsing JSON Policy Documents

The `PolicyDocument.fromJson` and `PolicyStatement.fromJson` static methods can be used to parse JSON objects. For example:

```python
policy_document = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "FirstStatement",
        "Effect": "Allow",
        "Action": ["iam:ChangePassword"],
        "Resource": "*"
    }, {
        "Sid": "SecondStatement",
        "Effect": "Allow",
        "Action": "s3:ListAllMyBuckets",
        "Resource": "*"
    }, {
        "Sid": "ThirdStatement",
        "Effect": "Allow",
        "Action": ["s3:List*", "s3:Get*"
        ],
        "Resource": ["arn:aws:s3:::confidential-data", "arn:aws:s3:::confidential-data/*"
        ],
        "Condition": {"Bool": {"aws:_multi_factor_auth_present": "true"}}
    }
    ]
}

custom_policy_document = iam.PolicyDocument.from_json(policy_document)

# You can pass this document as an initial document to a ManagedPolicy
# or inline Policy.
new_managed_policy = iam.ManagedPolicy(self, "MyNewManagedPolicy",
    document=custom_policy_document
)
new_policy = iam.Policy(self, "MyNewPolicy",
    document=custom_policy_document
)
```

## Permissions Boundaries

[Permissions
Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
can be used as a mechanism to prevent privilege esclation by creating new
`Role`s. Permissions Boundaries are a Managed Policy, attached to Roles or
Users, that represent the *maximum* set of permissions they can have. The
effective set of permissions of a Role (or User) will be the intersection of
the Identity Policy and the Permissions Boundary attached to the Role (or
User). Permissions Boundaries are typically created by account
Administrators, and their use on newly created `Role`s will be enforced by
IAM policies.

It is possible to attach Permissions Boundaries to all Roles created in a construct
tree all at once:

```python
# Directly apply the boundary to a Role you create
# role: iam.Role

# Apply the boundary to an Role that was implicitly created for you
# fn: lambda.Function

# Remove a Permissions Boundary that is inherited, for example from the Stack level
# custom_resource: CustomResource
# This imports an existing policy.
boundary = iam.ManagedPolicy.from_managed_policy_arn(self, "Boundary", "arn:aws:iam::123456789012:policy/boundary")

# This creates a new boundary
boundary2 = iam.ManagedPolicy(self, "Boundary2",
    statements=[
        iam.PolicyStatement(
            effect=iam.Effect.DENY,
            actions=["iam:*"],
            resources=["*"]
        )
    ]
)
iam.PermissionsBoundary.of(role).apply(boundary)
iam.PermissionsBoundary.of(fn).apply(boundary)

# Apply the boundary to all Roles in a stack
iam.PermissionsBoundary.of(self).apply(boundary)
iam.PermissionsBoundary.of(custom_resource).clear()
```

## OpenID Connect Providers

OIDC identity providers are entities in IAM that describe an external identity
provider (IdP) service that supports the [OpenID Connect](http://openid.net/connect) (OIDC) standard, such
as Google or Salesforce. You use an IAM OIDC identity provider when you want to
establish trust between an OIDC-compatible IdP and your AWS account. This is
useful when creating a mobile app or web application that requires access to AWS
resources, but you don't want to create custom sign-in code or manage your own
user identities. For more information about this scenario, see [About Web
Identity Federation] and the relevant documentation in the [Amazon Cognito
Identity Pools Developer Guide].

The following examples defines an OpenID Connect provider. Two client IDs
(audiences) are will be able to send authentication requests to
[https://openid/connect](https://openid/connect).

```python
provider = iam.OpenIdConnectProvider(self, "MyProvider",
    url="https://openid/connect",
    client_ids=["myclient1", "myclient2"]
)
```

You can specify an optional list of `thumbprints`. If not specified, the
thumbprint of the root certificate authority (CA) will automatically be obtained
from the host as described
[here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html).

Once you define an OpenID connect provider, you can use it with AWS services
that expect an IAM OIDC provider. For example, when you define an [Amazon
Cognito identity
pool](https://docs.aws.amazon.com/cognito/latest/developerguide/open-id.html)
you can reference the provider's ARN as follows:

```python
import monocdk as cognito

# my_provider: iam.OpenIdConnectProvider

cognito.CfnIdentityPool(self, "IdentityPool",
    open_id_connect_provider_arns=[my_provider.open_id_connect_provider_arn],
    # And the other properties for your identity pool
    allow_unauthenticated_identities=False
)
```

The `OpenIdConnectPrincipal` class can be used as a principal used with a `OpenIdConnectProvider`, for example:

```python
provider = iam.OpenIdConnectProvider(self, "MyProvider",
    url="https://openid/connect",
    client_ids=["myclient1", "myclient2"]
)
principal = iam.OpenIdConnectPrincipal(provider)
```

## SAML provider

An IAM SAML 2.0 identity provider is an entity in IAM that describes an external
identity provider (IdP) service that supports the SAML 2.0 (Security Assertion
Markup Language 2.0) standard. You use an IAM identity provider when you want
to establish trust between a SAML-compatible IdP such as Shibboleth or Active
Directory Federation Services and AWS, so that users in your organization can
access AWS resources. IAM SAML identity providers are used as principals in an
IAM trust policy.

```python
iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
```

The `SamlPrincipal` class can be used as a principal with a `SamlProvider`:

```python
provider = iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
principal = iam.SamlPrincipal(provider, {
    "StringEquals": {
        "SAML:iss": "issuer"
    }
})
```

When creating a role for programmatic and AWS Management Console access, use the `SamlConsolePrincipal`
class:

```python
provider = iam.SamlProvider(self, "Provider",
    metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
)
iam.Role(self, "Role",
    assumed_by=iam.SamlConsolePrincipal(provider)
)
```

## Users

IAM manages users for your AWS account. To create a new user:

```python
user = iam.User(self, "MyUser")
```

To import an existing user by name [with path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names):

```python
user = iam.User.from_user_name(self, "MyImportedUserByName", "johnsmith")
```

To import an existing user by ARN:

```python
user = iam.User.from_user_arn(self, "MyImportedUserByArn", "arn:aws:iam::123456789012:user/johnsmith")
```

To import an existing user by attributes:

```python
user = iam.User.from_user_attributes(self, "MyImportedUserByAttributes",
    user_arn="arn:aws:iam::123456789012:user/johnsmith"
)
```

### Access Keys

The ability for a user to make API calls via the CLI or an SDK is enabled by the user having an
access key pair. To create an access key:

```python
user = iam.User(self, "MyUser")
access_key = iam.AccessKey(self, "MyAccessKey", user=user)
```

You can force CloudFormation to rotate the access key by providing a monotonically increasing `serial`
property. Simply provide a higher serial value than any number used previously:

```python
user = iam.User(self, "MyUser")
access_key = iam.AccessKey(self, "MyAccessKey", user=user, serial=1)
```

An access key may only be associated with a single user and cannot be "moved" between users. Changing
the user associated with an access key replaces the access key (and its ID and secret value).

## Groups

An IAM user group is a collection of IAM users. User groups let you specify permissions for multiple users.

```python
group = iam.Group(self, "MyGroup")
```

To import an existing group by ARN:

```python
group = iam.Group.from_group_arn(self, "MyImportedGroupByArn", "arn:aws:iam::account-id:group/group-name")
```

To import an existing group by name [with path](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html#identifiers-friendly-names):

```python
group = iam.Group.from_group_name(self, "MyImportedGroupByName", "group-name")
```

To add a user to a group (both for a new and imported user/group):

```python
user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');

user.add_to_group(group)
# or
group.add_user(user)
```

## Features

* Policy name uniqueness is enforced. If two policies by the same name are attached to the same
  principal, the attachment will fail.
* Policy names are not required - the CDK logical ID will be used and ensured to be unique.
* Policies are validated during synthesis to ensure that they have actions, and that policies
  attached to IAM principals specify relevant resources, while policies attached to resources
  specify which IAM principals they apply to.
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
    IConstruct as _IConstruct_5a0f9c5e,
    IDependable as _IDependable_1175c9f7,
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResolveContext as _IResolveContext_e363e2cb,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.AccessKeyProps",
    jsii_struct_bases=[],
    name_mapping={"user": "user", "serial": "serial", "status": "status"},
)
class AccessKeyProps:
    def __init__(
        self,
        *,
        user: "IUser",
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional["AccessKeyStatus"] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM access key.

        :param user: (experimental) The IAM user this key will belong to. Changing this value will result in the access key being deleted and a new access key (with a different ID and secret value) being assigned to the new user.
        :param serial: (experimental) A CloudFormation-specific value that signifies the access key should be replaced/rotated. This value can only be incremented. Incrementing this value will cause CloudFormation to replace the Access Key resource. Default: - No serial value
        :param status: (experimental) The status of the access key. An Active access key is allowed to be used to make API calls; An Inactive key cannot. Default: - The access key is active

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
            user = iam.User(self, "User")
            access_key = iam.AccessKey(self, "AccessKey", user=user)
            secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
            secretsmanager.Secret(self, "Secret",
                secret_string_beta1=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbe6acddff2cdc94d9b64a2ce1a7fdb2adfa8031ce287d3cb87983191a5e8696)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user": user,
        }
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def user(self) -> "IUser":
        '''(experimental) The IAM user this key will belong to.

        Changing this value will result in the access key being deleted and a new
        access key (with a different ID and secret value) being assigned to the new
        user.

        :stability: experimental
        '''
        result = self._values.get("user")
        assert result is not None, "Required property 'user' is missing"
        return typing.cast("IUser", result)

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''(experimental) A CloudFormation-specific value that signifies the access key should be replaced/rotated.

        This value can only be incremented. Incrementing this
        value will cause CloudFormation to replace the Access Key resource.

        :default: - No serial value

        :stability: experimental
        '''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional["AccessKeyStatus"]:
        '''(experimental) The status of the access key.

        An Active access key is allowed to be used
        to make API calls; An Inactive key cannot.

        :default: - The access key is active

        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["AccessKeyStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AccessKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_iam.AccessKeyStatus")
class AccessKeyStatus(enum.Enum):
    '''(experimental) Valid statuses for an IAM Access Key.

    :stability: experimental
    '''

    ACTIVE = "ACTIVE"
    '''(experimental) An active access key.

    An active key can be used to make API calls.

    :stability: experimental
    '''
    INACTIVE = "INACTIVE"
    '''(experimental) An inactive access key.

    An inactive key cannot be used to make API calls.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_iam.AddToPrincipalPolicyResult",
    jsii_struct_bases=[],
    name_mapping={
        "statement_added": "statementAdded",
        "policy_dependable": "policyDependable",
    },
)
class AddToPrincipalPolicyResult:
    def __init__(
        self,
        *,
        statement_added: builtins.bool,
        policy_dependable: typing.Optional[_IDependable_1175c9f7] = None,
    ) -> None:
        '''(experimental) Result of calling ``addToPrincipalPolicy``.

        :param statement_added: (experimental) Whether the statement was added to the identity's policies.
        :param policy_dependable: (experimental) Dependable which allows depending on the policy change being applied. Default: - Required if ``statementAdded`` is true.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_iam as iam
            
            # dependable: monocdk.IDependable
            
            add_to_principal_policy_result = iam.AddToPrincipalPolicyResult(
                statement_added=False,
            
                # the properties below are optional
                policy_dependable=dependable
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe0b7791b49f374eae9ddd4592e3e27bd665823872e35acb72e3d36c0159389a)
            check_type(argname="argument statement_added", value=statement_added, expected_type=type_hints["statement_added"])
            check_type(argname="argument policy_dependable", value=policy_dependable, expected_type=type_hints["policy_dependable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statement_added": statement_added,
        }
        if policy_dependable is not None:
            self._values["policy_dependable"] = policy_dependable

    @builtins.property
    def statement_added(self) -> builtins.bool:
        '''(experimental) Whether the statement was added to the identity's policies.

        :stability: experimental
        '''
        result = self._values.get("statement_added")
        assert result is not None, "Required property 'statement_added' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def policy_dependable(self) -> typing.Optional[_IDependable_1175c9f7]:
        '''(experimental) Dependable which allows depending on the policy change being applied.

        :default: - Required if ``statementAdded`` is true.

        :stability: experimental
        '''
        result = self._values.get("policy_dependable")
        return typing.cast(typing.Optional[_IDependable_1175c9f7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddToPrincipalPolicyResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.AddToResourcePolicyResult",
    jsii_struct_bases=[],
    name_mapping={
        "statement_added": "statementAdded",
        "policy_dependable": "policyDependable",
    },
)
class AddToResourcePolicyResult:
    def __init__(
        self,
        *,
        statement_added: builtins.bool,
        policy_dependable: typing.Optional[_IDependable_1175c9f7] = None,
    ) -> None:
        '''(experimental) Result of calling addToResourcePolicy.

        :param statement_added: (experimental) Whether the statement was added.
        :param policy_dependable: (experimental) Dependable which allows depending on the policy change being applied. Default: - If ``statementAdded`` is true, the resource object itself. Otherwise, no dependable.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            bucket = s3.Bucket.from_bucket_name(self, "existingBucket", "bucket-name")
            
            # No policy statement will be added to the resource
            result = bucket.add_to_resource_policy(iam.PolicyStatement(
                actions=["s3:GetObject"],
                resources=[bucket.arn_for_objects("file.txt")],
                principals=[iam.AccountRootPrincipal()]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c935a67875d0eb3bc280f234ffb6a5e6c1b6907c3a829725db60a932519606fd)
            check_type(argname="argument statement_added", value=statement_added, expected_type=type_hints["statement_added"])
            check_type(argname="argument policy_dependable", value=policy_dependable, expected_type=type_hints["policy_dependable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "statement_added": statement_added,
        }
        if policy_dependable is not None:
            self._values["policy_dependable"] = policy_dependable

    @builtins.property
    def statement_added(self) -> builtins.bool:
        '''(experimental) Whether the statement was added.

        :stability: experimental
        '''
        result = self._values.get("statement_added")
        assert result is not None, "Required property 'statement_added' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def policy_dependable(self) -> typing.Optional[_IDependable_1175c9f7]:
        '''(experimental) Dependable which allows depending on the policy change being applied.

        :default:

        - If ``statementAdded`` is true, the resource object itself.
        Otherwise, no dependable.

        :stability: experimental
        '''
        result = self._values.get("policy_dependable")
        return typing.cast(typing.Optional[_IDependable_1175c9f7], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddToResourcePolicyResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnAccessKey(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnAccessKey",
):
    '''A CloudFormation ``AWS::IAM::AccessKey``.

    Creates a new AWS secret access key and corresponding AWS access key ID for the specified user. The default status for new keys is ``Active`` .

    For information about quotas on the number of keys you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       To ensure the security of your AWS account , the secret access key is accessible only during key and user creation. You must save the key (for example, in a text file) if you want to be able to access it again. If a secret key is lost, you can rotate access keys by increasing the value of the ``serial`` property.

    :cloudformationResource: AWS::IAM::AccessKey
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_access_key = iam.CfnAccessKey(self, "MyCfnAccessKey",
            user_name="userName",
        
            # the properties below are optional
            serial=123,
            status="status"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        user_name: builtins.str,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::AccessKey``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param user_name: The name of the IAM user that the new key will belong to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param serial: This value is specific to CloudFormation and can only be *incremented* . Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.
        :param status: The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4622828dd713c58f4ad3885641f58a22d8a4d322c47114fb3693a2bf274b77f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessKeyProps(user_name=user_name, serial=serial, status=status)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a00815c8171f70131e403ae4165db1dafff1b18767e259e719a0dd4e72259c86)
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
            type_hints = typing.get_type_hints(_typecheckingstub__44b26c0b448ecd9334ee7eae692819bec4930e840f280ccf562dce8b91ae19f7)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSecretAccessKey")
    def attr_secret_access_key(self) -> builtins.str:
        '''Returns the secret access key for the specified AWS::IAM::AccessKey resource.

        For example: wJalrXUtnFEMI/K7MDENG/bPxRfiCYzEXAMPLEKEY.

        :cloudformationAttribute: SecretAccessKey
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSecretAccessKey"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''The name of the IAM user that the new key will belong to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__743d882a0c50d74bdc367c8d68f65befe4d1dfb6e42a8d9e7c71aedee0dc6d79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @builtins.property
    @jsii.member(jsii_name="serial")
    def serial(self) -> typing.Optional[jsii.Number]:
        '''This value is specific to CloudFormation and can only be *incremented* .

        Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "serial"))

    @serial.setter
    def serial(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c4060de3e744bb046559add0d34704383ee7e3fdfc2679236201b1bbef4d915)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serial", value)

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the access key.

        ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "status"))

    @status.setter
    def status(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ac006dbce0a77c0001f6ee6abe6fe754999c8be632037ca4fc80fca5c6417c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "status", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnAccessKeyProps",
    jsii_struct_bases=[],
    name_mapping={"user_name": "userName", "serial": "serial", "status": "status"},
)
class CfnAccessKeyProps:
    def __init__(
        self,
        *,
        user_name: builtins.str,
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessKey``.

        :param user_name: The name of the IAM user that the new key will belong to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param serial: This value is specific to CloudFormation and can only be *incremented* . Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.
        :param status: The status of the access key. ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_access_key_props = iam.CfnAccessKeyProps(
                user_name="userName",
            
                # the properties below are optional
                serial=123,
                status="status"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__23281560958a53aa55e7c7d7b74a2ac7cd445f3c6d88008c032934ebe282dd4b)
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
            check_type(argname="argument serial", value=serial, expected_type=type_hints["serial"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_name": user_name,
        }
        if serial is not None:
            self._values["serial"] = serial
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def user_name(self) -> builtins.str:
        '''The name of the IAM user that the new key will belong to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-username
        '''
        result = self._values.get("user_name")
        assert result is not None, "Required property 'user_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def serial(self) -> typing.Optional[jsii.Number]:
        '''This value is specific to CloudFormation and can only be *incremented* .

        Incrementing this value notifies CloudFormation that you want to rotate your access key. When you update your stack, CloudFormation will replace the existing access key with a new key.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-serial
        '''
        result = self._values.get("serial")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def status(self) -> typing.Optional[builtins.str]:
        '''The status of the access key.

        ``Active`` means that the key is valid for API calls, while ``Inactive`` means it is not.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-accesskey.html#cfn-iam-accesskey-status
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessKeyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnGroup(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnGroup",
):
    '''A CloudFormation ``AWS::IAM::Group``.

    Creates a new group.

    For information about the number of groups you can create, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Group
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # policy_document: Any
        
        cfn_group = iam.CfnGroup(self, "MyCfnGroup",
            group_name="groupName",
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            policies=[iam.CfnGroup.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnGroup.PolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Group``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: The name of the group to create. Do not include the path in this value. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param managed_policy_arns: The Amazon Resource Name (ARN) of the IAM policy you want to attach. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM group. To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ . .. epigraph:: The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e728d9278d640c1582ba0a6418104e3e717678849840d6c54e0f3b68920414e7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnGroupProps(
            group_name=group_name,
            managed_policy_arns=managed_policy_arns,
            path=path,
            policies=policies,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a912a189f77fe9aae4ffeaca33b3b3d80c4362f90ac12ceed858e1ed5bef3c08)
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
            type_hints = typing.get_type_hints(_typecheckingstub__aa86338033b2057a17eb608fd8f2884a0ed98711b9634b5d9bdedbb896f98518)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::Group`` resource.

        For example: ``arn:aws:iam::123456789012:group/mystack-mygroup-1DZETITOWEKVO`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to create. Do not include the path in this value.

        The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__656a942f6352918fbbd5a060020337c33703544d104d97f690597c7be27b426b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44d20024ca68eb57c1b884076c14fb159d1810dbf66f9513641a9cb53b0949e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c9b2f9b371a2358831cbf25db9b62a28d9963dc6e0ab19dd82de40ff13bb407d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGroup.PolicyProperty", _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM group.

        To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ .
        .. epigraph::

           The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGroup.PolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnGroup.PolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66a8ebd02b16d4bf555fcbcbe6e18b19ece72ba3419302ed79dd15c762f239cb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iam.CfnGroup.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The policy document.
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnGroup.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__90c1d907a3f012b9a1419dac96167bfb515682f874f994c772bf99b6982ee1c2)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The policy document.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "policies": "policies",
    },
)
class CfnGroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnGroup``.

        :param group_name: The name of the group to create. Do not include the path in this value. The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param managed_policy_arns: The Amazon Resource Name (ARN) of the IAM policy you want to attach. For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM group. To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ . .. epigraph:: The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # policy_document: Any
            
            cfn_group_props = iam.CfnGroupProps(
                group_name="groupName",
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                policies=[iam.CfnGroup.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__99c61736404e2b584bad16733704f81032060b7f21b40a1c5952295bfe969ac3)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if policies is not None:
            self._values["policies"] = policies

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''The name of the group to create. Do not include the path in this value.

        The group name must be unique within the account. Group names are not distinguished by case. For example, you cannot create groups named both "ADMINS" and "admins". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name.
        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-groupname
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The Amazon Resource Name (ARN) of the IAM policy you want to attach.

        For more information about ARNs, see `Amazon Resource Names (ARNs) <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the group. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGroup.PolicyProperty, _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM group.

        To view AWS::IAM::Group snippets, see `Declaring an IAM Group Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-group>`_ .
        .. epigraph::

           The name of each inline policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a group, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-group.html#cfn-iam-group-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGroup.PolicyProperty, _IResolvable_a771d0ef]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnInstanceProfile(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnInstanceProfile",
):
    '''A CloudFormation ``AWS::IAM::InstanceProfile``.

    Creates a new instance profile. For information about instance profiles, see `Using instance profiles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2_instance-profiles.html>`_ .

    For information about the number of instance profiles you can create, see `IAM object quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::InstanceProfile
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_instance_profile = iam.CfnInstanceProfile(self, "MyCfnInstanceProfile",
            roles=["roles"],
        
            # the properties below are optional
            instance_profile_name="instanceProfileName",
            path="path"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        roles: typing.Sequence[builtins.str],
        instance_profile_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::InstanceProfile``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param roles: The name of the role to associate with the instance profile. Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.
        :param instance_profile_name: The name of the instance profile to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param path: The path to the instance profile. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b80712086ce0ba5d6d345e5d4efc7f6a4a4c49f2d2b8d8aaf831ce2e99e7d4aa)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnInstanceProfileProps(
            roles=roles, instance_profile_name=instance_profile_name, path=path
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3541f2c18a3521f1e375fda06f3a1b0a093487447c90294ab41949de5db70b42)
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
            type_hints = typing.get_type_hints(_typecheckingstub__af31761f00835f6e239eb1832794d6c294be454029ac1dd70540aab55da85192)
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
        '''Returns the Amazon Resource Name (ARN) for the instance profile. For example:.

        ``{"Fn::GetAtt" : ["MyProfile", "Arn"] }``

        This returns a value such as ``arn:aws:iam::1234567890:instance-profile/MyProfile-ASDNSDLKJ`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.List[builtins.str]:
        '''The name of the role to associate with the instance profile.

        Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4286d427208028975bf80e37a6cd9f21e7dd589a5f68dd4f716ab4df191166ee)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="instanceProfileName")
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "instanceProfileName"))

    @instance_profile_name.setter
    def instance_profile_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__81ba92744d35d2c0943e21772e62771328a98fb6bc0d33686b3510519504cc23)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "instanceProfileName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the instance profile.

        For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b7a2adee77ab1c223b0e58b56e85f8d129bd8d254b533d779505ccce1e73f30)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnInstanceProfileProps",
    jsii_struct_bases=[],
    name_mapping={
        "roles": "roles",
        "instance_profile_name": "instanceProfileName",
        "path": "path",
    },
)
class CfnInstanceProfileProps:
    def __init__(
        self,
        *,
        roles: typing.Sequence[builtins.str],
        instance_profile_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnInstanceProfile``.

        :param roles: The name of the role to associate with the instance profile. Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.
        :param instance_profile_name: The name of the instance profile to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param path: The path to the instance profile. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_instance_profile_props = iam.CfnInstanceProfileProps(
                roles=["roles"],
            
                # the properties below are optional
                instance_profile_name="instanceProfileName",
                path="path"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fe81c53dc01117f631ea31d93fea1fb265aa69568c02ffaa833de39a23b6083f)
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument instance_profile_name", value=instance_profile_name, expected_type=type_hints["instance_profile_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "roles": roles,
        }
        if instance_profile_name is not None:
            self._values["instance_profile_name"] = instance_profile_name
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def roles(self) -> typing.List[builtins.str]:
        '''The name of the role to associate with the instance profile.

        Only one role can be assigned to an EC2 instance at a time, and all applications on the instance share the same role and permissions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-roles
        '''
        result = self._values.get("roles")
        assert result is not None, "Required property 'roles' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def instance_profile_name(self) -> typing.Optional[builtins.str]:
        '''The name of the instance profile to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-instanceprofilename
        '''
        result = self._values.get("instance_profile_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the instance profile.

        For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-instanceprofile.html#cfn-iam-instanceprofile-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnInstanceProfileProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnManagedPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnManagedPolicy",
):
    '''A CloudFormation ``AWS::IAM::ManagedPolicy``.

    Creates a new managed policy for your AWS account .

    This operation creates a policy version with a version identifier of ``v1`` and sets v1 as the policy's default version. For more information about policy versions, see `Versioning for managed policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-versions.html>`_ in the *IAM User Guide* .

    As a best practice, you can validate your IAM policies. To learn more, see `Validating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_policy-validator.html>`_ in the *IAM User Guide* .

    For more information about managed policies in general, see `Managed policies and inline policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::ManagedPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # policy_document: Any
        
        cfn_managed_policy = iam.CfnManagedPolicy(self, "MyCfnManagedPolicy",
            policy_document=policy_document,
        
            # the properties below are optional
            description="description",
            groups=["groups"],
            managed_policy_name="managedPolicyName",
            path="path",
            roles=["roles"],
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ManagedPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The JSON policy document that you want to use as the content for the new policy. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ . To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* . The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param groups: The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param managed_policy_name: The friendly name of the policy. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use an asterisk (*) in the path name.
        :param roles: The name (friendly name, not ARN) of the role to attach the policy to. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name (friendly name, not ARN) of the IAM user to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d7295fe873b5468acdca1388cb7fb4e18371ad4d39c0152419700e704304042)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnManagedPolicyProps(
            policy_document=policy_document,
            description=description,
            groups=groups,
            managed_policy_name=managed_policy_name,
            path=path,
            roles=roles,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41c7f166512551a40454caf84a801f191ff025a03bd7924636c060368739a7b)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ca6919a09b81613537222dfc3e9b07fdee77cb01e3a0b11b217a43b63aeb5e2c)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''The JSON policy document that you want to use as the content for the new policy.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ .

        To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* .

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4deb783ba798693331e1a4b36fc73b51fa59c567295ce97bab6c623292f96c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it cannot be changed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__182977da84f3bd39f60a2c5be5cdbc310439eb2eb555c9bc47fc91f05197078e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the group to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__beadf8f7e74db656fef53b215e2ba7b877cbe26cccf42010c8ad896a945ef274)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the policy.

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "managedPolicyName"))

    @managed_policy_name.setter
    def managed_policy_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__136772522a7194fa3e838acac2bceb751bbe3e32d32f19fb0b9b0ebc0ee0a713)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyName", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use an asterisk (*) in the path name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df69b36e387aa8502db47854dcd52cc893a9a41a014d92c9ec51551358bf9588)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the role to attach the policy to.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c096bb8bbdde3619b74dcd78e95d7475217fced4652b9510f6aec35c1f8e7dfb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the IAM user to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dd7765634021d5587ca4726d6acf091879e8a0d53d0bea4032186164e1b844d3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnManagedPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "description": "description",
        "groups": "groups",
        "managed_policy_name": "managedPolicyName",
        "path": "path",
        "roles": "roles",
        "users": "users",
    },
)
class CfnManagedPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnManagedPolicy``.

        :param policy_document: The JSON policy document that you want to use as the content for the new policy. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ . To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* . The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param description: A friendly description of the policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed.
        :param groups: The name (friendly name, not ARN) of the group to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param managed_policy_name: The friendly name of the policy. .. epigraph:: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param path: The path for the policy. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: You cannot use an asterisk (*) in the path name.
        :param roles: The name (friendly name, not ARN) of the role to attach the policy to. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name (friendly name, not ARN) of the IAM user to attach the policy to. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # policy_document: Any
            
            cfn_managed_policy_props = iam.CfnManagedPolicyProps(
                policy_document=policy_document,
            
                # the properties below are optional
                description="description",
                groups=["groups"],
                managed_policy_name="managedPolicyName",
                path="path",
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__793d161e4a973c6db5c396c8a47fc90cdc692ddcfbb89a293d37c39f2ebbc217)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
        }
        if description is not None:
            self._values["description"] = description
        if groups is not None:
            self._values["groups"] = groups
        if managed_policy_name is not None:
            self._values["managed_policy_name"] = managed_policy_name
        if path is not None:
            self._values["path"] = path
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The JSON policy document that you want to use as the content for the new policy.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The maximum length of the policy document that you can pass in this operation, including whitespace, is listed below. To view the maximum character counts of a managed policy with no whitespaces, see `IAM and AWS STS character quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html#reference_iam-quotas-entity-length>`_ .

        To learn more about JSON policy grammar, see `Grammar of the IAM JSON policy language <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_grammar.html>`_ in the *IAM User Guide* .

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A friendly description of the policy.

        Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables."

        The policy description is immutable. After a value is assigned, it cannot be changed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the group to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''The friendly name of the policy.

        .. epigraph::

           If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-managedpolicyname
        '''
        result = self._values.get("managed_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the policy.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           You cannot use an asterisk (*) in the path name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-ec2-dhcpoptions-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the role to attach the policy to.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name (friendly name, not ARN) of the IAM user to attach the policy to.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-managedpolicy.html#cfn-iam-managedpolicy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnManagedPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnOIDCProvider(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnOIDCProvider",
):
    '''A CloudFormation ``AWS::IAM::OIDCProvider``.

    Creates or updates an IAM entity to describe an identity provider (IdP) that supports `OpenID Connect (OIDC) <https://docs.aws.amazon.com/http://openid.net/connect/>`_ .

    The OIDC provider that you create with this operation can be used as a principal in a role's trust policy. Such a policy establishes a trust relationship between AWS and the OIDC provider.

    When you create the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that identify the application or applications that are allowed to authenticate using the OIDC provider
    - A list of tags that are attached to the specified IAM OIDC provider
    - A list of thumbprints of one or more server certificates that the IdP uses

    You get all of this information from the OIDC IdP that you want to use to access AWS .

    When you update the IAM OIDC provider, you specify the following:

    - The URL of the OIDC identity provider (IdP) to trust
    - A list of client IDs (also known as audiences) that replaces the existing list of client IDs associated with the OIDC IdP
    - A list of tags that replaces the existing list of tags attached to the specified IAM OIDC provider
    - A list of thumbprints that replaces the existing list of server certificates thumbprints that the IdP uses

    .. epigraph::

       The trust for the OIDC provider is derived from the IAM provider that this operation creates. Therefore, it is best to limit access to the `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ operation to highly privileged users.

    :cloudformationResource: AWS::IAM::OIDCProvider
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_oIDCProvider = iam.CfnOIDCProvider(self, "MyCfnOIDCProvider",
            thumbprint_list=["thumbprintList"],
        
            # the properties below are optional
            client_id_list=["clientIdList"],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            url="url"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        thumbprint_list: typing.Sequence[builtins.str],
        client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::OIDCProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param thumbprint_list: A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param client_id_list: A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param tags: A list of tags that are attached to the specified IAM OIDC provider. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        :param url: The URL that the IAM OIDC provider resource object is associated with. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4ad356568baf3cc2c3ab2fe48047c07cc488508a8e0c88b07f17fab78b77545)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnOIDCProviderProps(
            thumbprint_list=thumbprint_list,
            client_id_list=client_id_list,
            tags=tags,
            url=url,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7fbb5c40440a88d129adf49c1348cf1801247b1c39ac63e524bfdaf5f217e23)
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
            type_hints = typing.get_type_hints(_typecheckingstub__c7aeb2363702ea0c2b5a06a8b47a8faa7791f02ddbfeb42b818befa38f55e378)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::OIDCProvider`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that are attached to the specified IAM OIDC provider.

        The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="thumbprintList")
    def thumbprint_list(self) -> typing.List[builtins.str]:
        '''A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-thumbprintlist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "thumbprintList"))

    @thumbprint_list.setter
    def thumbprint_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fcfc0fcfb444f04128fe566c2f1d534c6e9863fb2d19b70381880d35103b638c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "thumbprintList", value)

    @builtins.property
    @jsii.member(jsii_name="clientIdList")
    def client_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-clientidlist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "clientIdList"))

    @client_id_list.setter
    def client_id_list(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bda381b9f9f2a2b619886cfc87c71e1f01263b4daedaabc8a80a2e62e11877da)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "clientIdList", value)

    @builtins.property
    @jsii.member(jsii_name="url")
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL that the IAM OIDC provider resource object is associated with.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-url
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "url"))

    @url.setter
    def url(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__afdb30f5b29978d4574a35c2784bea041bd9039ed42ba84722ce78e7cacffe66)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "url", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnOIDCProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "thumbprint_list": "thumbprintList",
        "client_id_list": "clientIdList",
        "tags": "tags",
        "url": "url",
    },
)
class CfnOIDCProviderProps:
    def __init__(
        self,
        *,
        thumbprint_list: typing.Sequence[builtins.str],
        client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        url: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnOIDCProvider``.

        :param thumbprint_list: A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param client_id_list: A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .
        :param tags: A list of tags that are attached to the specified IAM OIDC provider. The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        :param url: The URL that the IAM OIDC provider resource object is associated with. For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_oIDCProvider_props = iam.CfnOIDCProviderProps(
                thumbprint_list=["thumbprintList"],
            
                # the properties below are optional
                client_id_list=["clientIdList"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                url="url"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a996edfa5ca2351f0144d6072930b51a302848a2db7fe007666d4fca5abe476)
            check_type(argname="argument thumbprint_list", value=thumbprint_list, expected_type=type_hints["thumbprint_list"])
            check_type(argname="argument client_id_list", value=client_id_list, expected_type=type_hints["client_id_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "thumbprint_list": thumbprint_list,
        }
        if client_id_list is not None:
            self._values["client_id_list"] = client_id_list
        if tags is not None:
            self._values["tags"] = tags
        if url is not None:
            self._values["url"] = url

    @builtins.property
    def thumbprint_list(self) -> typing.List[builtins.str]:
        '''A list of certificate thumbprints that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-thumbprintlist
        '''
        result = self._values.get("thumbprint_list")
        assert result is not None, "Required property 'thumbprint_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def client_id_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of client IDs (also known as audiences) that are associated with the specified IAM OIDC provider resource object.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-clientidlist
        '''
        result = self._values.get("client_id_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that are attached to the specified IAM OIDC provider.

        The returned list of tags is sorted by tag key. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def url(self) -> typing.Optional[builtins.str]:
        '''The URL that the IAM OIDC provider resource object is associated with.

        For more information, see `CreateOpenIDConnectProvider <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateOpenIDConnectProvider.html>`_ .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-oidcprovider.html#cfn-iam-oidcprovider-url
        '''
        result = self._values.get("url")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnOIDCProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnPolicy(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnPolicy",
):
    '''A CloudFormation ``AWS::IAM::Policy``.

    Adds or updates an inline policy document that is embedded in the specified IAM user, group, or role.

    An IAM user can also have a managed policy attached to it. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

    The Groups, Roles, and Users properties are optional. However, you must specify at least one of these properties.

    For information about policy documents see `Creating IAM policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_create.html>`_ in the *IAM User Guide* .

    For information about limits on the number of inline policies that you can embed in an identity, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Policy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # policy_document: Any
        
        cfn_policy = iam.CfnPolicy(self, "MyCfnPolicy",
            policy_document=policy_document,
            policy_name="policyName",
        
            # the properties below are optional
            groups=["groups"],
            roles=["roles"],
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        policy_document: typing.Any,
        policy_name: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param groups: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param roles: The name of the role to associate the policy with. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fab3465f374f0ef915abf45cb5039f4e6ff0e76499029b9710c11318e39dcf9)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            policy_document=policy_document,
            policy_name=policy_name,
            groups=groups,
            roles=roles,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a98c43992dae03ae7744dd53cc779bcb3a614c9404fb7a1dbdc16f9a34e1391)
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
            type_hints = typing.get_type_hints(_typecheckingstub__f0221c026571cb360ea6ac10a8498e4191d7070b47e3d4c7eddf7decc167929e)
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
    @jsii.member(jsii_name="policyDocument")
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "policyDocument"))

    @policy_document.setter
    def policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5371162b66e4e4ec284d5ebf4afcac85a2168c4dc032c8707a4e888b2db7bf0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f15aa6a15100d07c733f3eb1fa07d624f59c1f67eeb9e7463b9e0160dc41f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be497bbf4efa2df1cfce18e7afea9ae541f26bf743f79b5f339cfa287047b9f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="roles")
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate the policy with.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "roles"))

    @roles.setter
    def roles(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__635797cbee390cbcf746a9192dfaff877ecae263c5ecee87a169e0c95495388f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roles", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__154d54b8d9f75c1aaf34dcf8f925274020a73188bc3e0d517c9dca67fdb9ccc4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "policy_document": "policyDocument",
        "policy_name": "policyName",
        "groups": "groups",
        "roles": "roles",
        "users": "users",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        policy_document: typing.Any,
        policy_name: builtins.str,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        roles: typing.Optional[typing.Sequence[builtins.str]] = None,
        users: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPolicy``.

        :param policy_document: The policy document. You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param policy_name: The name of the policy document. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param groups: The name of the group to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.
        :param roles: The name of the role to associate the policy with. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param users: The name of the user to associate the policy with. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # policy_document: Any
            
            cfn_policy_props = iam.CfnPolicyProps(
                policy_document=policy_document,
                policy_name="policyName",
            
                # the properties below are optional
                groups=["groups"],
                roles=["roles"],
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e08e6f0ff6f44a0242113a667e938008874cbf05ceceaeb5fde54cd3082868e9)
            check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy_document": policy_document,
            "policy_name": policy_name,
        }
        if groups is not None:
            self._values["groups"] = groups
        if roles is not None:
            self._values["roles"] = roles
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def policy_document(self) -> typing.Any:
        '''The policy document.

        You must provide policies in JSON format in IAM. However, for AWS CloudFormation templates formatted in YAML, you can provide the policy in JSON or YAML format. AWS CloudFormation always converts a YAML policy to JSON format before submitting it to IAM.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policydocument
        '''
        result = self._values.get("policy_document")
        assert result is not None, "Required property 'policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the policy document.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the group to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the role to associate the policy with.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-roles
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The name of the user to associate the policy with.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-policy.html#cfn-iam-policy-users
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnRole(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnRole",
):
    '''A CloudFormation ``AWS::IAM::Role``.

    Creates a new role for your AWS account . For more information about roles, see `IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/WorkingWithRoles.html>`_ . For information about quotas for role names and the number of roles you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::Role
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # assume_role_policy_document: Any
        # policy_document: Any
        
        cfn_role = iam.CfnRole(self, "MyCfnRole",
            assume_role_policy_document=assume_role_policy_document,
        
            # the properties below are optional
            description="description",
            managed_policy_arns=["managedPolicyArns"],
            max_session_duration=123,
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam.CfnRole.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            role_name="roleName",
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
        assume_role_policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_session_duration: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnRole.PolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::Role``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param assume_role_policy_document: The trust policy that is associated with this role. Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .
        :param description: A description of the role that you provide.
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param max_session_duration: The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours. Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .
        :param path: The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the policy used to set the permissions boundary for the role. For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM role. When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ . A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* . For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* . .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param role_name: A name for the IAM role, up to 64 characters in length. For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* . This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param tags: A list of tags that are attached to the role. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce964e0de267d204f32999fa5a654c0e2e5f9458b332c3922394b3b7e02ebc0e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRoleProps(
            assume_role_policy_document=assume_role_policy_document,
            description=description,
            managed_policy_arns=managed_policy_arns,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            policies=policies,
            role_name=role_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad081a33db5bfd7b92131b1366301a0048c67e3d38822293dbb9615c546d7fc8)
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
            type_hints = typing.get_type_hints(_typecheckingstub__7db76988ea3967babb7fa78dbb28dc5b821761602b8c268536c74a320dce2906)
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
        '''Returns the Amazon Resource Name (ARN) for the role. For example:.

        ``{"Fn::GetAtt" : ["MyRole", "Arn"] }``

        This will return a value such as ``arn:aws:iam::1234567890:role/MyRole-AJJHDSKSDF`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrRoleId")
    def attr_role_id(self) -> builtins.str:
        '''Returns the stable and unique string identifying the role. For example, ``AIDAJQABLZS4A3QDU576Q`` .

        For more information about IDs, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_identifiers.html>`_ in the *IAM User Guide* .

        :cloudformationAttribute: RoleId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrRoleId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that are attached to the role.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicyDocument")
    def assume_role_policy_document(self) -> typing.Any:
        '''The trust policy that is associated with this role.

        Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        '''
        return typing.cast(typing.Any, jsii.get(self, "assumeRolePolicyDocument"))

    @assume_role_policy_document.setter
    def assume_role_policy_document(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef08307620961b0d29bc42964ef20cb5e5385d5efaa273219063c111342967c4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "assumeRolePolicyDocument", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role that you provide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a721ce165cd2aa06da526e8bd6cc3e789a63a27591062e6603b72fcd979f2750)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d8aaa92a31c7d868a553d185b83d6920d2ade158fb295ee2b4806c7a9f0c332)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="maxSessionDuration")
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        '''The maximum session duration (in seconds) that you want to set for the specified role.

        If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours.

        Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "maxSessionDuration"))

    @max_session_duration.setter
    def max_session_duration(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e0ba76eb15f186e1ee30a4b0457e9a415ed432127a38ba0e392346b634848ba4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "maxSessionDuration", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c1a75bda1e43eedef2aa097843785d4d746c74032b6f333c3ec9fffd4df75d7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the policy used to set the permissions boundary for the role.

        For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__26ebd0e1dd466e235f65dfebbd85644096e38d87d4941392a795c66173e88ef9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRole.PolicyProperty", _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM role.

        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ .

        A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRole.PolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnRole.PolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5126d35f269a24e9610eb38a4e55b1c0ca0050aaf09e182e27ad03bb0101664e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role, up to 64 characters in length.

        For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* .

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "roleName"))

    @role_name.setter
    def role_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e99aa335ce899dc15561f63b4ff1e92b27063fa7686b486b9956bfa29fb6614e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iam.CfnRole.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnRole.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a59c2b44c2d2cb21703aaf8d4f06fffaf75db69f17c6bd2a7e63f6ac7396ce3)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_policy_document": "assumeRolePolicyDocument",
        "description": "description",
        "managed_policy_arns": "managedPolicyArns",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "role_name": "roleName",
        "tags": "tags",
    },
)
class CfnRoleProps:
    def __init__(
        self,
        *,
        assume_role_policy_document: typing.Any,
        description: typing.Optional[builtins.str] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        max_session_duration: typing.Optional[jsii.Number] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        role_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRole``.

        :param assume_role_policy_document: The trust policy that is associated with this role. Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .
        :param description: A description of the role that you provide.
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param max_session_duration: The maximum session duration (in seconds) that you want to set for the specified role. If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours. Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .
        :param path: The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the policy used to set the permissions boundary for the role. For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM role. When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ . A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* . For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* . .. epigraph:: If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.
        :param role_name: A name for the IAM role, up to 64 characters in length. For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* . This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        :param tags: A list of tags that are attached to the role. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # assume_role_policy_document: Any
            # policy_document: Any
            
            cfn_role_props = iam.CfnRoleProps(
                assume_role_policy_document=assume_role_policy_document,
            
                # the properties below are optional
                description="description",
                managed_policy_arns=["managedPolicyArns"],
                max_session_duration=123,
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam.CfnRole.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                role_name="roleName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24419d7834f7ce64b604b8867d44aed4da20d872bf81ec3c43125c330c24c164)
            check_type(argname="argument assume_role_policy_document", value=assume_role_policy_document, expected_type=type_hints["assume_role_policy_document"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assume_role_policy_document": assume_role_policy_document,
        }
        if description is not None:
            self._values["description"] = description
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if role_name is not None:
            self._values["role_name"] = role_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def assume_role_policy_document(self) -> typing.Any:
        '''The trust policy that is associated with this role.

        Trust policies define which entities can assume the role. You can associate only one trust policy with a role. For an example of a policy that can be used to assume a role, see `Template Examples <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#aws-resource-iam-role--examples>`_ . For more information about the elements that you can use in an IAM policy, see `IAM Policy Elements Reference <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-assumerolepolicydocument
        '''
        result = self._values.get("assume_role_policy_document")
        assert result is not None, "Required property 'assume_role_policy_document' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the role that you provide.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the role.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[jsii.Number]:
        '''The maximum session duration (in seconds) that you want to set for the specified role.

        If you do not specify a value for this setting, the default value of one hour is applied. This setting can have a value from 1 hour to 12 hours.

        Anyone who assumes the role from the AWS CLI or API can use the ``DurationSeconds`` API parameter or the ``duration-seconds`` AWS CLI parameter to request a longer session. The ``MaxSessionDuration`` setting determines the maximum duration that can be requested using the ``DurationSeconds`` parameter. If users don't specify a value for the ``DurationSeconds`` parameter, their security credentials are valid for one hour by default. This applies when you use the ``AssumeRole*`` API operations or the ``assume-role*`` AWS CLI operations but does not apply when you use those operations to create a console URL. For more information, see `Using IAM roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-maxsessionduration
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path to the role. For more information about paths, see `IAM Identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the policy used to set the permissions boundary for the role.

        For more information about permissions boundaries, see `Permissions boundaries for IAM identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRole.PolicyProperty, _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM role.

        When you embed an inline policy in a role, the inline policy is used as part of the role's access (permissions) policy. The role's trust policy is created at the same time as the role. You can update a role's trust policy later. For more information about IAM roles, go to `Using Roles to Delegate Permissions and Federate Identities <https://docs.aws.amazon.com/IAM/latest/UserGuide/roles-toplevel.html>`_ .

        A role can also have an attached managed policy. For information about policies, see `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

        For information about limits on the number of inline policies that you can embed with a role, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If an external policy (such as ``AWS::IAM::Policy`` or ``AWS::IAM::ManagedPolicy`` ) has a ``Ref`` to a role and if a resource (such as ``AWS::ECS::Service`` ) also has a ``Ref`` to the same role, add a ``DependsOn`` attribute to the resource to make the resource depend on the external policy. This dependency ensures that the role's policy is available throughout the resource's lifecycle. For example, when you delete a stack with an ``AWS::ECS::Service`` resource, the ``DependsOn`` attribute ensures that AWS CloudFormation deletes the ``AWS::ECS::Service`` resource before deleting its role's policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRole.PolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''A name for the IAM role, up to 64 characters in length.

        For valid values, see the ``RoleName`` parameter for the ```CreateRole`` <https://docs.aws.amazon.com/IAM/latest/APIReference/API_CreateRole.html>`_ action in the *IAM User Guide* .

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The role name must be unique within the account. Role names are not distinguished by case. For example, you cannot create roles named both "Role1" and "role1".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-rolename
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that are attached to the role.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-role.html#cfn-iam-role-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnSAMLProvider(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnSAMLProvider",
):
    '''A CloudFormation ``AWS::IAM::SAMLProvider``.

    Creates an IAM resource that describes an identity provider (IdP) that supports SAML 2.0.

    The SAML provider resource that you create with this operation can be used as a principal in an IAM role's trust policy. Such a policy can enable federated users who sign in using the SAML IdP to assume the role. You can create an IAM role that supports Web-based single sign-on (SSO) to the AWS Management Console or one that supports API access to AWS .

    When you create the SAML provider resource, you upload a SAML metadata document that you get from your IdP. That document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that the IdP sends. You must generate the metadata document using the identity management software that is used as your organization's IdP.
    .. epigraph::

       This operation requires `Signature Version 4 <https://docs.aws.amazon.com/general/latest/gr/signature-version-4.html>`_ .

    For more information, see `Enabling SAML 2.0 federated users to access the AWS Management Console <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_enable-console-saml.html>`_ and `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::SAMLProvider
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_sAMLProvider = iam.CfnSAMLProvider(self, "MyCfnSAMLProvider",
            saml_metadata_document="samlMetadataDocument",
        
            # the properties below are optional
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
        saml_metadata_document: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::SAMLProvider``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param saml_metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP. For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*
        :param name: The name of the provider to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that you want to attach to the new IAM SAML provider. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8c257694f667971c2df1b72a987c0f9386a93ef3f21627c59b459b4c8f3a660)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnSAMLProviderProps(
            saml_metadata_document=saml_metadata_document, name=name, tags=tags
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43564e8969a6acf8449cee6b9eb7262457145a7dde9996dca88012a41b5f9a93)
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
            type_hints = typing.get_type_hints(_typecheckingstub__ebdad39afc6b940b3319b8250044ab55497ed3bc857990ed9724a64243d0102c)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::SAMLProvider`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that you want to attach to the new IAM SAML provider.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="samlMetadataDocument")
    def saml_metadata_document(self) -> builtins.str:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-samlmetadatadocument
        '''
        return typing.cast(builtins.str, jsii.get(self, "samlMetadataDocument"))

    @saml_metadata_document.setter
    def saml_metadata_document(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4f7b9cfd72d5f1fa79cef048b9fc8442e28d84854eb45a3e35f41e06d47b57e4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "samlMetadataDocument", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b187478871231f90dba3a4372534773fa3ad18ca59a8366c591b62417d01c7d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnSAMLProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "saml_metadata_document": "samlMetadataDocument",
        "name": "name",
        "tags": "tags",
    },
)
class CfnSAMLProviderProps:
    def __init__(
        self,
        *,
        saml_metadata_document: builtins.str,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnSAMLProvider``.

        :param saml_metadata_document: An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP. For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*
        :param name: The name of the provider to create. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that you want to attach to the new IAM SAML provider. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_sAMLProvider_props = iam.CfnSAMLProviderProps(
                saml_metadata_document="samlMetadataDocument",
            
                # the properties below are optional
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61c788f04c2dcaee21c72ba80b7027aeef890a05fd285247b03176e0ee9217c4)
            check_type(argname="argument saml_metadata_document", value=saml_metadata_document, expected_type=type_hints["saml_metadata_document"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "saml_metadata_document": saml_metadata_document,
        }
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def saml_metadata_document(self) -> builtins.str:
        '''An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        For more information, see `About SAML 2.0-based federation <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_saml.html>`_ in the *IAM User Guide*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-samlmetadatadocument
        '''
        result = self._values.get("saml_metadata_document")
        assert result is not None, "Required property 'saml_metadata_document' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the provider to create.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that you want to attach to the new IAM SAML provider.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-samlprovider.html#cfn-iam-samlprovider-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnSAMLProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServerCertificate(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnServerCertificate",
):
    '''A CloudFormation ``AWS::IAM::ServerCertificate``.

    Uploads a server certificate entity for the AWS account . The server certificate entity includes a public key certificate, a private key, and an optional certificate chain, which should all be PEM-encoded.

    We recommend that you use `AWS Certificate Manager <https://docs.aws.amazon.com/acm/>`_ to provision, manage, and deploy your server certificates. With ACM you can request a certificate, deploy it to AWS resources, and let ACM handle certificate renewals for you. Certificates provided by ACM are free. For more information about using ACM, see the `AWS Certificate Manager User Guide <https://docs.aws.amazon.com/acm/latest/userguide/>`_ .

    For more information about working with server certificates, see `Working with server certificates <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_server-certs.html>`_ in the *IAM User Guide* . This topic includes a list of AWS services that can use the server certificates that you manage with IAM.

    For information about the number of server certificates you can upload, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       Because the body of the public key certificate, private key, and the certificate chain can be large, you should use POST rather than GET when calling ``UploadServerCertificate`` . For information about setting up signatures and authorization through the API, see `Signing AWS API requests <https://docs.aws.amazon.com/general/latest/gr/signing_aws_api_requests.html>`_ in the *AWS General Reference* . For general information about using the Query API with IAM, see `Calling the API by making HTTP query requests <https://docs.aws.amazon.com/IAM/latest/UserGuide/programming.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::ServerCertificate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_server_certificate = iam.CfnServerCertificate(self, "MyCfnServerCertificate",
            certificate_body="certificateBody",
            certificate_chain="certificateChain",
            path="path",
            private_key="privateKey",
            server_certificate_name="serverCertificateName",
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
        certificate_body: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        server_certificate_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ServerCertificate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param certificate_body: The contents of the public key certificate.
        :param certificate_chain: The contents of the public key certificate chain.
        :param path: The path for the server certificate. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :param private_key: The contents of the private key in PEM-encoded format. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param server_certificate_name: The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that are attached to the server certificate. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33c4d49897e31f1a92d7ad3280920f7c0339c6a2b2750461c50a2a7fb2c33926)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServerCertificateProps(
            certificate_body=certificate_body,
            certificate_chain=certificate_chain,
            path=path,
            private_key=private_key,
            server_certificate_name=server_certificate_name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__328a969c0146798b7bfffc57507eb06737fcd9d1da82009f8c7c6b1bec226b02)
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
            type_hints = typing.get_type_hints(_typecheckingstub__095904f3405fee346d01283b9840e2a97774890c5a011071f8060cf5a23deae3)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::ServerCertificate`` resource.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that are attached to the server certificate.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="certificateBody")
    def certificate_body(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatebody
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateBody"))

    @certificate_body.setter
    def certificate_body(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__904fe41a95195bb9b11379edd250dd20dcae7c3702d4f42f6900ed8f74bc51f8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateBody", value)

    @builtins.property
    @jsii.member(jsii_name="certificateChain")
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate chain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatechain
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateChain"))

    @certificate_chain.setter
    def certificate_chain(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__169e7575044ef911af3d03a5433003ac9d61f0b92721f70d5ae8e48e49991f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateChain", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the server certificate.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6cd0e794ea5ae79edcc0d07e78be16d81c7e59efa9346d4294a951bbc46931f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="privateKey")
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The contents of the private key in PEM-encoded format.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-privatekey
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "privateKey"))

    @private_key.setter
    def private_key(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__901b4b2f545a1c797203446b757a14b3b9752451a65c7508a8147d918ff965e7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "privateKey", value)

    @builtins.property
    @jsii.member(jsii_name="serverCertificateName")
    def server_certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name for the server certificate.

        Do not include the path in this value. The name of the certificate cannot contain any spaces.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-servercertificatename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serverCertificateName"))

    @server_certificate_name.setter
    def server_certificate_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22a6764d73d26cdeb7c1f9c7096cf5221964eab7674a83b62b566da8730dc32)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serverCertificateName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnServerCertificateProps",
    jsii_struct_bases=[],
    name_mapping={
        "certificate_body": "certificateBody",
        "certificate_chain": "certificateChain",
        "path": "path",
        "private_key": "privateKey",
        "server_certificate_name": "serverCertificateName",
        "tags": "tags",
    },
)
class CfnServerCertificateProps:
    def __init__(
        self,
        *,
        certificate_body: typing.Optional[builtins.str] = None,
        certificate_chain: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        private_key: typing.Optional[builtins.str] = None,
        server_certificate_name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServerCertificate``.

        :param certificate_body: The contents of the public key certificate.
        :param certificate_chain: The contents of the public key certificate chain.
        :param path: The path for the server certificate. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters. .. epigraph:: If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).
        :param private_key: The contents of the private key in PEM-encoded format. The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following: - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` ) - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )
        :param server_certificate_name: The name for the server certificate. Do not include the path in this value. The name of the certificate cannot contain any spaces. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param tags: A list of tags that are attached to the server certificate. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_server_certificate_props = iam.CfnServerCertificateProps(
                certificate_body="certificateBody",
                certificate_chain="certificateChain",
                path="path",
                private_key="privateKey",
                server_certificate_name="serverCertificateName",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc9f649104fcdf3ec038a7145b62aafeb511114f799a114251dc4dfc013d81dc)
            check_type(argname="argument certificate_body", value=certificate_body, expected_type=type_hints["certificate_body"])
            check_type(argname="argument certificate_chain", value=certificate_chain, expected_type=type_hints["certificate_chain"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument private_key", value=private_key, expected_type=type_hints["private_key"])
            check_type(argname="argument server_certificate_name", value=server_certificate_name, expected_type=type_hints["server_certificate_name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if certificate_body is not None:
            self._values["certificate_body"] = certificate_body
        if certificate_chain is not None:
            self._values["certificate_chain"] = certificate_chain
        if path is not None:
            self._values["path"] = path
        if private_key is not None:
            self._values["private_key"] = private_key
        if server_certificate_name is not None:
            self._values["server_certificate_name"] = server_certificate_name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def certificate_body(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatebody
        '''
        result = self._values.get("certificate_body")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_chain(self) -> typing.Optional[builtins.str]:
        '''The contents of the public key certificate chain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-certificatechain
        '''
        result = self._values.get("certificate_chain")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the server certificate.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        .. epigraph::

           If you are uploading a server certificate specifically for use with Amazon CloudFront distributions, you must specify a path using the ``path`` parameter. The path must begin with ``/cloudfront`` and must include a trailing slash (for example, ``/cloudfront/test/`` ).

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_key(self) -> typing.Optional[builtins.str]:
        '''The contents of the private key in PEM-encoded format.

        The `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ used to validate this parameter is a string of characters consisting of the following:

        - Any printable ASCII character ranging from the space character ( ``\\ u0020`` ) through the end of the ASCII character range
        - The printable characters in the Basic Latin and Latin-1 Supplement character set (through ``\\ u00FF`` )
        - The special characters tab ( ``\\ u0009`` ), line feed ( ``\\ u000A`` ), and carriage return ( ``\\ u000D`` )

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-privatekey
        '''
        result = self._values.get("private_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def server_certificate_name(self) -> typing.Optional[builtins.str]:
        '''The name for the server certificate.

        Do not include the path in this value. The name of the certificate cannot contain any spaces.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-servercertificatename
        '''
        result = self._values.get("server_certificate_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that are attached to the server certificate.

        For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servercertificate.html#cfn-iam-servercertificate-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServerCertificateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnServiceLinkedRole(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnServiceLinkedRole",
):
    '''A CloudFormation ``AWS::IAM::ServiceLinkedRole``.

    Creates an IAM role that is linked to a specific AWS service. The service controls the attached policies and when the role can be deleted. This helps ensure that the service is not broken by an unexpectedly changed or deleted role, which could put your AWS resources into an unknown state. Allowing the service to control the role helps improve service stability and proper cleanup when a service and its role are no longer needed. For more information, see `Using service-linked roles <https://docs.aws.amazon.com/IAM/latest/UserGuide/using-service-linked-roles.html>`_ in the *IAM User Guide* .

    To attach a policy to this service-linked role, you must make the request using the AWS service that depends on this role.

    :cloudformationResource: AWS::IAM::ServiceLinkedRole
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
    :exampleMetadata: infused

    Example::

        slr = iam.CfnServiceLinkedRole(self, "ElasticSLR",
            aws_service_name="es.amazonaws.com"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        aws_service_name: builtins.str,
        custom_suffix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::ServiceLinkedRole``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param aws_service_name: The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` . Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.
        :param custom_suffix: A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix. Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :param description: The description of the role.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0c6506b6ae6f00af5ac5c449a0cbf864904cd5557ef9ab8dbe7a152aedd1e0f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceLinkedRoleProps(
            aws_service_name=aws_service_name,
            custom_suffix=custom_suffix,
            description=description,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__667c3c3cd1a347c5769025eb5e3cdf57842d62f8296b42b3f3f20ac576add0e6)
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
            type_hints = typing.get_type_hints(_typecheckingstub__5e1f4d38ec22dee0a0f5faa36f17a18c0107e5f667206a3027ab1e803ad84793)
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
    @jsii.member(jsii_name="awsServiceName")
    def aws_service_name(self) -> builtins.str:
        '''The service principal for the AWS service to which this role is attached.

        You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .

        Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        '''
        return typing.cast(builtins.str, jsii.get(self, "awsServiceName"))

    @aws_service_name.setter
    def aws_service_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dd2e2739ab49d8892778787276d93dab4bf6364d8190f75fb0c371eea3cd941)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "awsServiceName", value)

    @builtins.property
    @jsii.member(jsii_name="customSuffix")
    def custom_suffix(self) -> typing.Optional[builtins.str]:
        '''A string that you provide, which is combined with the service-provided prefix to form the complete role name.

        If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.

        Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customSuffix"))

    @custom_suffix.setter
    def custom_suffix(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1435440d155e997493d0b3652087e4f0924a3ef70640be30d9345027c0450d33)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customSuffix", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7a13d645b2dde2bb411e864575230c0f6aeb1f72de5485a5bfa8c9252be4f30a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnServiceLinkedRoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "aws_service_name": "awsServiceName",
        "custom_suffix": "customSuffix",
        "description": "description",
    },
)
class CfnServiceLinkedRoleProps:
    def __init__(
        self,
        *,
        aws_service_name: builtins.str,
        custom_suffix: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceLinkedRole``.

        :param aws_service_name: The service principal for the AWS service to which this role is attached. You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` . Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.
        :param custom_suffix: A string that you provide, which is combined with the service-provided prefix to form the complete role name. If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix. Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.
        :param description: The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html
        :exampleMetadata: infused

        Example::

            slr = iam.CfnServiceLinkedRole(self, "ElasticSLR",
                aws_service_name="es.amazonaws.com"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bb7850752f6463384c57ddc16a5f1dd07a73db3410a913522e100febfda97de)
            check_type(argname="argument aws_service_name", value=aws_service_name, expected_type=type_hints["aws_service_name"])
            check_type(argname="argument custom_suffix", value=custom_suffix, expected_type=type_hints["custom_suffix"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "aws_service_name": aws_service_name,
        }
        if custom_suffix is not None:
            self._values["custom_suffix"] = custom_suffix
        if description is not None:
            self._values["description"] = description

    @builtins.property
    def aws_service_name(self) -> builtins.str:
        '''The service principal for the AWS service to which this role is attached.

        You use a string similar to a URL but without the http:// in front. For example: ``elasticbeanstalk.amazonaws.com`` .

        Service principals are unique and case-sensitive. To find the exact service principal for your service-linked role, see `AWS services that work with IAM <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_aws-services-that-work-with-iam.html>`_ in the *IAM User Guide* . Look for the services that have *Yes* in the *Service-Linked Role* column. Choose the *Yes* link to view the service-linked role documentation for that service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-awsservicename
        '''
        result = self._values.get("aws_service_name")
        assert result is not None, "Required property 'aws_service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def custom_suffix(self) -> typing.Optional[builtins.str]:
        '''A string that you provide, which is combined with the service-provided prefix to form the complete role name.

        If you make multiple requests for the same service, then you must supply a different ``CustomSuffix`` for each request. Otherwise the request fails with a duplicate role name error. For example, you could add ``-1`` or ``-debug`` to the suffix.

        Some services do not support the ``CustomSuffix`` parameter. If you provide an optional suffix and the operation fails, try the operation again without the suffix.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-customsuffix
        '''
        result = self._values.get("custom_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description of the role.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-servicelinkedrole.html#cfn-iam-servicelinkedrole-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceLinkedRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUser(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnUser",
):
    '''A CloudFormation ``AWS::IAM::User``.

    Creates a new IAM user for your AWS account .

    For information about quotas for the number of IAM users you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .

    :cloudformationResource: AWS::IAM::User
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # policy_document: Any
        
        cfn_user = iam.CfnUser(self, "MyCfnUser",
            groups=["groups"],
            login_profile=iam.CfnUser.LoginProfileProperty(
                password="password",
        
                # the properties below are optional
                password_reset_required=False
            ),
            managed_policy_arns=["managedPolicyArns"],
            path="path",
            permissions_boundary="permissionsBoundary",
            policies=[iam.CfnUser.PolicyProperty(
                policy_document=policy_document,
                policy_name="policyName"
            )],
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            user_name="userName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_profile: typing.Optional[typing.Union[typing.Union["CfnUser.LoginProfileProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnUser.PolicyProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::User``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param groups: A list of group names to which you want to add the user.
        :param login_profile: Creates a password for the specified IAM user. A password allows an IAM user to access AWS services through the AWS Management Console . You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console . For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path for the user name. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the managed policy that is used to set the permissions boundary for the user. A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM user. To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ . .. epigraph:: The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        :param tags: A list of tags that you want to attach to the new user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param user_name: The name of the user to create. Do not include the path in this value. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__684a0c7011928d2cc111a24fe8a18bb4d08c3f126b65ba884514a712a16d297e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserProps(
            groups=groups,
            login_profile=login_profile,
            managed_policy_arns=managed_policy_arns,
            path=path,
            permissions_boundary=permissions_boundary,
            policies=policies,
            tags=tags,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88716a13390db0fdec2c4d193d8376a0c0033b8a36a8bc17fb92d24426d18d9d)
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
            type_hints = typing.get_type_hints(_typecheckingstub__013d48bf94780cca8cd196c67c7fb6e67b57a4290f7c3469f97b2864093796dd)
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
        '''Returns the Amazon Resource Name (ARN) for the specified ``AWS::IAM::User`` resource.

        For example: ``arn:aws:iam::123456789012:user/mystack-myuser-1CCXAFG2H2U4D`` .

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that you want to attach to the new user.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="groups")
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of group names to which you want to add the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "groups"))

    @groups.setter
    def groups(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__43b6c3e559a7988eb41890d1e3c84f2f2ffdbb5096692d64feb7ab4a4167c678)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groups", value)

    @builtins.property
    @jsii.member(jsii_name="loginProfile")
    def login_profile(
        self,
    ) -> typing.Optional[typing.Union["CfnUser.LoginProfileProperty", _IResolvable_a771d0ef]]:
        '''Creates a password for the specified IAM user.

        A password allows an IAM user to access AWS services through the AWS Management Console .

        You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console .

        For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        '''
        return typing.cast(typing.Optional[typing.Union["CfnUser.LoginProfileProperty", _IResolvable_a771d0ef]], jsii.get(self, "loginProfile"))

    @login_profile.setter
    def login_profile(
        self,
        value: typing.Optional[typing.Union["CfnUser.LoginProfileProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e430934b039692641886ac2d0e6ca8344634938fa8d5439366ec41ca00254bf7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "loginProfile", value)

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArns")
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "managedPolicyArns"))

    @managed_policy_arns.setter
    def managed_policy_arns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__20bb0ddd9cc063059f1c56a4924340627d01d6f7cacbf14b12686f018a2d7384)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "managedPolicyArns", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df5e2c08492371c820c30dcd287f174838188363f3cfdb35b44e45460fffa05b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the managed policy that is used to set the permissions boundary for the user.

        A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "permissionsBoundary"))

    @permissions_boundary.setter
    def permissions_boundary(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a40e432b9728c24dc2744e29104d48734acf3f1ef86dcba6bc0a81828e8c618)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "permissionsBoundary", value)

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.PolicyProperty", _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM user.

        To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ .
        .. epigraph::

           The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.PolicyProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "policies"))

    @policies.setter
    def policies(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnUser.PolicyProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e02bdccbc0be3c4695c49c7ac3d5a48f68c5a90b925d3dd6152bbec363da866c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policies", value)

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to create. Do not include the path in this value.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "userName"))

    @user_name.setter
    def user_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__001fb0a534147dacfc94693a3ba7dfecc211986fcc261dd6cd6605c5e56e21e9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "userName", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_iam.CfnUser.LoginProfileProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "password_reset_required": "passwordResetRequired",
        },
    )
    class LoginProfileProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            password_reset_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Creates a password for the specified user, giving the user the ability to access AWS services through the AWS Management Console .

            For more information about managing passwords, see `Managing Passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

            :param password: The user's password.
            :param password_reset_required: Specifies whether the user is required to set a new password on next sign-in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iam as iam
                
                login_profile_property = iam.CfnUser.LoginProfileProperty(
                    password="password",
                
                    # the properties below are optional
                    password_reset_required=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__54ef2d2672c787807815b09e4b9da212346c539f44cd34480979aa3366b36fc6)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument password_reset_required", value=password_reset_required, expected_type=type_hints["password_reset_required"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
            }
            if password_reset_required is not None:
                self._values["password_reset_required"] = password_reset_required

        @builtins.property
        def password(self) -> builtins.str:
            '''The user's password.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def password_reset_required(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Specifies whether the user is required to set a new password on next sign-in.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user-loginprofile.html#cfn-iam-user-loginprofile-passwordresetrequired
            '''
            result = self._values.get("password_reset_required")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "LoginProfileProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_iam.CfnUser.PolicyProperty",
        jsii_struct_bases=[],
        name_mapping={
            "policy_document": "policyDocument",
            "policy_name": "policyName",
        },
    )
    class PolicyProperty:
        def __init__(
            self,
            *,
            policy_document: typing.Any,
            policy_name: builtins.str,
        ) -> None:
            '''Contains information about an attached policy.

            An attached policy is a managed policy that has been attached to a user, group, or role.

            For more information about managed policies, refer to `Managed Policies and Inline Policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/policies-managed-vs-inline.html>`_ in the *IAM User Guide* .

            :param policy_document: The entire contents of the policy that defines permissions. For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .
            :param policy_name: The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_iam as iam
                
                # policy_document: Any
                
                policy_property = iam.CfnUser.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a05cf007b9f709458d8ebb65fcb9ae6373bfbff233eb448b9c829adc1c6d189)
                check_type(argname="argument policy_document", value=policy_document, expected_type=type_hints["policy_document"])
                check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "policy_document": policy_document,
                "policy_name": policy_name,
            }

        @builtins.property
        def policy_document(self) -> typing.Any:
            '''The entire contents of the policy that defines permissions.

            For more information, see `Overview of JSON policies <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json>`_ .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policydocument
            '''
            result = self._values.get("policy_document")
            assert result is not None, "Required property 'policy_document' is missing"
            return typing.cast(typing.Any, result)

        @builtins.property
        def policy_name(self) -> builtins.str:
            '''The friendly name (not ARN) identifying the policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-policy.html#cfn-iam-policies-policyname
            '''
            result = self._values.get("policy_name")
            assert result is not None, "Required property 'policy_name' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnUserProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "login_profile": "loginProfile",
        "managed_policy_arns": "managedPolicyArns",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "policies": "policies",
        "tags": "tags",
        "user_name": "userName",
    },
)
class CfnUserProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence[builtins.str]] = None,
        login_profile: typing.Optional[typing.Union[typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[builtins.str] = None,
        policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnUser``.

        :param groups: A list of group names to which you want to add the user.
        :param login_profile: Creates a password for the specified IAM user. A password allows an IAM user to access AWS services through the AWS Management Console . You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console . For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .
        :param managed_policy_arns: A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user. For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .
        :param path: The path for the user name. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param permissions_boundary: The ARN of the managed policy that is used to set the permissions boundary for the user. A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* . For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .
        :param policies: Adds or updates an inline policy document that is embedded in the specified IAM user. To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ . .. epigraph:: The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail. For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .
        :param tags: A list of tags that you want to attach to the new user. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param user_name: The name of the user to create. Do not include the path in this value. This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john". If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ . .. epigraph:: Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # policy_document: Any
            
            cfn_user_props = iam.CfnUserProps(
                groups=["groups"],
                login_profile=iam.CfnUser.LoginProfileProperty(
                    password="password",
            
                    # the properties below are optional
                    password_reset_required=False
                ),
                managed_policy_arns=["managedPolicyArns"],
                path="path",
                permissions_boundary="permissionsBoundary",
                policies=[iam.CfnUser.PolicyProperty(
                    policy_document=policy_document,
                    policy_name="policyName"
                )],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                user_name="userName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__78e0bbff574663d9a1ac08f43a6abed3e19785a386d126b2c2b600053e266cca)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument login_profile", value=login_profile, expected_type=type_hints["login_profile"])
            check_type(argname="argument managed_policy_arns", value=managed_policy_arns, expected_type=type_hints["managed_policy_arns"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument policies", value=policies, expected_type=type_hints["policies"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if login_profile is not None:
            self._values["login_profile"] = login_profile
        if managed_policy_arns is not None:
            self._values["managed_policy_arns"] = managed_policy_arns
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if policies is not None:
            self._values["policies"] = policies
        if tags is not None:
            self._values["tags"] = tags
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of group names to which you want to add the user.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-groups
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def login_profile(
        self,
    ) -> typing.Optional[typing.Union[CfnUser.LoginProfileProperty, _IResolvable_a771d0ef]]:
        '''Creates a password for the specified IAM user.

        A password allows an IAM user to access AWS services through the AWS Management Console .

        You can use the AWS CLI , the AWS API, or the *Users* page in the IAM console to create a password for any IAM user. Use `ChangePassword <https://docs.aws.amazon.com/IAM/latest/APIReference/API_ChangePassword.html>`_ to update your own existing password in the *My Security Credentials* page in the AWS Management Console .

        For more information about managing passwords, see `Managing passwords <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_ManagingLogins.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-loginprofile
        '''
        result = self._values.get("login_profile")
        return typing.cast(typing.Optional[typing.Union[CfnUser.LoginProfileProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def managed_policy_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''A list of Amazon Resource Names (ARNs) of the IAM managed policies that you want to attach to the user.

        For more information about ARNs, see `Amazon Resource Names (ARNs) and AWS Service Namespaces <https://docs.aws.amazon.com/general/latest/gr/aws-arns-and-namespaces.html>`_ in the *AWS General Reference* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-managepolicyarns
        '''
        result = self._values.get("managed_policy_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the user name.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[builtins.str]:
        '''The ARN of the managed policy that is used to set the permissions boundary for the user.

        A permissions boundary policy defines the maximum permissions that identity-based policies can grant to an entity, but does not grant permissions. Permissions boundaries do not define the maximum permissions that a resource-based policy can grant to an entity. To learn more, see `Permissions boundaries for IAM entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html>`_ in the *IAM User Guide* .

        For more information about policy types, see `Policy types <https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policy-types>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-permissionsboundary
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def policies(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.PolicyProperty, _IResolvable_a771d0ef]]]]:
        '''Adds or updates an inline policy document that is embedded in the specified IAM user.

        To view AWS::IAM::User snippets, see `Declaring an IAM User Resource <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/quickref-iam.html#scenario-iam-user>`_ .
        .. epigraph::

           The name of each policy for a role, user, or group must be unique. If you don't choose unique names, updates to the IAM identity will fail.

        For information about limits on the number of inline policies that you can embed in a user, see `Limitations on IAM Entities <https://docs.aws.amazon.com/IAM/latest/UserGuide/LimitationsOnEntities.html>`_ in the *IAM User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-policies
        '''
        result = self._values.get("policies")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.PolicyProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that you want to attach to the new user.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''The name of the user to create. Do not include the path in this value.

        This parameter allows (per its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-. The user name must be unique within the account. User names are not distinguished by case. For example, you cannot create users named both "John" and "john".

        If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name.

        If you specify a name, you must specify the ``CAPABILITY_NAMED_IAM`` value to acknowledge your template's capabilities. For more information, see `Acknowledging IAM Resources in AWS CloudFormation Templates <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities>`_ .
        .. epigraph::

           Naming an IAM resource can cause an unrecoverable error if you reuse the same template in multiple Regions. To prevent this, we recommend using ``Fn::Join`` and ``AWS::Region`` to create a Region-specific name, as in the following example: ``{"Fn::Join": ["", [{"Ref": "AWS::Region"}, {"Ref": "MyResourceName"}]]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-user.html#cfn-iam-user-username
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnUserToGroupAddition(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnUserToGroupAddition",
):
    '''A CloudFormation ``AWS::IAM::UserToGroupAddition``.

    Adds the specified user to the specified group.

    :cloudformationResource: AWS::IAM::UserToGroupAddition
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_user_to_group_addition = iam.CfnUserToGroupAddition(self, "MyCfnUserToGroupAddition",
            group_name="groupName",
            users=["users"]
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        group_name: builtins.str,
        users: typing.Sequence[builtins.str],
    ) -> None:
        '''Create a new ``AWS::IAM::UserToGroupAddition``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param group_name: The name of the group to update. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param users: A list of the names of the users that you want to add to the group.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f87307cb0d01ccb9fd86f9193f327cf6991be45b8d8a92b19fdd9e6f30cfc6d2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnUserToGroupAdditionProps(group_name=group_name, users=users)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__07d9db6e767a4d909cc4b8b7dbb6c2b2e0c846d72c804344bf1772be47915176)
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
            type_hints = typing.get_type_hints(_typecheckingstub__e6422ec8e46050ae22c2ddea742c8b612f073f0388a88dab96778e51ae6f0ef8)
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
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''The name of the group to update.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @group_name.setter
    def group_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74b078a0d03ba0f23f3eb2446775c1fd260acebfc5b8658500705200a8549a0b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "groupName", value)

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        '''A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7b2076c4668173824c8e623332053f838f49f4c24a04b5d61cae8cfb303145af)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnUserToGroupAdditionProps",
    jsii_struct_bases=[],
    name_mapping={"group_name": "groupName", "users": "users"},
)
class CfnUserToGroupAdditionProps:
    def __init__(
        self,
        *,
        group_name: builtins.str,
        users: typing.Sequence[builtins.str],
    ) -> None:
        '''Properties for defining a ``CfnUserToGroupAddition``.

        :param group_name: The name of the group to update. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        :param users: A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_user_to_group_addition_props = iam.CfnUserToGroupAdditionProps(
                group_name="groupName",
                users=["users"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__263aabd4f6f34733d87b4115e20c0ec840e846c26574891e4aa46ca24e4a74e3)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "group_name": group_name,
            "users": users,
        }

    @builtins.property
    def group_name(self) -> builtins.str:
        '''The name of the group to update.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-groupname
        '''
        result = self._values.get("group_name")
        assert result is not None, "Required property 'group_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''A list of the names of the users that you want to add to the group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-iam-addusertogroup.html#cfn-iam-addusertogroup-users
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnUserToGroupAdditionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnVirtualMFADevice(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CfnVirtualMFADevice",
):
    '''A CloudFormation ``AWS::IAM::VirtualMFADevice``.

    Creates a new virtual MFA device for the AWS account . After creating the virtual MFA, use `EnableMFADevice <https://docs.aws.amazon.com/IAM/latest/APIReference/API_EnableMFADevice.html>`_ to attach the MFA device to an IAM user. For more information about creating and working with virtual MFA devices, see `Using a virtual MFA device <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_VirtualMFA.html>`_ in the *IAM User Guide* .

    For information about the maximum number of MFA devices you can create, see `IAM and AWS STS quotas <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_iam-quotas.html>`_ in the *IAM User Guide* .
    .. epigraph::

       The seed information contained in the QR code and the Base32 string should be treated like any other secret access information. In other words, protect the seed information as you would your AWS access keys or your passwords. After you provision your virtual device, you should ensure that the information is destroyed following secure procedures.

    :cloudformationResource: AWS::IAM::VirtualMFADevice
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        cfn_virtual_mFADevice = iam.CfnVirtualMFADevice(self, "MyCfnVirtualMFADevice",
            users=["users"],
        
            # the properties below are optional
            path="path",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            virtual_mfa_device_name="virtualMfaDeviceName"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        users: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_mfa_device_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::IAM::VirtualMFADevice``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param users: The IAM user associated with this virtual MFA device.
        :param path: The path for the virtual MFA device. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param tags: A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param virtual_mfa_device_name: The name of the virtual MFA device, which must be unique. Use with path to uniquely identify a virtual MFA device. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__48d0a2bafee0df44ebb2d917e04cdf7aecc71b03018aab980db4a8031024e308)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnVirtualMFADeviceProps(
            users=users,
            path=path,
            tags=tags,
            virtual_mfa_device_name=virtual_mfa_device_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40bcf3f29a5ed35f71d0024e2771f29f12441810d8eacbfb4cab10fb1db73271)
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
            type_hints = typing.get_type_hints(_typecheckingstub__adf85a67b00a5d84c5a0974bb758338236e31f6b26b0252699c991c1aa7c7db0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrSerialNumber")
    def attr_serial_number(self) -> builtins.str:
        '''Returns the serial number for the specified ``AWS::IAM::VirtualMFADevice`` resource.

        :cloudformationAttribute: SerialNumber
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrSerialNumber"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''A list of tags that you want to attach to the new IAM virtual MFA device.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="users")
    def users(self) -> typing.List[builtins.str]:
        '''The IAM user associated with this virtual MFA device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-users
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "users"))

    @users.setter
    def users(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__612ce800090ba82ade073ea4dbf3a212419055abf7b33d4feb9812d71e34a777)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "users", value)

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the virtual MFA device.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-path
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "path"))

    @path.setter
    def path(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4437c569b52f9903d7582d66f4d4423ee04874b73a90959c57b836d43b9cb1a0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "path", value)

    @builtins.property
    @jsii.member(jsii_name="virtualMfaDeviceName")
    def virtual_mfa_device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual MFA device, which must be unique.

        Use with path to uniquely identify a virtual MFA device.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-virtualmfadevicename
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "virtualMfaDeviceName"))

    @virtual_mfa_device_name.setter
    def virtual_mfa_device_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dea1e81beed1ddf9663744d1ddec8495abf547135b923491e1efee8c0632a5ea)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "virtualMfaDeviceName", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CfnVirtualMFADeviceProps",
    jsii_struct_bases=[],
    name_mapping={
        "users": "users",
        "path": "path",
        "tags": "tags",
        "virtual_mfa_device_name": "virtualMfaDeviceName",
    },
)
class CfnVirtualMFADeviceProps:
    def __init__(
        self,
        *,
        users: typing.Sequence[builtins.str],
        path: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
        virtual_mfa_device_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnVirtualMFADevice``.

        :param users: The IAM user associated with this virtual MFA device.
        :param path: The path for the virtual MFA device. For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* . This parameter is optional. If it is not included, it defaults to a slash (/). This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.
        :param tags: A list of tags that you want to attach to the new IAM virtual MFA device. Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* . .. epigraph:: If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.
        :param virtual_mfa_device_name: The name of the virtual MFA device, which must be unique. Use with path to uniquely identify a virtual MFA device. This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            cfn_virtual_mFADevice_props = iam.CfnVirtualMFADeviceProps(
                users=["users"],
            
                # the properties below are optional
                path="path",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                virtual_mfa_device_name="virtualMfaDeviceName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56b034abefc62813f16a987adf2fc982ed3092448f85315cd7a73e39052fe0f0)
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument virtual_mfa_device_name", value=virtual_mfa_device_name, expected_type=type_hints["virtual_mfa_device_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "users": users,
        }
        if path is not None:
            self._values["path"] = path
        if tags is not None:
            self._values["tags"] = tags
        if virtual_mfa_device_name is not None:
            self._values["virtual_mfa_device_name"] = virtual_mfa_device_name

    @builtins.property
    def users(self) -> typing.List[builtins.str]:
        '''The IAM user associated with this virtual MFA device.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-users
        '''
        result = self._values.get("users")
        assert result is not None, "Required property 'users' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''The path for the virtual MFA device.

        For more information about paths, see `IAM identifiers <https://docs.aws.amazon.com/IAM/latest/UserGuide/Using_Identifiers.html>`_ in the *IAM User Guide* .

        This parameter is optional. If it is not included, it defaults to a slash (/).

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! ( ``\\ u0021`` ) through the DEL character ( ``\\ u007F`` ), including most punctuation characters, digits, and upper and lowercased letters.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-path
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''A list of tags that you want to attach to the new IAM virtual MFA device.

        Each tag consists of a key name and an associated value. For more information about tagging, see `Tagging IAM resources <https://docs.aws.amazon.com/IAM/latest/UserGuide/id_tags.html>`_ in the *IAM User Guide* .
        .. epigraph::

           If any one of the tags is invalid or if you exceed the allowed maximum number of tags, then the entire request fails and the resource is not created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    @builtins.property
    def virtual_mfa_device_name(self) -> typing.Optional[builtins.str]:
        '''The name of the virtual MFA device, which must be unique.

        Use with path to uniquely identify a virtual MFA device.

        This parameter allows (through its `regex pattern <https://docs.aws.amazon.com/http://wikipedia.org/wiki/regex>`_ ) a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-iam-virtualmfadevice.html#cfn-iam-virtualmfadevice-virtualmfadevicename
        '''
        result = self._values.get("virtual_mfa_device_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnVirtualMFADeviceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.CommonGrantOptions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
    },
)
class CommonGrantOptions:
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> None:
        '''(experimental) Basic options for a grant operation.

        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # grantable: iam.IGrantable
            
            common_grant_options = iam.CommonGrantOptions(
                actions=["actions"],
                grantee=grantable,
                resource_arns=["resourceArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b314d0430939f5e61d9ccffd7b0afec5cfab9709af782d0ba58b1e43a2e9352c)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
        }

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to grant.

        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''(experimental) The principal to grant to.

        :default: if principal is undefined, no work is done.

        :stability: experimental
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''(experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CommonGrantOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ComparablePrincipal(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.ComparablePrincipal",
):
    '''(experimental) Helper class for working with ``IComparablePrincipal``s.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        comparable_principal = iam.ComparablePrincipal()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="dedupeStringFor")
    @builtins.classmethod
    def dedupe_string_for(cls, x: "IPrincipal") -> typing.Optional[builtins.str]:
        '''(experimental) Return the dedupeString of the given principal, if available.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d748c7aa7bab2a43d26bb3d15942dac0380385cd7889b24ed4ca2f0d9d3a2941)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(typing.Optional[builtins.str], jsii.sinvoke(cls, "dedupeStringFor", [x]))

    @jsii.member(jsii_name="isComparablePrincipal")
    @builtins.classmethod
    def is_comparable_principal(cls, x: "IPrincipal") -> builtins.bool:
        '''(experimental) Whether or not the given principal is a comparable principal.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8db93bead5186c0248601fce80ea0d4471eebdb74a995a3fc52312ba1e0ed3f2)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(builtins.bool, jsii.sinvoke(cls, "isComparablePrincipal", [x]))


@jsii.implements(_IDependable_1175c9f7)
class CompositeDependable(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CompositeDependable",
):
    '''(experimental) Composite dependable.

    Not as simple as eagerly getting the dependency roots from the
    inner dependables, as they may be mutable so we need to defer
    the query.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_iam as iam
        
        # dependable: monocdk.IDependable
        
        composite_dependable = iam.CompositeDependable(dependable)
    '''

    def __init__(self, *dependables: _IDependable_1175c9f7) -> None:
        '''
        :param dependables: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__796fbf18d6a487ed99258d14dcf05d8b766095a618d7d9ceb8298c8a75c811cc)
            check_type(argname="argument dependables", value=dependables, expected_type=typing.Tuple[type_hints["dependables"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*dependables])


@jsii.enum(jsii_type="monocdk.aws_iam.Effect")
class Effect(enum.Enum):
    '''(experimental) The Effect element of an IAM policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_effect.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # books: apigateway.Resource
        # iam_user: iam.User
        
        
        get_books = books.add_method("GET", apigateway.HttpIntegration("http://amazon.com"),
            authorization_type=apigateway.AuthorizationType.IAM
        )
        
        iam_user.attach_inline_policy(iam.Policy(self, "AllowBooks",
            statements=[
                iam.PolicyStatement(
                    actions=["execute-api:Invoke"],
                    effect=iam.Effect.ALLOW,
                    resources=[get_books.method_arn]
                )
            ]
        ))
    '''

    ALLOW = "ALLOW"
    '''(experimental) Allows access to a resource in an IAM policy statement.

    By default, access to resources are denied.

    :stability: experimental
    '''
    DENY = "DENY"
    '''(experimental) Explicitly deny access to a resource.

    By default, all requests are denied implicitly.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html
    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_iam.FromRoleArnOptions",
    jsii_struct_bases=[],
    name_mapping={
        "add_grants_to_resources": "addGrantsToResources",
        "mutable": "mutable",
    },
)
class FromRoleArnOptions:
    def __init__(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options allowing customizing the behavior of {@link Role.fromRoleArn}.

        :param add_grants_to_resources: (experimental) For immutable roles: add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false
        :param mutable: (experimental) Whether the imported role can be modified by attaching policy resources to it. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            role = iam.Role.from_role_arn(self, "Role", "arn:aws:iam::123456789012:role/MyExistingRole",
                # Set 'mutable' to 'false' to use the role as-is and prevent adding new
                # policies to it. The default is 'true', which means the role may be
                # modified as part of the deployment.
                mutable=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__113dd30efbd95031e80d8a2e8a7306de2e9a90ed6555dcf24c8f32424c5d6313)
            check_type(argname="argument add_grants_to_resources", value=add_grants_to_resources, expected_type=type_hints["add_grants_to_resources"])
            check_type(argname="argument mutable", value=mutable, expected_type=type_hints["mutable"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_grants_to_resources is not None:
            self._values["add_grants_to_resources"] = add_grants_to_resources
        if mutable is not None:
            self._values["mutable"] = mutable

    @builtins.property
    def add_grants_to_resources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) For immutable roles: add grants to resources instead of dropping them.

        If this is ``false`` or not specified, grant permissions added to this role are ignored.
        It is your own responsibility to make sure the role has the required permissions.

        If this is ``true``, any grant permissions will be added to the resource instead.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("add_grants_to_resources")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def mutable(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the imported role can be modified by attaching policy resources to it.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("mutable")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FromRoleArnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IDependable_1175c9f7)
class Grant(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_iam.Grant"):
    '''(experimental) Result of a grant() operation.

    This class is not instantiable by consumers on purpose, so that they will be
    required to call the Grant factory functions.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # instance: ec2.Instance
        # volume: ec2.Volume
        
        
        attach_grant = volume.grant_attach_volume_by_resource_tag(instance.grant_principal, [instance])
        detach_grant = volume.grant_detach_volume_by_resource_tag(instance.grant_principal, [instance])
    '''

    @jsii.member(jsii_name="addToPrincipal")
    @builtins.classmethod
    def add_to_principal(
        cls,
        *,
        scope: typing.Optional[_IConstruct_5a0f9c5e] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''(experimental) Try to grant the given permissions to the given principal.

        Absence of a principal leads to a warning, but failing to add
        the permissions to a present principal is not an error.

        :param scope: (experimental) Construct to report warnings on in case grant could not be registered. Default: - the construct in which this construct is defined
        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        options = GrantOnPrincipalOptions(
            scope=scope, actions=actions, grantee=grantee, resource_arns=resource_arns
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipal", [options]))

    @jsii.member(jsii_name="addToPrincipalAndResource")
    @builtins.classmethod
    def add_to_principal_and_resource(
        cls,
        *,
        resource: "IResourceWithPolicy",
        resource_policy_principal: typing.Optional["IPrincipal"] = None,
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''(experimental) Add a grant both on the principal and on the resource.

        As long as any principal is given, granting on the principal may fail (in
        case of a non-identity principal), but granting on the resource will
        never fail.

        Statement will be the resource statement.

        :param resource: (experimental) The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: (experimental) The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: (experimental) When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        options = GrantOnPrincipalAndResourceOptions(
            resource=resource,
            resource_policy_principal=resource_policy_principal,
            resource_self_arns=resource_self_arns,
            actions=actions,
            grantee=grantee,
            resource_arns=resource_arns,
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipalAndResource", [options]))

    @jsii.member(jsii_name="addToPrincipalOrResource")
    @builtins.classmethod
    def add_to_principal_or_resource(
        cls,
        *,
        resource: "IResourceWithPolicy",
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
    ) -> "Grant":
        '''(experimental) Grant the given permissions to the principal.

        The permissions will be added to the principal policy primarily, falling
        back to the resource policy if necessary. The permissions must be granted
        somewhere.

        - Trying to grant permissions to a principal that does not admit adding to
          the principal policy while not providing a resource with a resource policy
          is an error.
        - Trying to grant permissions to an absent principal (possible in the
          case of imported resources) leads to a warning being added to the
          resource construct.

        :param resource: (experimental) The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: (experimental) When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs
        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        options = GrantWithResourceOptions(
            resource=resource,
            resource_self_arns=resource_self_arns,
            actions=actions,
            grantee=grantee,
            resource_arns=resource_arns,
        )

        return typing.cast("Grant", jsii.sinvoke(cls, "addToPrincipalOrResource", [options]))

    @jsii.member(jsii_name="drop")
    @builtins.classmethod
    def drop(cls, grantee: "IGrantable", _intent: builtins.str) -> "Grant":
        '''(experimental) Returns a "no-op" ``Grant`` object which represents a "dropped grant".

        This can be used for e.g. imported resources where you may not be able to modify
        the resource's policy or some underlying policy which you don't know about.

        :param grantee: The intended grantee.
        :param _intent: The user's intent (will be ignored at the moment).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2500d7ad2db0c1fe22f3b01cfc2344ff5f1a9197e561fd337325ac0135e230b7)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument _intent", value=_intent, expected_type=type_hints["_intent"])
        return typing.cast("Grant", jsii.sinvoke(cls, "drop", [grantee, _intent]))

    @jsii.member(jsii_name="applyBefore")
    def apply_before(self, *constructs: _IConstruct_5a0f9c5e) -> None:
        '''(experimental) Make sure this grant is applied before the given constructs are deployed.

        The same as construct.node.addDependency(grant), but slightly nicer to read.

        :param constructs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__33afaae65484f02d97629c95ea07b3503a1b777c130d956c9a5ed0063b7bf6e3)
            check_type(argname="argument constructs", value=constructs, expected_type=typing.Tuple[type_hints["constructs"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "applyBefore", [*constructs]))

    @jsii.member(jsii_name="assertSuccess")
    def assert_success(self) -> None:
        '''(experimental) Throw an error if this grant wasn't successful.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "assertSuccess", []))

    @builtins.property
    @jsii.member(jsii_name="success")
    def success(self) -> builtins.bool:
        '''(experimental) Whether the grant operation was successful.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "success"))

    @builtins.property
    @jsii.member(jsii_name="principalStatement")
    def principal_statement(self) -> typing.Optional["PolicyStatement"]:
        '''(experimental) The statement that was added to the principal's policy.

        Can be accessed to (e.g.) add additional conditions to the statement.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["PolicyStatement"], jsii.get(self, "principalStatement"))

    @builtins.property
    @jsii.member(jsii_name="resourceStatement")
    def resource_statement(self) -> typing.Optional["PolicyStatement"]:
        '''(experimental) The statement that was added to the resource policy.

        Can be accessed to (e.g.) add additional conditions to the statement.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["PolicyStatement"], jsii.get(self, "resourceStatement"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.GrantOnPrincipalAndResourceOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "resource": "resource",
        "resource_policy_principal": "resourcePolicyPrincipal",
        "resource_self_arns": "resourceSelfArns",
    },
)
class GrantOnPrincipalAndResourceOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        resource: "IResourceWithPolicy",
        resource_policy_principal: typing.Optional["IPrincipal"] = None,
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for a grant operation to both identity and resource.

        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.
        :param resource: (experimental) The resource with a resource policy. The statement will always be added to the resource policy.
        :param resource_policy_principal: (experimental) The principal to use in the statement for the resource policy. Default: - the principal of the grantee will be used
        :param resource_self_arns: (experimental) When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # grantable: iam.IGrantable
            # principal: iam.IPrincipal
            # resource_with_policy: iam.IResourceWithPolicy
            
            grant_on_principal_and_resource_options = iam.GrantOnPrincipalAndResourceOptions(
                actions=["actions"],
                grantee=grantable,
                resource=resource_with_policy,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                resource_policy_principal=principal,
                resource_self_arns=["resourceSelfArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4e3ebcd9a880a1e9c5fe53e41a03ffc19eee30fa132f3c0fc69047719415312a)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_policy_principal", value=resource_policy_principal, expected_type=type_hints["resource_policy_principal"])
            check_type(argname="argument resource_self_arns", value=resource_self_arns, expected_type=type_hints["resource_self_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
            "resource": resource,
        }
        if resource_policy_principal is not None:
            self._values["resource_policy_principal"] = resource_policy_principal
        if resource_self_arns is not None:
            self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to grant.

        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''(experimental) The principal to grant to.

        :default: if principal is undefined, no work is done.

        :stability: experimental
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''(experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        '''(experimental) The resource with a resource policy.

        The statement will always be added to the resource policy.

        :stability: experimental
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast("IResourceWithPolicy", result)

    @builtins.property
    def resource_policy_principal(self) -> typing.Optional["IPrincipal"]:
        '''(experimental) The principal to use in the statement for the resource policy.

        :default: - the principal of the grantee will be used

        :stability: experimental
        '''
        result = self._values.get("resource_policy_principal")
        return typing.cast(typing.Optional["IPrincipal"], result)

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        :default: Same as regular resource ARNs

        :stability: experimental
        '''
        result = self._values.get("resource_self_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOnPrincipalAndResourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.GrantOnPrincipalOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "scope": "scope",
    },
)
class GrantOnPrincipalOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        scope: typing.Optional[_IConstruct_5a0f9c5e] = None,
    ) -> None:
        '''(experimental) Options for a grant operation that only applies to principals.

        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.
        :param scope: (experimental) Construct to report warnings on in case grant could not be registered. Default: - the construct in which this construct is defined

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_iam as iam
            
            # construct: monocdk.Construct
            # grantable: iam.IGrantable
            
            grant_on_principal_options = iam.GrantOnPrincipalOptions(
                actions=["actions"],
                grantee=grantable,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                scope=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32be6673535c40632c5e1aa0155055224c1c616a2a976e92191a0498336b70d1)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
        }
        if scope is not None:
            self._values["scope"] = scope

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to grant.

        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''(experimental) The principal to grant to.

        :default: if principal is undefined, no work is done.

        :stability: experimental
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''(experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def scope(self) -> typing.Optional[_IConstruct_5a0f9c5e]:
        '''(experimental) Construct to report warnings on in case grant could not be registered.

        :default: - the construct in which this construct is defined

        :stability: experimental
        '''
        result = self._values.get("scope")
        return typing.cast(typing.Optional[_IConstruct_5a0f9c5e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantOnPrincipalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.GrantWithResourceOptions",
    jsii_struct_bases=[CommonGrantOptions],
    name_mapping={
        "actions": "actions",
        "grantee": "grantee",
        "resource_arns": "resourceArns",
        "resource": "resource",
        "resource_self_arns": "resourceSelfArns",
    },
)
class GrantWithResourceOptions(CommonGrantOptions):
    def __init__(
        self,
        *,
        actions: typing.Sequence[builtins.str],
        grantee: "IGrantable",
        resource_arns: typing.Sequence[builtins.str],
        resource: "IResourceWithPolicy",
        resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Options for a grant operation.

        :param actions: (experimental) The actions to grant.
        :param grantee: (experimental) The principal to grant to. Default: if principal is undefined, no work is done.
        :param resource_arns: (experimental) The resource ARNs to grant to.
        :param resource: (experimental) The resource with a resource policy. The statement will be added to the resource policy if it couldn't be added to the principal policy.
        :param resource_self_arns: (experimental) When referring to the resource in a resource policy, use this as ARN. (Depending on the resource type, this needs to be '*' in a resource policy). Default: Same as regular resource ARNs

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # grantable: iam.IGrantable
            # resource_with_policy: iam.IResourceWithPolicy
            
            grant_with_resource_options = iam.GrantWithResourceOptions(
                actions=["actions"],
                grantee=grantable,
                resource=resource_with_policy,
                resource_arns=["resourceArns"],
            
                # the properties below are optional
                resource_self_arns=["resourceSelfArns"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d857fadaf9384d4f4bea13ca3123a8b1cfb66ac6f0189af3664729097e0d8a5)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
            check_type(argname="argument resource_self_arns", value=resource_self_arns, expected_type=type_hints["resource_self_arns"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "actions": actions,
            "grantee": grantee,
            "resource_arns": resource_arns,
            "resource": resource,
        }
        if resource_self_arns is not None:
            self._values["resource_self_arns"] = resource_self_arns

    @builtins.property
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) The actions to grant.

        :stability: experimental
        '''
        result = self._values.get("actions")
        assert result is not None, "Required property 'actions' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def grantee(self) -> "IGrantable":
        '''(experimental) The principal to grant to.

        :default: if principal is undefined, no work is done.

        :stability: experimental
        '''
        result = self._values.get("grantee")
        assert result is not None, "Required property 'grantee' is missing"
        return typing.cast("IGrantable", result)

    @builtins.property
    def resource_arns(self) -> typing.List[builtins.str]:
        '''(experimental) The resource ARNs to grant to.

        :stability: experimental
        '''
        result = self._values.get("resource_arns")
        assert result is not None, "Required property 'resource_arns' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def resource(self) -> "IResourceWithPolicy":
        '''(experimental) The resource with a resource policy.

        The statement will be added to the resource policy if it couldn't be
        added to the principal policy.

        :stability: experimental
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast("IResourceWithPolicy", result)

    @builtins.property
    def resource_self_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) When referring to the resource in a resource policy, use this as ARN.

        (Depending on the resource type, this needs to be '*' in a resource policy).

        :default: Same as regular resource ARNs

        :stability: experimental
        '''
        result = self._values.get("resource_self_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GrantWithResourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.GroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "group_name": "groupName",
        "managed_policies": "managedPolicies",
        "path": "path",
    },
)
class GroupProps:
    def __init__(
        self,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.Sequence["IManagedPolicy"]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM group.

        :param group_name: (experimental) A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: (experimental) The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # managed_policy: iam.ManagedPolicy
            
            group_props = iam.GroupProps(
                group_name="groupName",
                managed_policies=[managed_policy],
                path="path"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3457a99d3d669d5f6820eab0f29541cc813d92b70e68b1ab5501f52a2d9b4c0)
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if group_name is not None:
            self._values["group_name"] = group_name
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the IAM group.

        For valid values, see the GroupName parameter
        for the CreateGroup action in the IAM API Reference. If you don't specify
        a name, AWS CloudFormation generates a unique physical ID and uses that
        ID for the group name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default: Generated by CloudFormation (recommended)

        :stability: experimental
        '''
        result = self._values.get("group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List["IManagedPolicy"]]:
        '''(experimental) A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.

        :stability: experimental
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List["IManagedPolicy"]], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the group.

        For more information about paths, see `IAM
        Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_
        in the IAM User Guide.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_iam.IAccessKey")
class IAccessKey(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IAM Access Key.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''(experimental) The Access Key ID.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _SecretValue_c18506ef:
        '''(experimental) The Secret Access Key.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAccessKeyProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an IAM Access Key.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IAccessKey"

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''(experimental) The Access Key ID.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _SecretValue_c18506ef:
        '''(experimental) The Secret Access Key.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_SecretValue_c18506ef, jsii.get(self, "secretAccessKey"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAccessKey).__jsii_proxy_class__ = lambda : _IAccessKeyProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IGrantable")
class IGrantable(typing_extensions.Protocol):
    '''(experimental) Any object that has an associated principal that a permission can be granted to.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        ...


class _IGrantableProxy:
    '''(experimental) Any object that has an associated principal that a permission can be granted to.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IGrantable"

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> "IPrincipal":
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast("IPrincipal", jsii.get(self, "grantPrincipal"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGrantable).__jsii_proxy_class__ = lambda : _IGrantableProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IManagedPolicy")
class IManagedPolicy(typing_extensions.Protocol):
    '''(experimental) A managed policy.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''(experimental) The ARN of the managed policy.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IManagedPolicyProxy:
    '''(experimental) A managed policy.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IManagedPolicy"

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''(experimental) The ARN of the managed policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IManagedPolicy).__jsii_proxy_class__ = lambda : _IManagedPolicyProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IOpenIdConnectProvider")
class IOpenIdConnectProvider(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IAM OpenID Connect provider.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''(experimental) The issuer for OIDC Provider.

        :stability: experimental
        '''
        ...


class _IOpenIdConnectProviderProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an IAM OpenID Connect provider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IOpenIdConnectProvider"

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderArn"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''(experimental) The issuer for OIDC Provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderIssuer"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IOpenIdConnectProvider).__jsii_proxy_class__ = lambda : _IOpenIdConnectProviderProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IPolicy")
class IPolicy(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) Represents an IAM Policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''(experimental) The name of this policy.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IPolicyProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) Represents an IAM Policy.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_manage.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IPolicy"

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''(experimental) The name of this policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPolicy).__jsii_proxy_class__ = lambda : _IPolicyProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IPrincipal")
class IPrincipal(IGrantable, typing_extensions.Protocol):
    '''(experimental) Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> builtins.bool:
        '''(deprecated) Add to the policy of this principal.

        :param statement: -

        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.

        :deprecated: Use ``addToPrincipalPolicy`` instead.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        ...


class _IPrincipalProxy(
    jsii.proxy_for(IGrantable), # type: ignore[misc]
):
    '''(experimental) Represents a logical IAM principal.

    An IPrincipal describes a logical entity that can perform AWS API calls
    against sets of resources, optionally under certain conditions.

    Examples of simple principals are IAM objects that you create, such
    as Users or Roles.

    An example of a more complex principals is a ``ServicePrincipal`` (such as
    ``new ServicePrincipal("sns.amazonaws.com")``, which represents the Simple
    Notifications Service).

    A single logical Principal may also map to a set of physical principals.
    For example, ``new OrganizationPrincipal('o-1234')`` represents all
    identities that are part of the given AWS Organization.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IPrincipal"

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> "PrincipalPolicyFragment":
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast("PrincipalPolicyFragment", jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: "PolicyStatement") -> builtins.bool:
        '''(deprecated) Add to the policy of this principal.

        :param statement: -

        :return:

        true if the statement was added, false if the principal in
        question does not have a policy document to add the statement to.

        :deprecated: Use ``addToPrincipalPolicy`` instead.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cef352b1b4609818242fbd4ce07299724c199dae36651f4b74a862ae89535fb)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e9e7c38ccab985da14ec9adb31b03cc2f7e0773c2f15e694434de0b6ce1aee)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IPrincipal).__jsii_proxy_class__ = lambda : _IPrincipalProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IResourceWithPolicy")
class IResourceWithPolicy(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A resource with a resource policy that can be added to.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToResourcePolicyResult:
        '''(experimental) Add a statement to the resource's resource policy.

        :param statement: -

        :stability: experimental
        '''
        ...


class _IResourceWithPolicyProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A resource with a resource policy that can be added to.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IResourceWithPolicy"

    @jsii.member(jsii_name="addToResourcePolicy")
    def add_to_resource_policy(
        self,
        statement: "PolicyStatement",
    ) -> AddToResourcePolicyResult:
        '''(experimental) Add a statement to the resource's resource policy.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd76918a27747150e0e6707e087c913d95d340a16a9f3f2adc165770291fe4a4)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToResourcePolicyResult, jsii.invoke(self, "addToResourcePolicy", [statement]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IResourceWithPolicy).__jsii_proxy_class__ = lambda : _IResourceWithPolicyProxy


@jsii.interface(jsii_type="monocdk.aws_iam.ISamlProvider")
class ISamlProvider(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A SAML provider.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the provider.

        :stability: experimental
        :attribute: true
        '''
        ...


class _ISamlProviderProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A SAML provider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.ISamlProvider"

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the provider.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "samlProviderArn"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISamlProvider).__jsii_proxy_class__ = lambda : _ISamlProviderProxy


@jsii.implements(IManagedPolicy)
class ManagedPolicy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.ManagedPolicy",
):
    '''(experimental) Managed policy.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_role = iam.Role(self, "My Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        fn = lambda_.Function(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_16_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            role=my_role
        )
        
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        my_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional["PolicyDocument"] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param description: (experimental) A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param document: (experimental) Initial PolicyDocument to use for this ManagedPolicy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param groups: (experimental) Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: (experimental) The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: (experimental) The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: (experimental) Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: (experimental) Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: (experimental) Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dad52d68d4417c62f8e067aea7ba55944c0e1819ef0866e8d262826e784041a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManagedPolicyProps(
            description=description,
            document=document,
            groups=groups,
            managed_policy_name=managed_policy_name,
            path=path,
            roles=roles,
            statements=statements,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAwsManagedPolicyName")
    @builtins.classmethod
    def from_aws_managed_policy_name(
        cls,
        managed_policy_name: builtins.str,
    ) -> IManagedPolicy:
        '''(experimental) Import a managed policy from one of the policies that AWS manages.

        For this managed policy, you only need to know the name to be able to use it.

        Some managed policy names start with "service-role/", some start with
        "job-function/", and some don't start with anything. Include the
        prefix when constructing this object.

        :param managed_policy_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc98b3ba7579a754738b9d083fdd2784faeb06a8477e2ad12f851604f9a5d5db)
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromAwsManagedPolicyName", [managed_policy_name]))

    @jsii.member(jsii_name="fromManagedPolicyArn")
    @builtins.classmethod
    def from_managed_policy_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        managed_policy_arn: builtins.str,
    ) -> IManagedPolicy:
        '''(experimental) Import an external managed policy by ARN.

        For this managed policy, you only need to know the ARN to be able to use it.
        This can be useful if you got the ARN from a CloudFormation Export.

        If the imported Managed Policy ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        managed policy has a ``path`` (like ``arn:...:policy/AdminPolicy/AdminAllow``), the
        ``managedPolicyName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Managed Policy ARN should be supplied without the
        ``path`` in order to resolve the correct managed policy resource.

        :param scope: construct scope.
        :param id: construct id.
        :param managed_policy_arn: the ARN of the managed policy to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44ea6a7d7bc18419cb3ca0a4593c90b301c387b10a9cab19bd3f87afa912f908)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_policy_arn", value=managed_policy_arn, expected_type=type_hints["managed_policy_arn"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromManagedPolicyArn", [scope, id, managed_policy_arn]))

    @jsii.member(jsii_name="fromManagedPolicyName")
    @builtins.classmethod
    def from_managed_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        managed_policy_name: builtins.str,
    ) -> IManagedPolicy:
        '''(experimental) Import a customer managed policy from the managedPolicyName.

        For this managed policy, you only need to know the name to be able to use it.

        :param scope: -
        :param id: -
        :param managed_policy_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__66b9089da65cf6c2cc3350a479d670bc6a19f1b53e7f117ce01b4ee92412e548)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
        return typing.cast(IManagedPolicy, jsii.sinvoke(cls, "fromManagedPolicyName", [scope, id, managed_policy_name]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''(experimental) Adds a statement to the policy document.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d99c718d018f1ce06685d3378e7bd30cc042a840f95130042fcc9d9a7c38c4f6)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        '''(experimental) Attaches this policy to a group.

        :param group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73dc4c77a305b2a62ba7dfb3f923ae359ddface29ef9c6c77c64ac0b44ef14ac)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "attachToGroup", [group]))

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        '''(experimental) Attaches this policy to a role.

        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ec2ea2644d49f9637790e892ca423452da05d54959b505888286e12f814e296a)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "attachToRole", [role]))

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        '''(experimental) Attaches this policy to a user.

        :param user: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5be1ed600a4df9bb4370045150838cc261e4fc6239232235487c479bd9ac0a7d)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "attachToUser", [user]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''(experimental) The description of this policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        '''(experimental) The policy document.

        :stability: experimental
        '''
        return typing.cast("PolicyDocument", jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyArn")
    def managed_policy_arn(self) -> builtins.str:
        '''(experimental) Returns the ARN of this managed policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyArn"))

    @builtins.property
    @jsii.member(jsii_name="managedPolicyName")
    def managed_policy_name(self) -> builtins.str:
        '''(experimental) The name of this policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "managedPolicyName"))

    @builtins.property
    @jsii.member(jsii_name="path")
    def path(self) -> builtins.str:
        '''(experimental) The path of this policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "path"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.ManagedPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "document": "document",
        "groups": "groups",
        "managed_policy_name": "managedPolicyName",
        "path": "path",
        "roles": "roles",
        "statements": "statements",
        "users": "users",
    },
)
class ManagedPolicyProps:
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        document: typing.Optional["PolicyDocument"] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policy_name: typing.Optional[builtins.str] = None,
        path: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM managed policy.

        :param description: (experimental) A description of the managed policy. Typically used to store information about the permissions defined in the policy. For example, "Grants access to production DynamoDB tables." The policy description is immutable. After a value is assigned, it cannot be changed. Default: - empty
        :param document: (experimental) Initial PolicyDocument to use for this ManagedPolicy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param groups: (experimental) Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param managed_policy_name: (experimental) The name of the managed policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - A name is automatically generated.
        :param path: (experimental) The path for the policy. This parameter allows (through its regex pattern) a string of characters consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes. In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F), including most punctuation characters, digits, and upper and lowercased letters. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: - "/"
        :param roles: (experimental) Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: (experimental) Initial set of permissions to add to this policy document. You can also use ``addPermission(statement)`` to add permissions later. Default: - No statements.
        :param users: (experimental) Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            policy_document = {
                "Version": "2012-10-17",
                "Statement": [{
                    "Sid": "FirstStatement",
                    "Effect": "Allow",
                    "Action": ["iam:ChangePassword"],
                    "Resource": "*"
                }, {
                    "Sid": "SecondStatement",
                    "Effect": "Allow",
                    "Action": "s3:ListAllMyBuckets",
                    "Resource": "*"
                }, {
                    "Sid": "ThirdStatement",
                    "Effect": "Allow",
                    "Action": ["s3:List*", "s3:Get*"
                    ],
                    "Resource": ["arn:aws:s3:::confidential-data", "arn:aws:s3:::confidential-data/*"
                    ],
                    "Condition": {"Bool": {"aws:_multi_factor_auth_present": "true"}}
                }
                ]
            }
            
            custom_policy_document = iam.PolicyDocument.from_json(policy_document)
            
            # You can pass this document as an initial document to a ManagedPolicy
            # or inline Policy.
            new_managed_policy = iam.ManagedPolicy(self, "MyNewManagedPolicy",
                document=custom_policy_document
            )
            new_policy = iam.Policy(self, "MyNewPolicy",
                document=custom_policy_document
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4632e60b96836c3e86adf2c0b865fbb5df38c091802d4045f90fef2cdf85930)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policy_name", value=managed_policy_name, expected_type=type_hints["managed_policy_name"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if description is not None:
            self._values["description"] = description
        if document is not None:
            self._values["document"] = document
        if groups is not None:
            self._values["groups"] = groups
        if managed_policy_name is not None:
            self._values["managed_policy_name"] = managed_policy_name
        if path is not None:
            self._values["path"] = path
        if roles is not None:
            self._values["roles"] = roles
        if statements is not None:
            self._values["statements"] = statements
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the managed policy.

        Typically used to store information about the
        permissions defined in the policy. For example, "Grants access to production DynamoDB tables."
        The policy description is immutable. After a value is assigned, it cannot be changed.

        :default: - empty

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def document(self) -> typing.Optional["PolicyDocument"]:
        '''(experimental) Initial PolicyDocument to use for this ManagedPolicy.

        If omited, any
        ``PolicyStatement`` provided in the ``statements`` property will be applied
        against the empty default ``PolicyDocument``.

        :default: - An empty policy.

        :stability: experimental
        '''
        result = self._values.get("document")
        return typing.cast(typing.Optional["PolicyDocument"], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''(experimental) Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        :default: - No groups.

        :stability: experimental
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def managed_policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the managed policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        :default: - A name is automatically generated.

        :stability: experimental
        '''
        result = self._values.get("managed_policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path for the policy.

        This parameter allows (through its regex pattern) a string of characters
        consisting of either a forward slash (/) by itself or a string that must begin and end with forward slashes.
        In addition, it can contain any ASCII character from the ! (\\u0021) through the DEL character (\\u007F),
        including most punctuation characters, digits, and upper and lowercased letters.

        For more information about paths, see IAM Identifiers in the IAM User Guide.

        :default: - "/"

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        '''(experimental) Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        :default: - No roles.

        :stability: experimental
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List["IRole"]], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''(experimental) Initial set of permissions to add to this policy document.

        You can also use ``addPermission(statement)`` to add permissions later.

        :default: - No statements.

        :stability: experimental
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        '''(experimental) Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        :default: - No users.

        :stability: experimental
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["IUser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManagedPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IOpenIdConnectProvider)
class OpenIdConnectProvider(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.OpenIdConnectProvider",
):
    '''(experimental) IAM OIDC identity providers are entities in IAM that describe an external identity provider (IdP) service that supports the OpenID Connect (OIDC) standard, such as Google or Salesforce.

    You use an IAM OIDC identity provider
    when you want to establish trust between an OIDC-compatible IdP and your AWS
    account. This is useful when creating a mobile app or web application that
    requires access to AWS resources, but you don't want to create custom sign-in
    code or manage your own user identities.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_oidc.html
    :stability: experimental
    :resource: AWS::CloudFormation::CustomResource
    :exampleMetadata: infused

    Example::

        provider = iam.OpenIdConnectProvider(self, "MyProvider",
            url="https://openid/connect",
            client_ids=["myclient1", "myclient2"]
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        url: builtins.str,
        client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Defines an OpenID Connect provider.

        :param scope: The definition scope.
        :param id: Construct ID.
        :param url: (experimental) The URL of the identity provider. The URL must begin with https:// and should correspond to the iss claim in the provider's OpenID Connect ID tokens. Per the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a hostname, like https://server.example.org or https://example.com. You cannot register the same provider multiple times in a single AWS account. If you try to submit a URL that has already been used for an OpenID Connect provider in the AWS account, you will get an error.
        :param client_ids: (experimental) A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that's sent as the client_id parameter on OAuth requests.) You can register multiple client IDs with the same provider. For example, you might have multiple applications that use the same OIDC provider. You cannot register more than 100 client IDs with a single IAM OIDC provider. Client IDs are up to 255 characters long. Default: - no clients are allowed
        :param thumbprints: (experimental) A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates. Typically this list includes only one entry. However, IAM lets you have up to five thumbprints for an OIDC provider. This lets you maintain multiple thumbprints if the identity provider is rotating certificates. The server certificate thumbprint is the hex-encoded SHA-1 hash value of the X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string. You must provide at least one thumbprint when creating an IAM OIDC provider. For example, assume that the OIDC provider is server.example.com and the provider stores its keys at https://keys.server.example.com/openid-connect. In that case, the thumbprint string would be the hex-encoded SHA-1 hash value of the certificate used by https://keys.server.example.com. Default: - If no thumbprints are specified (an empty array or ``undefined``), the thumbprint of the root certificate authority will be obtained from the provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8f099ca9fde67df8fe4f8d106dc9b8c511302707b1d02da4b57394306a49149)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = OpenIdConnectProviderProps(
            url=url, client_ids=client_ids, thumbprints=thumbprints
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromOpenIdConnectProviderArn")
    @builtins.classmethod
    def from_open_id_connect_provider_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        open_id_connect_provider_arn: builtins.str,
    ) -> IOpenIdConnectProvider:
        '''(experimental) Imports an Open ID connect provider from an ARN.

        :param scope: The definition scope.
        :param id: ID of the construct.
        :param open_id_connect_provider_arn: the ARN to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65841d1f1daf7d051fb9333d7658c734c770539a18ef3d135b86316b57d79d05)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument open_id_connect_provider_arn", value=open_id_connect_provider_arn, expected_type=type_hints["open_id_connect_provider_arn"])
        return typing.cast(IOpenIdConnectProvider, jsii.sinvoke(cls, "fromOpenIdConnectProviderArn", [scope, id, open_id_connect_provider_arn]))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderArn")
    def open_id_connect_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the IAM OpenID Connect provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderArn"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderIssuer")
    def open_id_connect_provider_issuer(self) -> builtins.str:
        '''(experimental) The issuer for OIDC Provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderIssuer"))

    @builtins.property
    @jsii.member(jsii_name="openIdConnectProviderthumbprints")
    def open_id_connect_providerthumbprints(self) -> builtins.str:
        '''(experimental) The thumbprints configured for this provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "openIdConnectProviderthumbprints"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.OpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "url": "url",
        "client_ids": "clientIds",
        "thumbprints": "thumbprints",
    },
)
class OpenIdConnectProviderProps:
    def __init__(
        self,
        *,
        url: builtins.str,
        client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Initialization properties for ``OpenIdConnectProvider``.

        :param url: (experimental) The URL of the identity provider. The URL must begin with https:// and should correspond to the iss claim in the provider's OpenID Connect ID tokens. Per the OIDC standard, path components are allowed but query parameters are not. Typically the URL consists of only a hostname, like https://server.example.org or https://example.com. You cannot register the same provider multiple times in a single AWS account. If you try to submit a URL that has already been used for an OpenID Connect provider in the AWS account, you will get an error.
        :param client_ids: (experimental) A list of client IDs (also known as audiences). When a mobile or web app registers with an OpenID Connect provider, they establish a value that identifies the application. (This is the value that's sent as the client_id parameter on OAuth requests.) You can register multiple client IDs with the same provider. For example, you might have multiple applications that use the same OIDC provider. You cannot register more than 100 client IDs with a single IAM OIDC provider. Client IDs are up to 255 characters long. Default: - no clients are allowed
        :param thumbprints: (experimental) A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates. Typically this list includes only one entry. However, IAM lets you have up to five thumbprints for an OIDC provider. This lets you maintain multiple thumbprints if the identity provider is rotating certificates. The server certificate thumbprint is the hex-encoded SHA-1 hash value of the X.509 certificate used by the domain where the OpenID Connect provider makes its keys available. It is always a 40-character string. You must provide at least one thumbprint when creating an IAM OIDC provider. For example, assume that the OIDC provider is server.example.com and the provider stores its keys at https://keys.server.example.com/openid-connect. In that case, the thumbprint string would be the hex-encoded SHA-1 hash value of the certificate used by https://keys.server.example.com. Default: - If no thumbprints are specified (an empty array or ``undefined``), the thumbprint of the root certificate authority will be obtained from the provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html

        :stability: experimental
        :exampleMetadata: infused

        Example::

            provider = iam.OpenIdConnectProvider(self, "MyProvider",
                url="https://openid/connect",
                client_ids=["myclient1", "myclient2"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__194521551a8bd320b87c90b1f5e6b60046fffc45ea1ac6ac5c2553c8df84c3bf)
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
            check_type(argname="argument client_ids", value=client_ids, expected_type=type_hints["client_ids"])
            check_type(argname="argument thumbprints", value=thumbprints, expected_type=type_hints["thumbprints"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "url": url,
        }
        if client_ids is not None:
            self._values["client_ids"] = client_ids
        if thumbprints is not None:
            self._values["thumbprints"] = thumbprints

    @builtins.property
    def url(self) -> builtins.str:
        '''(experimental) The URL of the identity provider.

        The URL must begin with https:// and
        should correspond to the iss claim in the provider's OpenID Connect ID
        tokens. Per the OIDC standard, path components are allowed but query
        parameters are not. Typically the URL consists of only a hostname, like
        https://server.example.org or https://example.com.

        You cannot register the same provider multiple times in a single AWS
        account. If you try to submit a URL that has already been used for an
        OpenID Connect provider in the AWS account, you will get an error.

        :stability: experimental
        '''
        result = self._values.get("url")
        assert result is not None, "Required property 'url' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def client_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of client IDs (also known as audiences).

        When a mobile or web app
        registers with an OpenID Connect provider, they establish a value that
        identifies the application. (This is the value that's sent as the client_id
        parameter on OAuth requests.)

        You can register multiple client IDs with the same provider. For example,
        you might have multiple applications that use the same OIDC provider. You
        cannot register more than 100 client IDs with a single IAM OIDC provider.

        Client IDs are up to 255 characters long.

        :default: - no clients are allowed

        :stability: experimental
        '''
        result = self._values.get("client_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def thumbprints(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of server certificate thumbprints for the OpenID Connect (OIDC) identity provider's server certificates.

        Typically this list includes only one entry. However, IAM lets you have up
        to five thumbprints for an OIDC provider. This lets you maintain multiple
        thumbprints if the identity provider is rotating certificates.

        The server certificate thumbprint is the hex-encoded SHA-1 hash value of
        the X.509 certificate used by the domain where the OpenID Connect provider
        makes its keys available. It is always a 40-character string.

        You must provide at least one thumbprint when creating an IAM OIDC
        provider. For example, assume that the OIDC provider is server.example.com
        and the provider stores its keys at
        https://keys.server.example.com/openid-connect. In that case, the
        thumbprint string would be the hex-encoded SHA-1 hash value of the
        certificate used by https://keys.server.example.com.

        :default:

        - If no thumbprints are specified (an empty array or ``undefined``),
        the thumbprint of the root certificate authority will be obtained from the
        provider's server as described in https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc_verify-thumbprint.html

        :stability: experimental
        '''
        result = self._values.get("thumbprints")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PermissionsBoundary(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.PermissionsBoundary",
):
    '''(experimental) Modify the Permissions Boundaries of Users and Roles in a construct tree.

    Example::

       policy = iam.ManagedPolicy.from_aws_managed_policy_name("ReadOnlyAccess")
       iam.PermissionsBoundary.of(self).apply(policy)

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # project: codebuild.Project
        
        iam.PermissionsBoundary.of(project).apply(codebuild.UntrustedCodeBoundaryPolicy(self, "Boundary"))
    '''

    @jsii.member(jsii_name="of")
    @builtins.classmethod
    def of(cls, scope: _constructs_77d1e7e8.IConstruct) -> "PermissionsBoundary":
        '''(experimental) Access the Permissions Boundaries of a construct tree.

        :param scope: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e465496c36009643e8e100ab459cf1a1795fa41ba4340d5f71f520aebfbb7785)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast("PermissionsBoundary", jsii.sinvoke(cls, "of", [scope]))

    @jsii.member(jsii_name="apply")
    def apply(self, boundary_policy: IManagedPolicy) -> None:
        '''(experimental) Apply the given policy as Permissions Boundary to all Roles and Users in the scope.

        Will override any Permissions Boundaries configured previously; in case
        a Permission Boundary is applied in multiple scopes, the Boundary applied
        closest to the Role wins.

        :param boundary_policy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a18ae37fcb7498b0a25b802f460754eaa037765be71770dc04c80e051da74a7)
            check_type(argname="argument boundary_policy", value=boundary_policy, expected_type=type_hints["boundary_policy"])
        return typing.cast(None, jsii.invoke(self, "apply", [boundary_policy]))

    @jsii.member(jsii_name="clear")
    def clear(self) -> None:
        '''(experimental) Remove previously applied Permissions Boundaries.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "clear", []))


@jsii.implements(IPolicy)
class Policy(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.Policy",
):
    '''(experimental) The AWS::IAM::Policy resource associates an IAM policy with IAM users, roles, or groups.

    For more information about IAM policies, see `Overview of IAM
    Policies <http://docs.aws.amazon.com/IAM/latest/UserGuide/policies_overview.html>`_
    in the IAM User Guide guide.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # post_auth_fn: lambda.Function
        
        
        userpool = cognito.UserPool(self, "myuserpool",
            lambda_triggers=certificatemanager.aws_cognito.UserPoolTriggers(
                post_authentication=post_auth_fn
            )
        )
        
        # provide permissions to describe the user pool scoped to the ARN the user pool
        post_auth_fn.role.attach_inline_policy(iam.Policy(self, "userpool-policy",
            statements=[iam.PolicyStatement(
                actions=["cognito-idp:DescribeUserPool"],
                resources=[userpool.user_pool_arn]
            )]
        ))
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        document: typing.Optional["PolicyDocument"] = None,
        force: typing.Optional[builtins.bool] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        policy_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param document: (experimental) Initial PolicyDocument to use for this Policy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param force: (experimental) Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can set this to ``true``. Default: false
        :param groups: (experimental) Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: (experimental) The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: (experimental) Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: (experimental) Initial set of permissions to add to this policy document. You can also use ``addStatements(...statement)`` to add permissions later. Default: - No statements.
        :param users: (experimental) Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dfb9f54f1d6d67ba10ae1851caf3d9ac0c99e277ad2f5b898837bac846c7ffe)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PolicyProps(
            document=document,
            force=force,
            groups=groups,
            policy_name=policy_name,
            roles=roles,
            statements=statements,
            users=users,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromPolicyName")
    @builtins.classmethod
    def from_policy_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        policy_name: builtins.str,
    ) -> IPolicy:
        '''(experimental) Import a policy in this app based on its name.

        :param scope: -
        :param id: -
        :param policy_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd8be90172bdb2af6d199744f23c4574d1d621a0ea5dde4d3ff84f28c260d6dd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
        return typing.cast(IPolicy, jsii.sinvoke(cls, "fromPolicyName", [scope, id, policy_name]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''(experimental) Adds a statement to the policy document.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfbae63bd491de9985a184344c9e53ceac666bb2e7279576ea881d152cf59c3a)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="attachToGroup")
    def attach_to_group(self, group: "IGroup") -> None:
        '''(experimental) Attaches this policy to a group.

        :param group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__88ff22e4b732f1c4d955b295276c95310eab4fc157c2718ac6618f20cfc2d784)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "attachToGroup", [group]))

    @jsii.member(jsii_name="attachToRole")
    def attach_to_role(self, role: "IRole") -> None:
        '''(experimental) Attaches this policy to a role.

        :param role: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ecf54afb4d65976a4c5a91f513c0d3536d44e06f03337230dbb0ace314c15693)
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        return typing.cast(None, jsii.invoke(self, "attachToRole", [role]))

    @jsii.member(jsii_name="attachToUser")
    def attach_to_user(self, user: "IUser") -> None:
        '''(experimental) Attaches this policy to a user.

        :param user: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f6dc5ece5b25150251648ee7f6109ff96f8b58ffd33b779cfdb946ee6b7c7197)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "attachToUser", [user]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="document")
    def document(self) -> "PolicyDocument":
        '''(experimental) The policy document.

        :stability: experimental
        '''
        return typing.cast("PolicyDocument", jsii.get(self, "document"))

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''(experimental) The name of this policy.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))


@jsii.implements(_IResolvable_a771d0ef)
class PolicyDocument(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.PolicyDocument",
):
    '''(experimental) A PolicyDocument is a collection of statements.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        my_trusted_admin_role = iam.Role.from_role_arn(self, "TrustedRole", "arn:aws:iam:....")
        # Creates a limited admin policy and assigns to the account root.
        my_custom_policy = iam.PolicyDocument(
            statements=[iam.PolicyStatement(
                actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"
                ],
                principals=[iam.AccountRootPrincipal()],
                resources=["*"]
            )]
        )
        key = kms.Key(self, "MyKey",
            policy=my_custom_policy
        )
    '''

    def __init__(
        self,
        *,
        assign_sids: typing.Optional[builtins.bool] = None,
        minimize: typing.Optional[builtins.bool] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
    ) -> None:
        '''
        :param assign_sids: (experimental) Automatically assign Statement Ids to all statements. Default: false
        :param minimize: (experimental) Try to minimize the policy by merging statements. To avoid overrunning the maximum policy size, combine statements if they produce the same result. Merging happens according to the following rules: - The Effect of both statements is the same - Neither of the statements have a 'Sid' - Combine Principals if the rest of the statement is exactly the same. - Combine Resources if the rest of the statement is exactly the same. - Combine Actions if the rest of the statement is exactly the same. - We will never combine NotPrincipals, NotResources or NotActions, because doing so would change the meaning of the policy document. Default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set
        :param statements: (experimental) Initial statements to add to the policy document. Default: - No statements

        :stability: experimental
        '''
        props = PolicyDocumentProps(
            assign_sids=assign_sids, minimize=minimize, statements=statements
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromJson")
    @builtins.classmethod
    def from_json(cls, obj: typing.Any) -> "PolicyDocument":
        '''(experimental) Creates a new PolicyDocument based on the object provided.

        This will accept an object created from the ``.toJSON()`` call

        :param obj: the PolicyDocument in object form.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3632bf0429b2ead03fc2244dad500274e6b30852db6957a77e85a2331f7496)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("PolicyDocument", jsii.sinvoke(cls, "fromJson", [obj]))

    @jsii.member(jsii_name="addStatements")
    def add_statements(self, *statement: "PolicyStatement") -> None:
        '''(experimental) Adds a statement to the policy document.

        :param statement: the statement to add.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5c31df481edfc978e75bc2420910bedca67066cae379c96e6b3e333b41135d)
            check_type(argname="argument statement", value=statement, expected_type=typing.Tuple[type_hints["statement"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addStatements", [*statement]))

    @jsii.member(jsii_name="resolve")
    def resolve(self, context: _IResolveContext_e363e2cb) -> typing.Any:
        '''(experimental) Produce the Token's value at resolution time.

        :param context: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8ec693e55c88e20f55aa23668c3b9bc909dfdfde7ae24f32be8dcb1e0214534)
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
        return typing.cast(typing.Any, jsii.invoke(self, "resolve", [context]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''(experimental) JSON-ify the document.

        Used when JSON.stringify() is called

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Encode the policy document as a string.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="validateForAnyPolicy")
    def validate_for_any_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that all policy statements in the policy document satisfies the requirements for any policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForAnyPolicy", []))

    @jsii.member(jsii_name="validateForIdentityPolicy")
    def validate_for_identity_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that all policy statements in the policy document satisfies the requirements for an identity-based policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForIdentityPolicy", []))

    @jsii.member(jsii_name="validateForResourcePolicy")
    def validate_for_resource_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that all policy statements in the policy document satisfies the requirements for a resource-based policy.

        :return: An array of validation error messages, or an empty array if the document is valid.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#access_policies-json
        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForResourcePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="creationStack")
    def creation_stack(self) -> typing.List[builtins.str]:
        '''(experimental) The creation stack of this resolvable which will be appended to errors thrown during resolution.

        This may return an array with a single informational element indicating how
        to get this property populated, if it was skipped for performance reasons.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "creationStack"))

    @builtins.property
    @jsii.member(jsii_name="isEmpty")
    def is_empty(self) -> builtins.bool:
        '''(experimental) Whether the policy document contains any statements.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isEmpty"))

    @builtins.property
    @jsii.member(jsii_name="statementCount")
    def statement_count(self) -> jsii.Number:
        '''(experimental) The number of statements already added to this policy.

        Can be used, for example, to generate unique "sid"s within the policy.

        :stability: experimental
        '''
        return typing.cast(jsii.Number, jsii.get(self, "statementCount"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.PolicyDocumentProps",
    jsii_struct_bases=[],
    name_mapping={
        "assign_sids": "assignSids",
        "minimize": "minimize",
        "statements": "statements",
    },
)
class PolicyDocumentProps:
    def __init__(
        self,
        *,
        assign_sids: typing.Optional[builtins.bool] = None,
        minimize: typing.Optional[builtins.bool] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
    ) -> None:
        '''(experimental) Properties for a new PolicyDocument.

        :param assign_sids: (experimental) Automatically assign Statement Ids to all statements. Default: false
        :param minimize: (experimental) Try to minimize the policy by merging statements. To avoid overrunning the maximum policy size, combine statements if they produce the same result. Merging happens according to the following rules: - The Effect of both statements is the same - Neither of the statements have a 'Sid' - Combine Principals if the rest of the statement is exactly the same. - Combine Resources if the rest of the statement is exactly the same. - Combine Actions if the rest of the statement is exactly the same. - We will never combine NotPrincipals, NotResources or NotActions, because doing so would change the meaning of the policy document. Default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set
        :param statements: (experimental) Initial statements to add to the policy document. Default: - No statements

        :stability: experimental
        :exampleMetadata: infused

        Example::

            my_trusted_admin_role = iam.Role.from_role_arn(self, "TrustedRole", "arn:aws:iam:....")
            # Creates a limited admin policy and assigns to the account root.
            my_custom_policy = iam.PolicyDocument(
                statements=[iam.PolicyStatement(
                    actions=["kms:Create*", "kms:Describe*", "kms:Enable*", "kms:List*", "kms:Put*"
                    ],
                    principals=[iam.AccountRootPrincipal()],
                    resources=["*"]
                )]
            )
            key = kms.Key(self, "MyKey",
                policy=my_custom_policy
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3a1e3e91edf736d55dc46a58a60e2362c7a732a2db413abcddca5bf4ad76e678)
            check_type(argname="argument assign_sids", value=assign_sids, expected_type=type_hints["assign_sids"])
            check_type(argname="argument minimize", value=minimize, expected_type=type_hints["minimize"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assign_sids is not None:
            self._values["assign_sids"] = assign_sids
        if minimize is not None:
            self._values["minimize"] = minimize
        if statements is not None:
            self._values["statements"] = statements

    @builtins.property
    def assign_sids(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically assign Statement Ids to all statements.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("assign_sids")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minimize(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Try to minimize the policy by merging statements.

        To avoid overrunning the maximum policy size, combine statements if they produce
        the same result. Merging happens according to the following rules:

        - The Effect of both statements is the same
        - Neither of the statements have a 'Sid'
        - Combine Principals if the rest of the statement is exactly the same.
        - Combine Resources if the rest of the statement is exactly the same.
        - Combine Actions if the rest of the statement is exactly the same.
        - We will never combine NotPrincipals, NotResources or NotActions, because doing
          so would change the meaning of the policy document.

        :default: - false, unless the feature flag ``@aws-cdk/aws-iam:minimizePolicies`` is set

        :stability: experimental
        '''
        result = self._values.get("minimize")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''(experimental) Initial statements to add to the policy document.

        :default: - No statements

        :stability: experimental
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyDocumentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.PolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "document": "document",
        "force": "force",
        "groups": "groups",
        "policy_name": "policyName",
        "roles": "roles",
        "statements": "statements",
        "users": "users",
    },
)
class PolicyProps:
    def __init__(
        self,
        *,
        document: typing.Optional[PolicyDocument] = None,
        force: typing.Optional[builtins.bool] = None,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        policy_name: typing.Optional[builtins.str] = None,
        roles: typing.Optional[typing.Sequence["IRole"]] = None,
        statements: typing.Optional[typing.Sequence["PolicyStatement"]] = None,
        users: typing.Optional[typing.Sequence["IUser"]] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM inline policy document.

        :param document: (experimental) Initial PolicyDocument to use for this Policy. If omited, any ``PolicyStatement`` provided in the ``statements`` property will be applied against the empty default ``PolicyDocument``. Default: - An empty policy.
        :param force: (experimental) Force creation of an ``AWS::IAM::Policy``. Unless set to ``true``, this ``Policy`` construct will not materialize to an ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect (for example, if it remains unattached to an IAM identity or if it has no statements). This is generally desired behavior, since it prevents creating invalid--and hence undeployable--CloudFormation templates. In cases where you know the policy must be created and it is actually an error if no statements have been added to it, you can set this to ``true``. Default: false
        :param groups: (experimental) Groups to attach this policy to. You can also use ``attachToGroup(group)`` to attach this policy to a group. Default: - No groups.
        :param policy_name: (experimental) The name of the policy. If you specify multiple policies for an entity, specify unique names. For example, if you specify a list of policies for an IAM role, each policy must have a unique name. Default: - Uses the logical ID of the policy resource, which is ensured to be unique within the stack.
        :param roles: (experimental) Roles to attach this policy to. You can also use ``attachToRole(role)`` to attach this policy to a role. Default: - No roles.
        :param statements: (experimental) Initial set of permissions to add to this policy document. You can also use ``addStatements(...statement)`` to add permissions later. Default: - No statements.
        :param users: (experimental) Users to attach this policy to. You can also use ``attachToUser(user)`` to attach this policy to a user. Default: - No users.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # post_auth_fn: lambda.Function
            
            
            userpool = cognito.UserPool(self, "myuserpool",
                lambda_triggers=certificatemanager.aws_cognito.UserPoolTriggers(
                    post_authentication=post_auth_fn
                )
            )
            
            # provide permissions to describe the user pool scoped to the ARN the user pool
            post_auth_fn.role.attach_inline_policy(iam.Policy(self, "userpool-policy",
                statements=[iam.PolicyStatement(
                    actions=["cognito-idp:DescribeUserPool"],
                    resources=[userpool.user_pool_arn]
                )]
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61168007cabc979f17e4045d10fd09b836a743bcf6b65bb055cc5a4d1d5f4450)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument roles", value=roles, expected_type=type_hints["roles"])
            check_type(argname="argument statements", value=statements, expected_type=type_hints["statements"])
            check_type(argname="argument users", value=users, expected_type=type_hints["users"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if document is not None:
            self._values["document"] = document
        if force is not None:
            self._values["force"] = force
        if groups is not None:
            self._values["groups"] = groups
        if policy_name is not None:
            self._values["policy_name"] = policy_name
        if roles is not None:
            self._values["roles"] = roles
        if statements is not None:
            self._values["statements"] = statements
        if users is not None:
            self._values["users"] = users

    @builtins.property
    def document(self) -> typing.Optional[PolicyDocument]:
        '''(experimental) Initial PolicyDocument to use for this Policy.

        If omited, any
        ``PolicyStatement`` provided in the ``statements`` property will be applied
        against the empty default ``PolicyDocument``.

        :default: - An empty policy.

        :stability: experimental
        '''
        result = self._values.get("document")
        return typing.cast(typing.Optional[PolicyDocument], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force creation of an ``AWS::IAM::Policy``.

        Unless set to ``true``, this ``Policy`` construct will not materialize to an
        ``AWS::IAM::Policy`` CloudFormation resource in case it would have no effect
        (for example, if it remains unattached to an IAM identity or if it has no
        statements). This is generally desired behavior, since it prevents
        creating invalid--and hence undeployable--CloudFormation templates.

        In cases where you know the policy must be created and it is actually
        an error if no statements have been added to it, you can set this to ``true``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''(experimental) Groups to attach this policy to.

        You can also use ``attachToGroup(group)`` to attach this policy to a group.

        :default: - No groups.

        :stability: experimental
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def policy_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the policy.

        If you specify multiple policies for an entity,
        specify unique names. For example, if you specify a list of policies for
        an IAM role, each policy must have a unique name.

        :default:

        - Uses the logical ID of the policy resource, which is ensured
        to be unique within the stack.

        :stability: experimental
        '''
        result = self._values.get("policy_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def roles(self) -> typing.Optional[typing.List["IRole"]]:
        '''(experimental) Roles to attach this policy to.

        You can also use ``attachToRole(role)`` to attach this policy to a role.

        :default: - No roles.

        :stability: experimental
        '''
        result = self._values.get("roles")
        return typing.cast(typing.Optional[typing.List["IRole"]], result)

    @builtins.property
    def statements(self) -> typing.Optional[typing.List["PolicyStatement"]]:
        '''(experimental) Initial set of permissions to add to this policy document.

        You can also use ``addStatements(...statement)`` to add permissions later.

        :default: - No statements.

        :stability: experimental
        '''
        result = self._values.get("statements")
        return typing.cast(typing.Optional[typing.List["PolicyStatement"]], result)

    @builtins.property
    def users(self) -> typing.Optional[typing.List["IUser"]]:
        '''(experimental) Users to attach this policy to.

        You can also use ``attachToUser(user)`` to attach this policy to a user.

        :default: - No users.

        :stability: experimental
        '''
        result = self._values.get("users")
        return typing.cast(typing.Optional[typing.List["IUser"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PolicyStatement(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.PolicyStatement",
):
    '''(experimental) Represents a statement in an IAM policy document.

    :stability: experimental
    :exampleMetadata: lit=lib/aws-ec2/test/integ.vpc-endpoint.lit.ts infused

    Example::

        # Add gateway endpoints when creating the VPC
        vpc = ec2.Vpc(self, "MyVpc",
            gateway_endpoints={
                "S3": cdk.aws_ec2.GatewayVpcEndpointOptions(
                    service=ec2.GatewayVpcEndpointAwsService.S3
                )
            }
        )
        
        # Alternatively gateway endpoints can be added on the VPC
        dynamo_db_endpoint = vpc.add_gateway_endpoint("DynamoDbEndpoint",
            service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
        )
        
        # This allows to customize the endpoint policy
        dynamo_db_endpoint.add_to_policy(
            iam.PolicyStatement( # Restrict to listing and describing tables
                principals=[iam.AnyPrincipal()],
                actions=["dynamodb:DescribeTable", "dynamodb:ListTables"],
                resources=["*"]))
        
        # Add an interface endpoint
        vpc.add_interface_endpoint("EcrDockerEndpoint",
            service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER
        )
    '''

    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param actions: (experimental) List of actions to add to the statement. Default: - no actions
        :param conditions: (experimental) Conditions to add to the statement. Default: - no condition
        :param effect: (experimental) Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: (experimental) List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: (experimental) List of not principals to add to the statement. Default: - no not principals
        :param not_resources: (experimental) NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: (experimental) List of principals to add to the statement. Default: - no principals
        :param resources: (experimental) Resource ARNs to add to the statement. Default: - no resources
        :param sid: (experimental) The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid

        :stability: experimental
        '''
        props = PolicyStatementProps(
            actions=actions,
            conditions=conditions,
            effect=effect,
            not_actions=not_actions,
            not_principals=not_principals,
            not_resources=not_resources,
            principals=principals,
            resources=resources,
            sid=sid,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromJson")
    @builtins.classmethod
    def from_json(cls, obj: typing.Any) -> "PolicyStatement":
        '''(experimental) Creates a new PolicyStatement based on the object provided.

        This will accept an object created from the ``.toJSON()`` call

        :param obj: the PolicyStatement in object form.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2d81dc6903db9408e732b9147d1459376b20b2f56b34385b9ca1bbc838ef935a)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast("PolicyStatement", jsii.sinvoke(cls, "fromJson", [obj]))

    @jsii.member(jsii_name="addAccountCondition")
    def add_account_condition(self, account_id: builtins.str) -> None:
        '''(experimental) Add a condition that limits to a given account.

        This method can only be called once: subsequent calls will overwrite earlier calls.

        :param account_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b276d93375472e08f6c170e4fbd9016a4051fa5b2ef4929883b26597f46bcd1a)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast(None, jsii.invoke(self, "addAccountCondition", [account_id]))

    @jsii.member(jsii_name="addAccountRootPrincipal")
    def add_account_root_principal(self) -> None:
        '''(experimental) Adds an AWS account root user principal to this policy statement.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAccountRootPrincipal", []))

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: builtins.str) -> None:
        '''(experimental) Specify allowed actions into the "Action" section of the policy statement.

        :param actions: actions that will be allowed.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_action.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5b5a7b77ff7202dab9bc7900741472abbc2b16815252b295efeff76a27e6a749)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addActions", [*actions]))

    @jsii.member(jsii_name="addAllResources")
    def add_all_resources(self) -> None:
        '''(experimental) Adds a ``"*"`` resource to this statement.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAllResources", []))

    @jsii.member(jsii_name="addAnyPrincipal")
    def add_any_principal(self) -> None:
        '''(experimental) Adds all identities in all accounts ("*") to this policy statement.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "addAnyPrincipal", []))

    @jsii.member(jsii_name="addArnPrincipal")
    def add_arn_principal(self, arn: builtins.str) -> None:
        '''(experimental) Specify a principal using the ARN  identifier of the principal.

        You cannot specify IAM groups and instance profiles as principals.

        :param arn: ARN identifier of AWS account, IAM user, or IAM role (i.e. arn:aws:iam::123456789012:user/user-name).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6c4df8a651eedc12f9e5af9112392fdd73941ff488c0b4c9cc4a11eac27d0909)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        return typing.cast(None, jsii.invoke(self, "addArnPrincipal", [arn]))

    @jsii.member(jsii_name="addAwsAccountPrincipal")
    def add_aws_account_principal(self, account_id: builtins.str) -> None:
        '''(experimental) Specify AWS account ID as the principal entity to the "Principal" section of a policy statement.

        :param account_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__271e56250dffe5f4952052fef870839dbaab36f0f9580bcf78e75bf0e1ee5d9b)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        return typing.cast(None, jsii.invoke(self, "addAwsAccountPrincipal", [account_id]))

    @jsii.member(jsii_name="addCanonicalUserPrincipal")
    def add_canonical_user_principal(self, canonical_user_id: builtins.str) -> None:
        '''(experimental) Adds a canonical user ID principal to this policy document.

        :param canonical_user_id: unique identifier assigned by AWS for every account.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__25377aa4146b0cfc4aca617e39ef2132cd58391b2b8b311cbf9df52d0d218cdd)
            check_type(argname="argument canonical_user_id", value=canonical_user_id, expected_type=type_hints["canonical_user_id"])
        return typing.cast(None, jsii.invoke(self, "addCanonicalUserPrincipal", [canonical_user_id]))

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: builtins.str, value: typing.Any) -> None:
        '''(experimental) Add a condition to the Policy.

        If multiple calls are made to add a condition with the same operator and field, only
        the last one wins. For example::

           # stmt: iam.PolicyStatement


           stmt.add_condition("StringEquals", {"aws:SomeField": "1"})
           stmt.add_condition("StringEquals", {"aws:SomeField": "2"})

        Will end up with the single condition ``StringEquals: { 'aws:SomeField': '2' }``.

        If you meant to add a condition to say that the field can be *either* ``1`` or ``2``, write
        this::

           # stmt: iam.PolicyStatement


           stmt.add_condition("StringEquals", {"aws:SomeField": ["1", "2"]})

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__205662599e2ab097d3776122bb70402c2145e3bf80c05a85826abcb3cb815958)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addCondition", [key, value]))

    @jsii.member(jsii_name="addConditions")
    def add_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''(experimental) Add multiple conditions to the Policy.

        See the ``addCondition`` function for a caveat on calling this method multiple times.

        :param conditions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de8e5dc92c4a814303dec0fec7ed657322b0fde5baa8f656dc01c687ae18eed3)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addConditions", [conditions]))

    @jsii.member(jsii_name="addFederatedPrincipal")
    def add_federated_principal(
        self,
        federated: typing.Any,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''(experimental) Adds a federated identity provider such as Amazon Cognito to this policy statement.

        :param federated: federated identity provider (i.e. 'cognito-identity.amazonaws.com').
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e4e4b1c824f3af8de88fb63c5b483545c5096f66a77b917b21ab036a36275e44)
            check_type(argname="argument federated", value=federated, expected_type=type_hints["federated"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addFederatedPrincipal", [federated, conditions]))

    @jsii.member(jsii_name="addNotActions")
    def add_not_actions(self, *not_actions: builtins.str) -> None:
        '''(experimental) Explicitly allow all actions except the specified list of actions into the "NotAction" section of the policy document.

        :param not_actions: actions that will be denied. All other actions will be permitted.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notaction.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb3d4e663af1bab2477aea1248f540ecb2f2f812229eeed50230565fbae710f)
            check_type(argname="argument not_actions", value=not_actions, expected_type=typing.Tuple[type_hints["not_actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotActions", [*not_actions]))

    @jsii.member(jsii_name="addNotPrincipals")
    def add_not_principals(self, *not_principals: IPrincipal) -> None:
        '''(experimental) Specify principals that is not allowed or denied access to the "NotPrincipal" section of a policy statement.

        :param not_principals: IAM principals that will be denied access.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notprincipal.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc94005e473308a931a0f02157a67a691341f074bcbd691ee0b6a3e36b6c3d3)
            check_type(argname="argument not_principals", value=not_principals, expected_type=typing.Tuple[type_hints["not_principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotPrincipals", [*not_principals]))

    @jsii.member(jsii_name="addNotResources")
    def add_not_resources(self, *arns: builtins.str) -> None:
        '''(experimental) Specify resources that this policy statement will not apply to in the "NotResource" section of this policy statement.

        All resources except the specified list will be matched.

        :param arns: Amazon Resource Names (ARNs) of the resources that this policy statement does not apply to.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_notresource.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30146f1cf248be33e5cbe79c0ec8de33f1925d8cd3b70ef35a4b983e6b88099c)
            check_type(argname="argument arns", value=arns, expected_type=typing.Tuple[type_hints["arns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addNotResources", [*arns]))

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: IPrincipal) -> None:
        '''(experimental) Adds principals to the "Principal" section of a policy statement.

        :param principals: IAM principals that will be added.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9940906039248437ca8811ef47f32f1dbdd27b9d7c689e2d438c3a54c89e04c6)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPrincipals", [*principals]))

    @jsii.member(jsii_name="addResources")
    def add_resources(self, *arns: builtins.str) -> None:
        '''(experimental) Specify resources that this policy statement applies into the "Resource" section of this policy statement.

        :param arns: Amazon Resource Names (ARNs) of the resources that this policy statement applies to.

        :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_resource.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef8af799da1ef5a11db264fafe9da3cfad1a253e580b8f76a6a80ba0ef19b151)
            check_type(argname="argument arns", value=arns, expected_type=typing.Tuple[type_hints["arns"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addResources", [*arns]))

    @jsii.member(jsii_name="addServicePrincipal")
    def add_service_principal(
        self,
        service: builtins.str,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a service principal to this policy statement.

        :param service: the service name for which a service principal is requested (e.g: ``s3.amazonaws.com``).
        :param conditions: (experimental) Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ccc0bea9078c7ce635862e6e0635008835785be6ae5ff978b4baeb1b75038395)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        return typing.cast(None, jsii.invoke(self, "addServicePrincipal", [service, opts]))

    @jsii.member(jsii_name="copy")
    def copy(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> "PolicyStatement":
        '''(experimental) Create a new ``PolicyStatement`` with the same exact properties as this one, except for the overrides.

        :param actions: (experimental) List of actions to add to the statement. Default: - no actions
        :param conditions: (experimental) Conditions to add to the statement. Default: - no condition
        :param effect: (experimental) Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: (experimental) List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: (experimental) List of not principals to add to the statement. Default: - no not principals
        :param not_resources: (experimental) NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: (experimental) List of principals to add to the statement. Default: - no principals
        :param resources: (experimental) Resource ARNs to add to the statement. Default: - no resources
        :param sid: (experimental) The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid

        :stability: experimental
        '''
        overrides = PolicyStatementProps(
            actions=actions,
            conditions=conditions,
            effect=effect,
            not_actions=not_actions,
            not_principals=not_principals,
            not_resources=not_resources,
            principals=principals,
            resources=resources,
            sid=sid,
        )

        return typing.cast("PolicyStatement", jsii.invoke(self, "copy", [overrides]))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Any:
        '''(experimental) JSON-ify the statement.

        Used when JSON.stringify() is called

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toStatementJson")
    def to_statement_json(self) -> typing.Any:
        '''(experimental) JSON-ify the policy statement.

        Used when JSON.stringify() is called

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.invoke(self, "toStatementJson", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) String representation of this policy statement.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="validateForAnyPolicy")
    def validate_for_any_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that the policy statement satisfies base requirements for a policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForAnyPolicy", []))

    @jsii.member(jsii_name="validateForIdentityPolicy")
    def validate_for_identity_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that the policy statement satisfies all requirements for an identity-based policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForIdentityPolicy", []))

    @jsii.member(jsii_name="validateForResourcePolicy")
    def validate_for_resource_policy(self) -> typing.List[builtins.str]:
        '''(experimental) Validate that the policy statement satisfies all requirements for a resource-based policy.

        :return: An array of validation error messages, or an empty array if the statement is valid.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validateForResourcePolicy", []))

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(self) -> typing.List[builtins.str]:
        '''(experimental) The Actions added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "actions"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Any:
        '''(experimental) The conditions added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="hasPrincipal")
    def has_principal(self) -> builtins.bool:
        '''(experimental) Indicates if this permission has a "Principal" section.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "hasPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="hasResource")
    def has_resource(self) -> builtins.bool:
        '''(experimental) Indicates if this permission has at least one resource associated with it.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "hasResource"))

    @builtins.property
    @jsii.member(jsii_name="notActions")
    def not_actions(self) -> typing.List[builtins.str]:
        '''(experimental) The NotActions added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notActions"))

    @builtins.property
    @jsii.member(jsii_name="notPrincipals")
    def not_principals(self) -> typing.List[IPrincipal]:
        '''(experimental) The NotPrincipals added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[IPrincipal], jsii.get(self, "notPrincipals"))

    @builtins.property
    @jsii.member(jsii_name="notResources")
    def not_resources(self) -> typing.List[builtins.str]:
        '''(experimental) The NotResources added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "notResources"))

    @builtins.property
    @jsii.member(jsii_name="principals")
    def principals(self) -> typing.List[IPrincipal]:
        '''(experimental) The Principals added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[IPrincipal], jsii.get(self, "principals"))

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.List[builtins.str]:
        '''(experimental) The Resources added to this statement.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resources"))

    @builtins.property
    @jsii.member(jsii_name="effect")
    def effect(self) -> Effect:
        '''(experimental) Whether to allow or deny the actions in this statement.

        :stability: experimental
        '''
        return typing.cast(Effect, jsii.get(self, "effect"))

    @effect.setter
    def effect(self, value: Effect) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__57af2f06bec70b266e419c7f2c85362e6acdff8a706bcc994349e83af3c968db)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "effect", value)

    @builtins.property
    @jsii.member(jsii_name="sid")
    def sid(self) -> typing.Optional[builtins.str]:
        '''(experimental) Statement ID for this statement.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "sid"))

    @sid.setter
    def sid(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30ce2fa4ca8c0a1380260d20859de828af206679d35e2522d1d87820070572c1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "sid", value)


@jsii.data_type(
    jsii_type="monocdk.aws_iam.PolicyStatementProps",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "conditions": "conditions",
        "effect": "effect",
        "not_actions": "notActions",
        "not_principals": "notPrincipals",
        "not_resources": "notResources",
        "principals": "principals",
        "resources": "resources",
        "sid": "sid",
    },
)
class PolicyStatementProps:
    def __init__(
        self,
        *,
        actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        effect: typing.Optional[Effect] = None,
        not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
        not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        sid: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Interface for creating a policy statement.

        :param actions: (experimental) List of actions to add to the statement. Default: - no actions
        :param conditions: (experimental) Conditions to add to the statement. Default: - no condition
        :param effect: (experimental) Whether to allow or deny the actions in this statement. Default: Effect.ALLOW
        :param not_actions: (experimental) List of not actions to add to the statement. Default: - no not-actions
        :param not_principals: (experimental) List of not principals to add to the statement. Default: - no not principals
        :param not_resources: (experimental) NotResource ARNs to add to the statement. Default: - no not-resources
        :param principals: (experimental) List of principals to add to the statement. Default: - no principals
        :param resources: (experimental) Resource ARNs to add to the statement. Default: - no resources
        :param sid: (experimental) The Sid (statement ID) is an optional identifier that you provide for the policy statement. You can assign a Sid value to each statement in a statement array. In services that let you specify an ID element, such as SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In IAM, the Sid value must be unique within a JSON policy. Default: - no sid

        :stability: experimental
        :exampleMetadata: lit=lib/aws-ec2/test/integ.vpc-endpoint.lit.ts infused

        Example::

            # Add gateway endpoints when creating the VPC
            vpc = ec2.Vpc(self, "MyVpc",
                gateway_endpoints={
                    "S3": cdk.aws_ec2.GatewayVpcEndpointOptions(
                        service=ec2.GatewayVpcEndpointAwsService.S3
                    )
                }
            )
            
            # Alternatively gateway endpoints can be added on the VPC
            dynamo_db_endpoint = vpc.add_gateway_endpoint("DynamoDbEndpoint",
                service=ec2.GatewayVpcEndpointAwsService.DYNAMODB
            )
            
            # This allows to customize the endpoint policy
            dynamo_db_endpoint.add_to_policy(
                iam.PolicyStatement( # Restrict to listing and describing tables
                    principals=[iam.AnyPrincipal()],
                    actions=["dynamodb:DescribeTable", "dynamodb:ListTables"],
                    resources=["*"]))
            
            # Add an interface endpoint
            vpc.add_interface_endpoint("EcrDockerEndpoint",
                service=ec2.InterfaceVpcEndpointAwsService.ECR_DOCKER
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6398a73f5c1fa66544eaacc0b385f398deb11198b0409323b4a2ac9bbd50bbec)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument effect", value=effect, expected_type=type_hints["effect"])
            check_type(argname="argument not_actions", value=not_actions, expected_type=type_hints["not_actions"])
            check_type(argname="argument not_principals", value=not_principals, expected_type=type_hints["not_principals"])
            check_type(argname="argument not_resources", value=not_resources, expected_type=type_hints["not_resources"])
            check_type(argname="argument principals", value=principals, expected_type=type_hints["principals"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument sid", value=sid, expected_type=type_hints["sid"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if conditions is not None:
            self._values["conditions"] = conditions
        if effect is not None:
            self._values["effect"] = effect
        if not_actions is not None:
            self._values["not_actions"] = not_actions
        if not_principals is not None:
            self._values["not_principals"] = not_principals
        if not_resources is not None:
            self._values["not_resources"] = not_resources
        if principals is not None:
            self._values["principals"] = principals
        if resources is not None:
            self._values["resources"] = resources
        if sid is not None:
            self._values["sid"] = sid

    @builtins.property
    def actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of actions to add to the statement.

        :default: - no actions

        :stability: experimental
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Conditions to add to the statement.

        :default: - no condition

        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def effect(self) -> typing.Optional[Effect]:
        '''(experimental) Whether to allow or deny the actions in this statement.

        :default: Effect.ALLOW

        :stability: experimental
        '''
        result = self._values.get("effect")
        return typing.cast(typing.Optional[Effect], result)

    @builtins.property
    def not_actions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of not actions to add to the statement.

        :default: - no not-actions

        :stability: experimental
        '''
        result = self._values.get("not_actions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def not_principals(self) -> typing.Optional[typing.List[IPrincipal]]:
        '''(experimental) List of not principals to add to the statement.

        :default: - no not principals

        :stability: experimental
        '''
        result = self._values.get("not_principals")
        return typing.cast(typing.Optional[typing.List[IPrincipal]], result)

    @builtins.property
    def not_resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) NotResource ARNs to add to the statement.

        :default: - no not-resources

        :stability: experimental
        '''
        result = self._values.get("not_resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def principals(self) -> typing.Optional[typing.List[IPrincipal]]:
        '''(experimental) List of principals to add to the statement.

        :default: - no principals

        :stability: experimental
        '''
        result = self._values.get("principals")
        return typing.cast(typing.Optional[typing.List[IPrincipal]], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Resource ARNs to add to the statement.

        :default: - no resources

        :stability: experimental
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def sid(self) -> typing.Optional[builtins.str]:
        '''(experimental) The Sid (statement ID) is an optional identifier that you provide for the policy statement.

        You can assign a Sid value to each statement in a
        statement array. In services that let you specify an ID element, such as
        SQS and SNS, the Sid value is just a sub-ID of the policy document's ID. In
        IAM, the Sid value must be unique within a JSON policy.

        :default: - no sid

        :stability: experimental
        '''
        result = self._values.get("sid")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PolicyStatementProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PrincipalPolicyFragment(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.PrincipalPolicyFragment",
):
    '''(experimental) A collection of the fields in a PolicyStatement that can be used to identify a principal.

    This consists of the JSON used in the "Principal" field, and optionally a
    set of "Condition"s that need to be applied to the policy.

    Generally, a principal looks like::

        { '<TYPE>': ['ID', 'ID', ...] }

    And this is also the type of the field ``principalJson``.  However, there is a
    special type of principal that is just the string '*', which is treated
    differently by some services. To represent that principal, ``principalJson``
    should contain ``{ 'LiteralString': ['*'] }``.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # conditions: Any
        
        principal_policy_fragment = iam.PrincipalPolicyFragment({
            "principal_json_key": ["principalJson"]
        }, {
            "conditions_key": conditions
        })
    '''

    def __init__(
        self,
        principal_json: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param principal_json: JSON of the "Principal" section in a policy statement.
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_. conditions that need to be applied to this policy

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4dfdfaf4a8557ed0cdbcfc5a5eb7ba633d0e36aa0d72292279006f4d8d9136b4)
            check_type(argname="argument principal_json", value=principal_json, expected_type=type_hints["principal_json"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [principal_json, conditions])

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        conditions that need to be applied to this policy

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="principalJson")
    def principal_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) JSON of the "Principal" section in a policy statement.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.get(self, "principalJson"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.RoleProps",
    jsii_struct_bases=[],
    name_mapping={
        "assumed_by": "assumedBy",
        "description": "description",
        "external_id": "externalId",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class RoleProps:
    def __init__(
        self,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_Duration_070aa057] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM Role.

        :param assumed_by: (experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: (experimental) A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: (experimental) List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: (experimental) A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: (experimental) The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: (experimental) The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: (experimental) A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            lambda_role = iam.Role(self, "Role",
                assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
                description="Example role..."
            )
            
            stream = kinesis.Stream(self, "MyEncryptedStream",
                encryption=kinesis.StreamEncryption.KMS
            )
            
            # give lambda permissions to read stream
            stream.grant_read(lambda_role)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c149e46fe10c4eb704222ab3e79527beda947d4a2270860533c2ccb61ee1c0da)
            check_type(argname="argument assumed_by", value=assumed_by, expected_type=type_hints["assumed_by"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
            check_type(argname="argument inline_policies", value=inline_policies, expected_type=type_hints["inline_policies"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assumed_by": assumed_by,
        }
        if description is not None:
            self._values["description"] = description
        if external_id is not None:
            self._values["external_id"] = external_id
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> IPrincipal:
        '''(experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.

        :stability: experimental
        '''
        result = self._values.get("assumed_by")
        assert result is not None, "Required property 'assumed_by' is missing"
        return typing.cast(IPrincipal, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :deprecated: see {@link externalIds}

        :stability: deprecated
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :stability: experimental
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PolicyDocument]]:
        '''(experimental) A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.

        :stability: experimental
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PolicyDocument]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''(experimental) A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.

        :stability: experimental
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :stability: experimental
        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''(experimental) AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :stability: experimental
        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.

        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class SamlMetadataDocument(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_iam.SamlMetadataDocument",
):
    '''(experimental) A SAML metadata document.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        principal = iam.SamlPrincipal(provider, {
            "StringEquals": {
                "SAML:iss": "issuer"
            }
        })
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromFile")
    @builtins.classmethod
    def from_file(cls, path: builtins.str) -> "SamlMetadataDocument":
        '''(experimental) Create a SAML metadata document from a XML file.

        :param path: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da567a775537491ac75c3385e477ac8fe0ede0cfbde8a376c82e637de0d993da)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("SamlMetadataDocument", jsii.sinvoke(cls, "fromFile", [path]))

    @jsii.member(jsii_name="fromXml")
    @builtins.classmethod
    def from_xml(cls, xml: builtins.str) -> "SamlMetadataDocument":
        '''(experimental) Create a SAML metadata document from a XML string.

        :param xml: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d31368d32d9224f7bc9126566b7baddeb27bdd48513bd89fc04dab0c1300927f)
            check_type(argname="argument xml", value=xml, expected_type=type_hints["xml"])
        return typing.cast("SamlMetadataDocument", jsii.sinvoke(cls, "fromXml", [xml]))

    @builtins.property
    @jsii.member(jsii_name="xml")
    @abc.abstractmethod
    def xml(self) -> builtins.str:
        '''(experimental) The XML content of the metadata document.

        :stability: experimental
        '''
        ...


class _SamlMetadataDocumentProxy(SamlMetadataDocument):
    @builtins.property
    @jsii.member(jsii_name="xml")
    def xml(self) -> builtins.str:
        '''(experimental) The XML content of the metadata document.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "xml"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, SamlMetadataDocument).__jsii_proxy_class__ = lambda : _SamlMetadataDocumentProxy


@jsii.implements(ISamlProvider)
class SamlProvider(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.SamlProvider",
):
    '''(experimental) A SAML provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        iam.Role(self, "Role",
            assumed_by=iam.SamlConsolePrincipal(provider)
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        metadata_document: SamlMetadataDocument,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param metadata_document: (experimental) An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.
        :param name: (experimental) The name of the provider to create. This parameter allows a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- Length must be between 1 and 128 characters. Default: - a CloudFormation generated name

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__864508c4669028fd7e3c06733b9b5ce02d2308457848993e6cce89d91634b9a2)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SamlProviderProps(metadata_document=metadata_document, name=name)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromSamlProviderArn")
    @builtins.classmethod
    def from_saml_provider_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        saml_provider_arn: builtins.str,
    ) -> ISamlProvider:
        '''(experimental) Import an existing provider.

        :param scope: -
        :param id: -
        :param saml_provider_arn: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__82548cb57afec0eaf176df75ed6892b9133960fb6ac19cb9344c6e52cd04a488)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument saml_provider_arn", value=saml_provider_arn, expected_type=type_hints["saml_provider_arn"])
        return typing.cast(ISamlProvider, jsii.sinvoke(cls, "fromSamlProviderArn", [scope, id, saml_provider_arn]))

    @builtins.property
    @jsii.member(jsii_name="samlProviderArn")
    def saml_provider_arn(self) -> builtins.str:
        '''(experimental) The Amazon Resource Name (ARN) of the provider.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "samlProviderArn"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.SamlProviderProps",
    jsii_struct_bases=[],
    name_mapping={"metadata_document": "metadataDocument", "name": "name"},
)
class SamlProviderProps:
    def __init__(
        self,
        *,
        metadata_document: SamlMetadataDocument,
        name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a SAML provider.

        :param metadata_document: (experimental) An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.
        :param name: (experimental) The name of the provider to create. This parameter allows a string of characters consisting of upper and lowercase alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@- Length must be between 1 and 128 characters. Default: - a CloudFormation generated name

        :stability: experimental
        :exampleMetadata: infused

        Example::

            provider = iam.SamlProvider(self, "Provider",
                metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
            )
            iam.Role(self, "Role",
                assumed_by=iam.SamlConsolePrincipal(provider)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d0cddf4acd86a0cac8503cb45d0f9c64bbfda87865d17fad11a3a20561cc571)
            check_type(argname="argument metadata_document", value=metadata_document, expected_type=type_hints["metadata_document"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "metadata_document": metadata_document,
        }
        if name is not None:
            self._values["name"] = name

    @builtins.property
    def metadata_document(self) -> SamlMetadataDocument:
        '''(experimental) An XML document generated by an identity provider (IdP) that supports SAML 2.0. The document includes the issuer's name, expiration information, and keys that can be used to validate the SAML authentication response (assertions) that are received from the IdP. You must generate the metadata document using the identity management software that is used as your organization's IdP.

        :stability: experimental
        '''
        result = self._values.get("metadata_document")
        assert result is not None, "Required property 'metadata_document' is missing"
        return typing.cast(SamlMetadataDocument, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the provider to create.

        This parameter allows a string of characters consisting of upper and
        lowercase alphanumeric characters with no spaces. You can also include
        any of the following characters: _+=,.@-

        Length must be between 1 and 128 characters.

        :default: - a CloudFormation generated name

        :stability: experimental
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SamlProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.ServicePrincipalOpts",
    jsii_struct_bases=[],
    name_mapping={"conditions": "conditions", "region": "region"},
)
class ServicePrincipalOpts:
    def __init__(
        self,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for a service principal.

        :param conditions: (experimental) Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            # conditions: Any
            
            service_principal_opts = iam.ServicePrincipalOpts(
                conditions={
                    "conditions_key": conditions
                },
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__581a7da6857e4f36f15e3c5fc909349991557d9fa3f94b6219153dfa7db7a80d)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if conditions is not None:
            self._values["conditions"] = conditions
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def conditions(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''(experimental) Additional conditions to add to the Service Principal.

        :default: - No conditions

        :stability: experimental
        '''
        result = self._values.get("conditions")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The region in which the service is operating.

        :default: - the current Stack's region.

        :deprecated: You should not need to set this. The stack's region is always correct.

        :stability: deprecated
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ServicePrincipalOpts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IPrincipal)
class UnknownPrincipal(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.UnknownPrincipal",
):
    '''(experimental) A principal for use in resources that need to have a role but it's unknown.

    Some resources have roles associated with them which they assume, such as
    Lambda Functions, CodeBuild projects, StepFunctions machines, etc.

    When those resources are imported, their actual roles are not always
    imported with them. When that happens, we use an instance of this class
    instead, which will add user warnings when statements are attempted to be
    added to it.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import constructs as constructs
        from monocdk import aws_iam as iam
        
        # construct: constructs.Construct
        
        unknown_principal = iam.UnknownPrincipal(
            resource=construct
        )
    '''

    def __init__(self, *, resource: _constructs_77d1e7e8.IConstruct) -> None:
        '''
        :param resource: (experimental) The resource the role proxy is for.

        :stability: experimental
        '''
        props = UnknownPrincipalProps(resource=resource)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c171271638560e474bb6457862deb486d25007ad0b1c2f70f4f2344d07008279)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff07c7242537ab918ada0c6526a010028e02485214d5425b760fa30baa8b56b7)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.UnknownPrincipalProps",
    jsii_struct_bases=[],
    name_mapping={"resource": "resource"},
)
class UnknownPrincipalProps:
    def __init__(self, *, resource: _constructs_77d1e7e8.IConstruct) -> None:
        '''(experimental) Properties for an UnknownPrincipal.

        :param resource: (experimental) The resource the role proxy is for.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import constructs as constructs
            from monocdk import aws_iam as iam
            
            # construct: constructs.Construct
            
            unknown_principal_props = iam.UnknownPrincipalProps(
                resource=construct
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e5d735bd94d763b95b269f67d9036fb16090725d38b77920844a2a62ea9156da)
            check_type(argname="argument resource", value=resource, expected_type=type_hints["resource"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "resource": resource,
        }

    @builtins.property
    def resource(self) -> _constructs_77d1e7e8.IConstruct:
        '''(experimental) The resource the role proxy is for.

        :stability: experimental
        '''
        result = self._values.get("resource")
        assert result is not None, "Required property 'resource' is missing"
        return typing.cast(_constructs_77d1e7e8.IConstruct, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UnknownPrincipalProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.UserAttributes",
    jsii_struct_bases=[],
    name_mapping={"user_arn": "userArn"},
)
class UserAttributes:
    def __init__(self, *, user_arn: builtins.str) -> None:
        '''(experimental) Represents a user defined outside of this stack.

        :param user_arn: (experimental) The ARN of the user. Format: arn::iam:::user/

        :stability: experimental
        :exampleMetadata: infused

        Example::

            user = iam.User.from_user_attributes(self, "MyImportedUserByAttributes",
                user_arn="arn:aws:iam::123456789012:user/johnsmith"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c85d294e09e4ae543d25a57c9415a2268820e8445bc6f61658f201fa86f0ed0)
            check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "user_arn": user_arn,
        }

    @builtins.property
    def user_arn(self) -> builtins.str:
        '''(experimental) The ARN of the user.

        Format: arn::iam:::user/

        :stability: experimental
        '''
        result = self._values.get("user_arn")
        assert result is not None, "Required property 'user_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserAttributes(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.UserProps",
    jsii_struct_bases=[],
    name_mapping={
        "groups": "groups",
        "managed_policies": "managedPolicies",
        "password": "password",
        "password_reset_required": "passwordResetRequired",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "user_name": "userName",
    },
)
class UserProps:
    def __init__(
        self,
        *,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        password: typing.Optional[_SecretValue_c18506ef] = None,
        password_reset_required: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining an IAM user.

        :param groups: (experimental) Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: (experimental) The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: (experimental) Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: (experimental) The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: (experimental) A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)

        :stability: experimental
        :exampleMetadata: lit=lib/aws-iam/test/example.attaching.lit.ts infused

        Example::

            user = User(self, "MyUser", password=cdk.SecretValue.unsafe_plain_text("1234"))
            group = Group(self, "MyGroup")
            
            policy = Policy(self, "MyPolicy")
            policy.attach_to_user(user)
            group.attach_inline_policy(policy)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__08b575100a7ce017470e9390aad6bfab83dc8c5d77f17b823020bd4d51f621d1)
            check_type(argname="argument groups", value=groups, expected_type=type_hints["groups"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument password_reset_required", value=password_reset_required, expected_type=type_hints["password_reset_required"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if groups is not None:
            self._values["groups"] = groups
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if password is not None:
            self._values["password"] = password
        if password_reset_required is not None:
            self._values["password_reset_required"] = password_reset_required
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if user_name is not None:
            self._values["user_name"] = user_name

    @builtins.property
    def groups(self) -> typing.Optional[typing.List["IGroup"]]:
        '''(experimental) Groups to add this user to.

        You can also use ``addToGroup`` to add this
        user to a group.

        :default: - No groups.

        :stability: experimental
        '''
        result = self._values.get("groups")
        return typing.cast(typing.Optional[typing.List["IGroup"]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''(experimental) A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.

        :stability: experimental
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) The password for the user. This is required so the user can access the AWS Management Console.

        You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or
        use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in
        Secrets Manager.

        :default: - User won't be able to access the management console without a password.

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    @builtins.property
    def password_reset_required(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console.

        If this is set to 'true', you must also specify "initialPassword".

        :default: false

        :stability: experimental
        '''
        result = self._values.get("password_reset_required")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path for the user name.

        For more information about paths, see IAM
        Identifiers in the IAM User Guide.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''(experimental) AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :stability: experimental
        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def user_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the IAM user.

        For valid values, see the UserName parameter for
        the CreateUser action in the IAM API Reference. If you don't specify a
        name, AWS CloudFormation generates a unique physical ID and uses that ID
        for the user name.

        If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default: - Generated by CloudFormation (recommended)

        :stability: experimental
        '''
        result = self._values.get("user_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UserProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_iam.WithoutPolicyUpdatesOptions",
    jsii_struct_bases=[],
    name_mapping={"add_grants_to_resources": "addGrantsToResources"},
)
class WithoutPolicyUpdatesOptions:
    def __init__(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for the ``withoutPolicyUpdates()`` modifier of a Role.

        :param add_grants_to_resources: (experimental) Add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            
            without_policy_updates_options = iam.WithoutPolicyUpdatesOptions(
                add_grants_to_resources=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd849220168d4299a9c0514b8702a859ef436a369e5ccfecea319856f95c140a)
            check_type(argname="argument add_grants_to_resources", value=add_grants_to_resources, expected_type=type_hints["add_grants_to_resources"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if add_grants_to_resources is not None:
            self._values["add_grants_to_resources"] = add_grants_to_resources

    @builtins.property
    def add_grants_to_resources(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Add grants to resources instead of dropping them.

        If this is ``false`` or not specified, grant permissions added to this role are ignored.
        It is your own responsibility to make sure the role has the required permissions.

        If this is ``true``, any grant permissions will be added to the resource instead.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("add_grants_to_resources")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WithoutPolicyUpdatesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAccessKey)
class AccessKey(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.AccessKey",
):
    '''(experimental) Define a new IAM Access Key.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Creates a new IAM user, access and secret keys, and stores the secret access key in a Secret.
        user = iam.User(self, "User")
        access_key = iam.AccessKey(self, "AccessKey", user=user)
        secret_value = secretsmanager.SecretStringValueBeta1.from_token(access_key.secret_access_key.to_string())
        secretsmanager.Secret(self, "Secret",
            secret_string_beta1=secret_value
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user: "IUser",
        serial: typing.Optional[jsii.Number] = None,
        status: typing.Optional[AccessKeyStatus] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param user: (experimental) The IAM user this key will belong to. Changing this value will result in the access key being deleted and a new access key (with a different ID and secret value) being assigned to the new user.
        :param serial: (experimental) A CloudFormation-specific value that signifies the access key should be replaced/rotated. This value can only be incremented. Incrementing this value will cause CloudFormation to replace the Access Key resource. Default: - No serial value
        :param status: (experimental) The status of the access key. An Active access key is allowed to be used to make API calls; An Inactive key cannot. Default: - The access key is active

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35f4e25dd90a0166dddfb93b56c4925b9c0c95c5f5cdf961521f068f69a588f8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AccessKeyProps(user=user, serial=serial, status=status)

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="accessKeyId")
    def access_key_id(self) -> builtins.str:
        '''(experimental) The Access Key ID.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "accessKeyId"))

    @builtins.property
    @jsii.member(jsii_name="secretAccessKey")
    def secret_access_key(self) -> _SecretValue_c18506ef:
        '''(experimental) The Secret Access Key.

        :stability: experimental
        '''
        return typing.cast(_SecretValue_c18506ef, jsii.get(self, "secretAccessKey"))


@jsii.interface(jsii_type="monocdk.aws_iam.IAssumeRolePrincipal")
class IAssumeRolePrincipal(IPrincipal, typing_extensions.Protocol):
    '''(experimental) A type of principal that has more control over its own representation in AssumeRolePolicyDocuments.

    More complex types of identity providers need more control over Role's policy documents
    than simply ``{ Effect: 'Allow', Action: 'AssumeRole', Principal: <Whatever> }``.

    If that control is necessary, they can implement ``IAssumeRolePrincipal`` to get full
    access to a Role's AssumeRolePolicyDocument.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''(experimental) Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -

        :stability: experimental
        '''
        ...


class _IAssumeRolePrincipalProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
):
    '''(experimental) A type of principal that has more control over its own representation in AssumeRolePolicyDocuments.

    More complex types of identity providers need more control over Role's policy documents
    than simply ``{ Effect: 'Allow', Action: 'AssumeRole', Principal: <Whatever> }``.

    If that control is necessary, they can implement ``IAssumeRolePrincipal`` to get full
    access to a Role's AssumeRolePolicyDocument.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IAssumeRolePrincipal"

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''(experimental) Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6dbf71f98677bf20cf72272f274a21831b1b888c5315820d292eae2eeed7c1d3)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [document]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IAssumeRolePrincipal).__jsii_proxy_class__ = lambda : _IAssumeRolePrincipalProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IComparablePrincipal")
class IComparablePrincipal(IPrincipal, typing_extensions.Protocol):
    '''(experimental) Interface for principals that can be compared.

    This only needs to be implemented for principals that could potentially be value-equal.
    Identity-equal principals will be handled correctly by default.

    :stability: experimental
    '''

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return a string format of this principal which should be identical if the two principals are the same.

        :stability: experimental
        '''
        ...


class _IComparablePrincipalProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
):
    '''(experimental) Interface for principals that can be compared.

    This only needs to be implemented for principals that could potentially be value-equal.
    Identity-equal principals will be handled correctly by default.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IComparablePrincipal"

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return a string format of this principal which should be identical if the two principals are the same.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IComparablePrincipal).__jsii_proxy_class__ = lambda : _IComparablePrincipalProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IIdentity")
class IIdentity(IPrincipal, _IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A construct that represents an IAM principal, such as a user, group or role.

    :stability: experimental
    '''

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to this principal.

        :param policy: The managed policy.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        ...


class _IIdentityProxy(
    jsii.proxy_for(IPrincipal), # type: ignore[misc]
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A construct that represents an IAM principal, such as a user, group or role.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IIdentity"

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to this principal.

        :param policy: The managed policy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__add78e4a012ac5a260e7e9782d2f6e755add0b5c33ba64238feb0256ef4bcd98)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches an inline policy to this principal.

        This is the same as calling ``policy.addToXxx(principal)``.

        :param policy: The policy resource to attach to this principal [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8244486e506664384e2b08ea4eb8b1b4bf1d90fb2a0a3136b08e48cf6234b430)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IIdentity).__jsii_proxy_class__ = lambda : _IIdentityProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IRole")
class IRole(IIdentity, typing_extensions.Protocol):
    '''(experimental) A Role object.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''(experimental) Returns the ARN of this role.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''(experimental) Returns the name of this role.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''(experimental) Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, grantee: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to assume this role.

        :param grantee: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to pass this role.

        :param grantee: -

        :stability: experimental
        '''
        ...


class _IRoleProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''(experimental) A Role object.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IRole"

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''(experimental) Returns the ARN of this role.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''(experimental) Returns the name of this role.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''(experimental) Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bcc1543d3ef692b780cef712ecc2c8064195db4578f509ffbd40d266514159d3)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, grantee: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to assume this role.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbc3971c4569a7d573d4926686b751414db60dfae9950adb818218f774d6f3da)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [grantee]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, grantee: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to pass this role.

        :param grantee: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdf670b10089d7aea62be6948d8dc376dbdedbbac5c9cfe8a6191d770942a446)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [grantee]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IRole).__jsii_proxy_class__ = lambda : _IRoleProxy


@jsii.interface(jsii_type="monocdk.aws_iam.IUser")
class IUser(IIdentity, typing_extensions.Protocol):
    '''(experimental) Represents an IAM user.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''(experimental) The user's ARN.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''(experimental) The user's name.

        :stability: experimental
        :attribute: true
        '''
        ...

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''(experimental) Adds this user to a group.

        :param group: -

        :stability: experimental
        '''
        ...


class _IUserProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''(experimental) Represents an IAM user.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_users.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IUser"

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''(experimental) The user's ARN.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userArn"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''(experimental) The user's name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''(experimental) Adds this user to a group.

        :param group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e92203682cd1883c076086b5e61a8c04fe1534c212bf91a28d660ba43f30c9fc)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "addToGroup", [group]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IUser).__jsii_proxy_class__ = lambda : _IUserProxy


@jsii.implements(IRole)
class LazyRole(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.LazyRole",
):
    '''(experimental) An IAM role that only gets attached to the construct tree once it gets used, not before.

    This construct can be used to simplify logic in other constructs
    which need to create a role but only if certain configurations occur
    (such as when AutoScaling is configured). The role can be configured in one
    place, but if it never gets used it doesn't get instantiated and will
    not be synthesized or deployed.

    :stability: experimental
    :resource: AWS::IAM::Role
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_iam as iam
        
        # duration: monocdk.Duration
        # managed_policy: iam.ManagedPolicy
        # policy_document: iam.PolicyDocument
        # principal: iam.IPrincipal
        
        lazy_role = iam.LazyRole(self, "MyLazyRole",
            assumed_by=principal,
        
            # the properties below are optional
            description="description",
            external_id="externalId",
            external_ids=["externalIds"],
            inline_policies={
                "inline_policies_key": policy_document
            },
            managed_policies=[managed_policy],
            max_session_duration=duration,
            path="path",
            permissions_boundary=managed_policy,
            role_name="roleName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_Duration_070aa057] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assumed_by: (experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: (experimental) A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: (experimental) List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: (experimental) A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: (experimental) The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: (experimental) The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: (experimental) A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e03b8360b0f91b923f85c677c80e60e38c1be627f4f0572496720d0d6c8ffeb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = LazyRoleProps(
            assumed_by=assumed_by,
            description=description,
            external_id=external_id,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to this role.

        :param policy: The managed policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f82147871c003ca3af37d433e1df2c3fab1edaaa565940469a02f59fffaf7979)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bb488592708dcaf06c69158b1e6a00e4d1d544c27f056d1f524be01afb248bc2)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__570166d9fafcc05052ccdbb1f037c62725e64382a87f3bfa34372d525bc0af5c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches a policy to this role.

        :param policy: The policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97ffcbc478353b2fad6a52151d35d1248d0cb1079275b8390738499f67d36ffb)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @jsii.member(jsii_name="grant")
    def grant(self, identity: IPrincipal, *actions: builtins.str) -> Grant:
        '''(experimental) Grant the actions defined in actions to the identity Principal on this resource.

        :param identity: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbb2fadd9e0a60e5d9a7b6dd4e0dc493db1403c88308c3617ce971474beafe92)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [identity, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, identity: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to assume this role.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c22fe70395f166dafe3685a23d397f1f248d2d4c601811b3b9fd8ac71e9c1d5)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [identity]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to pass this role.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d72fdc6abc447f62e0aa20b4a63c39cbab640d58abacb18ece2bd496d371006)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [identity]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''(experimental) Returns the ARN of this role.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''(experimental) Returns the stable and unique string identifying the role (i.e. AIDAJQABLZS4A3QDU576Q).

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''(experimental) Returns the name of this role.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


@jsii.data_type(
    jsii_type="monocdk.aws_iam.LazyRoleProps",
    jsii_struct_bases=[RoleProps],
    name_mapping={
        "assumed_by": "assumedBy",
        "description": "description",
        "external_id": "externalId",
        "external_ids": "externalIds",
        "inline_policies": "inlinePolicies",
        "managed_policies": "managedPolicies",
        "max_session_duration": "maxSessionDuration",
        "path": "path",
        "permissions_boundary": "permissionsBoundary",
        "role_name": "roleName",
    },
)
class LazyRoleProps(RoleProps):
    def __init__(
        self,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_Duration_070aa057] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for defining a LazyRole.

        :param assumed_by: (experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: (experimental) A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: (experimental) List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: (experimental) A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: (experimental) The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: (experimental) The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: (experimental) A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_iam as iam
            
            # duration: monocdk.Duration
            # managed_policy: iam.ManagedPolicy
            # policy_document: iam.PolicyDocument
            # principal: iam.IPrincipal
            
            lazy_role_props = iam.LazyRoleProps(
                assumed_by=principal,
            
                # the properties below are optional
                description="description",
                external_id="externalId",
                external_ids=["externalIds"],
                inline_policies={
                    "inline_policies_key": policy_document
                },
                managed_policies=[managed_policy],
                max_session_duration=duration,
                path="path",
                permissions_boundary=managed_policy,
                role_name="roleName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35206d4b64a96a6e4cae952d5a347b4ce64f8cc3b3cff47a5eea0905047e23f5)
            check_type(argname="argument assumed_by", value=assumed_by, expected_type=type_hints["assumed_by"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument external_id", value=external_id, expected_type=type_hints["external_id"])
            check_type(argname="argument external_ids", value=external_ids, expected_type=type_hints["external_ids"])
            check_type(argname="argument inline_policies", value=inline_policies, expected_type=type_hints["inline_policies"])
            check_type(argname="argument managed_policies", value=managed_policies, expected_type=type_hints["managed_policies"])
            check_type(argname="argument max_session_duration", value=max_session_duration, expected_type=type_hints["max_session_duration"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument permissions_boundary", value=permissions_boundary, expected_type=type_hints["permissions_boundary"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "assumed_by": assumed_by,
        }
        if description is not None:
            self._values["description"] = description
        if external_id is not None:
            self._values["external_id"] = external_id
        if external_ids is not None:
            self._values["external_ids"] = external_ids
        if inline_policies is not None:
            self._values["inline_policies"] = inline_policies
        if managed_policies is not None:
            self._values["managed_policies"] = managed_policies
        if max_session_duration is not None:
            self._values["max_session_duration"] = max_session_duration
        if path is not None:
            self._values["path"] = path
        if permissions_boundary is not None:
            self._values["permissions_boundary"] = permissions_boundary
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def assumed_by(self) -> IPrincipal:
        '''(experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role.

        You can later modify the assume role policy document by accessing it via
        the ``assumeRolePolicy`` property.

        :stability: experimental
        '''
        result = self._values.get("assumed_by")
        assert result is not None, "Required property 'assumed_by' is missing"
        return typing.cast(IPrincipal, result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the role.

        It can be up to 1000 characters long.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ID that the role assumer needs to provide when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :deprecated: see {@link externalIds}

        :stability: deprecated
        '''
        result = self._values.get("external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of IDs that the role assumer needs to provide one of when assuming this role.

        If the configured and provided external IDs do not match, the
        AssumeRole operation will fail.

        :default: No external ID required

        :stability: experimental
        '''
        result = self._values.get("external_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def inline_policies(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, PolicyDocument]]:
        '''(experimental) A list of named policies to inline into this role.

        These policies will be
        created with the role, whereas those added by ``addToPolicy`` are added
        using a separate CloudFormation resource (allowing a way around circular
        dependencies that could otherwise be introduced).

        :default: - No policy is inlined in the Role resource.

        :stability: experimental
        '''
        result = self._values.get("inline_policies")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, PolicyDocument]], result)

    @builtins.property
    def managed_policies(self) -> typing.Optional[typing.List[IManagedPolicy]]:
        '''(experimental) A list of managed policies associated with this role.

        You can add managed policies later using
        ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``.

        :default: - No managed policies.

        :stability: experimental
        '''
        result = self._values.get("managed_policies")
        return typing.cast(typing.Optional[typing.List[IManagedPolicy]], result)

    @builtins.property
    def max_session_duration(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum session duration that you want to set for the specified role.

        This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours.

        Anyone who assumes the role from the AWS CLI or API can use the
        DurationSeconds API parameter or the duration-seconds CLI parameter to
        request a longer session. The MaxSessionDuration setting determines the
        maximum duration that can be requested using the DurationSeconds
        parameter.

        If users don't specify a value for the DurationSeconds parameter, their
        security credentials are valid for one hour by default. This applies when
        you use the AssumeRole* API operations or the assume-role* CLI operations
        but does not apply when you use those operations to create a console URL.

        :default: Duration.hours(1)

        :stability: experimental
        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use.html
        '''
        result = self._values.get("max_session_duration")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path associated with this role.

        For information about IAM paths, see
        Friendly Names and Paths in IAM User Guide.

        :default: /

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''(experimental) AWS supports permissions boundaries for IAM entities (users or roles).

        A permissions boundary is an advanced feature for using a managed policy
        to set the maximum permissions that an identity-based policy can grant to
        an IAM entity. An entity's permissions boundary allows it to perform only
        the actions that are allowed by both its identity-based policies and its
        permissions boundaries.

        :default: - No permissions boundary.

        :stability: experimental
        :link: https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html
        '''
        result = self._values.get("permissions_boundary")
        return typing.cast(typing.Optional[IManagedPolicy], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the IAM role.

        For valid values, see the RoleName parameter for
        the CreateRole action in the IAM API Reference.

        IMPORTANT: If you specify a name, you cannot perform updates that require
        replacement of this resource. You can perform updates that require no or
        some interruption. If you must replace the resource, specify a new name.

        If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to
        acknowledge your template's capabilities. For more information, see
        Acknowledging IAM Resources in AWS CloudFormation Templates.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that ID
        for the role name.

        :stability: experimental
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LazyRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IAssumeRolePrincipal, IComparablePrincipal)
class PrincipalBase(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.aws_iam.PrincipalBase",
):
    '''(experimental) Base class for policy principals.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        principal = iam.AccountPrincipal("123456789000").with_conditions({"StringEquals": {"foo": "baz"}})
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, document: PolicyDocument) -> None:
        '''(experimental) Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param document: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8e077464030e496b0ecaf34e9a4377c6240462f7e7a566e0f26ca423c0cfa2cc)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [document]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6e92bd111395b981b850c0e359a23e0febc94c0b6f1b91dd7167ccd3748df4b)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        _statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param _statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb0e5831d6c7e3f862e8edea8ec808dffd29df9c3ce1891c23efcde5ff1f0a8b)
            check_type(argname="argument _statement", value=_statement, expected_type=type_hints["_statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [_statement]))

    @jsii.member(jsii_name="dedupeString")
    @abc.abstractmethod
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) JSON-ify the principal.

        Used when JSON.stringify() is called

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @jsii.member(jsii_name="withConditions")
    def with_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> "PrincipalBase":
        '''(experimental) Returns a new PrincipalWithConditions using this principal as the base, with the passed conditions added.

        When there is a value for the same operator and key in both the principal and the
        conditions parameter, the value from the conditions parameter will be used.

        :param conditions: -

        :return: a new PrincipalWithConditions object.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12e58dd8fcf40965f7a1d7f10fccbc9ae1532d45a12c3ddc59da2f0c5be2b2f2)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast("PrincipalBase", jsii.invoke(self, "withConditions", [conditions]))

    @jsii.member(jsii_name="withSessionTags")
    def with_session_tags(self) -> "PrincipalBase":
        '''(experimental) Returns a new principal using this principal as the base, with session tags enabled.

        :return: a new SessionTagsPrincipal object.

        :stability: experimental
        '''
        return typing.cast("PrincipalBase", jsii.invoke(self, "withSessionTags", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    @abc.abstractmethod
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class _PrincipalBaseProxy(PrincipalBase):
    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PrincipalBase).__jsii_proxy_class__ = lambda : _PrincipalBaseProxy


class PrincipalWithConditions(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.PrincipalWithConditions",
):
    '''(experimental) An IAM principal with additional conditions specifying when the policy is in effect.

    For more information about conditions, see:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # conditions: Any
        # principal: iam.IPrincipal
        
        principal_with_conditions = iam.PrincipalWithConditions(principal, {
            "conditions_key": conditions
        })
    '''

    def __init__(
        self,
        principal: IPrincipal,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param principal: -
        :param conditions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__907a939090db89995a634ed440ca4844c184f565312f829f90e20647b8cdea46)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [principal, conditions])

    @jsii.member(jsii_name="addCondition")
    def add_condition(self, key: builtins.str, value: typing.Any) -> None:
        '''(experimental) Add a condition to the principal.

        :param key: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d0ab7befbf9ce0e652b11615524ad9d0cf84a9c98a56c94a74718b2ad667f135)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast(None, jsii.invoke(self, "addCondition", [key, value]))

    @jsii.member(jsii_name="addConditions")
    def add_conditions(
        self,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''(experimental) Adds multiple conditions to the principal.

        Values from the conditions parameter will overwrite existing values with the same operator
        and key.

        :param conditions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8144bc8222b46ef67f74a9f7de481be58fb4aa8afc00202f97b645b8ab8685e)
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        return typing.cast(None, jsii.invoke(self, "addConditions", [conditions]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa22b07b42fefa67222d548e28b71eca4a1553f90677315ad98ae91584f7e172)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__69986f0f604db3130d3901d5f966f67189b394a9c6eb300f1b060d0d4c5c9f0a)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="appendDedupe")
    def _append_dedupe(self, append: builtins.str) -> typing.Optional[builtins.str]:
        '''(experimental) Append the given string to the wrapped principal's dedupe string (if available).

        :param append: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dfed0f6c9d2d923edc4752aff66321c6f9e28fe508f08c60acd229904819a1cf)
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "appendDedupe", [append]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toJSON")
    def to_json(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) JSON-ify the principal.

        Used when JSON.stringify() is called

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], jsii.invoke(self, "toJSON", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


@jsii.implements(IRole)
class Role(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.Role",
):
    '''(experimental) IAM Role.

    Defines an IAM role. The role is created with an assume policy document associated with
    the specified AWS service principal defined in ``serviceAssumeRole``.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Example role..."
        )
        
        stream = kinesis.Stream(self, "MyEncryptedStream",
            encryption=kinesis.StreamEncryption.KMS
        )
        
        # give lambda permissions to read stream
        stream.grant_read(lambda_role)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        assumed_by: IPrincipal,
        description: typing.Optional[builtins.str] = None,
        external_id: typing.Optional[builtins.str] = None,
        external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        max_session_duration: typing.Optional[_Duration_070aa057] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param assumed_by: (experimental) The IAM principal (i.e. ``new ServicePrincipal('sns.amazonaws.com')``) which can assume this role. You can later modify the assume role policy document by accessing it via the ``assumeRolePolicy`` property.
        :param description: (experimental) A description of the role. It can be up to 1000 characters long. Default: - No description.
        :param external_id: (deprecated) ID that the role assumer needs to provide when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param external_ids: (experimental) List of IDs that the role assumer needs to provide one of when assuming this role. If the configured and provided external IDs do not match, the AssumeRole operation will fail. Default: No external ID required
        :param inline_policies: (experimental) A list of named policies to inline into this role. These policies will be created with the role, whereas those added by ``addToPolicy`` are added using a separate CloudFormation resource (allowing a way around circular dependencies that could otherwise be introduced). Default: - No policy is inlined in the Role resource.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param max_session_duration: (experimental) The maximum session duration that you want to set for the specified role. This setting can have a value from 1 hour (3600sec) to 12 (43200sec) hours. Anyone who assumes the role from the AWS CLI or API can use the DurationSeconds API parameter or the duration-seconds CLI parameter to request a longer session. The MaxSessionDuration setting determines the maximum duration that can be requested using the DurationSeconds parameter. If users don't specify a value for the DurationSeconds parameter, their security credentials are valid for one hour by default. This applies when you use the AssumeRole* API operations or the assume-role* CLI operations but does not apply when you use those operations to create a console URL. Default: Duration.hours(1)
        :param path: (experimental) The path associated with this role. For information about IAM paths, see Friendly Names and Paths in IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param role_name: (experimental) A name for the IAM role. For valid values, see the RoleName parameter for the CreateRole action in the IAM API Reference. IMPORTANT: If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the role name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__32f33d3f9b8835fa27b2cbfa9ec4de4220d331f9dad55dd7093e77c01a5fc9e1)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = RoleProps(
            assumed_by=assumed_by,
            description=description,
            external_id=external_id,
            external_ids=external_ids,
            inline_policies=inline_policies,
            managed_policies=managed_policies,
            max_session_duration=max_session_duration,
            path=path,
            permissions_boundary=permissions_boundary,
            role_name=role_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromRoleArn")
    @builtins.classmethod
    def from_role_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_arn: builtins.str,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
        mutable: typing.Optional[builtins.bool] = None,
    ) -> IRole:
        '''(experimental) Import an external role by ARN.

        If the imported Role ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        role has a ``path`` (like ``arn:...:role/AdminRoles/Alice``), the
        ``roleName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Role ARN should be supplied without the
        ``path`` in order to resolve the correct role resource.

        :param scope: construct scope.
        :param id: construct id.
        :param role_arn: the ARN of the role to import.
        :param add_grants_to_resources: (experimental) For immutable roles: add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false
        :param mutable: (experimental) Whether the imported role can be modified by attaching policy resources to it. Default: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f50ec63b16b80cf0582ff7e8a9c895736dcf4fbb49af60acd6fa04c04759362d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
        options = FromRoleArnOptions(
            add_grants_to_resources=add_grants_to_resources, mutable=mutable
        )

        return typing.cast(IRole, jsii.sinvoke(cls, "fromRoleArn", [scope, id, role_arn, options]))

    @jsii.member(jsii_name="fromRoleName")
    @builtins.classmethod
    def from_role_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        role_name: builtins.str,
    ) -> IRole:
        '''(experimental) Import an external role by name.

        The imported role is assumed to exist in the same account as the account
        the scope's containing Stack is being deployed to.

        :param scope: -
        :param id: -
        :param role_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__652b63d9f8c86e7f9d2a8f4410c7cdeb4ac480af0128f0f966c91748bc60347a)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        return typing.cast(IRole, jsii.sinvoke(cls, "fromRoleName", [scope, id, role_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to this role.

        :param policy: The the managed policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__85daa53a67caf97805a1f126f6b883848bc7c8830183eb0cf8132df12421c96f)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fa16f9f99e97b6e3da5469a59e06d330caa48a0a0cec2685712db2928b13e84)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Adds a permission to the role's default policy document.

        If there is no default policy attached to this role, it will be created.

        :param statement: The permission statement to add to the policy document.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__417e4df00b877dd56a8895ef2ff3b14dc7d092bea4be368e6f57f4e8682184b3)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches a policy to this role.

        :param policy: The policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__702e0f53acb2af0aede54f824bccbd41ccc5836fbd6a3bac737323542229b1c1)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @jsii.member(jsii_name="grant")
    def grant(self, grantee: IPrincipal, *actions: builtins.str) -> Grant:
        '''(experimental) Grant the actions defined in actions to the identity Principal on this resource.

        :param grantee: -
        :param actions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97d44787a8d68ebc0e17c435680d5d2770ad7622e36f192e02281269a7281d28)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(Grant, jsii.invoke(self, "grant", [grantee, *actions]))

    @jsii.member(jsii_name="grantAssumeRole")
    def grant_assume_role(self, identity: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to assume this role.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd4bad4aac5266006daa976287b18f959f658269e4fdfa91c45c4fd82e3c0a49)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantAssumeRole", [identity]))

    @jsii.member(jsii_name="grantPassRole")
    def grant_pass_role(self, identity: IPrincipal) -> Grant:
        '''(experimental) Grant permissions to the given principal to pass this role.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8421288fe8a40d213cb5384a789755121e56e1a93ea8c645848cf87fa519f57d)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(Grant, jsii.invoke(self, "grantPassRole", [identity]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @jsii.member(jsii_name="withoutPolicyUpdates")
    def without_policy_updates(
        self,
        *,
        add_grants_to_resources: typing.Optional[builtins.bool] = None,
    ) -> IRole:
        '''(experimental) Return a copy of this Role object whose Policies will not be updated.

        Use the object returned by this method if you want this Role to be used by
        a construct without it automatically updating the Role's Policies.

        If you do, you are responsible for adding the correct statements to the
        Role's policies yourself.

        :param add_grants_to_resources: (experimental) Add grants to resources instead of dropping them. If this is ``false`` or not specified, grant permissions added to this role are ignored. It is your own responsibility to make sure the role has the required permissions. If this is ``true``, any grant permissions will be added to the resource instead. Default: false

        :stability: experimental
        '''
        options = WithoutPolicyUpdatesOptions(
            add_grants_to_resources=add_grants_to_resources
        )

        return typing.cast(IRole, jsii.invoke(self, "withoutPolicyUpdates", [options]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Returns the role.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''(experimental) Returns the ARN of this role.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @builtins.property
    @jsii.member(jsii_name="roleId")
    def role_id(self) -> builtins.str:
        '''(experimental) Returns the stable and unique string identifying the role.

        For example,
        AIDAJQABLZS4A3QDU576Q.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleId"))

    @builtins.property
    @jsii.member(jsii_name="roleName")
    def role_name(self) -> builtins.str:
        '''(experimental) Returns the name of the role.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleName"))

    @builtins.property
    @jsii.member(jsii_name="assumeRolePolicy")
    def assume_role_policy(self) -> typing.Optional[PolicyDocument]:
        '''(experimental) The assume role policy document associated with this role.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[PolicyDocument], jsii.get(self, "assumeRolePolicy"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''(experimental) Returns the permissions boundary attached to this role.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IManagedPolicy], jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class ServicePrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.ServicePrincipal",
):
    '''(experimental) An IAM principal that represents an AWS service (i.e. sqs.amazonaws.com).

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_role = iam.Role(self, "Role",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"),
            description="Example role..."
        )
        
        stream = kinesis.Stream(self, "MyEncryptedStream",
            encryption=kinesis.StreamEncryption.KMS
        )
        
        # give lambda permissions to read stream
        stream.grant_read(lambda_role)
    '''

    def __init__(
        self,
        service: builtins.str,
        *,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param service: AWS service (i.e. sqs.amazonaws.com).
        :param conditions: (experimental) Additional conditions to add to the Service Principal. Default: - No conditions
        :param region: (deprecated) The region in which the service is operating. Default: - the current Stack's region.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__592c5610dbe0789759022de7d57483b42e60153345097fdbeda1ab7914d0c122)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        opts = ServicePrincipalOpts(conditions=conditions, region=region)

        jsii.create(self.__class__, self, [service, opts])

    @jsii.member(jsii_name="servicePrincipalName")
    @builtins.classmethod
    def service_principal_name(cls, service: builtins.str) -> builtins.str:
        '''(experimental) Translate the given service principal name based on the region it's used in.

        For example, for Chinese regions this may (depending on whether that's necessary
        for the given service principal) append ``.cn`` to the name.

        The ``region-info`` module is used to obtain this information.

        :param service: -

        :stability: experimental

        Example::

            principal_name = iam.ServicePrincipal.service_principal_name("ec2.amazonaws.com")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e1ae3127ae5aeafcb4b0fcf3059ff1b3042e514f1aa28b3d02a9d2c2f549333)
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        return typing.cast(builtins.str, jsii.sinvoke(cls, "servicePrincipalName", [service]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="service")
    def service(self) -> builtins.str:
        '''(experimental) AWS service (i.e. sqs.amazonaws.com).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "service"))


class SessionTagsPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.SessionTagsPrincipal",
):
    '''(experimental) Enables session tags on role assumptions from a principal.

    For more information on session tags, see:
    https://docs.aws.amazon.com/IAM/latest/UserGuide/id_session-tags.html

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # principal: iam.IPrincipal
        
        session_tags_principal = iam.SessionTagsPrincipal(principal)
    '''

    def __init__(self, principal: IPrincipal) -> None:
        '''
        :param principal: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38690d13b9084bf44e851d32958e11efa278673502b2c7745c1f09f3876df807)
            check_type(argname="argument principal", value=principal, expected_type=type_hints["principal"])
        jsii.create(self.__class__, self, [principal])

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, doc: PolicyDocument) -> None:
        '''(experimental) Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param doc: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9658287d4a9daeee3f6c0d3f57370d6d65b7b40113e35d565eae8388c8201e62)
            check_type(argname="argument doc", value=doc, expected_type=type_hints["doc"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [doc]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ad180a531b77f4378fda874ad2ae26abb325d0700cc32bb0a996160b36d7385c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fb50acd2019a9721cb4823417e973fd189466606ee7d2eecf695d0f9afbaaac9)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="appendDedupe")
    def _append_dedupe(self, append: builtins.str) -> typing.Optional[builtins.str]:
        '''(experimental) Append the given string to the wrapped principal's dedupe string (if available).

        :param append: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68e87721f0c6a230150fcce5a9d9700c625618a64120094c3ef554483e8dc3fa)
            check_type(argname="argument append", value=append, expected_type=type_hints["append"])
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "appendDedupe", [append]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class StarPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.StarPrincipal",
):
    '''(experimental) A principal that uses a literal '*' in the IAM JSON language.

    Some services behave differently when you specify ``Principal: "*"``
    or ``Principal: { AWS: "*" }`` in their resource policy.

    ``StarPrincipal`` renders to ``Principal: *``. Most of the time, you
    should use ``AnyPrincipal`` instead.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        star_principal = iam.StarPrincipal()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.implements(IIdentity, IUser)
class User(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.User",
):
    '''(experimental) Define a new IAM user.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
        group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');
        
        user.add_to_group(group)
        # or
        group.add_user(user)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        groups: typing.Optional[typing.Sequence["IGroup"]] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        password: typing.Optional[_SecretValue_c18506ef] = None,
        password_reset_required: typing.Optional[builtins.bool] = None,
        path: typing.Optional[builtins.str] = None,
        permissions_boundary: typing.Optional[IManagedPolicy] = None,
        user_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param groups: (experimental) Groups to add this user to. You can also use ``addToGroup`` to add this user to a group. Default: - No groups.
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param password: (experimental) The password for the user. This is required so the user can access the AWS Management Console. You can use ``SecretValue.unsafePlainText`` to specify a password in plain text or use ``secretsmanager.Secret.fromSecretAttributes`` to reference a secret in Secrets Manager. Default: - User won't be able to access the management console without a password.
        :param password_reset_required: (experimental) Specifies whether the user is required to set a new password the next time the user logs in to the AWS Management Console. If this is set to 'true', you must also specify "initialPassword". Default: false
        :param path: (experimental) The path for the user name. For more information about paths, see IAM Identifiers in the IAM User Guide. Default: /
        :param permissions_boundary: (experimental) AWS supports permissions boundaries for IAM entities (users or roles). A permissions boundary is an advanced feature for using a managed policy to set the maximum permissions that an identity-based policy can grant to an IAM entity. An entity's permissions boundary allows it to perform only the actions that are allowed by both its identity-based policies and its permissions boundaries. Default: - No permissions boundary.
        :param user_name: (experimental) A name for the IAM user. For valid values, see the UserName parameter for the CreateUser action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the user name. If you specify a name, you cannot perform updates that require replacement of this resource. You can perform updates that require no or some interruption. If you must replace the resource, specify a new name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: - Generated by CloudFormation (recommended)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5dee86759655ab923761104bb56d1f12ad4c0731ea241ffeb50c2e470d880b3c)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UserProps(
            groups=groups,
            managed_policies=managed_policies,
            password=password,
            password_reset_required=password_reset_required,
            path=path,
            permissions_boundary=permissions_boundary,
            user_name=user_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromUserArn")
    @builtins.classmethod
    def from_user_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        user_arn: builtins.str,
    ) -> IUser:
        '''(experimental) Import an existing user given a user ARN.

        If the ARN comes from a Token, the User cannot have a path; if so, any attempt
        to reference its username will fail.

        :param scope: construct scope.
        :param id: construct id.
        :param user_arn: the ARN of an existing user to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10bf3e67c76d3acf460c81230bcf47453a39505ca992f234397150d11814e478)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_arn", value=user_arn, expected_type=type_hints["user_arn"])
        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserArn", [scope, id, user_arn]))

    @jsii.member(jsii_name="fromUserAttributes")
    @builtins.classmethod
    def from_user_attributes(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        user_arn: builtins.str,
    ) -> IUser:
        '''(experimental) Import an existing user given user attributes.

        If the ARN comes from a Token, the User cannot have a path; if so, any attempt
        to reference its username will fail.

        :param scope: construct scope.
        :param id: construct id.
        :param user_arn: (experimental) The ARN of the user. Format: arn::iam:::user/

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1556269e381e138692f70c0dd6bce45d226899c04e136cbae5311d26b3375ba6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        attrs = UserAttributes(user_arn=user_arn)

        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserAttributes", [scope, id, attrs]))

    @jsii.member(jsii_name="fromUserName")
    @builtins.classmethod
    def from_user_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        user_name: builtins.str,
    ) -> IUser:
        '''(experimental) Import an existing user given a username.

        :param scope: construct scope.
        :param id: construct id.
        :param user_name: the username of the existing user to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d3d05881f527ce602c738f7cc6350d8fee2015ef6826bfeac6b56fca236506d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument user_name", value=user_name, expected_type=type_hints["user_name"])
        return typing.cast(IUser, jsii.sinvoke(cls, "fromUserName", [scope, id, user_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to the user.

        :param policy: The managed policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18a4f92ef80e58f9cc6695e5df3e03d8c9fdb2f452f9cbfb2250274c34d9bae4)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToGroup")
    def add_to_group(self, group: "IGroup") -> None:
        '''(experimental) Adds this user to a group.

        :param group: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bc84fade0de8b90894d4708df23e756d8cb2e74657b1878ca14d49e15c41ce66)
            check_type(argname="argument group", value=group, expected_type=type_hints["group"])
        return typing.cast(None, jsii.invoke(self, "addToGroup", [group]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bec12b2fa2a30f72af5d5c42bff5eee0b1e8a39481c5c3eb09ae060b8569d9a4)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Adds an IAM statement to the default policy.

        :param statement: -

        :return: true

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__930760e685c2d057d6a9ee89c4adb0113503799945533a20ba9789e405bdb556)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches a policy to this user.

        :param policy: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e174a7ffee8820ea7e207febcc8b419df11ae0ba30f342f6dc6269543d9625b)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="userArn")
    def user_arn(self) -> builtins.str:
        '''(experimental) An attribute that represents the user's ARN.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userArn"))

    @builtins.property
    @jsii.member(jsii_name="userName")
    def user_name(self) -> builtins.str:
        '''(experimental) An attribute that represents the user name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "userName"))

    @builtins.property
    @jsii.member(jsii_name="permissionsBoundary")
    def permissions_boundary(self) -> typing.Optional[IManagedPolicy]:
        '''(experimental) Returns the permissions boundary attached  to this user.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[IManagedPolicy], jsii.get(self, "permissionsBoundary"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class ArnPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.ArnPrincipal",
):
    '''(experimental) Specify a principal by the Amazon Resource Name (ARN).

    You can specify AWS accounts, IAM users, Federated SAML users, IAM roles, and specific assumed-role sessions.
    You cannot specify IAM groups or instance profiles as principals

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_principal.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # network_load_balancer1: elbv2.NetworkLoadBalancer
        # network_load_balancer2: elbv2.NetworkLoadBalancer
        
        
        ec2.VpcEndpointService(self, "EndpointService",
            vpc_endpoint_service_load_balancers=[network_load_balancer1, network_load_balancer2],
            acceptance_required=True,
            allowed_principals=[iam.ArnPrincipal("arn:aws:iam::123456789012:root")]
        )
    '''

    def __init__(self, arn: builtins.str) -> None:
        '''
        :param arn: Amazon Resource Name (ARN) of the principal entity (i.e. arn:aws:iam::123456789012:user/user-name).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dbf90d8cafb8f0b630efbe073236f22413b280fa54f11d870715730622499b97)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
        jsii.create(self.__class__, self, [arn])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="inOrganization")
    def in_organization(self, organization_id: builtins.str) -> PrincipalBase:
        '''(experimental) A convenience method for adding a condition that the principal is part of the specified AWS Organization.

        :param organization_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2818679fa41b811c914f2ca591255bfdb457f05e9fd4e083d4ec5b5c2b588ac8)
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        return typing.cast(PrincipalBase, jsii.invoke(self, "inOrganization", [organization_id]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) Amazon Resource Name (ARN) of the principal entity (i.e. arn:aws:iam::123456789012:user/user-name).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class CanonicalUserPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CanonicalUserPrincipal",
):
    '''(experimental) A policy principal for canonicalUserIds - useful for S3 bucket policies that use Origin Access identities.

    See https://docs.aws.amazon.com/general/latest/gr/acct-identifiers.html

    and

    https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html

    for more details.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        canonical_user_principal = iam.CanonicalUserPrincipal("canonicalUserId")
    '''

    def __init__(self, canonical_user_id: builtins.str) -> None:
        '''
        :param canonical_user_id: unique identifier assigned by AWS for every account. root user and IAM users for an account all see the same ID. (i.e. 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be)

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b731f56519babd91d826dc8dbcfcc1814a537e1bdc7fe8b600a5fd292661cecf)
            check_type(argname="argument canonical_user_id", value=canonical_user_id, expected_type=type_hints["canonical_user_id"])
        jsii.create(self.__class__, self, [canonical_user_id])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="canonicalUserId")
    def canonical_user_id(self) -> builtins.str:
        '''(experimental) unique identifier assigned by AWS for every account.

        root user and IAM users for an account all see the same ID.
        (i.e. 79a59df900b949e55d96a1e698fbacedfd6e09d98eacf8f8d5218e7cd47ef2be)

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "canonicalUserId"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class CompositePrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.CompositePrincipal",
):
    '''(experimental) Represents a principal that has multiple types of principals.

    A composite principal cannot
    have conditions. i.e. multiple ServicePrincipals that form a composite principal

    :stability: experimental
    :exampleMetadata: infused

    Example::

        role = iam.Role(self, "MyRole",
            assumed_by=iam.CompositePrincipal(
                iam.ServicePrincipal("ec2.amazonaws.com"),
                iam.AccountPrincipal("1818188181818187272"))
        )
    '''

    def __init__(self, *principals: IPrincipal) -> None:
        '''
        :param principals: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__047315fec9a3d924fa7b11c3178d502037b3569ccba735b91ef02f8a1b4f053c)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        jsii.create(self.__class__, self, [*principals])

    @jsii.member(jsii_name="addPrincipals")
    def add_principals(self, *principals: IPrincipal) -> "CompositePrincipal":
        '''(experimental) Adds IAM principals to the composite principal.

        Composite principals cannot have
        conditions.

        :param principals: IAM principals that will be added to the composite principal.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ccf36a015b5d38719a0881891ec44c3a7a2c8040e1fd4662e01e2b1648f1562)
            check_type(argname="argument principals", value=principals, expected_type=typing.Tuple[type_hints["principals"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast("CompositePrincipal", jsii.invoke(self, "addPrincipals", [*principals]))

    @jsii.member(jsii_name="addToAssumeRolePolicy")
    def add_to_assume_role_policy(self, doc: PolicyDocument) -> None:
        '''(experimental) Add the princpial to the AssumeRolePolicyDocument.

        Add the statements to the AssumeRolePolicyDocument necessary to give this principal
        permissions to assume the given role.

        :param doc: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b0db1f06ffb47fe72ad98ce9d4defc17ace56c2c223afcea989b2e35f28b9c)
            check_type(argname="argument doc", value=doc, expected_type=type_hints["doc"])
        return typing.cast(None, jsii.invoke(self, "addToAssumeRolePolicy", [doc]))

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class FederatedPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.FederatedPrincipal",
):
    '''(experimental) Principal entity that represents a federated identity provider such as Amazon Cognito, that can be used to provide temporary security credentials to users who have been authenticated.

    Additional condition keys are available when the temporary security credentials are used to make a request.
    You can use these keys to write policies that limit the access of federated users.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_iam-condition-keys.html#condition-keys-wif
    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        # conditions: Any
        
        federated_principal = iam.FederatedPrincipal("federated", {
            "conditions_key": conditions
        }, "assumeRoleAction")
    '''

    def __init__(
        self,
        federated: builtins.str,
        conditions: typing.Mapping[builtins.str, typing.Any],
        assume_role_action: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param federated: federated identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.
        :param assume_role_action: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67bbf4c25c041bc2f89f5c5d7dec5b718973c5000f6c0803f89a4ac34a03e1a)
            check_type(argname="argument federated", value=federated, expected_type=type_hints["federated"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
            check_type(argname="argument assume_role_action", value=assume_role_action, expected_type=type_hints["assume_role_action"])
        jsii.create(self.__class__, self, [federated, conditions, assume_role_action])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="conditions")
    def conditions(self) -> typing.Mapping[builtins.str, typing.Any]:
        '''(experimental) The conditions under which the policy is in effect.

        See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "conditions"))

    @builtins.property
    @jsii.member(jsii_name="federated")
    def federated(self) -> builtins.str:
        '''(experimental) federated identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "federated"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


@jsii.interface(jsii_type="monocdk.aws_iam.IGroup")
class IGroup(IIdentity, typing_extensions.Protocol):
    '''(experimental) Represents an IAM Group.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) Returns the IAM Group ARN.

        :stability: experimental
        :attribute: true
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) Returns the IAM Group Name.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IGroupProxy(
    jsii.proxy_for(IIdentity), # type: ignore[misc]
):
    '''(experimental) Represents an IAM Group.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_iam.IGroup"

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) Returns the IAM Group ARN.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) Returns the IAM Group Name.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IGroup).__jsii_proxy_class__ = lambda : _IGroupProxy


class OrganizationPrincipal(
    PrincipalBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.OrganizationPrincipal",
):
    '''(experimental) A principal that represents an AWS Organization.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        organization_principal = iam.OrganizationPrincipal("organizationId")
    '''

    def __init__(self, organization_id: builtins.str) -> None:
        '''
        :param organization_id: The unique identifier (ID) of an organization (i.e. o-12345abcde).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__58df4c9802f623fc2c52ce35a7ac517c5a5a27c19f402bac97c1752438af3319)
            check_type(argname="argument organization_id", value=organization_id, expected_type=type_hints["organization_id"])
        jsii.create(self.__class__, self, [organization_id])

    @jsii.member(jsii_name="dedupeString")
    def dedupe_string(self) -> typing.Optional[builtins.str]:
        '''(experimental) Return whether or not this principal is equal to the given principal.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.invoke(self, "dedupeString", []))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="organizationId")
    def organization_id(self) -> builtins.str:
        '''(experimental) The unique identifier (ID) of an organization (i.e. o-12345abcde).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "organizationId"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class SamlPrincipal(
    FederatedPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.SamlPrincipal",
):
    '''(experimental) Principal entity that represents a SAML federated identity provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        principal = iam.SamlPrincipal(provider, {
            "StringEquals": {
                "SAML:iss": "issuer"
            }
        })
    '''

    def __init__(
        self,
        saml_provider: ISamlProvider,
        conditions: typing.Mapping[builtins.str, typing.Any],
    ) -> None:
        '''
        :param saml_provider: -
        :param conditions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24b7c3d44e12e24b06cf1c138cecfd5c2e0c69d472500d13859975460666e935)
            check_type(argname="argument saml_provider", value=saml_provider, expected_type=type_hints["saml_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [saml_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class WebIdentityPrincipal(
    FederatedPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.WebIdentityPrincipal",
):
    '''(experimental) A principal that represents a federated identity provider as Web Identity such as Cognito, Amazon, Facebook, Google, etc.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        principal = iam.WebIdentityPrincipal("cognito-identity.amazonaws.com", {
            "StringEquals": {"cognito-identity.amazonaws.com:aud": "us-east-2:12345678-abcd-abcd-abcd-123456"},
            "ForAnyValue:StringLike": {"cognito-identity.amazonaws.com:amr": "unauthenticated"}
        })
    '''

    def __init__(
        self,
        identity_provider: builtins.str,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param identity_provider: identity provider (i.e. 'cognito-identity.amazonaws.com' for users authenticated through Cognito).
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5f1b67266317d4890fa969cd5148e820db2a47a79eebd553f240a319b40b5701)
            check_type(argname="argument identity_provider", value=identity_provider, expected_type=type_hints["identity_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [identity_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class AccountPrincipal(
    ArnPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.AccountPrincipal",
):
    '''(experimental) Specify AWS account ID as the principal entity in a policy to delegate authority to the account.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        cluster = neptune.DatabaseCluster(self, "Cluster",
            vpc=vpc,
            instance_type=neptune.InstanceType.R5_LARGE,
            iam_authentication=True
        )
        role = iam.Role(self, "DBRole", assumed_by=iam.AccountPrincipal(self.account))
        cluster.grant_connect(role)
    '''

    def __init__(self, account_id: typing.Any) -> None:
        '''
        :param account_id: AWS account ID (i.e. 123456789012).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13ba0f59001ad809f7eaa618802f41bd1b3c589ccc4c38817645572420f3a7cf)
            check_type(argname="argument account_id", value=account_id, expected_type=type_hints["account_id"])
        jsii.create(self.__class__, self, [account_id])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="accountId")
    def account_id(self) -> typing.Any:
        '''(experimental) AWS account ID (i.e. 123456789012).

        :stability: experimental
        '''
        return typing.cast(typing.Any, jsii.get(self, "accountId"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class AccountRootPrincipal(
    AccountPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.AccountRootPrincipal",
):
    '''(experimental) Use the AWS account into which a stack is deployed as the principal entity in a policy.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        bucket = s3.Bucket(self, "MyBucket")
        result = bucket.add_to_resource_policy(iam.PolicyStatement(
            actions=["s3:GetObject"],
            resources=[bucket.arn_for_objects("file.txt")],
            principals=[iam.AccountRootPrincipal()]
        ))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class AnyPrincipal(
    ArnPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.AnyPrincipal",
):
    '''(experimental) A principal representing all AWS identities in all accounts.

    Some services behave differently when you specify ``Principal: '*'``
    or ``Principal: { AWS: "*" }`` in their resource policy.

    ``AnyPrincipal`` renders to ``Principal: { AWS: "*" }``. This is correct
    most of the time, but in cases where you need the other principal,
    use ``StarPrincipal`` instead.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        topic = sns.Topic(self, "Topic")
        topic_policy = sns.TopicPolicy(self, "TopicPolicy",
            topics=[topic]
        )
        
        topic_policy.document.add_statements(iam.PolicyStatement(
            actions=["sns:Subscribe"],
            principals=[iam.AnyPrincipal()],
            resources=[topic.topic_arn]
        ))
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


class Anyone(AnyPrincipal, metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_iam.Anyone"):
    '''(deprecated) A principal representing all identities in all accounts.

    :deprecated: use ``AnyPrincipal``

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_iam as iam
        
        anyone = iam.Anyone()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])


@jsii.implements(IGroup)
class Group(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.Group",
):
    '''(experimental) An IAM Group (collection of IAM users) lets you specify permissions for multiple users, which can make it easier to manage permissions for those users.

    :see: https://docs.aws.amazon.com/IAM/latest/UserGuide/id_groups.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        user = iam.User(self, "MyUser") # or User.fromUserName(stack, 'User', 'johnsmith');
        group = iam.Group(self, "MyGroup") # or Group.fromGroupArn(stack, 'Group', 'arn:aws:iam::account-id:group/group-name');
        
        user.add_to_group(group)
        # or
        group.add_user(user)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        group_name: typing.Optional[builtins.str] = None,
        managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param group_name: (experimental) A name for the IAM group. For valid values, see the GroupName parameter for the CreateGroup action in the IAM API Reference. If you don't specify a name, AWS CloudFormation generates a unique physical ID and uses that ID for the group name. If you specify a name, you must specify the CAPABILITY_NAMED_IAM value to acknowledge your template's capabilities. For more information, see Acknowledging IAM Resources in AWS CloudFormation Templates. Default: Generated by CloudFormation (recommended)
        :param managed_policies: (experimental) A list of managed policies associated with this role. You can add managed policies later using ``addManagedPolicy(ManagedPolicy.fromAwsManagedPolicyName(policyName))``. Default: - No managed policies.
        :param path: (experimental) The path to the group. For more information about paths, see `IAM Identifiers <http://docs.aws.amazon.com/IAM/latest/UserGuide/index.html?Using_Identifiers.html>`_ in the IAM User Guide. Default: /

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__700efe0d66285b17214ae296baf6ef2aa4fc27fb0633c58e87ab8d0748ba63d8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GroupProps(
            group_name=group_name, managed_policies=managed_policies, path=path
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromGroupArn")
    @builtins.classmethod
    def from_group_arn(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_arn: builtins.str,
    ) -> IGroup:
        '''(experimental) Import an external group by ARN.

        If the imported Group ARN is a Token (such as a
        ``CfnParameter.valueAsString`` or a ``Fn.importValue()``) *and* the referenced
        group has a ``path`` (like ``arn:...:group/AdminGroup/NetworkAdmin``), the
        ``groupName`` property will not resolve to the correct value. Instead it
        will resolve to the first path component. We unfortunately cannot express
        the correct calculation of the full path name as a CloudFormation
        expression. In this scenario the Group ARN should be supplied without the
        ``path`` in order to resolve the correct group resource.

        :param scope: construct scope.
        :param id: construct id.
        :param group_arn: the ARN of the group to import (e.g. ``arn:aws:iam::account-id:group/group-name``).

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2aa81f20c8515398c4324df8298cb489ab5ede846a4d9a8d1f2d835e81a7c371)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_arn", value=group_arn, expected_type=type_hints["group_arn"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupArn", [scope, id, group_arn]))

    @jsii.member(jsii_name="fromGroupName")
    @builtins.classmethod
    def from_group_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        group_name: builtins.str,
    ) -> IGroup:
        '''(experimental) Import an existing group by given name (with path).

        This method has same caveats of ``fromGroupArn``

        :param scope: construct scope.
        :param id: construct id.
        :param group_name: the groupName (path included) of the existing group to import.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bc59992dfdbc023bba8cdd068b8b3f818a5df6d2b6a1955e88d9f675c81eba)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument group_name", value=group_name, expected_type=type_hints["group_name"])
        return typing.cast(IGroup, jsii.sinvoke(cls, "fromGroupName", [scope, id, group_name]))

    @jsii.member(jsii_name="addManagedPolicy")
    def add_managed_policy(self, policy: IManagedPolicy) -> None:
        '''(experimental) Attaches a managed policy to this group.

        :param policy: The managed policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6041eeb96684d237ffa6143289acc7c061fe775fcc98b1bf2a1cc1a3383363ad)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "addManagedPolicy", [policy]))

    @jsii.member(jsii_name="addToPolicy")
    def add_to_policy(self, statement: PolicyStatement) -> builtins.bool:
        '''(experimental) Add to the policy of this principal.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9e362c4ea76fb3b5b4980b0b8f40c1d2aa3a51baffa918dd6cf0367ff8ab6bb)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(builtins.bool, jsii.invoke(self, "addToPolicy", [statement]))

    @jsii.member(jsii_name="addToPrincipalPolicy")
    def add_to_principal_policy(
        self,
        statement: PolicyStatement,
    ) -> AddToPrincipalPolicyResult:
        '''(experimental) Adds an IAM statement to the default policy.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db8f0815713df243685119bc70a363aa602e95f1ddb9db93d4b9dcbd1d91e3de)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(AddToPrincipalPolicyResult, jsii.invoke(self, "addToPrincipalPolicy", [statement]))

    @jsii.member(jsii_name="addUser")
    def add_user(self, user: IUser) -> None:
        '''(experimental) Adds a user to this group.

        :param user: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2fb2a1dc663863ae3309eef8b61e61678818ba17e23f7b6ca697f311d6ffdda4)
            check_type(argname="argument user", value=user, expected_type=type_hints["user"])
        return typing.cast(None, jsii.invoke(self, "addUser", [user]))

    @jsii.member(jsii_name="attachInlinePolicy")
    def attach_inline_policy(self, policy: Policy) -> None:
        '''(experimental) Attaches a policy to this group.

        :param policy: The policy to attach.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__30d0aa908c57c5c50269e9cf04d8c0e818286fb53234b6b96c7234257c2c6076)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
        return typing.cast(None, jsii.invoke(self, "attachInlinePolicy", [policy]))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleAction")
    def assume_role_action(self) -> builtins.str:
        '''(experimental) When this Principal is used in an AssumeRole policy, the action to use.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "assumeRoleAction"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> IPrincipal:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(IPrincipal, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="groupArn")
    def group_arn(self) -> builtins.str:
        '''(experimental) Returns the IAM Group ARN.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupArn"))

    @builtins.property
    @jsii.member(jsii_name="groupName")
    def group_name(self) -> builtins.str:
        '''(experimental) Returns the IAM Group Name.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "groupName"))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))

    @builtins.property
    @jsii.member(jsii_name="principalAccount")
    def principal_account(self) -> typing.Optional[builtins.str]:
        '''(experimental) The AWS account ID of this principal.

        Can be undefined when the account is not known
        (for example, for service principals).
        Can be a Token - in that case,
        it's assumed to be AWS::AccountId.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "principalAccount"))


class OpenIdConnectPrincipal(
    WebIdentityPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.OpenIdConnectPrincipal",
):
    '''(experimental) A principal that represents a federated identity provider as from a OpenID Connect provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        provider = iam.OpenIdConnectProvider(self, "MyProvider",
            url="https://openid/connect",
            client_ids=["myclient1", "myclient2"]
        )
        principal = iam.OpenIdConnectPrincipal(provider)
    '''

    def __init__(
        self,
        open_id_connect_provider: IOpenIdConnectProvider,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param open_id_connect_provider: OpenID Connect provider.
        :param conditions: The conditions under which the policy is in effect. See `the IAM documentation <https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_elements_condition.html>`_.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a74d9838aaabd9c97bb3d9113dd4fb3247c08d3cf3b7e9356475657e698db9f)
            check_type(argname="argument open_id_connect_provider", value=open_id_connect_provider, expected_type=type_hints["open_id_connect_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [open_id_connect_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="policyFragment")
    def policy_fragment(self) -> PrincipalPolicyFragment:
        '''(experimental) Return the policy fragment that identifies this principal in a Policy.

        :stability: experimental
        '''
        return typing.cast(PrincipalPolicyFragment, jsii.get(self, "policyFragment"))


class SamlConsolePrincipal(
    SamlPrincipal,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_iam.SamlConsolePrincipal",
):
    '''(experimental) Principal entity that represents a SAML federated identity provider for programmatic and AWS Management Console access.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        provider = iam.SamlProvider(self, "Provider",
            metadata_document=iam.SamlMetadataDocument.from_file("/path/to/saml-metadata-document.xml")
        )
        iam.Role(self, "Role",
            assumed_by=iam.SamlConsolePrincipal(provider)
        )
    '''

    def __init__(
        self,
        saml_provider: ISamlProvider,
        conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''
        :param saml_provider: -
        :param conditions: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__786d01dc3c981565ec1dac3a15c0dce0451583bf0ac3fa6a47e2deddf45dc040)
            check_type(argname="argument saml_provider", value=saml_provider, expected_type=type_hints["saml_provider"])
            check_type(argname="argument conditions", value=conditions, expected_type=type_hints["conditions"])
        jsii.create(self.__class__, self, [saml_provider, conditions])

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Returns a string representation of an object.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))


__all__ = [
    "AccessKey",
    "AccessKeyProps",
    "AccessKeyStatus",
    "AccountPrincipal",
    "AccountRootPrincipal",
    "AddToPrincipalPolicyResult",
    "AddToResourcePolicyResult",
    "AnyPrincipal",
    "Anyone",
    "ArnPrincipal",
    "CanonicalUserPrincipal",
    "CfnAccessKey",
    "CfnAccessKeyProps",
    "CfnGroup",
    "CfnGroupProps",
    "CfnInstanceProfile",
    "CfnInstanceProfileProps",
    "CfnManagedPolicy",
    "CfnManagedPolicyProps",
    "CfnOIDCProvider",
    "CfnOIDCProviderProps",
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnRole",
    "CfnRoleProps",
    "CfnSAMLProvider",
    "CfnSAMLProviderProps",
    "CfnServerCertificate",
    "CfnServerCertificateProps",
    "CfnServiceLinkedRole",
    "CfnServiceLinkedRoleProps",
    "CfnUser",
    "CfnUserProps",
    "CfnUserToGroupAddition",
    "CfnUserToGroupAdditionProps",
    "CfnVirtualMFADevice",
    "CfnVirtualMFADeviceProps",
    "CommonGrantOptions",
    "ComparablePrincipal",
    "CompositeDependable",
    "CompositePrincipal",
    "Effect",
    "FederatedPrincipal",
    "FromRoleArnOptions",
    "Grant",
    "GrantOnPrincipalAndResourceOptions",
    "GrantOnPrincipalOptions",
    "GrantWithResourceOptions",
    "Group",
    "GroupProps",
    "IAccessKey",
    "IAssumeRolePrincipal",
    "IComparablePrincipal",
    "IGrantable",
    "IGroup",
    "IIdentity",
    "IManagedPolicy",
    "IOpenIdConnectProvider",
    "IPolicy",
    "IPrincipal",
    "IResourceWithPolicy",
    "IRole",
    "ISamlProvider",
    "IUser",
    "LazyRole",
    "LazyRoleProps",
    "ManagedPolicy",
    "ManagedPolicyProps",
    "OpenIdConnectPrincipal",
    "OpenIdConnectProvider",
    "OpenIdConnectProviderProps",
    "OrganizationPrincipal",
    "PermissionsBoundary",
    "Policy",
    "PolicyDocument",
    "PolicyDocumentProps",
    "PolicyProps",
    "PolicyStatement",
    "PolicyStatementProps",
    "PrincipalBase",
    "PrincipalPolicyFragment",
    "PrincipalWithConditions",
    "Role",
    "RoleProps",
    "SamlConsolePrincipal",
    "SamlMetadataDocument",
    "SamlPrincipal",
    "SamlProvider",
    "SamlProviderProps",
    "ServicePrincipal",
    "ServicePrincipalOpts",
    "SessionTagsPrincipal",
    "StarPrincipal",
    "UnknownPrincipal",
    "UnknownPrincipalProps",
    "User",
    "UserAttributes",
    "UserProps",
    "WebIdentityPrincipal",
    "WithoutPolicyUpdatesOptions",
]

publication.publish()

def _typecheckingstub__dbe6acddff2cdc94d9b64a2ce1a7fdb2adfa8031ce287d3cb87983191a5e8696(
    *,
    user: IUser,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[AccessKeyStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe0b7791b49f374eae9ddd4592e3e27bd665823872e35acb72e3d36c0159389a(
    *,
    statement_added: builtins.bool,
    policy_dependable: typing.Optional[_IDependable_1175c9f7] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c935a67875d0eb3bc280f234ffb6a5e6c1b6907c3a829725db60a932519606fd(
    *,
    statement_added: builtins.bool,
    policy_dependable: typing.Optional[_IDependable_1175c9f7] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4622828dd713c58f4ad3885641f58a22d8a4d322c47114fb3693a2bf274b77f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    user_name: builtins.str,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a00815c8171f70131e403ae4165db1dafff1b18767e259e719a0dd4e72259c86(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44b26c0b448ecd9334ee7eae692819bec4930e840f280ccf562dce8b91ae19f7(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__743d882a0c50d74bdc367c8d68f65befe4d1dfb6e42a8d9e7c71aedee0dc6d79(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c4060de3e744bb046559add0d34704383ee7e3fdfc2679236201b1bbef4d915(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ac006dbce0a77c0001f6ee6abe6fe754999c8be632037ca4fc80fca5c6417c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__23281560958a53aa55e7c7d7b74a2ac7cd445f3c6d88008c032934ebe282dd4b(
    *,
    user_name: builtins.str,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e728d9278d640c1582ba0a6418104e3e717678849840d6c54e0f3b68920414e7(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a912a189f77fe9aae4ffeaca33b3b3d80c4362f90ac12ceed858e1ed5bef3c08(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa86338033b2057a17eb608fd8f2884a0ed98711b9634b5d9bdedbb896f98518(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__656a942f6352918fbbd5a060020337c33703544d104d97f690597c7be27b426b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44d20024ca68eb57c1b884076c14fb159d1810dbf66f9513641a9cb53b0949e6(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c9b2f9b371a2358831cbf25db9b62a28d9963dc6e0ab19dd82de40ff13bb407d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66a8ebd02b16d4bf555fcbcbe6e18b19ece72ba3419302ed79dd15c762f239cb(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnGroup.PolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__90c1d907a3f012b9a1419dac96167bfb515682f874f994c772bf99b6982ee1c2(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__99c61736404e2b584bad16733704f81032060b7f21b40a1c5952295bfe969ac3(
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnGroup.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80712086ce0ba5d6d345e5d4efc7f6a4a4c49f2d2b8d8aaf831ce2e99e7d4aa(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    roles: typing.Sequence[builtins.str],
    instance_profile_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3541f2c18a3521f1e375fda06f3a1b0a093487447c90294ab41949de5db70b42(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af31761f00835f6e239eb1832794d6c294be454029ac1dd70540aab55da85192(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4286d427208028975bf80e37a6cd9f21e7dd589a5f68dd4f716ab4df191166ee(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81ba92744d35d2c0943e21772e62771328a98fb6bc0d33686b3510519504cc23(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b7a2adee77ab1c223b0e58b56e85f8d129bd8d254b533d779505ccce1e73f30(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fe81c53dc01117f631ea31d93fea1fb265aa69568c02ffaa833de39a23b6083f(
    *,
    roles: typing.Sequence[builtins.str],
    instance_profile_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d7295fe873b5468acdca1388cb7fb4e18371ad4d39c0152419700e704304042(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41c7f166512551a40454caf84a801f191ff025a03bd7924636c060368739a7b(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca6919a09b81613537222dfc3e9b07fdee77cb01e3a0b11b217a43b63aeb5e2c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4deb783ba798693331e1a4b36fc73b51fa59c567295ce97bab6c623292f96c79(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__182977da84f3bd39f60a2c5be5cdbc310439eb2eb555c9bc47fc91f05197078e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__beadf8f7e74db656fef53b215e2ba7b877cbe26cccf42010c8ad896a945ef274(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__136772522a7194fa3e838acac2bceb751bbe3e32d32f19fb0b9b0ebc0ee0a713(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df69b36e387aa8502db47854dcd52cc893a9a41a014d92c9ec51551358bf9588(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c096bb8bbdde3619b74dcd78e95d7475217fced4652b9510f6aec35c1f8e7dfb(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dd7765634021d5587ca4726d6acf091879e8a0d53d0bea4032186164e1b844d3(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__793d161e4a973c6db5c396c8a47fc90cdc692ddcfbb89a293d37c39f2ebbc217(
    *,
    policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4ad356568baf3cc2c3ab2fe48047c07cc488508a8e0c88b07f17fab78b77545(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    thumbprint_list: typing.Sequence[builtins.str],
    client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7fbb5c40440a88d129adf49c1348cf1801247b1c39ac63e524bfdaf5f217e23(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7aeb2363702ea0c2b5a06a8b47a8faa7791f02ddbfeb42b818befa38f55e378(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fcfc0fcfb444f04128fe566c2f1d534c6e9863fb2d19b70381880d35103b638c(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bda381b9f9f2a2b619886cfc87c71e1f01263b4daedaabc8a80a2e62e11877da(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__afdb30f5b29978d4574a35c2784bea041bd9039ed42ba84722ce78e7cacffe66(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a996edfa5ca2351f0144d6072930b51a302848a2db7fe007666d4fca5abe476(
    *,
    thumbprint_list: typing.Sequence[builtins.str],
    client_id_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    url: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fab3465f374f0ef915abf45cb5039f4e6ff0e76499029b9710c11318e39dcf9(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a98c43992dae03ae7744dd53cc779bcb3a614c9404fb7a1dbdc16f9a34e1391(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f0221c026571cb360ea6ac10a8498e4191d7070b47e3d4c7eddf7decc167929e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5371162b66e4e4ec284d5ebf4afcac85a2168c4dc032c8707a4e888b2db7bf0(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f15aa6a15100d07c733f3eb1fa07d624f59c1f67eeb9e7463b9e0160dc41f8(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be497bbf4efa2df1cfce18e7afea9ae541f26bf743f79b5f339cfa287047b9f0(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__635797cbee390cbcf746a9192dfaff877ecae263c5ecee87a169e0c95495388f(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__154d54b8d9f75c1aaf34dcf8f925274020a73188bc3e0d517c9dca67fdb9ccc4(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e08e6f0ff6f44a0242113a667e938008874cbf05ceceaeb5fde54cd3082868e9(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    roles: typing.Optional[typing.Sequence[builtins.str]] = None,
    users: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce964e0de267d204f32999fa5a654c0e2e5f9458b332c3922394b3b7e02ebc0e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    assume_role_policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_duration: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad081a33db5bfd7b92131b1366301a0048c67e3d38822293dbb9615c546d7fc8(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7db76988ea3967babb7fa78dbb28dc5b821761602b8c268536c74a320dce2906(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef08307620961b0d29bc42964ef20cb5e5385d5efaa273219063c111342967c4(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a721ce165cd2aa06da526e8bd6cc3e789a63a27591062e6603b72fcd979f2750(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d8aaa92a31c7d868a553d185b83d6920d2ade158fb295ee2b4806c7a9f0c332(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e0ba76eb15f186e1ee30a4b0457e9a415ed432127a38ba0e392346b634848ba4(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c1a75bda1e43eedef2aa097843785d4d746c74032b6f333c3ec9fffd4df75d7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__26ebd0e1dd466e235f65dfebbd85644096e38d87d4941392a795c66173e88ef9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5126d35f269a24e9610eb38a4e55b1c0ca0050aaf09e182e27ad03bb0101664e(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnRole.PolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e99aa335ce899dc15561f63b4ff1e92b27063fa7686b486b9956bfa29fb6614e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a59c2b44c2d2cb21703aaf8d4f06fffaf75db69f17c6bd2a7e63f6ac7396ce3(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24419d7834f7ce64b604b8867d44aed4da20d872bf81ec3c43125c330c24c164(
    *,
    assume_role_policy_document: typing.Any,
    description: typing.Optional[builtins.str] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    max_session_duration: typing.Optional[jsii.Number] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnRole.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    role_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8c257694f667971c2df1b72a987c0f9386a93ef3f21627c59b459b4c8f3a660(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    saml_metadata_document: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43564e8969a6acf8449cee6b9eb7262457145a7dde9996dca88012a41b5f9a93(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebdad39afc6b940b3319b8250044ab55497ed3bc857990ed9724a64243d0102c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4f7b9cfd72d5f1fa79cef048b9fc8442e28d84854eb45a3e35f41e06d47b57e4(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b187478871231f90dba3a4372534773fa3ad18ca59a8366c591b62417d01c7d0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61c788f04c2dcaee21c72ba80b7027aeef890a05fd285247b03176e0ee9217c4(
    *,
    saml_metadata_document: builtins.str,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33c4d49897e31f1a92d7ad3280920f7c0339c6a2b2750461c50a2a7fb2c33926(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    certificate_body: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    server_certificate_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328a969c0146798b7bfffc57507eb06737fcd9d1da82009f8c7c6b1bec226b02(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__095904f3405fee346d01283b9840e2a97774890c5a011071f8060cf5a23deae3(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__904fe41a95195bb9b11379edd250dd20dcae7c3702d4f42f6900ed8f74bc51f8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__169e7575044ef911af3d03a5433003ac9d61f0b92721f70d5ae8e48e49991f2e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6cd0e794ea5ae79edcc0d07e78be16d81c7e59efa9346d4294a951bbc46931f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__901b4b2f545a1c797203446b757a14b3b9752451a65c7508a8147d918ff965e7(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22a6764d73d26cdeb7c1f9c7096cf5221964eab7674a83b62b566da8730dc32(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc9f649104fcdf3ec038a7145b62aafeb511114f799a114251dc4dfc013d81dc(
    *,
    certificate_body: typing.Optional[builtins.str] = None,
    certificate_chain: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    private_key: typing.Optional[builtins.str] = None,
    server_certificate_name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0c6506b6ae6f00af5ac5c449a0cbf864904cd5557ef9ab8dbe7a152aedd1e0f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    aws_service_name: builtins.str,
    custom_suffix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__667c3c3cd1a347c5769025eb5e3cdf57842d62f8296b42b3f3f20ac576add0e6(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1f4d38ec22dee0a0f5faa36f17a18c0107e5f667206a3027ab1e803ad84793(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dd2e2739ab49d8892778787276d93dab4bf6364d8190f75fb0c371eea3cd941(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1435440d155e997493d0b3652087e4f0924a3ef70640be30d9345027c0450d33(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7a13d645b2dde2bb411e864575230c0f6aeb1f72de5485a5bfa8c9252be4f30a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bb7850752f6463384c57ddc16a5f1dd07a73db3410a913522e100febfda97de(
    *,
    aws_service_name: builtins.str,
    custom_suffix: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__684a0c7011928d2cc111a24fe8a18bb4d08c3f126b65ba884514a712a16d297e(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_profile: typing.Optional[typing.Union[typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88716a13390db0fdec2c4d193d8376a0c0033b8a36a8bc17fb92d24426d18d9d(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__013d48bf94780cca8cd196c67c7fb6e67b57a4290f7c3469f97b2864093796dd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__43b6c3e559a7988eb41890d1e3c84f2f2ffdbb5096692d64feb7ab4a4167c678(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e430934b039692641886ac2d0e6ca8344634938fa8d5439366ec41ca00254bf7(
    value: typing.Optional[typing.Union[CfnUser.LoginProfileProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__20bb0ddd9cc063059f1c56a4924340627d01d6f7cacbf14b12686f018a2d7384(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df5e2c08492371c820c30dcd287f174838188363f3cfdb35b44e45460fffa05b(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a40e432b9728c24dc2744e29104d48734acf3f1ef86dcba6bc0a81828e8c618(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e02bdccbc0be3c4695c49c7ac3d5a48f68c5a90b925d3dd6152bbec363da866c(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnUser.PolicyProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__001fb0a534147dacfc94693a3ba7dfecc211986fcc261dd6cd6605c5e56e21e9(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__54ef2d2672c787807815b09e4b9da212346c539f44cd34480979aa3366b36fc6(
    *,
    password: builtins.str,
    password_reset_required: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a05cf007b9f709458d8ebb65fcb9ae6373bfbff233eb448b9c829adc1c6d189(
    *,
    policy_document: typing.Any,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__78e0bbff574663d9a1ac08f43a6abed3e19785a386d126b2c2b600053e266cca(
    *,
    groups: typing.Optional[typing.Sequence[builtins.str]] = None,
    login_profile: typing.Optional[typing.Union[typing.Union[CfnUser.LoginProfileProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    managed_policy_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[builtins.str] = None,
    policies: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnUser.PolicyProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f87307cb0d01ccb9fd86f9193f327cf6991be45b8d8a92b19fdd9e6f30cfc6d2(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    group_name: builtins.str,
    users: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__07d9db6e767a4d909cc4b8b7dbb6c2b2e0c846d72c804344bf1772be47915176(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6422ec8e46050ae22c2ddea742c8b612f073f0388a88dab96778e51ae6f0ef8(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74b078a0d03ba0f23f3eb2446775c1fd260acebfc5b8658500705200a8549a0b(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7b2076c4668173824c8e623332053f838f49f4c24a04b5d61cae8cfb303145af(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__263aabd4f6f34733d87b4115e20c0ec840e846c26574891e4aa46ca24e4a74e3(
    *,
    group_name: builtins.str,
    users: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__48d0a2bafee0df44ebb2d917e04cdf7aecc71b03018aab980db4a8031024e308(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    users: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_mfa_device_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40bcf3f29a5ed35f71d0024e2771f29f12441810d8eacbfb4cab10fb1db73271(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adf85a67b00a5d84c5a0974bb758338236e31f6b26b0252699c991c1aa7c7db0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__612ce800090ba82ade073ea4dbf3a212419055abf7b33d4feb9812d71e34a777(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4437c569b52f9903d7582d66f4d4423ee04874b73a90959c57b836d43b9cb1a0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dea1e81beed1ddf9663744d1ddec8495abf547135b923491e1efee8c0632a5ea(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56b034abefc62813f16a987adf2fc982ed3092448f85315cd7a73e39052fe0f0(
    *,
    users: typing.Sequence[builtins.str],
    path: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    virtual_mfa_device_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b314d0430939f5e61d9ccffd7b0afec5cfab9709af782d0ba58b1e43a2e9352c(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d748c7aa7bab2a43d26bb3d15942dac0380385cd7889b24ed4ca2f0d9d3a2941(
    x: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8db93bead5186c0248601fce80ea0d4471eebdb74a995a3fc52312ba1e0ed3f2(
    x: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__796fbf18d6a487ed99258d14dcf05d8b766095a618d7d9ceb8298c8a75c811cc(
    *dependables: _IDependable_1175c9f7,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__113dd30efbd95031e80d8a2e8a7306de2e9a90ed6555dcf24c8f32424c5d6313(
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
    mutable: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2500d7ad2db0c1fe22f3b01cfc2344ff5f1a9197e561fd337325ac0135e230b7(
    grantee: IGrantable,
    _intent: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__33afaae65484f02d97629c95ea07b3503a1b777c130d956c9a5ed0063b7bf6e3(
    *constructs: _IConstruct_5a0f9c5e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4e3ebcd9a880a1e9c5fe53e41a03ffc19eee30fa132f3c0fc69047719415312a(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    resource: IResourceWithPolicy,
    resource_policy_principal: typing.Optional[IPrincipal] = None,
    resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32be6673535c40632c5e1aa0155055224c1c616a2a976e92191a0498336b70d1(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    scope: typing.Optional[_IConstruct_5a0f9c5e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d857fadaf9384d4f4bea13ca3123a8b1cfb66ac6f0189af3664729097e0d8a5(
    *,
    actions: typing.Sequence[builtins.str],
    grantee: IGrantable,
    resource_arns: typing.Sequence[builtins.str],
    resource: IResourceWithPolicy,
    resource_self_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3457a99d3d669d5f6820eab0f29541cc813d92b70e68b1ab5501f52a2d9b4c0(
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cef352b1b4609818242fbd4ce07299724c199dae36651f4b74a862ae89535fb(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e9e7c38ccab985da14ec9adb31b03cc2f7e0773c2f15e694434de0b6ce1aee(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd76918a27747150e0e6707e087c913d95d340a16a9f3f2adc165770291fe4a4(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dad52d68d4417c62f8e067aea7ba55944c0e1819ef0866e8d262826e784041a2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    description: typing.Optional[builtins.str] = None,
    document: typing.Optional[PolicyDocument] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc98b3ba7579a754738b9d083fdd2784faeb06a8477e2ad12f851604f9a5d5db(
    managed_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44ea6a7d7bc18419cb3ca0a4593c90b301c387b10a9cab19bd3f87afa912f908(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    managed_policy_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__66b9089da65cf6c2cc3350a479d670bc6a19f1b53e7f117ce01b4ee92412e548(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    managed_policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d99c718d018f1ce06685d3378e7bd30cc042a840f95130042fcc9d9a7c38c4f6(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73dc4c77a305b2a62ba7dfb3f923ae359ddface29ef9c6c77c64ac0b44ef14ac(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ec2ea2644d49f9637790e892ca423452da05d54959b505888286e12f814e296a(
    role: IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5be1ed600a4df9bb4370045150838cc261e4fc6239232235487c479bd9ac0a7d(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4632e60b96836c3e86adf2c0b865fbb5df38c091802d4045f90fef2cdf85930(
    *,
    description: typing.Optional[builtins.str] = None,
    document: typing.Optional[PolicyDocument] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policy_name: typing.Optional[builtins.str] = None,
    path: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8f099ca9fde67df8fe4f8d106dc9b8c511302707b1d02da4b57394306a49149(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    url: builtins.str,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65841d1f1daf7d051fb9333d7658c734c770539a18ef3d135b86316b57d79d05(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    open_id_connect_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__194521551a8bd320b87c90b1f5e6b60046fffc45ea1ac6ac5c2553c8df84c3bf(
    *,
    url: builtins.str,
    client_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    thumbprints: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e465496c36009643e8e100ab459cf1a1795fa41ba4340d5f71f520aebfbb7785(
    scope: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a18ae37fcb7498b0a25b802f460754eaa037765be71770dc04c80e051da74a7(
    boundary_policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dfb9f54f1d6d67ba10ae1851caf3d9ac0c99e277ad2f5b898837bac846c7ffe(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    document: typing.Optional[PolicyDocument] = None,
    force: typing.Optional[builtins.bool] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    policy_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd8be90172bdb2af6d199744f23c4574d1d621a0ea5dde4d3ff84f28c260d6dd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    policy_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfbae63bd491de9985a184344c9e53ceac666bb2e7279576ea881d152cf59c3a(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__88ff22e4b732f1c4d955b295276c95310eab4fc157c2718ac6618f20cfc2d784(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ecf54afb4d65976a4c5a91f513c0d3536d44e06f03337230dbb0ace314c15693(
    role: IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f6dc5ece5b25150251648ee7f6109ff96f8b58ffd33b779cfdb946ee6b7c7197(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3632bf0429b2ead03fc2244dad500274e6b30852db6957a77e85a2331f7496(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5c31df481edfc978e75bc2420910bedca67066cae379c96e6b3e333b41135d(
    *statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8ec693e55c88e20f55aa23668c3b9bc909dfdfde7ae24f32be8dcb1e0214534(
    context: _IResolveContext_e363e2cb,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3a1e3e91edf736d55dc46a58a60e2362c7a732a2db413abcddca5bf4ad76e678(
    *,
    assign_sids: typing.Optional[builtins.bool] = None,
    minimize: typing.Optional[builtins.bool] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61168007cabc979f17e4045d10fd09b836a743bcf6b65bb055cc5a4d1d5f4450(
    *,
    document: typing.Optional[PolicyDocument] = None,
    force: typing.Optional[builtins.bool] = None,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    policy_name: typing.Optional[builtins.str] = None,
    roles: typing.Optional[typing.Sequence[IRole]] = None,
    statements: typing.Optional[typing.Sequence[PolicyStatement]] = None,
    users: typing.Optional[typing.Sequence[IUser]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2d81dc6903db9408e732b9147d1459376b20b2f56b34385b9ca1bbc838ef935a(
    obj: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b276d93375472e08f6c170e4fbd9016a4051fa5b2ef4929883b26597f46bcd1a(
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5a7b77ff7202dab9bc7900741472abbc2b16815252b295efeff76a27e6a749(
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6c4df8a651eedc12f9e5af9112392fdd73941ff488c0b4c9cc4a11eac27d0909(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271e56250dffe5f4952052fef870839dbaab36f0f9580bcf78e75bf0e1ee5d9b(
    account_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__25377aa4146b0cfc4aca617e39ef2132cd58391b2b8b311cbf9df52d0d218cdd(
    canonical_user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__205662599e2ab097d3776122bb70402c2145e3bf80c05a85826abcb3cb815958(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de8e5dc92c4a814303dec0fec7ed657322b0fde5baa8f656dc01c687ae18eed3(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e4e4b1c824f3af8de88fb63c5b483545c5096f66a77b917b21ab036a36275e44(
    federated: typing.Any,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb3d4e663af1bab2477aea1248f540ecb2f2f812229eeed50230565fbae710f(
    *not_actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc94005e473308a931a0f02157a67a691341f074bcbd691ee0b6a3e36b6c3d3(
    *not_principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30146f1cf248be33e5cbe79c0ec8de33f1925d8cd3b70ef35a4b983e6b88099c(
    *arns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9940906039248437ca8811ef47f32f1dbdd27b9d7c689e2d438c3a54c89e04c6(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef8af799da1ef5a11db264fafe9da3cfad1a253e580b8f76a6a80ba0ef19b151(
    *arns: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ccc0bea9078c7ce635862e6e0635008835785be6ae5ff978b4baeb1b75038395(
    service: builtins.str,
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__57af2f06bec70b266e419c7f2c85362e6acdff8a706bcc994349e83af3c968db(
    value: Effect,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30ce2fa4ca8c0a1380260d20859de828af206679d35e2522d1d87820070572c1(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6398a73f5c1fa66544eaacc0b385f398deb11198b0409323b4a2ac9bbd50bbec(
    *,
    actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    effect: typing.Optional[Effect] = None,
    not_actions: typing.Optional[typing.Sequence[builtins.str]] = None,
    not_principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
    not_resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    principals: typing.Optional[typing.Sequence[IPrincipal]] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    sid: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4dfdfaf4a8557ed0cdbcfc5a5eb7ba633d0e36aa0d72292279006f4d8d9136b4(
    principal_json: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c149e46fe10c4eb704222ab3e79527beda947d4a2270860533c2ccb61ee1c0da(
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_Duration_070aa057] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da567a775537491ac75c3385e477ac8fe0ede0cfbde8a376c82e637de0d993da(
    path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d31368d32d9224f7bc9126566b7baddeb27bdd48513bd89fc04dab0c1300927f(
    xml: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__864508c4669028fd7e3c06733b9b5ce02d2308457848993e6cce89d91634b9a2(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    metadata_document: SamlMetadataDocument,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__82548cb57afec0eaf176df75ed6892b9133960fb6ac19cb9344c6e52cd04a488(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    saml_provider_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d0cddf4acd86a0cac8503cb45d0f9c64bbfda87865d17fad11a3a20561cc571(
    *,
    metadata_document: SamlMetadataDocument,
    name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__581a7da6857e4f36f15e3c5fc909349991557d9fa3f94b6219153dfa7db7a80d(
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c171271638560e474bb6457862deb486d25007ad0b1c2f70f4f2344d07008279(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff07c7242537ab918ada0c6526a010028e02485214d5425b760fa30baa8b56b7(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e5d735bd94d763b95b269f67d9036fb16090725d38b77920844a2a62ea9156da(
    *,
    resource: _constructs_77d1e7e8.IConstruct,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c85d294e09e4ae543d25a57c9415a2268820e8445bc6f61658f201fa86f0ed0(
    *,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__08b575100a7ce017470e9390aad6bfab83dc8c5d77f17b823020bd4d51f621d1(
    *,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    password: typing.Optional[_SecretValue_c18506ef] = None,
    password_reset_required: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bd849220168d4299a9c0514b8702a859ef436a369e5ccfecea319856f95c140a(
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35f4e25dd90a0166dddfb93b56c4925b9c0c95c5f5cdf961521f068f69a588f8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user: IUser,
    serial: typing.Optional[jsii.Number] = None,
    status: typing.Optional[AccessKeyStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6dbf71f98677bf20cf72272f274a21831b1b888c5315820d292eae2eeed7c1d3(
    document: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__add78e4a012ac5a260e7e9782d2f6e755add0b5c33ba64238feb0256ef4bcd98(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8244486e506664384e2b08ea4eb8b1b4bf1d90fb2a0a3136b08e48cf6234b430(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bcc1543d3ef692b780cef712ecc2c8064195db4578f509ffbd40d266514159d3(
    grantee: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbc3971c4569a7d573d4926686b751414db60dfae9950adb818218f774d6f3da(
    grantee: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdf670b10089d7aea62be6948d8dc376dbdedbbac5c9cfe8a6191d770942a446(
    grantee: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e92203682cd1883c076086b5e61a8c04fe1534c212bf91a28d660ba43f30c9fc(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e03b8360b0f91b923f85c677c80e60e38c1be627f4f0572496720d0d6c8ffeb(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_Duration_070aa057] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f82147871c003ca3af37d433e1df2c3fab1edaaa565940469a02f59fffaf7979(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb488592708dcaf06c69158b1e6a00e4d1d544c27f056d1f524be01afb248bc2(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__570166d9fafcc05052ccdbb1f037c62725e64382a87f3bfa34372d525bc0af5c(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97ffcbc478353b2fad6a52151d35d1248d0cb1079275b8390738499f67d36ffb(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbb2fadd9e0a60e5d9a7b6dd4e0dc493db1403c88308c3617ce971474beafe92(
    identity: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c22fe70395f166dafe3685a23d397f1f248d2d4c601811b3b9fd8ac71e9c1d5(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d72fdc6abc447f62e0aa20b4a63c39cbab640d58abacb18ece2bd496d371006(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35206d4b64a96a6e4cae952d5a347b4ce64f8cc3b3cff47a5eea0905047e23f5(
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_Duration_070aa057] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8e077464030e496b0ecaf34e9a4377c6240462f7e7a566e0f26ca423c0cfa2cc(
    document: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6e92bd111395b981b850c0e359a23e0febc94c0b6f1b91dd7167ccd3748df4b(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb0e5831d6c7e3f862e8edea8ec808dffd29df9c3ce1891c23efcde5ff1f0a8b(
    _statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12e58dd8fcf40965f7a1d7f10fccbc9ae1532d45a12c3ddc59da2f0c5be2b2f2(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__907a939090db89995a634ed440ca4844c184f565312f829f90e20647b8cdea46(
    principal: IPrincipal,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d0ab7befbf9ce0e652b11615524ad9d0cf84a9c98a56c94a74718b2ad667f135(
    key: builtins.str,
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8144bc8222b46ef67f74a9f7de481be58fb4aa8afc00202f97b645b8ab8685e(
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa22b07b42fefa67222d548e28b71eca4a1553f90677315ad98ae91584f7e172(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__69986f0f604db3130d3901d5f966f67189b394a9c6eb300f1b060d0d4c5c9f0a(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dfed0f6c9d2d923edc4752aff66321c6f9e28fe508f08c60acd229904819a1cf(
    append: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__32f33d3f9b8835fa27b2cbfa9ec4de4220d331f9dad55dd7093e77c01a5fc9e1(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    assumed_by: IPrincipal,
    description: typing.Optional[builtins.str] = None,
    external_id: typing.Optional[builtins.str] = None,
    external_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    inline_policies: typing.Optional[typing.Mapping[builtins.str, PolicyDocument]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    max_session_duration: typing.Optional[_Duration_070aa057] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    role_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f50ec63b16b80cf0582ff7e8a9c895736dcf4fbb49af60acd6fa04c04759362d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_arn: builtins.str,
    *,
    add_grants_to_resources: typing.Optional[builtins.bool] = None,
    mutable: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__652b63d9f8c86e7f9d2a8f4410c7cdeb4ac480af0128f0f966c91748bc60347a(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    role_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__85daa53a67caf97805a1f126f6b883848bc7c8830183eb0cf8132df12421c96f(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fa16f9f99e97b6e3da5469a59e06d330caa48a0a0cec2685712db2928b13e84(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__417e4df00b877dd56a8895ef2ff3b14dc7d092bea4be368e6f57f4e8682184b3(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__702e0f53acb2af0aede54f824bccbd41ccc5836fbd6a3bac737323542229b1c1(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97d44787a8d68ebc0e17c435680d5d2770ad7622e36f192e02281269a7281d28(
    grantee: IPrincipal,
    *actions: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd4bad4aac5266006daa976287b18f959f658269e4fdfa91c45c4fd82e3c0a49(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8421288fe8a40d213cb5384a789755121e56e1a93ea8c645848cf87fa519f57d(
    identity: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__592c5610dbe0789759022de7d57483b42e60153345097fdbeda1ab7914d0c122(
    service: builtins.str,
    *,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e1ae3127ae5aeafcb4b0fcf3059ff1b3042e514f1aa28b3d02a9d2c2f549333(
    service: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38690d13b9084bf44e851d32958e11efa278673502b2c7745c1f09f3876df807(
    principal: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9658287d4a9daeee3f6c0d3f57370d6d65b7b40113e35d565eae8388c8201e62(
    doc: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ad180a531b77f4378fda874ad2ae26abb325d0700cc32bb0a996160b36d7385c(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fb50acd2019a9721cb4823417e973fd189466606ee7d2eecf695d0f9afbaaac9(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68e87721f0c6a230150fcce5a9d9700c625618a64120094c3ef554483e8dc3fa(
    append: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5dee86759655ab923761104bb56d1f12ad4c0731ea241ffeb50c2e470d880b3c(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    groups: typing.Optional[typing.Sequence[IGroup]] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    password: typing.Optional[_SecretValue_c18506ef] = None,
    password_reset_required: typing.Optional[builtins.bool] = None,
    path: typing.Optional[builtins.str] = None,
    permissions_boundary: typing.Optional[IManagedPolicy] = None,
    user_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10bf3e67c76d3acf460c81230bcf47453a39505ca992f234397150d11814e478(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1556269e381e138692f70c0dd6bce45d226899c04e136cbae5311d26b3375ba6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    user_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d3d05881f527ce602c738f7cc6350d8fee2015ef6826bfeac6b56fca236506d(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    user_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18a4f92ef80e58f9cc6695e5df3e03d8c9fdb2f452f9cbfb2250274c34d9bae4(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc84fade0de8b90894d4708df23e756d8cb2e74657b1878ca14d49e15c41ce66(
    group: IGroup,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bec12b2fa2a30f72af5d5c42bff5eee0b1e8a39481c5c3eb09ae060b8569d9a4(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__930760e685c2d057d6a9ee89c4adb0113503799945533a20ba9789e405bdb556(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e174a7ffee8820ea7e207febcc8b419df11ae0ba30f342f6dc6269543d9625b(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dbf90d8cafb8f0b630efbe073236f22413b280fa54f11d870715730622499b97(
    arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2818679fa41b811c914f2ca591255bfdb457f05e9fd4e083d4ec5b5c2b588ac8(
    organization_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b731f56519babd91d826dc8dbcfcc1814a537e1bdc7fe8b600a5fd292661cecf(
    canonical_user_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__047315fec9a3d924fa7b11c3178d502037b3569ccba735b91ef02f8a1b4f053c(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ccf36a015b5d38719a0881891ec44c3a7a2c8040e1fd4662e01e2b1648f1562(
    *principals: IPrincipal,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b0db1f06ffb47fe72ad98ce9d4defc17ace56c2c223afcea989b2e35f28b9c(
    doc: PolicyDocument,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67bbf4c25c041bc2f89f5c5d7dec5b718973c5000f6c0803f89a4ac34a03e1a(
    federated: builtins.str,
    conditions: typing.Mapping[builtins.str, typing.Any],
    assume_role_action: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__58df4c9802f623fc2c52ce35a7ac517c5a5a27c19f402bac97c1752438af3319(
    organization_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24b7c3d44e12e24b06cf1c138cecfd5c2e0c69d472500d13859975460666e935(
    saml_provider: ISamlProvider,
    conditions: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5f1b67266317d4890fa969cd5148e820db2a47a79eebd553f240a319b40b5701(
    identity_provider: builtins.str,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13ba0f59001ad809f7eaa618802f41bd1b3c589ccc4c38817645572420f3a7cf(
    account_id: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__700efe0d66285b17214ae296baf6ef2aa4fc27fb0633c58e87ab8d0748ba63d8(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    group_name: typing.Optional[builtins.str] = None,
    managed_policies: typing.Optional[typing.Sequence[IManagedPolicy]] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2aa81f20c8515398c4324df8298cb489ab5ede846a4d9a8d1f2d835e81a7c371(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bc59992dfdbc023bba8cdd068b8b3f818a5df6d2b6a1955e88d9f675c81eba(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    group_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6041eeb96684d237ffa6143289acc7c061fe775fcc98b1bf2a1cc1a3383363ad(
    policy: IManagedPolicy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9e362c4ea76fb3b5b4980b0b8f40c1d2aa3a51baffa918dd6cf0367ff8ab6bb(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db8f0815713df243685119bc70a363aa602e95f1ddb9db93d4b9dcbd1d91e3de(
    statement: PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2fb2a1dc663863ae3309eef8b61e61678818ba17e23f7b6ca697f311d6ffdda4(
    user: IUser,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__30d0aa908c57c5c50269e9cf04d8c0e818286fb53234b6b96c7234257c2c6076(
    policy: Policy,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a74d9838aaabd9c97bb3d9113dd4fb3247c08d3cf3b7e9356475657e698db9f(
    open_id_connect_provider: IOpenIdConnectProvider,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__786d01dc3c981565ec1dac3a15c0dce0451583bf0ac3fa6a47e2deddf45dc040(
    saml_provider: ISamlProvider,
    conditions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
) -> None:
    """Type checking stubs"""
    pass
