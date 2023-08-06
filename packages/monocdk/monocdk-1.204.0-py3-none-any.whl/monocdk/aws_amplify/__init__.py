'''
# AWS Amplify Construct Library

The AWS Amplify Console provides a Git-based workflow for deploying and hosting fullstack serverless web applications. A fullstack serverless app consists of a backend built with cloud resources such as GraphQL or REST APIs, file and data storage, and a frontend built with single page application frameworks such as React, Angular, Vue, or Gatsby.

## Setting up an app with branches, custom rules and a domain

To set up an Amplify Console app, define an `App`:

```python
import monocdk as codebuild


amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    build_spec=codebuild.BuildSpec.from_object_to_yaml({
        # Alternatively add a `amplify.yml` to the repo
        "version": "1.0",
        "frontend": {
            "phases": {
                "pre_build": {
                    "commands": ["yarn"
                    ]
                },
                "build": {
                    "commands": ["yarn build"
                    ]
                }
            },
            "artifacts": {
                "base_directory": "public",
                "files": -"**/*"
            }
        }
    })
)
```

To connect your `App` to GitLab, use the `GitLabSourceCodeProvider`:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitLabSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-gitlab-token")
    )
)
```

To connect your `App` to CodeCommit, use the `CodeCommitSourceCodeProvider`:

```python
import monocdk as codecommit


repository = codecommit.Repository(self, "Repo",
    repository_name="my-repo"
)

amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
)
```

The IAM role associated with the `App` will automatically be granted the permission
to pull the CodeCommit repository.

Add branches:

```python
# amplify_app: amplify.App


master = amplify_app.add_branch("master") # `id` will be used as repo branch name
dev = amplify_app.add_branch("dev",
    performance_mode=True
)
dev.add_environment("STAGE", "dev")
```

Auto build and pull request preview are enabled by default.

Add custom rules for redirection:

```python
# amplify_app: amplify.App

amplify_app.add_custom_rule({
    "source": "/docs/specific-filename.html",
    "target": "/documents/different-filename.html",
    "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
})
```

When working with a single page application (SPA), use the
`CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT` to set up a 200
rewrite for all files to `index.html` except for the following
file extensions: css, gif, ico, jpg, js, png, txt, svg, woff,
ttf, map, json, webmanifest.

```python
# my_single_page_app: amplify.App


my_single_page_app.add_custom_rule(amplify.CustomRule.SINGLE_PAGE_APPLICATION_REDIRECT)
```

Add a domain and map sub domains to branches:

```python
# amplify_app: amplify.App
# master: amplify.Branch
# dev: amplify.Branch


domain = amplify_app.add_domain("example.com",
    enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
    auto_subdomain_creation_patterns=["*", "pr*"]
)
domain.map_root(master) # map master branch to domain root
domain.map_sub_domain(master, "www")
domain.map_sub_domain(dev)
```

## Restricting access

Password protect the app with basic auth by specifying the `basicAuth` prop.

Use `BasicAuth.fromCredentials` when referencing an existing secret:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_credentials("username", SecretValue.secrets_manager("my-github-token"))
)
```

Use `BasicAuth.fromGeneratedPassword` to generate a password in Secrets Manager:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

Basic auth can be added to specific branches:

```python
# amplify_app: amplify.App

amplify_app.add_branch("feature/next",
    basic_auth=amplify.BasicAuth.from_generated_password("username")
)
```

## Automatically creating and deleting branches

Use the `autoBranchCreation` and `autoBranchDeletion` props to control creation/deletion
of branches:

```python
amplify_app = amplify.App(self, "MyApp",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
        patterns=["feature/*", "test/*"]),
    auto_branch_deletion=True
)
```

## Adding custom response headers

Use the `customResponseHeaders` prop to configure custom response headers for an Amplify app:

```python
amplify_app = amplify.App(self, "App",
    source_code_provider=amplify.GitHubSourceCodeProvider(
        owner="<user>",
        repository="<repo>",
        oauth_token=SecretValue.secrets_manager("my-github-token")
    ),
    custom_response_headers=[amplify.aws_amplify.CustomResponseHeader(
        pattern="*.json",
        headers={
            "custom-header-name-1": "custom-header-value-1",
            "custom-header-name-2": "custom-header-value-2"
        }
    ), amplify.aws_amplify.CustomResponseHeader(
        pattern="/path/*",
        headers={
            "custom-header-name-1": "custom-header-value-2"
        }
    )
    ]
)
```

## Deploying Assets

`sourceCodeProvider` is optional; when this is not specified the Amplify app can be deployed to using `.zip` packages. The `asset` property can be used to deploy S3 assets to Amplify as part of the CDK:

```python
import monocdk as assets

# asset: assets.Asset
# amplify_app: amplify.App

branch = amplify_app.add_branch("dev", asset=asset)
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
    IInspectable as _IInspectable_82c04a63,
    IResolvable as _IResolvable_a771d0ef,
    IResource as _IResource_8c1dbbbd,
    Resource as _Resource_abff4495,
    SecretValue as _SecretValue_c18506ef,
    TagManager as _TagManager_0b7ab120,
    TreeInspector as _TreeInspector_1cd1894e,
)
from ..aws_codebuild import BuildSpec as _BuildSpec_1d70c5a1
from ..aws_codecommit import IRepository as _IRepository_cdb2a3c0
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_s3_assets import Asset as _Asset_d07e8c00


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.AppProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_name": "appName",
        "auto_branch_creation": "autoBranchCreation",
        "auto_branch_deletion": "autoBranchDeletion",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "custom_response_headers": "customResponseHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "environment_variables": "environmentVariables",
        "role": "role",
        "source_code_provider": "sourceCodeProvider",
    },
)
class AppProps:
    def __init__(
        self,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union["AutoBranchCreation", typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union["CustomResponseHeader", typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence["CustomRule"]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        source_code_provider: typing.Optional["ISourceCodeProvider"] = None,
    ) -> None:
        '''(experimental) Properties for an App.

        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if isinstance(auto_branch_creation, dict):
            auto_branch_creation = AutoBranchCreation(**auto_branch_creation)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__51b008d8c501a3fb80936a4402973c0ed701b2981e76314db3652ff2fa00f16f)
            check_type(argname="argument app_name", value=app_name, expected_type=type_hints["app_name"])
            check_type(argname="argument auto_branch_creation", value=auto_branch_creation, expected_type=type_hints["auto_branch_creation"])
            check_type(argname="argument auto_branch_deletion", value=auto_branch_deletion, expected_type=type_hints["auto_branch_deletion"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument custom_response_headers", value=custom_response_headers, expected_type=type_hints["custom_response_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument source_code_provider", value=source_code_provider, expected_type=type_hints["source_code_provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if app_name is not None:
            self._values["app_name"] = app_name
        if auto_branch_creation is not None:
            self._values["auto_branch_creation"] = auto_branch_creation
        if auto_branch_deletion is not None:
            self._values["auto_branch_deletion"] = auto_branch_deletion
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if custom_response_headers is not None:
            self._values["custom_response_headers"] = custom_response_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if role is not None:
            self._values["role"] = role
        if source_code_provider is not None:
            self._values["source_code_provider"] = source_code_provider

    @builtins.property
    def app_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name for the application.

        :default: - a CDK generated name

        :stability: experimental
        '''
        result = self._values.get("app_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation(self) -> typing.Optional["AutoBranchCreation"]:
        '''(experimental) The auto branch creation configuration.

        Use this to automatically create
        branches that match a certain pattern.

        :default: - no auto branch creation

        :stability: experimental
        '''
        result = self._values.get("auto_branch_creation")
        return typing.cast(typing.Optional["AutoBranchCreation"], result)

    @builtins.property
    def auto_branch_deletion(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("auto_branch_deletion")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection at an
        app level to all your branches.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) BuildSpec for the application.

        Alternatively, add a ``amplify.yml``
        file to the repository.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def custom_response_headers(
        self,
    ) -> typing.Optional[typing.List["CustomResponseHeader"]]:
        '''(experimental) The custom HTTP response headers for an Amplify app.

        :default: - no custom response headers

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/custom-headers.html
        :stability: experimental
        '''
        result = self._values.get("custom_response_headers")
        return typing.cast(typing.Optional[typing.List["CustomResponseHeader"]], result)

    @builtins.property
    def custom_rules(self) -> typing.Optional[typing.List["CustomRule"]]:
        '''(experimental) Custom rewrite/redirect rules for the application.

        :default: - no custom rewrite/redirect rules

        :stability: experimental
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.List["CustomRule"]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the application.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - no environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM service role to associate with the application.

        The App
        implements IGrantable.

        :default: - a new role is created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def source_code_provider(self) -> typing.Optional["ISourceCodeProvider"]:
        '''(experimental) The source code provider for this application.

        :default: - not connected to a source code provider

        :stability: experimental
        '''
        result = self._values.get("source_code_provider")
        return typing.cast(typing.Optional["ISourceCodeProvider"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.AutoBranchCreation",
    jsii_struct_bases=[],
    name_mapping={
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "build_spec": "buildSpec",
        "environment_variables": "environmentVariables",
        "patterns": "patterns",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class AutoBranchCreation:
    def __init__(
        self,
        *,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional["BasicAuth"] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Auto branch creation configuration.

        :param auto_build: (experimental) Whether to enable auto building for the auto created branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the auto created branch. Default: - no password protection
        :param build_spec: (experimental) Build spec for the auto created branch. Default: - application build spec
        :param environment_variables: (experimental) Environment variables for the auto created branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param patterns: (experimental) Automated branch creation glob patterns. Default: - all repository branches
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews of the auto created branch. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the auto created branch. Default: true
        :param stage: (experimental) Stage for the auto created branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50ee861bf2b9208b9ce76bd1b3369c220c0503dac241a80278efe14a39c03ff7)
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument patterns", value=patterns, expected_type=type_hints["patterns"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if patterns is not None:
            self._values["patterns"] = patterns
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional["BasicAuth"]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the auto created branch.

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional["BasicAuth"], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) Build spec for the auto created branch.

        :default: - application build spec

        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def patterns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Automated branch creation glob patterns.

        :default: - all repository branches

        :stability: experimental
        '''
        result = self._values.get("patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews of the auto created branch.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the auto created branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the auto created branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AutoBranchCreation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class BasicAuth(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_amplify.BasicAuth"):
    '''(experimental) Basic Auth configuration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            basic_auth=amplify.BasicAuth.from_generated_password("username")
        )
    '''

    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        password: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''
        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        '''
        props = BasicAuthProps(
            username=username, encryption_key=encryption_key, password=password
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromCredentials")
    @builtins.classmethod
    def from_credentials(
        cls,
        username: builtins.str,
        password: _SecretValue_c18506ef,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration from a username and a password.

        :param username: The username.
        :param password: The password.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d98c9cf1ee25f79a9d30372ae0c3b4216c527fc9f2c585794b4ec0d11d14e6fd)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromCredentials", [username, password]))

    @jsii.member(jsii_name="fromGeneratedPassword")
    @builtins.classmethod
    def from_generated_password(
        cls,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
    ) -> "BasicAuth":
        '''(experimental) Creates a Basic Auth configuration with a password generated in Secrets Manager.

        :param username: The username.
        :param encryption_key: The encryption key to use to encrypt the password in Secrets Manager.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__619987267cc501f89370ec9cb33aacd01f36ac840fbc9a620eb14ba01b49a1af)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
        return typing.cast("BasicAuth", jsii.sinvoke(cls, "fromGeneratedPassword", [username, encryption_key]))

    @jsii.member(jsii_name="bind")
    def bind(self, scope: _Construct_e78e779f, id: builtins.str) -> "BasicAuthConfig":
        '''(experimental) Binds this Basic Auth configuration to an App.

        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38d36803115a5e2a9321b8f72998709dd5f0f7492a6fe1aa489b787b54a367f5)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        return typing.cast("BasicAuthConfig", jsii.invoke(self, "bind", [scope, id]))


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.BasicAuthConfig",
    jsii_struct_bases=[],
    name_mapping={
        "enable_basic_auth": "enableBasicAuth",
        "password": "password",
        "username": "username",
    },
)
class BasicAuthConfig:
    def __init__(
        self,
        *,
        enable_basic_auth: builtins.bool,
        password: builtins.str,
        username: builtins.str,
    ) -> None:
        '''(experimental) A Basic Auth configuration.

        :param enable_basic_auth: (experimental) Whether to enable Basic Auth.
        :param password: (experimental) The password.
        :param username: (experimental) The username.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            basic_auth_config = amplify.BasicAuthConfig(
                enable_basic_auth=False,
                password="password",
                username="username"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9d84e31c133918c5cf9278a488870b2f4ad9803b05caceee2773dc6cbbbcd93d)
            check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "enable_basic_auth": enable_basic_auth,
            "password": password,
            "username": username,
        }

    @builtins.property
    def enable_basic_auth(self) -> builtins.bool:
        '''(experimental) Whether to enable Basic Auth.

        :stability: experimental
        '''
        result = self._values.get("enable_basic_auth")
        assert result is not None, "Required property 'enable_basic_auth' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def password(self) -> builtins.str:
        '''(experimental) The password.

        :stability: experimental
        '''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.BasicAuthProps",
    jsii_struct_bases=[],
    name_mapping={
        "username": "username",
        "encryption_key": "encryptionKey",
        "password": "password",
    },
)
class BasicAuthProps:
    def __init__(
        self,
        *,
        username: builtins.str,
        encryption_key: typing.Optional[_IKey_36930160] = None,
        password: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''(experimental) Properties for a BasicAuth.

        :param username: (experimental) The username.
        :param encryption_key: (experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager. Default: - default master key
        :param password: (experimental) The password. Default: - A Secrets Manager generated password

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_amplify as amplify
            from monocdk import aws_kms as kms
            
            # key: kms.Key
            # secret_value: monocdk.SecretValue
            
            basic_auth_props = amplify.BasicAuthProps(
                username="username",
            
                # the properties below are optional
                encryption_key=key,
                password=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ec3ec350e2d049489cf569ac3bd615bed42401899f72f21e263529d58f7f30e)
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            check_type(argname="argument encryption_key", value=encryption_key, expected_type=type_hints["encryption_key"])
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "username": username,
        }
        if encryption_key is not None:
            self._values["encryption_key"] = encryption_key
        if password is not None:
            self._values["password"] = password

    @builtins.property
    def username(self) -> builtins.str:
        '''(experimental) The username.

        :stability: experimental
        '''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def encryption_key(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The encryption key to use to encrypt the password when it's generated in Secrets Manager.

        :default: - default master key

        :stability: experimental
        '''
        result = self._values.get("encryption_key")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def password(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) The password.

        :default: - A Secrets Manager generated password

        :stability: experimental
        '''
        result = self._values.get("password")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BasicAuthProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.BranchOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
    },
)
class BranchOptions:
    def __init__(
        self,
        *,
        asset: typing.Optional[_Asset_d07e8c00] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options to add a branch to an application.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # amplify_app: amplify.App
            
            
            master = amplify_app.add_branch("master") # `id` will be used as repo branch name
            dev = amplify_app.add_branch("dev",
                performance_mode=True
            )
            dev.add_environment("STAGE", "dev")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9f17bd266f6ab219e1769ee96b2c0f1aac33cae5337b7fd876126790cde69bc)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_Asset_d07e8c00]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_Asset_d07e8c00], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.BranchProps",
    jsii_struct_bases=[BranchOptions],
    name_mapping={
        "asset": "asset",
        "auto_build": "autoBuild",
        "basic_auth": "basicAuth",
        "branch_name": "branchName",
        "build_spec": "buildSpec",
        "description": "description",
        "environment_variables": "environmentVariables",
        "performance_mode": "performanceMode",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "pull_request_preview": "pullRequestPreview",
        "stage": "stage",
        "app": "app",
    },
)
class BranchProps(BranchOptions):
    def __init__(
        self,
        *,
        asset: typing.Optional[_Asset_d07e8c00] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
        app: "IApp",
    ) -> None:
        '''(experimental) Properties for a Branch.

        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage
        :param app: (experimental) The application within which the branch must be created.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_s3_assets as s3_assets
            
            # app: amplify.App
            # asset: s3_assets.Asset
            # basic_auth: amplify.BasicAuth
            # build_spec: codebuild.BuildSpec
            
            branch_props = amplify.BranchProps(
                app=app,
            
                # the properties below are optional
                asset=asset,
                auto_build=False,
                basic_auth=basic_auth,
                branch_name="branchName",
                build_spec=build_spec,
                description="description",
                environment_variables={
                    "environment_variables_key": "environmentVariables"
                },
                performance_mode=False,
                pull_request_environment_name="pullRequestEnvironmentName",
                pull_request_preview=False,
                stage="stage"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c64a504c40cc03256dce78384fbff64892846aa9a6f87230706679585a33e024)
            check_type(argname="argument asset", value=asset, expected_type=type_hints["asset"])
            check_type(argname="argument auto_build", value=auto_build, expected_type=type_hints["auto_build"])
            check_type(argname="argument basic_auth", value=basic_auth, expected_type=type_hints["basic_auth"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument performance_mode", value=performance_mode, expected_type=type_hints["performance_mode"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument pull_request_preview", value=pull_request_preview, expected_type=type_hints["pull_request_preview"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if asset is not None:
            self._values["asset"] = asset
        if auto_build is not None:
            self._values["auto_build"] = auto_build
        if basic_auth is not None:
            self._values["basic_auth"] = basic_auth
        if branch_name is not None:
            self._values["branch_name"] = branch_name
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if performance_mode is not None:
            self._values["performance_mode"] = performance_mode
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if pull_request_preview is not None:
            self._values["pull_request_preview"] = pull_request_preview
        if stage is not None:
            self._values["stage"] = stage

    @builtins.property
    def asset(self) -> typing.Optional[_Asset_d07e8c00]:
        '''(experimental) Asset for deployment.

        The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's
        startDeployment API to initiate and deploy a S3 asset onto the App.

        :default: - no asset

        :stability: experimental
        '''
        result = self._values.get("asset")
        return typing.cast(typing.Optional[_Asset_d07e8c00], result)

    @builtins.property
    def auto_build(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable auto building for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("auto_build")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def basic_auth(self) -> typing.Optional[BasicAuth]:
        '''(experimental) The Basic Auth configuration.

        Use this to set password protection for
        the branch

        :default: - no password protection

        :stability: experimental
        '''
        result = self._values.get("basic_auth")
        return typing.cast(typing.Optional[BasicAuth], result)

    @builtins.property
    def branch_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the branch.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("branch_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) BuildSpec for the branch.

        :default: - no build spec

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/build-settings.html
        :stability: experimental
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description for the branch.

        :default: - no description

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables for the branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :default: - application environment variables

        :stability: experimental
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def performance_mode(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge
        for a longer interval. When performance mode is enabled, hosting configuration or code changes
        can take up to 10 minutes to roll out.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("performance_mode")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The dedicated backend environment for the pull request previews.

        :default: - automatically provision a temporary backend

        :stability: experimental
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_preview(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable pull request preview for the branch.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("pull_request_preview")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage for the branch.

        :default: - no stage

        :stability: experimental
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application within which the branch must be created.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnApp(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.CfnApp",
):
    '''A CloudFormation ``AWS::Amplify::App``.

    The AWS::Amplify::App resource specifies Apps in Amplify Hosting. An App is a collection of branches.

    :cloudformationResource: AWS::Amplify::App
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplify as amplify
        
        cfn_app = amplify.CfnApp(self, "MyCfnApp",
            name="name",
        
            # the properties below are optional
            access_token="accessToken",
            auto_branch_creation_config=amplify.CfnApp.AutoBranchCreationConfigProperty(
                auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                enable_auto_branch_creation=False,
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage"
            ),
            basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                enable_basic_auth=False,
                password="password",
                username="username"
            ),
            build_spec="buildSpec",
            custom_headers="customHeaders",
            custom_rules=[amplify.CfnApp.CustomRuleProperty(
                source="source",
                target="target",
        
                # the properties below are optional
                condition="condition",
                status="status"
            )],
            description="description",
            enable_branch_auto_deletion=False,
            environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            iam_service_role="iamServiceRole",
            oauth_token="oauthToken",
            platform="platform",
            repository="repository",
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
        name: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        auto_branch_creation_config: typing.Optional[typing.Union[typing.Union["CfnApp.AutoBranchCreationConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        basic_auth_config: typing.Optional[typing.Union[typing.Union["CfnApp.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_headers: typing.Optional[builtins.str] = None,
        custom_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnApp.CustomRuleProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnApp.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        iam_service_role: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::App``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The name for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param access_token: The personal access token for a GitHub repository for an Amplify app. The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored. Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` . You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Minimum length of 1. Maximum length of 255.
        :param auto_branch_creation_config: Sets the configuration for your automatic branch creation.
        :param basic_auth_config: The credentials for basic authorization for an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param custom_headers: The custom HTTP headers for an Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 25000. *Pattern:* (?s).*
        :param custom_rules: The custom rewrite and redirect rules for an Amplify app.
        :param description: The description for an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_branch_auto_deletion: Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        :param environment_variables: The environment variables map for an Amplify app.
        :param iam_service_role: The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 1000. *Pattern:* (?s).*
        :param oauth_token: The OAuth token for a third-party source control system for an Amplify app. The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored. Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` . You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param platform: The platform for the Amplify app. For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .
        :param repository: The repository for an Amplify app. *Pattern:* (?s).*
        :param tags: The tag for an Amplify app.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__434fc35643e44a8d85c957c4bafa2785507f2009420463b5ec659229ca499e66)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAppProps(
            name=name,
            access_token=access_token,
            auto_branch_creation_config=auto_branch_creation_config,
            basic_auth_config=basic_auth_config,
            build_spec=build_spec,
            custom_headers=custom_headers,
            custom_rules=custom_rules,
            description=description,
            enable_branch_auto_deletion=enable_branch_auto_deletion,
            environment_variables=environment_variables,
            iam_service_role=iam_service_role,
            oauth_token=oauth_token,
            platform=platform,
            repository=repository,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c82756d0f09741bd83b20baa9923154dab15a410564b8be08b2c6dfc4f302375)
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
            type_hints = typing.get_type_hints(_typecheckingstub__59398f606cc7e89a28726621091ef7790dac5e234832474c9aa663e8a6c3dac0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrAppId")
    def attr_app_id(self) -> builtins.str:
        '''Unique Id for the Amplify App.

        :cloudformationAttribute: AppId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppId"))

    @builtins.property
    @jsii.member(jsii_name="attrAppName")
    def attr_app_name(self) -> builtins.str:
        '''Name for the Amplify App.

        :cloudformationAttribute: AppName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAppName"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''ARN for the Amplify App.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrDefaultDomain")
    def attr_default_domain(self) -> builtins.str:
        '''Default domain for the Amplify App.

        :cloudformationAttribute: DefaultDomain
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDefaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The name for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c59a9ec217b574b2095ac58a6cfed31b053c9c541342c6a7643f3d6daa17c5bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="accessToken")
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The personal access token for a GitHub repository for an Amplify app.

        The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored.

        Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` .

        You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "accessToken"))

    @access_token.setter
    def access_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__692e591f5e2e535a63be678f88cd1deb7dd4c35afcfb718f5275846cb90bdbc3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "accessToken", value)

    @builtins.property
    @jsii.member(jsii_name="autoBranchCreationConfig")
    def auto_branch_creation_config(
        self,
    ) -> typing.Optional[typing.Union["CfnApp.AutoBranchCreationConfigProperty", _IResolvable_a771d0ef]]:
        '''Sets the configuration for your automatic branch creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApp.AutoBranchCreationConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "autoBranchCreationConfig"))

    @auto_branch_creation_config.setter
    def auto_branch_creation_config(
        self,
        value: typing.Optional[typing.Union["CfnApp.AutoBranchCreationConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a92a2bd547aac90f83a4587ce5eafbe912b92ea07a0a49813b097b5e95f3ce4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoBranchCreationConfig", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_a771d0ef]]:
        '''The credentials for basic authorization for an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "basicAuthConfig"))

    @basic_auth_config.setter
    def basic_auth_config(
        self,
        value: typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e25ec07f80855a4967ee3cbcbcec0c097ad31c6e2bfe3ad7a7262929757c862)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildSpec"))

    @build_spec.setter
    def build_spec(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0261626ea69802002557a4142765dd8322168847532d687be0d7a4bbd6d1ed)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="customHeaders")
    def custom_headers(self) -> typing.Optional[builtins.str]:
        '''The custom HTTP headers for an Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 25000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customheaders
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customHeaders"))

    @custom_headers.setter
    def custom_headers(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8fde630eeae83e612b0dfc05467cb7f166e847f3a310293b9ddf3f2b55b9a17)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customHeaders", value)

    @builtins.property
    @jsii.member(jsii_name="customRules")
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.CustomRuleProperty", _IResolvable_a771d0ef]]]]:
        '''The custom rewrite and redirect rules for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.CustomRuleProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "customRules"))

    @custom_rules.setter
    def custom_rules(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.CustomRuleProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d6ce472b3b90f105077ca01bb24681443b12b8d8451d2c3734345252cc997261)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customRules", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbf65fef26cbe8a191c92daf4fb6725a4b14f08e521356c143731f0e9d767879)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enableBranchAutoDeletion")
    def enable_branch_auto_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-enablebranchautodeletion
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableBranchAutoDeletion"))

    @enable_branch_auto_deletion.setter
    def enable_branch_auto_deletion(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac0b22f44e7c4d3e5445474298c096e5db88f3967e9f9f71ca93da018f26efe7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableBranchAutoDeletion", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]]:
        '''The environment variables map for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44c4106e24f4930d06000f76f6d6d60907376f3d63ffc3db17172178c3db0201)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="iamServiceRole")
    def iam_service_role(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "iamServiceRole"))

    @iam_service_role.setter
    def iam_service_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cfa683aabc670dad5c9fa8ffe806f5dcdddcd7303da329b3567f8060fc5eb95)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "iamServiceRole", value)

    @builtins.property
    @jsii.member(jsii_name="oauthToken")
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token for a third-party source control system for an Amplify app.

        The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored.

        Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` .

        You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "oauthToken"))

    @oauth_token.setter
    def oauth_token(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cdd0160536b19d3a6088423e69485bfd8487f659e34d72c8fe7c7bf5d71b4d2a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "oauthToken", value)

    @builtins.property
    @jsii.member(jsii_name="platform")
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform for the Amplify app.

        For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-platform
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "platform"))

    @platform.setter
    def platform(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9eb2bbe8a91f76aa244cc8128f4de636a20b85f9fc4d976b736d15f70e987c79)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "platform", value)

    @builtins.property
    @jsii.member(jsii_name="repository")
    def repository(self) -> typing.Optional[builtins.str]:
        '''The repository for an Amplify app.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "repository"))

    @repository.setter
    def repository(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__46796368cef5b63f54c91b076ace69732b6e4bd0d64d6649d355834a65e70295)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "repository", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnApp.AutoBranchCreationConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "auto_branch_creation_patterns": "autoBranchCreationPatterns",
            "basic_auth_config": "basicAuthConfig",
            "build_spec": "buildSpec",
            "enable_auto_branch_creation": "enableAutoBranchCreation",
            "enable_auto_build": "enableAutoBuild",
            "enable_performance_mode": "enablePerformanceMode",
            "enable_pull_request_preview": "enablePullRequestPreview",
            "environment_variables": "environmentVariables",
            "framework": "framework",
            "pull_request_environment_name": "pullRequestEnvironmentName",
            "stage": "stage",
        },
    )
    class AutoBranchCreationConfigProperty:
        def __init__(
            self,
            *,
            auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
            basic_auth_config: typing.Optional[typing.Union[typing.Union["CfnApp.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
            build_spec: typing.Optional[builtins.str] = None,
            enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnApp.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
            framework: typing.Optional[builtins.str] = None,
            pull_request_environment_name: typing.Optional[builtins.str] = None,
            stage: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the AutoBranchCreationConfig property type to automatically create branches that match a certain pattern.

            :param auto_branch_creation_patterns: Automated branch creation glob patterns for the Amplify app.
            :param basic_auth_config: Sets password protection for your auto created branch.
            :param build_spec: The build specification (build spec) for the autocreated branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000.
            :param enable_auto_branch_creation: Enables automated branch creation for the Amplify app.
            :param enable_auto_build: Enables auto building for the auto created branch.
            :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
            :param enable_pull_request_preview: Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app. Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
            :param environment_variables: Environment variables for the auto created branch.
            :param framework: The framework for the autocreated branch.
            :param pull_request_environment_name: If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
            :param stage: Stage for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                auto_branch_creation_config_property = amplify.CfnApp.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__aaf0f556530f782682e2bde081ea20fe9c58fa6cf27d97e7449987004e4d12a9)
                check_type(argname="argument auto_branch_creation_patterns", value=auto_branch_creation_patterns, expected_type=type_hints["auto_branch_creation_patterns"])
                check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
                check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
                check_type(argname="argument enable_auto_branch_creation", value=enable_auto_branch_creation, expected_type=type_hints["enable_auto_branch_creation"])
                check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
                check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
                check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
                check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
                check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
                check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
                check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if auto_branch_creation_patterns is not None:
                self._values["auto_branch_creation_patterns"] = auto_branch_creation_patterns
            if basic_auth_config is not None:
                self._values["basic_auth_config"] = basic_auth_config
            if build_spec is not None:
                self._values["build_spec"] = build_spec
            if enable_auto_branch_creation is not None:
                self._values["enable_auto_branch_creation"] = enable_auto_branch_creation
            if enable_auto_build is not None:
                self._values["enable_auto_build"] = enable_auto_build
            if enable_performance_mode is not None:
                self._values["enable_performance_mode"] = enable_performance_mode
            if enable_pull_request_preview is not None:
                self._values["enable_pull_request_preview"] = enable_pull_request_preview
            if environment_variables is not None:
                self._values["environment_variables"] = environment_variables
            if framework is not None:
                self._values["framework"] = framework
            if pull_request_environment_name is not None:
                self._values["pull_request_environment_name"] = pull_request_environment_name
            if stage is not None:
                self._values["stage"] = stage

        @builtins.property
        def auto_branch_creation_patterns(
            self,
        ) -> typing.Optional[typing.List[builtins.str]]:
            '''Automated branch creation glob patterns for the Amplify app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-autobranchcreationpatterns
            '''
            result = self._values.get("auto_branch_creation_patterns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def basic_auth_config(
            self,
        ) -> typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_a771d0ef]]:
            '''Sets password protection for your auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-basicauthconfig
            '''
            result = self._values.get("basic_auth_config")
            return typing.cast(typing.Optional[typing.Union["CfnApp.BasicAuthConfigProperty", _IResolvable_a771d0ef]], result)

        @builtins.property
        def build_spec(self) -> typing.Optional[builtins.str]:
            '''The build specification (build spec) for the autocreated branch.

            *Length Constraints:* Minimum length of 1. Maximum length of 25000.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-buildspec
            '''
            result = self._values.get("build_spec")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def enable_auto_branch_creation(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables automated branch creation for the Amplify app.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobranchcreation
            '''
            result = self._values.get("enable_auto_branch_creation")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enable_auto_build(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables auto building for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableautobuild
            '''
            result = self._values.get("enable_auto_build")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enable_performance_mode(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables performance mode for the branch.

            Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enableperformancemode
            '''
            result = self._values.get("enable_performance_mode")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def enable_pull_request_preview(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Sets whether pull request previews are enabled for each branch that Amplify Hosting automatically creates for your app.

            Amplify creates previews by deploying your app to a unique URL whenever a pull request is opened for the branch. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

            To provide backend support for your preview, Amplify Hosting automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

            For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-enablepullrequestpreview
            '''
            result = self._values.get("enable_pull_request_preview")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def environment_variables(
            self,
        ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]]:
            '''Environment variables for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-environmentvariables
            '''
            result = self._values.get("environment_variables")
            return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnApp.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]], result)

        @builtins.property
        def framework(self) -> typing.Optional[builtins.str]:
            '''The framework for the autocreated branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-framework
            '''
            result = self._values.get("framework")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
            '''If pull request previews are enabled, you can use this property to specify a dedicated backend environment for your previews.

            For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI.

            To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

            If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify deletes this environment when the pull request is closed.

            For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

            *Length Constraints:* Maximum length of 20.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-pullrequestenvironmentname
            '''
            result = self._values.get("pull_request_environment_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def stage(self) -> typing.Optional[builtins.str]:
            '''Stage for the auto created branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-autobranchcreationconfig.html#cfn-amplify-app-autobranchcreationconfig-stage
            '''
            result = self._values.get("stage")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "AutoBranchCreationConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnApp.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enable_basic_auth": "enableBasicAuth",
            "password": "password",
            "username": "username",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
            password: typing.Optional[builtins.str] = None,
            username: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection at an app level to all your branches.

            :param enable_basic_auth: Enables basic authorization for the Amplify app's branches.
            :param password: The password for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param username: The user name for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                basic_auth_config_property = amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a4cbb2215ee3d6015fb9cb431fc49fc69edc55b3cf1b0beed92596bea90cc849)
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth
            if password is not None:
                self._values["password"] = password
            if username is not None:
                self._values["username"] = username

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables basic authorization for the Amplify app's branches.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        @builtins.property
        def password(self) -> typing.Optional[builtins.str]:
            '''The password for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-password
            '''
            result = self._values.get("password")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def username(self) -> typing.Optional[builtins.str]:
            '''The user name for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-basicauthconfig.html#cfn-amplify-app-basicauthconfig-username
            '''
            result = self._values.get("username")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnApp.CustomRuleProperty",
        jsii_struct_bases=[],
        name_mapping={
            "source": "source",
            "target": "target",
            "condition": "condition",
            "status": "status",
        },
    )
    class CustomRuleProperty:
        def __init__(
            self,
            *,
            source: builtins.str,
            target: builtins.str,
            condition: typing.Optional[builtins.str] = None,
            status: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The CustomRule property type allows you to specify redirects, rewrites, and reverse proxies.

            Redirects enable a web app to reroute navigation from one URL to another.

            :param source: The source pattern for a URL rewrite or redirect rule. *Length Constraints:* Minimum length of 1. Maximum length of 2048. *Pattern:* (?s).+
            :param target: The target pattern for a URL rewrite or redirect rule. *Length Constraints:* Minimum length of 1. Maximum length of 2048. *Pattern:* (?s).+
            :param condition: The condition for a URL rewrite or redirect rule, such as a country code. *Length Constraints:* Minimum length of 0. Maximum length of 2048. *Pattern:* (?s).*
            :param status: The status code for a URL rewrite or redirect rule. - **200** - Represents a 200 rewrite rule. - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL. - **302** - Represents a 302 temporary redirect rule. - **404** - Represents a 404 redirect rule. - **404-200** - Represents a 404 rewrite rule. *Length Constraints:* Minimum length of 3. Maximum length of 7. *Pattern:* .{3,7}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                custom_rule_property = amplify.CfnApp.CustomRuleProperty(
                    source="source",
                    target="target",
                
                    # the properties below are optional
                    condition="condition",
                    status="status"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fd5f9ca5c14cac075735bfeef56cb13d07593bcca30ff5c4cc9212046d72bec2)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument target", value=target, expected_type=type_hints["target"])
                check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
                check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source": source,
                "target": target,
            }
            if condition is not None:
                self._values["condition"] = condition
            if status is not None:
                self._values["status"] = status

        @builtins.property
        def source(self) -> builtins.str:
            '''The source pattern for a URL rewrite or redirect rule.

            *Length Constraints:* Minimum length of 1. Maximum length of 2048.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def target(self) -> builtins.str:
            '''The target pattern for a URL rewrite or redirect rule.

            *Length Constraints:* Minimum length of 1. Maximum length of 2048.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-target
            '''
            result = self._values.get("target")
            assert result is not None, "Required property 'target' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def condition(self) -> typing.Optional[builtins.str]:
            '''The condition for a URL rewrite or redirect rule, such as a country code.

            *Length Constraints:* Minimum length of 0. Maximum length of 2048.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-condition
            '''
            result = self._values.get("condition")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def status(self) -> typing.Optional[builtins.str]:
            '''The status code for a URL rewrite or redirect rule.

            - **200** - Represents a 200 rewrite rule.
            - **301** - Represents a 301 (moved pemanently) redirect rule. This and all future requests should be directed to the target URL.
            - **302** - Represents a 302 temporary redirect rule.
            - **404** - Represents a 404 redirect rule.
            - **404-200** - Represents a 404 rewrite rule.

            *Length Constraints:* Minimum length of 3. Maximum length of 7.

            *Pattern:* .{3,7}

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-customrule.html#cfn-amplify-app-customrule-status
            '''
            result = self._values.get("status")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CustomRuleProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnApp.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''Environment variables are key-value pairs that are available at build time.

            Set environment variables for all branches in your app.

            :param name: The environment variable name. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*
            :param value: The environment variable value. *Length Constraints:* Maximum length of 5500. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                environment_variable_property = amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__a498db20f59b442a77ceb6978d5f464308a3c7cc049f066c2adadab83e92c702)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The environment variable name.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The environment variable value.

            *Length Constraints:* Maximum length of 5500.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-app-environmentvariable.html#cfn-amplify-app-environmentvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CfnAppProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "access_token": "accessToken",
        "auto_branch_creation_config": "autoBranchCreationConfig",
        "basic_auth_config": "basicAuthConfig",
        "build_spec": "buildSpec",
        "custom_headers": "customHeaders",
        "custom_rules": "customRules",
        "description": "description",
        "enable_branch_auto_deletion": "enableBranchAutoDeletion",
        "environment_variables": "environmentVariables",
        "iam_service_role": "iamServiceRole",
        "oauth_token": "oauthToken",
        "platform": "platform",
        "repository": "repository",
        "tags": "tags",
    },
)
class CfnAppProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        access_token: typing.Optional[builtins.str] = None,
        auto_branch_creation_config: typing.Optional[typing.Union[typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        custom_headers: typing.Optional[builtins.str] = None,
        custom_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        description: typing.Optional[builtins.str] = None,
        enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        iam_service_role: typing.Optional[builtins.str] = None,
        oauth_token: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnApp``.

        :param name: The name for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param access_token: The personal access token for a GitHub repository for an Amplify app. The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored. Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` . You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Minimum length of 1. Maximum length of 255.
        :param auto_branch_creation_config: Sets the configuration for your automatic branch creation.
        :param basic_auth_config: The credentials for basic authorization for an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param custom_headers: The custom HTTP headers for an Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 25000. *Pattern:* (?s).*
        :param custom_rules: The custom rewrite and redirect rules for an Amplify app.
        :param description: The description for an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_branch_auto_deletion: Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.
        :param environment_variables: The environment variables map for an Amplify app.
        :param iam_service_role: The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app. *Length Constraints:* Minimum length of 0. Maximum length of 1000. *Pattern:* (?s).*
        :param oauth_token: The OAuth token for a third-party source control system for an Amplify app. The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored. Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` . You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app. Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* . *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param platform: The platform for the Amplify app. For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .
        :param repository: The repository for an Amplify app. *Pattern:* (?s).*
        :param tags: The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            cfn_app_props = amplify.CfnAppProps(
                name="name",
            
                # the properties below are optional
                access_token="accessToken",
                auto_branch_creation_config=amplify.CfnApp.AutoBranchCreationConfigProperty(
                    auto_branch_creation_patterns=["autoBranchCreationPatterns"],
                    basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                        enable_basic_auth=False,
                        password="password",
                        username="username"
                    ),
                    build_spec="buildSpec",
                    enable_auto_branch_creation=False,
                    enable_auto_build=False,
                    enable_performance_mode=False,
                    enable_pull_request_preview=False,
                    environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                        name="name",
                        value="value"
                    )],
                    framework="framework",
                    pull_request_environment_name="pullRequestEnvironmentName",
                    stage="stage"
                ),
                basic_auth_config=amplify.CfnApp.BasicAuthConfigProperty(
                    enable_basic_auth=False,
                    password="password",
                    username="username"
                ),
                build_spec="buildSpec",
                custom_headers="customHeaders",
                custom_rules=[amplify.CfnApp.CustomRuleProperty(
                    source="source",
                    target="target",
            
                    # the properties below are optional
                    condition="condition",
                    status="status"
                )],
                description="description",
                enable_branch_auto_deletion=False,
                environment_variables=[amplify.CfnApp.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                iam_service_role="iamServiceRole",
                oauth_token="oauthToken",
                platform="platform",
                repository="repository",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a3fa23d8f314a9d4082aac6f5c6c9593e22d122ab628a2366ce6591afee4c05f)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument auto_branch_creation_config", value=auto_branch_creation_config, expected_type=type_hints["auto_branch_creation_config"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument custom_headers", value=custom_headers, expected_type=type_hints["custom_headers"])
            check_type(argname="argument custom_rules", value=custom_rules, expected_type=type_hints["custom_rules"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_branch_auto_deletion", value=enable_branch_auto_deletion, expected_type=type_hints["enable_branch_auto_deletion"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument iam_service_role", value=iam_service_role, expected_type=type_hints["iam_service_role"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if auto_branch_creation_config is not None:
            self._values["auto_branch_creation_config"] = auto_branch_creation_config
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if custom_headers is not None:
            self._values["custom_headers"] = custom_headers
        if custom_rules is not None:
            self._values["custom_rules"] = custom_rules
        if description is not None:
            self._values["description"] = description
        if enable_branch_auto_deletion is not None:
            self._values["enable_branch_auto_deletion"] = enable_branch_auto_deletion
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if iam_service_role is not None:
            self._values["iam_service_role"] = iam_service_role
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token
        if platform is not None:
            self._values["platform"] = platform
        if repository is not None:
            self._values["repository"] = repository
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The name for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[builtins.str]:
        '''The personal access token for a GitHub repository for an Amplify app.

        The personal access token is used to authorize access to a GitHub repository using the Amplify GitHub App. The token is not stored.

        Use ``AccessToken`` for GitHub repositories only. To authorize access to a repository provider such as Bitbucket or CodeCommit, use ``OauthToken`` .

        You must specify either ``AccessToken`` or ``OauthToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-accesstoken
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def auto_branch_creation_config(
        self,
    ) -> typing.Optional[typing.Union[CfnApp.AutoBranchCreationConfigProperty, _IResolvable_a771d0ef]]:
        '''Sets the configuration for your automatic branch creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-autobranchcreationconfig
        '''
        result = self._values.get("auto_branch_creation_config")
        return typing.cast(typing.Optional[typing.Union[CfnApp.AutoBranchCreationConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[CfnApp.BasicAuthConfigProperty, _IResolvable_a771d0ef]]:
        '''The credentials for basic authorization for an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[CfnApp.BasicAuthConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_headers(self) -> typing.Optional[builtins.str]:
        '''The custom HTTP headers for an Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 25000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customheaders
        '''
        result = self._values.get("custom_headers")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_rules(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.CustomRuleProperty, _IResolvable_a771d0ef]]]]:
        '''The custom rewrite and redirect rules for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-customrules
        '''
        result = self._values.get("custom_rules")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.CustomRuleProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_branch_auto_deletion(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Automatically disconnect a branch in Amplify Hosting when you delete a branch from your Git repository.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-enablebranchautodeletion
        '''
        result = self._values.get("enable_branch_auto_deletion")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]]:
        '''The environment variables map for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def iam_service_role(self) -> typing.Optional[builtins.str]:
        '''The AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) of the Amplify app.

        *Length Constraints:* Minimum length of 0. Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-iamservicerole
        '''
        result = self._values.get("iam_service_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[builtins.str]:
        '''The OAuth token for a third-party source control system for an Amplify app.

        The OAuth token is used to create a webhook and a read-only deploy key using SSH cloning. The OAuth token is not stored.

        Use ``OauthToken`` for repository providers other than GitHub, such as Bitbucket or CodeCommit. To authorize access to GitHub as your repository provider, use ``AccessToken`` .

        You must specify either ``OauthToken`` or ``AccessToken`` when you create a new app.

        Existing Amplify apps deployed from a GitHub repository using OAuth continue to work with CI/CD. However, we strongly recommend that you migrate these apps to use the GitHub App. For more information, see `Migrating an existing OAuth app to the Amplify GitHub App <https://docs.aws.amazon.com/amplify/latest/userguide/setting-up-GitHub-access.html#migrating-to-github-app-auth>`_ in the *Amplify User Guide* .

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-oauthtoken
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''The platform for the Amplify app.

        For a static app, set the platform type to ``WEB`` . For a dynamic server-side rendered (SSR) app, set the platform type to ``WEB_COMPUTE`` . For an app requiring Amplify Hosting's original SSR support only, set the platform type to ``WEB_DYNAMIC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-platform
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository(self) -> typing.Optional[builtins.str]:
        '''The repository for an Amplify app.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-repository
        '''
        result = self._values.get("repository")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tag for an Amplify app.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-app.html#cfn-amplify-app-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAppProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnBranch(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.CfnBranch",
):
    '''A CloudFormation ``AWS::Amplify::Branch``.

    The AWS::Amplify::Branch resource specifies a new branch within an app.

    :cloudformationResource: AWS::Amplify::Branch
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplify as amplify
        
        cfn_branch = amplify.CfnBranch(self, "MyCfnBranch",
            app_id="appId",
            branch_name="branchName",
        
            # the properties below are optional
            basic_auth_config=amplify.CfnBranch.BasicAuthConfigProperty(
                password="password",
                username="username",
        
                # the properties below are optional
                enable_basic_auth=False
            ),
            build_spec="buildSpec",
            description="description",
            enable_auto_build=False,
            enable_performance_mode=False,
            enable_pull_request_preview=False,
            environment_variables=[amplify.CfnBranch.EnvironmentVariableProperty(
                name="name",
                value="value"
            )],
            framework="framework",
            pull_request_environment_name="pullRequestEnvironmentName",
            stage="stage",
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
        app_id: builtins.str,
        branch_name: builtins.str,
        basic_auth_config: typing.Optional[typing.Union[typing.Union["CfnBranch.BasicAuthConfigProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnBranch.EnvironmentVariableProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::Branch``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param branch_name: The name for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param description: The description for the branch that is part of an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_auto_build: Enables auto building for the branch.
        :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param environment_variables: The environment variables for the branch.
        :param framework: The framework for the branch.
        :param pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
        :param stage: Describes the current stage for the branch. *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST
        :param tags: The tag for the branch.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e22906e6f314a306082ab5ca373434ac23e808020cd7513e57a2e3514a41ffef)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnBranchProps(
            app_id=app_id,
            branch_name=branch_name,
            basic_auth_config=basic_auth_config,
            build_spec=build_spec,
            description=description,
            enable_auto_build=enable_auto_build,
            enable_performance_mode=enable_performance_mode,
            enable_pull_request_preview=enable_pull_request_preview,
            environment_variables=environment_variables,
            framework=framework,
            pull_request_environment_name=pull_request_environment_name,
            stage=stage,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a08f9b5abfa218705c88c36062454896b1790b0e7384e78ec8b206bc0aee0506)
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
            type_hints = typing.get_type_hints(_typecheckingstub__42e5434c62c34083b9ad0ad56612036b464d26bf2555147eee8e1016971401dd)
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
        '''ARN for a branch, part of an Amplify App.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrBranchName")
    def attr_branch_name(self) -> builtins.str:
        '''Name for a branch, part of an Amplify App.

        :cloudformationAttribute: BranchName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrBranchName"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _TagManager_0b7ab120:
        '''The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        '''
        return typing.cast(_TagManager_0b7ab120, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d12c122d429411ba51e8ece31c3d607507b49cc8a02a0f933de29d4ea067acfd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''The name for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

    @branch_name.setter
    def branch_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__337f911fe0bb76e9d91a457789e55e8b33a14d578bc60b9a38072160b2ef4c08)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "branchName", value)

    @builtins.property
    @jsii.member(jsii_name="basicAuthConfig")
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union["CfnBranch.BasicAuthConfigProperty", _IResolvable_a771d0ef]]:
        '''The basic authorization credentials for a branch of an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        '''
        return typing.cast(typing.Optional[typing.Union["CfnBranch.BasicAuthConfigProperty", _IResolvable_a771d0ef]], jsii.get(self, "basicAuthConfig"))

    @basic_auth_config.setter
    def basic_auth_config(
        self,
        value: typing.Optional[typing.Union["CfnBranch.BasicAuthConfigProperty", _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbda3eeea41eb763fa37a0331309894c15a391483a2062ccbbe2f31d8dc76d5e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "basicAuthConfig", value)

    @builtins.property
    @jsii.member(jsii_name="buildSpec")
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "buildSpec"))

    @build_spec.setter
    def build_spec(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b057554ba08e06e643c5d745a4471d362a122dde2e3a9074f6c3cbe28b403423)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "buildSpec", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the branch that is part of an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5869eda006f2853567f86d2d1a81323ebab97b912e0919af29ba0f8c23a76198)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoBuild")
    def enable_auto_build(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables auto building for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableAutoBuild"))

    @enable_auto_build.setter
    def enable_auto_build(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a9db0fbb5ab490a40d5c3d74f5a5c786822f390016c5a652b42336924f5f3d48)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoBuild", value)

    @builtins.property
    @jsii.member(jsii_name="enablePerformanceMode")
    def enable_performance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableperformancemode
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enablePerformanceMode"))

    @enable_performance_mode.setter
    def enable_performance_mode(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b41610d8e65ac49de38c07f7254b03e90d7ad49f83d85def9a8ff7f2411eebb5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePerformanceMode", value)

    @builtins.property
    @jsii.member(jsii_name="enablePullRequestPreview")
    def enable_pull_request_preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch.

        If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

        For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enablePullRequestPreview"))

    @enable_pull_request_preview.setter
    def enable_pull_request_preview(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bdea46c375aa57e6245c6fb1d2ecb0c6a484328e9ec617aae6d1f46ec143b722)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enablePullRequestPreview", value)

    @builtins.property
    @jsii.member(jsii_name="environmentVariables")
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBranch.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]]:
        '''The environment variables for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        '''
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBranch.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]], jsii.get(self, "environmentVariables"))

    @environment_variables.setter
    def environment_variables(
        self,
        value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnBranch.EnvironmentVariableProperty", _IResolvable_a771d0ef]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d430629ca4d978c3cf14632116d782c10a25ed44f678eb5aff4792d0706a0834)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "environmentVariables", value)

    @builtins.property
    @jsii.member(jsii_name="framework")
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-framework
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "framework"))

    @framework.setter
    def framework(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__903bf6daade000df2db23f9d75490fe010ff0969a220d3db52cadb7d716587c0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "framework", value)

    @builtins.property
    @jsii.member(jsii_name="pullRequestEnvironmentName")
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews.

        For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

        *Length Constraints:* Maximum length of 20.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "pullRequestEnvironmentName"))

    @pull_request_environment_name.setter
    def pull_request_environment_name(
        self,
        value: typing.Optional[builtins.str],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__243c9b879c11e2a81997242fb14de7627070a0bc396117ab8507fa113fe65124)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "pullRequestEnvironmentName", value)

    @builtins.property
    @jsii.member(jsii_name="stage")
    def stage(self) -> typing.Optional[builtins.str]:
        '''Describes the current stage for the branch.

        *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stage"))

    @stage.setter
    def stage(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1b90995678806d4268be9becd79e024c4daa59d185d36547bda43acfc2bb5d2f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stage", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnBranch.BasicAuthConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "password": "password",
            "username": "username",
            "enable_basic_auth": "enableBasicAuth",
        },
    )
    class BasicAuthConfigProperty:
        def __init__(
            self,
            *,
            password: builtins.str,
            username: builtins.str,
            enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        ) -> None:
            '''Use the BasicAuthConfig property type to set password protection for a specific branch.

            :param password: The password for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param username: The user name for basic authorization. *Length Constraints:* Minimum length of 1. Maximum length of 255.
            :param enable_basic_auth: Enables basic authorization for the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                basic_auth_config_property = amplify.CfnBranch.BasicAuthConfigProperty(
                    password="password",
                    username="username",
                
                    # the properties below are optional
                    enable_basic_auth=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0147d3cc5c7cdbb6b5faa2607b976c71e93c3e4aa0025eb73772eba56c26b3e3)
                check_type(argname="argument password", value=password, expected_type=type_hints["password"])
                check_type(argname="argument username", value=username, expected_type=type_hints["username"])
                check_type(argname="argument enable_basic_auth", value=enable_basic_auth, expected_type=type_hints["enable_basic_auth"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "password": password,
                "username": username,
            }
            if enable_basic_auth is not None:
                self._values["enable_basic_auth"] = enable_basic_auth

        @builtins.property
        def password(self) -> builtins.str:
            '''The password for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-password
            '''
            result = self._values.get("password")
            assert result is not None, "Required property 'password' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def username(self) -> builtins.str:
            '''The user name for basic authorization.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-username
            '''
            result = self._values.get("username")
            assert result is not None, "Required property 'username' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def enable_basic_auth(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
            '''Enables basic authorization for the branch.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-basicauthconfig.html#cfn-amplify-branch-basicauthconfig-enablebasicauth
            '''
            result = self._values.get("enable_basic_auth")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "BasicAuthConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnBranch.EnvironmentVariableProperty",
        jsii_struct_bases=[],
        name_mapping={"name": "name", "value": "value"},
    )
    class EnvironmentVariableProperty:
        def __init__(self, *, name: builtins.str, value: builtins.str) -> None:
            '''The EnvironmentVariable property type sets environment variables for a specific branch.

            Environment variables are key-value pairs that are available at build time.

            :param name: The environment variable name. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*
            :param value: The environment variable value. *Length Constraints:* Maximum length of 5500. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                environment_variable_property = amplify.CfnBranch.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5fea7d77d1bd8b1fa5dab055dee38eac5b174641a05f335cc737ecc327f8f4ff)
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "name": name,
                "value": value,
            }

        @builtins.property
        def name(self) -> builtins.str:
            '''The environment variable name.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''The environment variable value.

            *Length Constraints:* Maximum length of 5500.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-branch-environmentvariable.html#cfn-amplify-branch-environmentvariable-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "EnvironmentVariableProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CfnBranchProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "branch_name": "branchName",
        "basic_auth_config": "basicAuthConfig",
        "build_spec": "buildSpec",
        "description": "description",
        "enable_auto_build": "enableAutoBuild",
        "enable_performance_mode": "enablePerformanceMode",
        "enable_pull_request_preview": "enablePullRequestPreview",
        "environment_variables": "environmentVariables",
        "framework": "framework",
        "pull_request_environment_name": "pullRequestEnvironmentName",
        "stage": "stage",
        "tags": "tags",
    },
)
class CfnBranchProps:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        branch_name: builtins.str,
        basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
        build_spec: typing.Optional[builtins.str] = None,
        description: typing.Optional[builtins.str] = None,
        enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
        environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
        framework: typing.Optional[builtins.str] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        stage: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnBranch``.

        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param branch_name: The name for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
        :param basic_auth_config: The basic authorization credentials for a branch of an Amplify app. You must base64-encode the authorization credentials and provide them in the format ``user:password`` .
        :param build_spec: The build specification (build spec) for the branch. *Length Constraints:* Minimum length of 1. Maximum length of 25000. *Pattern:* (?s).+
        :param description: The description for the branch that is part of an Amplify app. *Length Constraints:* Maximum length of 1000. *Pattern:* (?s).*
        :param enable_auto_build: Enables auto building for the branch.
        :param enable_performance_mode: Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.
        :param enable_pull_request_preview: Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch. If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch. To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property. For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .
        :param environment_variables: The environment variables for the branch.
        :param framework: The framework for the branch.
        :param pull_request_environment_name: If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews. For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch. To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` . If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed. For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* . *Length Constraints:* Maximum length of 20. *Pattern:* (?s).*
        :param stage: Describes the current stage for the branch. *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST
        :param tags: The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            cfn_branch_props = amplify.CfnBranchProps(
                app_id="appId",
                branch_name="branchName",
            
                # the properties below are optional
                basic_auth_config=amplify.CfnBranch.BasicAuthConfigProperty(
                    password="password",
                    username="username",
            
                    # the properties below are optional
                    enable_basic_auth=False
                ),
                build_spec="buildSpec",
                description="description",
                enable_auto_build=False,
                enable_performance_mode=False,
                enable_pull_request_preview=False,
                environment_variables=[amplify.CfnBranch.EnvironmentVariableProperty(
                    name="name",
                    value="value"
                )],
                framework="framework",
                pull_request_environment_name="pullRequestEnvironmentName",
                stage="stage",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24f17b52e1d63abdc4a206fd2a13a8c94c1f92fe5fc5ca837b11f5ae50c7a552)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
            check_type(argname="argument basic_auth_config", value=basic_auth_config, expected_type=type_hints["basic_auth_config"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument enable_auto_build", value=enable_auto_build, expected_type=type_hints["enable_auto_build"])
            check_type(argname="argument enable_performance_mode", value=enable_performance_mode, expected_type=type_hints["enable_performance_mode"])
            check_type(argname="argument enable_pull_request_preview", value=enable_pull_request_preview, expected_type=type_hints["enable_pull_request_preview"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument framework", value=framework, expected_type=type_hints["framework"])
            check_type(argname="argument pull_request_environment_name", value=pull_request_environment_name, expected_type=type_hints["pull_request_environment_name"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "branch_name": branch_name,
        }
        if basic_auth_config is not None:
            self._values["basic_auth_config"] = basic_auth_config
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if description is not None:
            self._values["description"] = description
        if enable_auto_build is not None:
            self._values["enable_auto_build"] = enable_auto_build
        if enable_performance_mode is not None:
            self._values["enable_performance_mode"] = enable_performance_mode
        if enable_pull_request_preview is not None:
            self._values["enable_pull_request_preview"] = enable_pull_request_preview
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if framework is not None:
            self._values["framework"] = framework
        if pull_request_environment_name is not None:
            self._values["pull_request_environment_name"] = pull_request_environment_name
        if stage is not None:
            self._values["stage"] = stage
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-appid
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def branch_name(self) -> builtins.str:
        '''The name for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 255.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-branchname
        '''
        result = self._values.get("branch_name")
        assert result is not None, "Required property 'branch_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def basic_auth_config(
        self,
    ) -> typing.Optional[typing.Union[CfnBranch.BasicAuthConfigProperty, _IResolvable_a771d0ef]]:
        '''The basic authorization credentials for a branch of an Amplify app.

        You must base64-encode the authorization credentials and provide them in the format ``user:password`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-basicauthconfig
        '''
        result = self._values.get("basic_auth_config")
        return typing.cast(typing.Optional[typing.Union[CfnBranch.BasicAuthConfigProperty, _IResolvable_a771d0ef]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[builtins.str]:
        '''The build specification (build spec) for the branch.

        *Length Constraints:* Minimum length of 1. Maximum length of 25000.

        *Pattern:* (?s).+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-buildspec
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''The description for the branch that is part of an Amplify app.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_build(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables auto building for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableautobuild
        '''
        result = self._values.get("enable_auto_build")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_performance_mode(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables performance mode for the branch.

        Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enableperformancemode
        '''
        result = self._values.get("enable_performance_mode")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def enable_pull_request_preview(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Specifies whether Amplify Hosting creates a preview for each pull request that is made for this branch.

        If this property is enabled, Amplify deploys your app to a unique preview URL after each pull request is opened. Development and QA teams can use this preview to test the pull request before it's merged into a production or integration branch.

        To provide backend support for your preview, Amplify automatically provisions a temporary backend environment that it deletes when the pull request is closed. If you want to specify a dedicated backend environment for your previews, use the ``PullRequestEnvironmentName`` property.

        For more information, see `Web Previews <https://docs.aws.amazon.com/amplify/latest/userguide/pr-previews.html>`_ in the *AWS Amplify Hosting User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-enablepullrequestpreview
        '''
        result = self._values.get("enable_pull_request_preview")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBranch.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]]:
        '''The environment variables for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-environmentvariables
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBranch.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]], result)

    @builtins.property
    def framework(self) -> typing.Optional[builtins.str]:
        '''The framework for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-framework
        '''
        result = self._values.get("framework")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def pull_request_environment_name(self) -> typing.Optional[builtins.str]:
        '''If pull request previews are enabled for this branch, you can use this property to specify a dedicated backend environment for your previews.

        For example, you could specify an environment named ``prod`` , ``test`` , or ``dev`` that you initialized with the Amplify CLI and mapped to this branch.

        To enable pull request previews, set the ``EnablePullRequestPreview`` property to ``true`` .

        If you don't specify an environment, Amplify Hosting provides backend support for each preview by automatically provisioning a temporary backend environment. Amplify Hosting deletes this environment when the pull request is closed.

        For more information about creating backend environments, see `Feature Branch Deployments and Team Workflows <https://docs.aws.amazon.com/amplify/latest/userguide/multi-environments.html>`_ in the *AWS Amplify Hosting User Guide* .

        *Length Constraints:* Maximum length of 20.

        *Pattern:* (?s).*

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-pullrequestenvironmentname
        '''
        result = self._values.get("pull_request_environment_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stage(self) -> typing.Optional[builtins.str]:
        '''Describes the current stage for the branch.

        *Valid Values:* PRODUCTION | BETA | DEVELOPMENT | EXPERIMENTAL | PULL_REQUEST

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-stage
        '''
        result = self._values.get("stage")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_CfnTag_95fbdc29]]:
        '''The tag for the branch.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-branch.html#cfn-amplify-branch-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_CfnTag_95fbdc29]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnBranchProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IInspectable_82c04a63)
class CfnDomain(
    _CfnResource_e0a482dc,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.CfnDomain",
):
    '''A CloudFormation ``AWS::Amplify::Domain``.

    The AWS::Amplify::Domain resource allows you to connect a custom domain to your app.

    :cloudformationResource: AWS::Amplify::Domain
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_amplify as amplify
        
        cfn_domain = amplify.CfnDomain(self, "MyCfnDomain",
            app_id="appId",
            domain_name="domainName",
            sub_domain_settings=[amplify.CfnDomain.SubDomainSettingProperty(
                branch_name="branchName",
                prefix="prefix"
            )],
        
            # the properties below are optional
            auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
            auto_sub_domain_iam_role="autoSubDomainIamRole",
            enable_auto_sub_domain=False
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain_settings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union["CfnDomain.SubDomainSettingProperty", typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
        enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Create a new ``AWS::Amplify::Domain``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param domain_name: The domain name for the domain association. *Length Constraints:* Maximum length of 255. *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$
        :param sub_domain_settings: The setting for the subdomain.
        :param auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains. *Length Constraints:* Maximum length of 1000. *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+
        :param enable_auto_sub_domain: Enables the automated creation of subdomains for branches.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a612a4128896bb966b8ef1945fcb8bae3ca1ea3de63ccba9c7ab998d401a48ee)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnDomainProps(
            app_id=app_id,
            domain_name=domain_name,
            sub_domain_settings=sub_domain_settings,
            auto_sub_domain_creation_patterns=auto_sub_domain_creation_patterns,
            auto_sub_domain_iam_role=auto_sub_domain_iam_role,
            enable_auto_sub_domain=enable_auto_sub_domain,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _TreeInspector_1cd1894e) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9f6ebaf849f6a4b3da1a4d6fbf3982a9b12334bdcf529423b1e5ac0aa01a0154)
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
            type_hints = typing.get_type_hints(_typecheckingstub__8976d6ef36cae5f579630d3044cdf17e594d31501251bcfcc2cd085b4bd8468a)
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
        '''ARN for the Domain Association.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoSubDomainCreationPatterns")
    def attr_auto_sub_domain_creation_patterns(self) -> typing.List[builtins.str]:
        '''Branch patterns for the automatically created subdomain.

        :cloudformationAttribute: AutoSubDomainCreationPatterns
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "attrAutoSubDomainCreationPatterns"))

    @builtins.property
    @jsii.member(jsii_name="attrAutoSubDomainIamRole")
    def attr_auto_sub_domain_iam_role(self) -> builtins.str:
        '''The IAM service role for the subdomain.

        :cloudformationAttribute: AutoSubDomainIAMRole
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrAutoSubDomainIamRole"))

    @builtins.property
    @jsii.member(jsii_name="attrCertificateRecord")
    def attr_certificate_record(self) -> builtins.str:
        '''DNS Record for certificate verification.

        :cloudformationAttribute: CertificateRecord
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCertificateRecord"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainName")
    def attr_domain_name(self) -> builtins.str:
        '''Name of the domain.

        :cloudformationAttribute: DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDomainStatus")
    def attr_domain_status(self) -> builtins.str:
        '''Status for the Domain Association.

        :cloudformationAttribute: DomainStatus
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDomainStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrEnableAutoSubDomain")
    def attr_enable_auto_sub_domain(self) -> _IResolvable_a771d0ef:
        '''Specifies whether the automated creation of subdomains for branches is enabled.

        :cloudformationAttribute: EnableAutoSubDomain
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "attrEnableAutoSubDomain"))

    @builtins.property
    @jsii.member(jsii_name="attrStatusReason")
    def attr_status_reason(self) -> builtins.str:
        '''Reason for the current status of the domain.

        :cloudformationAttribute: StatusReason
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatusReason"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @app_id.setter
    def app_id(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ca667eb08871111d25c9213b4468b694b42ac7067adca0a7d104a85537d52c27)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "appId", value)

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''The domain name for the domain association.

        *Length Constraints:* Maximum length of 255.

        *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @domain_name.setter
    def domain_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a17079458a6f870ed963a275e80113d43a19893575da51f25bbcfdc72f266e01)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "domainName", value)

    @builtins.property
    @jsii.member(jsii_name="subDomainSettings")
    def sub_domain_settings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDomain.SubDomainSettingProperty", _IResolvable_a771d0ef]]]:
        '''The setting for the subdomain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        '''
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDomain.SubDomainSettingProperty", _IResolvable_a771d0ef]]], jsii.get(self, "subDomainSettings"))

    @sub_domain_settings.setter
    def sub_domain_settings(
        self,
        value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union["CfnDomain.SubDomainSettingProperty", _IResolvable_a771d0ef]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1806885de5be192c9e16b247cdcdc44a7b3bc351328d588dfd13b60673004039)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "subDomainSettings", value)

    @builtins.property
    @jsii.member(jsii_name="autoSubDomainCreationPatterns")
    def auto_sub_domain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the branch patterns for automatic subdomain creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomaincreationpatterns
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "autoSubDomainCreationPatterns"))

    @auto_sub_domain_creation_patterns.setter
    def auto_sub_domain_creation_patterns(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__be33644166d41cc01397ca93000e26dbaf34d48e0b8b2607eb12337df9297d43)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubDomainCreationPatterns", value)

    @builtins.property
    @jsii.member(jsii_name="autoSubDomainIamRole")
    def auto_sub_domain_iam_role(self) -> typing.Optional[builtins.str]:
        '''The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomainiamrole
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "autoSubDomainIamRole"))

    @auto_sub_domain_iam_role.setter
    def auto_sub_domain_iam_role(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0eb326101c1aad0647ab4fb2e8ac7f377cf9e1036b89a4f8a8db01b7be1e6e8c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "autoSubDomainIamRole", value)

    @builtins.property
    @jsii.member(jsii_name="enableAutoSubDomain")
    def enable_auto_sub_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-enableautosubdomain
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], jsii.get(self, "enableAutoSubDomain"))

    @enable_auto_sub_domain.setter
    def enable_auto_sub_domain(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da9d0350be0ca93fc88cccef74512d96d01e8b09386799600d3696125d6b32d6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "enableAutoSubDomain", value)

    @jsii.data_type(
        jsii_type="monocdk.aws_amplify.CfnDomain.SubDomainSettingProperty",
        jsii_struct_bases=[],
        name_mapping={"branch_name": "branchName", "prefix": "prefix"},
    )
    class SubDomainSettingProperty:
        def __init__(self, *, branch_name: builtins.str, prefix: builtins.str) -> None:
            '''The SubDomainSetting property type enables you to connect a subdomain (for example, example.exampledomain.com) to a specific branch.

            :param branch_name: The branch name setting for the subdomain. *Length Constraints:* Minimum length of 1. Maximum length of 255. *Pattern:* (?s).+
            :param prefix: The prefix setting for the subdomain. *Length Constraints:* Maximum length of 255. *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                from monocdk import aws_amplify as amplify
                
                sub_domain_setting_property = amplify.CfnDomain.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d244440484546b32ae4623efb4089d13990dd070ab694600d8fc32df2242743a)
                check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "branch_name": branch_name,
                "prefix": prefix,
            }

        @builtins.property
        def branch_name(self) -> builtins.str:
            '''The branch name setting for the subdomain.

            *Length Constraints:* Minimum length of 1. Maximum length of 255.

            *Pattern:* (?s).+

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-branchname
            '''
            result = self._values.get("branch_name")
            assert result is not None, "Required property 'branch_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> builtins.str:
            '''The prefix setting for the subdomain.

            *Length Constraints:* Maximum length of 255.

            *Pattern:* (?s).*

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-amplify-domain-subdomainsetting.html#cfn-amplify-domain-subdomainsetting-prefix
            '''
            result = self._values.get("prefix")
            assert result is not None, "Required property 'prefix' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SubDomainSettingProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CfnDomainProps",
    jsii_struct_bases=[],
    name_mapping={
        "app_id": "appId",
        "domain_name": "domainName",
        "sub_domain_settings": "subDomainSettings",
        "auto_sub_domain_creation_patterns": "autoSubDomainCreationPatterns",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
        "enable_auto_sub_domain": "enableAutoSubDomain",
    },
)
class CfnDomainProps:
    def __init__(
        self,
        *,
        app_id: builtins.str,
        domain_name: builtins.str,
        sub_domain_settings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
        auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
        enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    ) -> None:
        '''Properties for defining a ``CfnDomain``.

        :param app_id: The unique ID for an Amplify app. *Length Constraints:* Minimum length of 1. Maximum length of 20. *Pattern:* d[a-z0-9]+
        :param domain_name: The domain name for the domain association. *Length Constraints:* Maximum length of 255. *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$
        :param sub_domain_settings: The setting for the subdomain.
        :param auto_sub_domain_creation_patterns: Sets the branch patterns for automatic subdomain creation.
        :param auto_sub_domain_iam_role: The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains. *Length Constraints:* Maximum length of 1000. *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+
        :param enable_auto_sub_domain: Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            cfn_domain_props = amplify.CfnDomainProps(
                app_id="appId",
                domain_name="domainName",
                sub_domain_settings=[amplify.CfnDomain.SubDomainSettingProperty(
                    branch_name="branchName",
                    prefix="prefix"
                )],
            
                # the properties below are optional
                auto_sub_domain_creation_patterns=["autoSubDomainCreationPatterns"],
                auto_sub_domain_iam_role="autoSubDomainIamRole",
                enable_auto_sub_domain=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__da8febeb0d0a7befa7e9382025b5656388988688f9e0662e34454cf204a4a4bf)
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument sub_domain_settings", value=sub_domain_settings, expected_type=type_hints["sub_domain_settings"])
            check_type(argname="argument auto_sub_domain_creation_patterns", value=auto_sub_domain_creation_patterns, expected_type=type_hints["auto_sub_domain_creation_patterns"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
            check_type(argname="argument enable_auto_sub_domain", value=enable_auto_sub_domain, expected_type=type_hints["enable_auto_sub_domain"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app_id": app_id,
            "domain_name": domain_name,
            "sub_domain_settings": sub_domain_settings,
        }
        if auto_sub_domain_creation_patterns is not None:
            self._values["auto_sub_domain_creation_patterns"] = auto_sub_domain_creation_patterns
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role
        if enable_auto_sub_domain is not None:
            self._values["enable_auto_sub_domain"] = enable_auto_sub_domain

    @builtins.property
    def app_id(self) -> builtins.str:
        '''The unique ID for an Amplify app.

        *Length Constraints:* Minimum length of 1. Maximum length of 20.

        *Pattern:* d[a-z0-9]+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-appid
        '''
        result = self._values.get("app_id")
        assert result is not None, "Required property 'app_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''The domain name for the domain association.

        *Length Constraints:* Maximum length of 255.

        *Pattern:* ^(((?!-)[A-Za-z0-9-]{0,62}[A-Za-z0-9]).)+((?!-)[A-Za-z0-9-]{1,62}[A-Za-z0-9])(.)?$

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-domainname
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sub_domain_settings(
        self,
    ) -> typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDomain.SubDomainSettingProperty, _IResolvable_a771d0ef]]]:
        '''The setting for the subdomain.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-subdomainsettings
        '''
        result = self._values.get("sub_domain_settings")
        assert result is not None, "Required property 'sub_domain_settings' is missing"
        return typing.cast(typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDomain.SubDomainSettingProperty, _IResolvable_a771d0ef]]], result)

    @builtins.property
    def auto_sub_domain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets the branch patterns for automatic subdomain creation.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomaincreationpatterns
        '''
        result = self._values.get("auto_sub_domain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def auto_sub_domain_iam_role(self) -> typing.Optional[builtins.str]:
        '''The required AWS Identity and Access Management (IAM) service role for the Amazon Resource Name (ARN) for automatically creating subdomains.

        *Length Constraints:* Maximum length of 1000.

        *Pattern:* ^$|^arn:aws:iam::\\d{12}:role.+

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-autosubdomainiamrole
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_sub_domain(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]]:
        '''Enables the automated creation of subdomains for branches.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-amplify-domain.html#cfn-amplify-domain-enableautosubdomain
        '''
        result = self._values.get("enable_auto_sub_domain")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnDomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CodeCommitSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={"repository": "repository"},
)
class CodeCommitSourceCodeProviderProps:
    def __init__(self, *, repository: _IRepository_cdb2a3c0) -> None:
        '''(experimental) Properties for a CodeCommit source code provider.

        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as codecommit
            
            
            repository = codecommit.Repository(self, "Repo",
                repository_name="my-repo"
            )
            
            amplify_app = amplify.App(self, "App",
                source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5852be3beca47e381e011a9bfca854d7f75b0e81705c3489e2f0ee797290c952)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }

    @builtins.property
    def repository(self) -> _IRepository_cdb2a3c0:
        '''(experimental) The CodeCommit repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(_IRepository_cdb2a3c0, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CustomResponseHeader",
    jsii_struct_bases=[],
    name_mapping={"headers": "headers", "pattern": "pattern"},
)
class CustomResponseHeader:
    def __init__(
        self,
        *,
        headers: typing.Mapping[builtins.str, builtins.str],
        pattern: builtins.str,
    ) -> None:
        '''(experimental) Custom response header of an Amplify App.

        :param headers: (experimental) The map of custom headers to be applied.
        :param pattern: (experimental) These custom headers will be applied to all URL file paths that match this pattern.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            custom_response_header = amplify.CustomResponseHeader(
                headers={
                    "headers_key": "headers"
                },
                pattern="pattern"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f9c327c9a6b08787ccd6806194d7ba422fc108ab1416697df50be5e2464f12e)
            check_type(argname="argument headers", value=headers, expected_type=type_hints["headers"])
            check_type(argname="argument pattern", value=pattern, expected_type=type_hints["pattern"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "headers": headers,
            "pattern": pattern,
        }

    @builtins.property
    def headers(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The map of custom headers to be applied.

        :stability: experimental
        '''
        result = self._values.get("headers")
        assert result is not None, "Required property 'headers' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def pattern(self) -> builtins.str:
        '''(experimental) These custom headers will be applied to all URL file paths that match this pattern.

        :stability: experimental
        '''
        result = self._values.get("pattern")
        assert result is not None, "Required property 'pattern' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomResponseHeader(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CustomRule(metaclass=jsii.JSIIMeta, jsii_type="monocdk.aws_amplify.CustomRule"):
    '''(experimental) Custom rewrite/redirect rule for an Amplify App.

    :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule({
            "source": "/docs/specific-filename.html",
            "target": "/documents/different-filename.html",
            "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
        })
    '''

    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''
        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        '''
        options = CustomRuleOptions(
            source=source, target=target, condition=condition, status=status
        )

        jsii.create(self.__class__, self, [options])

    @jsii.python.classproperty
    @jsii.member(jsii_name="SINGLE_PAGE_APPLICATION_REDIRECT")
    def SINGLE_PAGE_APPLICATION_REDIRECT(cls) -> "CustomRule":
        '''(experimental) Sets up a 200 rewrite for all paths to ``index.html`` except for path containing a file extension.

        :stability: experimental
        '''
        return typing.cast("CustomRule", jsii.sget(cls, "SINGLE_PAGE_APPLICATION_REDIRECT"))

    @builtins.property
    @jsii.member(jsii_name="source")
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "source"))

    @builtins.property
    @jsii.member(jsii_name="target")
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "target"))

    @builtins.property
    @jsii.member(jsii_name="condition")
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "condition"))

    @builtins.property
    @jsii.member(jsii_name="status")
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        return typing.cast(typing.Optional["RedirectStatus"], jsii.get(self, "status"))


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.CustomRuleOptions",
    jsii_struct_bases=[],
    name_mapping={
        "source": "source",
        "target": "target",
        "condition": "condition",
        "status": "status",
    },
)
class CustomRuleOptions:
    def __init__(
        self,
        *,
        source: builtins.str,
        target: builtins.str,
        condition: typing.Optional[builtins.str] = None,
        status: typing.Optional["RedirectStatus"] = None,
    ) -> None:
        '''(experimental) Options for a custom rewrite/redirect rule for an Amplify App.

        :param source: (experimental) The source pattern for a URL rewrite or redirect rule.
        :param target: (experimental) The target pattern for a URL rewrite or redirect rule.
        :param condition: (experimental) The condition for a URL rewrite or redirect rule, e.g. country code. Default: - no condition
        :param status: (experimental) The status code for a URL rewrite or redirect rule. Default: PERMANENT_REDIRECT

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            custom_rule_options = amplify.CustomRuleOptions(
                source="source",
                target="target",
            
                # the properties below are optional
                condition="condition",
                status=amplify.RedirectStatus.REWRITE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d00fc5f798f803310b7ba418930b31919f8b8d9e308e4bb9baaed6f55c3f1367)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument condition", value=condition, expected_type=type_hints["condition"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "source": source,
            "target": target,
        }
        if condition is not None:
            self._values["condition"] = condition
        if status is not None:
            self._values["status"] = status

    @builtins.property
    def source(self) -> builtins.str:
        '''(experimental) The source pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def target(self) -> builtins.str:
        '''(experimental) The target pattern for a URL rewrite or redirect rule.

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("target")
        assert result is not None, "Required property 'target' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def condition(self) -> typing.Optional[builtins.str]:
        '''(experimental) The condition for a URL rewrite or redirect rule, e.g. country code.

        :default: - no condition

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("condition")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def status(self) -> typing.Optional["RedirectStatus"]:
        '''(experimental) The status code for a URL rewrite or redirect rule.

        :default: PERMANENT_REDIRECT

        :see: https://docs.aws.amazon.com/amplify/latest/userguide/redirects.html
        :stability: experimental
        '''
        result = self._values.get("status")
        return typing.cast(typing.Optional["RedirectStatus"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CustomRuleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Domain(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.Domain",
):
    '''(experimental) An Amplify Console domain.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        # master: amplify.Branch
        # dev: amplify.Branch
        
        
        domain = amplify_app.add_domain("example.com",
            enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
            auto_subdomain_creation_patterns=["*", "pr*"]
        )
        domain.map_root(master) # map master branch to domain root
        domain.map_sub_domain(master, "www")
        domain.map_sub_domain(dev)
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_IRole_59af6f50] = None,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e8092228538277a79a30edbb0b3a26474e47f93d98d37bb95371c32c2c59ba2e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = DomainProps(
            app=app,
            auto_sub_domain_iam_role=auto_sub_domain_iam_role,
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="mapRoot")
    def map_root(self, branch: "IBranch") -> "Domain":
        '''(experimental) Maps a branch to the domain root.

        :param branch: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2dc6fb652f4a13cbc17a9729c2741ca3a9b9dd661a6334d7401824cd7a0a77af)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        return typing.cast("Domain", jsii.invoke(self, "mapRoot", [branch]))

    @jsii.member(jsii_name="mapSubDomain")
    def map_sub_domain(
        self,
        branch: "IBranch",
        prefix: typing.Optional[builtins.str] = None,
    ) -> "Domain":
        '''(experimental) Maps a branch to a sub domain.

        :param branch: The branch.
        :param prefix: The prefix. Use '' to map to the root of the domain. Defaults to branch name.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__24450ddf502a17c78cda483f35858e07ee28d3458d4567453bd3eb983218f8ad)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        return typing.cast("Domain", jsii.invoke(self, "mapSubDomain", [branch, prefix]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(experimental) Validate the current construct.

        This method can be implemented by derived constructs in order to perform
        validation logic. It is called on all constructs before synthesis.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="certificateRecord")
    def certificate_record(self) -> builtins.str:
        '''(experimental) The DNS Record for certificate verification.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "certificateRecord"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainCreationPatterns")
    def domain_auto_sub_domain_creation_patterns(self) -> typing.List[builtins.str]:
        '''(experimental) Branch patterns for the automatically created subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "domainAutoSubDomainCreationPatterns"))

    @builtins.property
    @jsii.member(jsii_name="domainAutoSubDomainIamRole")
    def domain_auto_sub_domain_iam_role(self) -> builtins.str:
        '''(experimental) The IAM service role for the subdomain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainAutoSubDomainIamRole"))

    @builtins.property
    @jsii.member(jsii_name="domainEnableAutoSubDomain")
    def domain_enable_auto_sub_domain(self) -> _IResolvable_a771d0ef:
        '''(experimental) Specifies whether the automated creation of subdomains for branches is enabled.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(_IResolvable_a771d0ef, jsii.get(self, "domainEnableAutoSubDomain"))

    @builtins.property
    @jsii.member(jsii_name="domainName")
    def domain_name(self) -> builtins.str:
        '''(experimental) The name of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainName"))

    @builtins.property
    @jsii.member(jsii_name="domainStatus")
    def domain_status(self) -> builtins.str:
        '''(experimental) The status of the domain association.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "domainStatus"))

    @builtins.property
    @jsii.member(jsii_name="statusReason")
    def status_reason(self) -> builtins.str:
        '''(experimental) The reason for the current status of the domain.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "statusReason"))


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.DomainOptions",
    jsii_struct_bases=[],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
    },
)
class DomainOptions:
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options to add a domain to an application.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # amplify_app: amplify.App
            # master: amplify.Branch
            # dev: amplify.Branch
            
            
            domain = amplify_app.add_domain("example.com",
                enable_auto_subdomain=True,  # in case subdomains should be auto registered for branches
                auto_subdomain_creation_patterns=["*", "pr*"]
            )
            domain.map_root(master) # map master branch to domain root
            domain.map_sub_domain(master, "www")
            domain.map_sub_domain(dev)
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7250a71dde68e5a45257b779ec6ca0fe50a1b50dcc5b076d638ec13c0a10344d)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.DomainProps",
    jsii_struct_bases=[DomainOptions],
    name_mapping={
        "auto_subdomain_creation_patterns": "autoSubdomainCreationPatterns",
        "domain_name": "domainName",
        "enable_auto_subdomain": "enableAutoSubdomain",
        "sub_domains": "subDomains",
        "app": "app",
        "auto_sub_domain_iam_role": "autoSubDomainIamRole",
    },
)
class DomainProps(DomainOptions):
    def __init__(
        self,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union["SubDomain", typing.Dict[builtins.str, typing.Any]]]] = None,
        app: "IApp",
        auto_sub_domain_iam_role: typing.Optional[_IRole_59af6f50] = None,
    ) -> None:
        '''(experimental) Properties for a Domain.

        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains
        :param app: (experimental) The application to which the domain must be connected.
        :param auto_sub_domain_iam_role: (experimental) The IAM role with access to Route53 when using enableAutoSubdomain. Default: the IAM role from App.grantPrincipal

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            from monocdk import aws_iam as iam
            
            # app: amplify.App
            # branch: amplify.Branch
            # role: iam.Role
            
            domain_props = amplify.DomainProps(
                app=app,
            
                # the properties below are optional
                auto_subdomain_creation_patterns=["autoSubdomainCreationPatterns"],
                auto_sub_domain_iam_role=role,
                domain_name="domainName",
                enable_auto_subdomain=False,
                sub_domains=[amplify.SubDomain(
                    branch=branch,
            
                    # the properties below are optional
                    prefix="prefix"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b81eee0f9442b5fd8115685a5dd279fc18205b5f29fd20db7e28a961040c19e0)
            check_type(argname="argument auto_subdomain_creation_patterns", value=auto_subdomain_creation_patterns, expected_type=type_hints["auto_subdomain_creation_patterns"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument enable_auto_subdomain", value=enable_auto_subdomain, expected_type=type_hints["enable_auto_subdomain"])
            check_type(argname="argument sub_domains", value=sub_domains, expected_type=type_hints["sub_domains"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument auto_sub_domain_iam_role", value=auto_sub_domain_iam_role, expected_type=type_hints["auto_sub_domain_iam_role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "app": app,
        }
        if auto_subdomain_creation_patterns is not None:
            self._values["auto_subdomain_creation_patterns"] = auto_subdomain_creation_patterns
        if domain_name is not None:
            self._values["domain_name"] = domain_name
        if enable_auto_subdomain is not None:
            self._values["enable_auto_subdomain"] = enable_auto_subdomain
        if sub_domains is not None:
            self._values["sub_domains"] = sub_domains
        if auto_sub_domain_iam_role is not None:
            self._values["auto_sub_domain_iam_role"] = auto_sub_domain_iam_role

    @builtins.property
    def auto_subdomain_creation_patterns(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Branches which should automatically create subdomains.

        :default: - all repository branches ['*', 'pr*']

        :stability: experimental
        '''
        result = self._values.get("auto_subdomain_creation_patterns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def domain_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the domain.

        :default: - the construct's id

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def enable_auto_subdomain(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Automatically create subdomains for connected branches.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_auto_subdomain")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def sub_domains(self) -> typing.Optional[typing.List["SubDomain"]]:
        '''(experimental) Subdomains.

        :default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        result = self._values.get("sub_domains")
        return typing.cast(typing.Optional[typing.List["SubDomain"]], result)

    @builtins.property
    def app(self) -> "IApp":
        '''(experimental) The application to which the domain must be connected.

        :stability: experimental
        '''
        result = self._values.get("app")
        assert result is not None, "Required property 'app' is missing"
        return typing.cast("IApp", result)

    @builtins.property
    def auto_sub_domain_iam_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role with access to Route53 when using enableAutoSubdomain.

        :default: the IAM role from App.grantPrincipal

        :stability: experimental
        '''
        result = self._values.get("auto_sub_domain_iam_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DomainProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.GitHubSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitHubSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _SecretValue_c18506ef,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitHub source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitHubSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-github-token")
                ),
                auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                    patterns=["feature/*", "test/*"]),
                auto_branch_deletion=True
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__71709197ed7b4dacbbdda6e3f7d9c8a0592e66716e0288f2d8b4fc37d7606db0)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _SecretValue_c18506ef:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.GitLabSourceCodeProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "oauth_token": "oauthToken",
        "owner": "owner",
        "repository": "repository",
    },
)
class GitLabSourceCodeProviderProps:
    def __init__(
        self,
        *,
        oauth_token: _SecretValue_c18506ef,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''(experimental) Properties for a GitLab source code provider.

        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            amplify_app = amplify.App(self, "MyApp",
                source_code_provider=amplify.GitLabSourceCodeProvider(
                    owner="<user>",
                    repository="<repo>",
                    oauth_token=SecretValue.secrets_manager("my-gitlab-token")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b5030802eab58f0d1cce5ccdbc7c633f63ccbddd76ad6443f24f90069c62bc56)
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
            check_type(argname="argument owner", value=owner, expected_type=type_hints["owner"])
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "oauth_token": oauth_token,
            "owner": owner,
            "repository": repository,
        }

    @builtins.property
    def oauth_token(self) -> _SecretValue_c18506ef:
        '''(experimental) A personal access token with the ``repo`` scope.

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        assert result is not None, "Required property 'oauth_token' is missing"
        return typing.cast(_SecretValue_c18506ef, result)

    @builtins.property
    def owner(self) -> builtins.str:
        '''(experimental) The user or organization owning the repository.

        :stability: experimental
        '''
        result = self._values.get("owner")
        assert result is not None, "Required property 'owner' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The name of the repository.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitLabSourceCodeProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.aws_amplify.IApp")
class IApp(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IAppProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_amplify.IApp"

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IApp).__jsii_proxy_class__ = lambda : _IAppProxy


@jsii.interface(jsii_type="monocdk.aws_amplify.IBranch")
class IBranch(_IResource_8c1dbbbd, typing_extensions.Protocol):
    '''(experimental) A branch.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        ...


class _IBranchProxy(
    jsii.proxy_for(_IResource_8c1dbbbd), # type: ignore[misc]
):
    '''(experimental) A branch.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_amplify.IBranch"

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IBranch).__jsii_proxy_class__ = lambda : _IBranchProxy


@jsii.interface(jsii_type="monocdk.aws_amplify.ISourceCodeProvider")
class ISourceCodeProvider(typing_extensions.Protocol):
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        ...


class _ISourceCodeProviderProxy:
    '''(experimental) A source code provider.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_amplify.ISourceCodeProvider"

    @jsii.member(jsii_name="bind")
    def bind(self, app: "App") -> "SourceCodeProviderConfig":
        '''(experimental) Binds the source code provider to an app.

        :param app: The app [disable-awslint:ref-via-interface].

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c92443503479ba23727d684d5fb140a6d6cb6e5322a229d0c9c8ba655f49eaed)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast("SourceCodeProviderConfig", jsii.invoke(self, "bind", [app]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ISourceCodeProvider).__jsii_proxy_class__ = lambda : _ISourceCodeProviderProxy


@jsii.enum(jsii_type="monocdk.aws_amplify.RedirectStatus")
class RedirectStatus(enum.Enum):
    '''(experimental) The status code for a URL rewrite or redirect rule.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        amplify_app.add_custom_rule({
            "source": "/docs/specific-filename.html",
            "target": "/documents/different-filename.html",
            "status": amplify.RedirectStatus.TEMPORARY_REDIRECT
        })
    '''

    REWRITE = "REWRITE"
    '''(experimental) Rewrite (200).

    :stability: experimental
    '''
    PERMANENT_REDIRECT = "PERMANENT_REDIRECT"
    '''(experimental) Permanent redirect (301).

    :stability: experimental
    '''
    TEMPORARY_REDIRECT = "TEMPORARY_REDIRECT"
    '''(experimental) Temporary redirect (302).

    :stability: experimental
    '''
    NOT_FOUND = "NOT_FOUND"
    '''(experimental) Not found (404).

    :stability: experimental
    '''
    NOT_FOUND_REWRITE = "NOT_FOUND_REWRITE"
    '''(experimental) Not found rewrite (404).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.SourceCodeProviderConfig",
    jsii_struct_bases=[],
    name_mapping={
        "repository": "repository",
        "access_token": "accessToken",
        "oauth_token": "oauthToken",
    },
)
class SourceCodeProviderConfig:
    def __init__(
        self,
        *,
        repository: builtins.str,
        access_token: typing.Optional[_SecretValue_c18506ef] = None,
        oauth_token: typing.Optional[_SecretValue_c18506ef] = None,
    ) -> None:
        '''(experimental) Configuration for the source code provider.

        :param repository: (experimental) The repository for the application. Must use the ``HTTPS`` protocol. For example, ``https://github.com/aws/aws-cdk``.
        :param access_token: (experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. Token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is sepcified. Default: - do not use a token
        :param oauth_token: (experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key. OAuth token is not stored. Either ``accessToken`` or ``oauthToken`` must be specified if ``repository`` is specified. Default: - do not use a token

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_amplify as amplify
            
            # secret_value: monocdk.SecretValue
            
            source_code_provider_config = amplify.SourceCodeProviderConfig(
                repository="repository",
            
                # the properties below are optional
                access_token=secret_value,
                oauth_token=secret_value
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1cc076493484abfa9208f91039353a73e013f10ac61617e1fa9bb4fb98a03cb8)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument access_token", value=access_token, expected_type=type_hints["access_token"])
            check_type(argname="argument oauth_token", value=oauth_token, expected_type=type_hints["oauth_token"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "repository": repository,
        }
        if access_token is not None:
            self._values["access_token"] = access_token
        if oauth_token is not None:
            self._values["oauth_token"] = oauth_token

    @builtins.property
    def repository(self) -> builtins.str:
        '''(experimental) The repository for the application. Must use the ``HTTPS`` protocol.

        For example, ``https://github.com/aws/aws-cdk``.

        :stability: experimental
        '''
        result = self._values.get("repository")
        assert result is not None, "Required property 'repository' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def access_token(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) Personal Access token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        Token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is sepcified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("access_token")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    @builtins.property
    def oauth_token(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) OAuth token for 3rd party source control system for an Amplify App, used to create webhook and read-only deploy key.

        OAuth token is not stored.

        Either ``accessToken`` or ``oauthToken`` must be specified if ``repository``
        is specified.

        :default: - do not use a token

        :stability: experimental
        '''
        result = self._values.get("oauth_token")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SourceCodeProviderConfig(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_amplify.SubDomain",
    jsii_struct_bases=[],
    name_mapping={"branch": "branch", "prefix": "prefix"},
)
class SubDomain:
    def __init__(
        self,
        *,
        branch: IBranch,
        prefix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Sub domain settings.

        :param branch: (experimental) The branch.
        :param prefix: (experimental) The prefix. Use '' to map to the root of the domain Default: - the branch name

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_amplify as amplify
            
            # branch: amplify.Branch
            
            sub_domain = amplify.SubDomain(
                branch=branch,
            
                # the properties below are optional
                prefix="prefix"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd5a132a499029eea877f8448bb2a355b95e4b65fd5f983108cd1ddb458a8698)
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
            check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "branch": branch,
        }
        if prefix is not None:
            self._values["prefix"] = prefix

    @builtins.property
    def branch(self) -> IBranch:
        '''(experimental) The branch.

        :stability: experimental
        '''
        result = self._values.get("branch")
        assert result is not None, "Required property 'branch' is missing"
        return typing.cast(IBranch, result)

    @builtins.property
    def prefix(self) -> typing.Optional[builtins.str]:
        '''(experimental) The prefix.

        Use '' to map to the root of the domain

        :default: - the branch name

        :stability: experimental
        '''
        result = self._values.get("prefix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SubDomain(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IApp, _IGrantable_4c5a91d1)
class App(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.App",
):
    '''(experimental) An Amplify Console application.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                patterns=["feature/*", "test/*"]),
            auto_branch_deletion=True
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app_name: typing.Optional[builtins.str] = None,
        auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
        auto_branch_deletion: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
        custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        source_code_provider: typing.Optional[ISourceCodeProvider] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app_name: (experimental) The name for the application. Default: - a CDK generated name
        :param auto_branch_creation: (experimental) The auto branch creation configuration. Use this to automatically create branches that match a certain pattern. Default: - no auto branch creation
        :param auto_branch_deletion: (experimental) Automatically disconnect a branch in the Amplify Console when you delete a branch from your Git repository. Default: false
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection at an app level to all your branches. Default: - no password protection
        :param build_spec: (experimental) BuildSpec for the application. Alternatively, add a ``amplify.yml`` file to the repository. Default: - no build spec
        :param custom_response_headers: (experimental) The custom HTTP response headers for an Amplify app. Default: - no custom response headers
        :param custom_rules: (experimental) Custom rewrite/redirect rules for the application. Default: - no custom rewrite/redirect rules
        :param description: (experimental) A description for the application. Default: - no description
        :param environment_variables: (experimental) Environment variables for the application. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - no environment variables
        :param role: (experimental) The IAM service role to associate with the application. The App implements IGrantable. Default: - a new role is created
        :param source_code_provider: (experimental) The source code provider for this application. Default: - not connected to a source code provider

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__56a3027633886462440d9711ae64b6b0266f1ddcafb8abc3553758ca0d81bba4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = AppProps(
            app_name=app_name,
            auto_branch_creation=auto_branch_creation,
            auto_branch_deletion=auto_branch_deletion,
            basic_auth=basic_auth,
            build_spec=build_spec,
            custom_response_headers=custom_response_headers,
            custom_rules=custom_rules,
            description=description,
            environment_variables=environment_variables,
            role=role,
            source_code_provider=source_code_provider,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromAppId")
    @builtins.classmethod
    def from_app_id(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        app_id: builtins.str,
    ) -> IApp:
        '''(experimental) Import an existing application.

        :param scope: -
        :param id: -
        :param app_id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__84d7ffb8cd5281aaad35b02e166f1524091922bb8019458be60d7f0288d4ca42)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument app_id", value=app_id, expected_type=type_hints["app_id"])
        return typing.cast(IApp, jsii.sinvoke(cls, "fromAppId", [scope, id, app_id]))

    @jsii.member(jsii_name="addAutoBranchEnvironment")
    def add_auto_branch_environment(
        self,
        name: builtins.str,
        value: builtins.str,
    ) -> "App":
        '''(experimental) Adds an environment variable to the auto created branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ab225937b70a3468893f4b338550c1e03f39d358ffd2cbbfbc29505c17738e4)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addAutoBranchEnvironment", [name, value]))

    @jsii.member(jsii_name="addBranch")
    def add_branch(
        self,
        id: builtins.str,
        *,
        asset: typing.Optional[_Asset_d07e8c00] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> "Branch":
        '''(experimental) Adds a branch to this application.

        :param id: -
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a5e574853f21f489daf4f6ed4dbfd0b5b21800d67cfb4a066638c5a41ae27bcd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = BranchOptions(
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            stage=stage,
        )

        return typing.cast("Branch", jsii.invoke(self, "addBranch", [id, options]))

    @jsii.member(jsii_name="addCustomRule")
    def add_custom_rule(self, rule: CustomRule) -> "App":
        '''(experimental) Adds a custom rewrite/redirect rule to this application.

        :param rule: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f9fcf80c120c5e149883e9cad67aa44011806d3951848501953d3d7cfac19d9f)
            check_type(argname="argument rule", value=rule, expected_type=type_hints["rule"])
        return typing.cast("App", jsii.invoke(self, "addCustomRule", [rule]))

    @jsii.member(jsii_name="addDomain")
    def add_domain(
        self,
        id: builtins.str,
        *,
        auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
        domain_name: typing.Optional[builtins.str] = None,
        enable_auto_subdomain: typing.Optional[builtins.bool] = None,
        sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> Domain:
        '''(experimental) Adds a domain to this application.

        :param id: -
        :param auto_subdomain_creation_patterns: (experimental) Branches which should automatically create subdomains. Default: - all repository branches ['*', 'pr*']
        :param domain_name: (experimental) The name of the domain. Default: - the construct's id
        :param enable_auto_subdomain: (experimental) Automatically create subdomains for connected branches. Default: false
        :param sub_domains: (experimental) Subdomains. Default: - use ``addSubDomain()`` to add subdomains

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5422655ecee9bc71dfca63c7b69dea00a3e9d846e442b79e70b64b1ce51694a8)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = DomainOptions(
            auto_subdomain_creation_patterns=auto_subdomain_creation_patterns,
            domain_name=domain_name,
            enable_auto_subdomain=enable_auto_subdomain,
            sub_domains=sub_domains,
        )

        return typing.cast(Domain, jsii.invoke(self, "addDomain", [id, options]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "App":
        '''(experimental) Adds an environment variable to this application.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b74cf945f7de715193137a5bf206f75e4735d2636c7831654cf9f7e498f19cd)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("App", jsii.invoke(self, "addEnvironment", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="appId")
    def app_id(self) -> builtins.str:
        '''(experimental) The application id.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "appId"))

    @builtins.property
    @jsii.member(jsii_name="appName")
    def app_name(self) -> builtins.str:
        '''(experimental) The name of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "appName"))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="defaultDomain")
    def default_domain(self) -> builtins.str:
        '''(experimental) The default domain of the application.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "defaultDomain"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))


@jsii.implements(IBranch)
class Branch(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.Branch",
):
    '''(experimental) An Amplify Console branch.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # amplify_app: amplify.App
        
        
        master = amplify_app.add_branch("master") # `id` will be used as repo branch name
        dev = amplify_app.add_branch("dev",
            performance_mode=True
        )
        dev.add_environment("STAGE", "dev")
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        app: IApp,
        asset: typing.Optional[_Asset_d07e8c00] = None,
        auto_build: typing.Optional[builtins.bool] = None,
        basic_auth: typing.Optional[BasicAuth] = None,
        branch_name: typing.Optional[builtins.str] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        description: typing.Optional[builtins.str] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        performance_mode: typing.Optional[builtins.bool] = None,
        pull_request_environment_name: typing.Optional[builtins.str] = None,
        pull_request_preview: typing.Optional[builtins.bool] = None,
        stage: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param app: (experimental) The application within which the branch must be created.
        :param asset: (experimental) Asset for deployment. The Amplify app must not have a sourceCodeProvider configured as this resource uses Amplify's startDeployment API to initiate and deploy a S3 asset onto the App. Default: - no asset
        :param auto_build: (experimental) Whether to enable auto building for the branch. Default: true
        :param basic_auth: (experimental) The Basic Auth configuration. Use this to set password protection for the branch Default: - no password protection
        :param branch_name: (experimental) The name of the branch. Default: - the construct's id
        :param build_spec: (experimental) BuildSpec for the branch. Default: - no build spec
        :param description: (experimental) A description for the branch. Default: - no description
        :param environment_variables: (experimental) Environment variables for the branch. All environment variables that you add are encrypted to prevent rogue access so you can use them to store secret information. Default: - application environment variables
        :param performance_mode: (experimental) Enables performance mode for the branch. Performance mode optimizes for faster hosting performance by keeping content cached at the edge for a longer interval. When performance mode is enabled, hosting configuration or code changes can take up to 10 minutes to roll out. Default: false
        :param pull_request_environment_name: (experimental) The dedicated backend environment for the pull request previews. Default: - automatically provision a temporary backend
        :param pull_request_preview: (experimental) Whether to enable pull request preview for the branch. Default: true
        :param stage: (experimental) Stage for the branch. Default: - no stage

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__10ee070971d47b4cf5bdb23407ae8e5b9d9bb77ec466ba6ef0571196048365f0)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BranchProps(
            app=app,
            asset=asset,
            auto_build=auto_build,
            basic_auth=basic_auth,
            branch_name=branch_name,
            build_spec=build_spec,
            description=description,
            environment_variables=environment_variables,
            performance_mode=performance_mode,
            pull_request_environment_name=pull_request_environment_name,
            pull_request_preview=pull_request_preview,
            stage=stage,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="fromBranchName")
    @builtins.classmethod
    def from_branch_name(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        branch_name: builtins.str,
    ) -> IBranch:
        '''(experimental) Import an existing branch.

        :param scope: -
        :param id: -
        :param branch_name: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e264d47e0fec34da9ad37df148f875636925737b031b3356109ce15828b80ad6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument branch_name", value=branch_name, expected_type=type_hints["branch_name"])
        return typing.cast(IBranch, jsii.sinvoke(cls, "fromBranchName", [scope, id, branch_name]))

    @jsii.member(jsii_name="addEnvironment")
    def add_environment(self, name: builtins.str, value: builtins.str) -> "Branch":
        '''(experimental) Adds an environment variable to this branch.

        All environment variables that you add are encrypted to prevent rogue
        access so you can use them to store secret information.

        :param name: -
        :param value: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35113950b120739f77f7fda77f4d45a1aa34a1328b0aa1f2af8b483c6a0f75e1)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("Branch", jsii.invoke(self, "addEnvironment", [name, value]))

    @builtins.property
    @jsii.member(jsii_name="arn")
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the branch.

        :stability: experimental
        :attribute: true
        '''
        return typing.cast(builtins.str, jsii.get(self, "arn"))

    @builtins.property
    @jsii.member(jsii_name="branchName")
    def branch_name(self) -> builtins.str:
        '''(experimental) The name of the branch.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "branchName"))


@jsii.implements(ISourceCodeProvider)
class CodeCommitSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.CodeCommitSourceCodeProvider",
):
    '''(experimental) CodeCommit source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as codecommit
        
        
        repository = codecommit.Repository(self, "Repo",
            repository_name="my-repo"
        )
        
        amplify_app = amplify.App(self, "App",
            source_code_provider=amplify.CodeCommitSourceCodeProvider(repository=repository)
        )
    '''

    def __init__(self, *, repository: _IRepository_cdb2a3c0) -> None:
        '''
        :param repository: (experimental) The CodeCommit repository.

        :stability: experimental
        '''
        props = CodeCommitSourceCodeProviderProps(repository=repository)

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a82a2b88b3da6a96fc72a4927f6f29660802641e102567bd4e4091392ef00c78)
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [app]))


@jsii.implements(ISourceCodeProvider)
class GitHubSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.GitHubSourceCodeProvider",
):
    '''(experimental) GitHub source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitHubSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-github-token")
            ),
            auto_branch_creation=amplify.aws_amplify.AutoBranchCreation( # Automatically connect branches that match a pattern set
                patterns=["feature/*", "test/*"]),
            auto_branch_deletion=True
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _SecretValue_c18506ef,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitHubSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1fc94697438547ad019064569a1b73de73c06ef622e975c18a62cac7cd500be8)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


@jsii.implements(ISourceCodeProvider)
class GitLabSourceCodeProvider(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_amplify.GitLabSourceCodeProvider",
):
    '''(experimental) GitLab source code provider.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        amplify_app = amplify.App(self, "MyApp",
            source_code_provider=amplify.GitLabSourceCodeProvider(
                owner="<user>",
                repository="<repo>",
                oauth_token=SecretValue.secrets_manager("my-gitlab-token")
            )
        )
    '''

    def __init__(
        self,
        *,
        oauth_token: _SecretValue_c18506ef,
        owner: builtins.str,
        repository: builtins.str,
    ) -> None:
        '''
        :param oauth_token: (experimental) A personal access token with the ``repo`` scope.
        :param owner: (experimental) The user or organization owning the repository.
        :param repository: (experimental) The name of the repository.

        :stability: experimental
        '''
        props = GitLabSourceCodeProviderProps(
            oauth_token=oauth_token, owner=owner, repository=repository
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(self, _app: App) -> SourceCodeProviderConfig:
        '''(experimental) Binds the source code provider to an app.

        :param _app: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9df7d127d3fe5f641af76fb6fdea99ac056b4d541b4a4638ff0d97fccf811942)
            check_type(argname="argument _app", value=_app, expected_type=type_hints["_app"])
        return typing.cast(SourceCodeProviderConfig, jsii.invoke(self, "bind", [_app]))


__all__ = [
    "App",
    "AppProps",
    "AutoBranchCreation",
    "BasicAuth",
    "BasicAuthConfig",
    "BasicAuthProps",
    "Branch",
    "BranchOptions",
    "BranchProps",
    "CfnApp",
    "CfnAppProps",
    "CfnBranch",
    "CfnBranchProps",
    "CfnDomain",
    "CfnDomainProps",
    "CodeCommitSourceCodeProvider",
    "CodeCommitSourceCodeProviderProps",
    "CustomResponseHeader",
    "CustomRule",
    "CustomRuleOptions",
    "Domain",
    "DomainOptions",
    "DomainProps",
    "GitHubSourceCodeProvider",
    "GitHubSourceCodeProviderProps",
    "GitLabSourceCodeProvider",
    "GitLabSourceCodeProviderProps",
    "IApp",
    "IBranch",
    "ISourceCodeProvider",
    "RedirectStatus",
    "SourceCodeProviderConfig",
    "SubDomain",
]

publication.publish()

def _typecheckingstub__51b008d8c501a3fb80936a4402973c0ed701b2981e76314db3652ff2fa00f16f(
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50ee861bf2b9208b9ce76bd1b3369c220c0503dac241a80278efe14a39c03ff7(
    *,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d98c9cf1ee25f79a9d30372ae0c3b4216c527fc9f2c585794b4ec0d11d14e6fd(
    username: builtins.str,
    password: _SecretValue_c18506ef,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__619987267cc501f89370ec9cb33aacd01f36ac840fbc9a620eb14ba01b49a1af(
    username: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38d36803115a5e2a9321b8f72998709dd5f0f7492a6fe1aa489b787b54a367f5(
    scope: _Construct_e78e779f,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9d84e31c133918c5cf9278a488870b2f4ad9803b05caceee2773dc6cbbbcd93d(
    *,
    enable_basic_auth: builtins.bool,
    password: builtins.str,
    username: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ec3ec350e2d049489cf569ac3bd615bed42401899f72f21e263529d58f7f30e(
    *,
    username: builtins.str,
    encryption_key: typing.Optional[_IKey_36930160] = None,
    password: typing.Optional[_SecretValue_c18506ef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9f17bd266f6ab219e1769ee96b2c0f1aac33cae5337b7fd876126790cde69bc(
    *,
    asset: typing.Optional[_Asset_d07e8c00] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c64a504c40cc03256dce78384fbff64892846aa9a6f87230706679585a33e024(
    *,
    asset: typing.Optional[_Asset_d07e8c00] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
    app: IApp,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__434fc35643e44a8d85c957c4bafa2785507f2009420463b5ec659229ca499e66(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    auto_branch_creation_config: typing.Optional[typing.Union[typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_headers: typing.Optional[builtins.str] = None,
    custom_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    iam_service_role: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c82756d0f09741bd83b20baa9923154dab15a410564b8be08b2c6dfc4f302375(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59398f606cc7e89a28726621091ef7790dac5e234832474c9aa663e8a6c3dac0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c59a9ec217b574b2095ac58a6cfed31b053c9c541342c6a7643f3d6daa17c5bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__692e591f5e2e535a63be678f88cd1deb7dd4c35afcfb718f5275846cb90bdbc3(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a92a2bd547aac90f83a4587ce5eafbe912b92ea07a0a49813b097b5e95f3ce4(
    value: typing.Optional[typing.Union[CfnApp.AutoBranchCreationConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e25ec07f80855a4967ee3cbcbcec0c097ad31c6e2bfe3ad7a7262929757c862(
    value: typing.Optional[typing.Union[CfnApp.BasicAuthConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0261626ea69802002557a4142765dd8322168847532d687be0d7a4bbd6d1ed(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8fde630eeae83e612b0dfc05467cb7f166e847f3a310293b9ddf3f2b55b9a17(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d6ce472b3b90f105077ca01bb24681443b12b8d8451d2c3734345252cc997261(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.CustomRuleProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbf65fef26cbe8a191c92daf4fb6725a4b14f08e521356c143731f0e9d767879(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac0b22f44e7c4d3e5445474298c096e5db88f3967e9f9f71ca93da018f26efe7(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44c4106e24f4930d06000f76f6d6d60907376f3d63ffc3db17172178c3db0201(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnApp.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cfa683aabc670dad5c9fa8ffe806f5dcdddcd7303da329b3567f8060fc5eb95(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cdd0160536b19d3a6088423e69485bfd8487f659e34d72c8fe7c7bf5d71b4d2a(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9eb2bbe8a91f76aa244cc8128f4de636a20b85f9fc4d976b736d15f70e987c79(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__46796368cef5b63f54c91b076ace69732b6e4bd0d64d6649d355834a65e70295(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aaf0f556530f782682e2bde081ea20fe9c58fa6cf27d97e7449987004e4d12a9(
    *,
    auto_branch_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    enable_auto_branch_creation: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a4cbb2215ee3d6015fb9cb431fc49fc69edc55b3cf1b0beed92596bea90cc849(
    *,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    password: typing.Optional[builtins.str] = None,
    username: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd5f9ca5c14cac075735bfeef56cb13d07593bcca30ff5c4cc9212046d72bec2(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a498db20f59b442a77ceb6978d5f464308a3c7cc049f066c2adadab83e92c702(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a3fa23d8f314a9d4082aac6f5c6c9593e22d122ab628a2366ce6591afee4c05f(
    *,
    name: builtins.str,
    access_token: typing.Optional[builtins.str] = None,
    auto_branch_creation_config: typing.Optional[typing.Union[typing.Union[CfnApp.AutoBranchCreationConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnApp.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    custom_headers: typing.Optional[builtins.str] = None,
    custom_rules: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.CustomRuleProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    description: typing.Optional[builtins.str] = None,
    enable_branch_auto_deletion: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnApp.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    iam_service_role: typing.Optional[builtins.str] = None,
    oauth_token: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e22906e6f314a306082ab5ca373434ac23e808020cd7513e57a2e3514a41ffef(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    app_id: builtins.str,
    branch_name: builtins.str,
    basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a08f9b5abfa218705c88c36062454896b1790b0e7384e78ec8b206bc0aee0506(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42e5434c62c34083b9ad0ad56612036b464d26bf2555147eee8e1016971401dd(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d12c122d429411ba51e8ece31c3d607507b49cc8a02a0f933de29d4ea067acfd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__337f911fe0bb76e9d91a457789e55e8b33a14d578bc60b9a38072160b2ef4c08(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbda3eeea41eb763fa37a0331309894c15a391483a2062ccbbe2f31d8dc76d5e(
    value: typing.Optional[typing.Union[CfnBranch.BasicAuthConfigProperty, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b057554ba08e06e643c5d745a4471d362a122dde2e3a9074f6c3cbe28b403423(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5869eda006f2853567f86d2d1a81323ebab97b912e0919af29ba0f8c23a76198(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a9db0fbb5ab490a40d5c3d74f5a5c786822f390016c5a652b42336924f5f3d48(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b41610d8e65ac49de38c07f7254b03e90d7ad49f83d85def9a8ff7f2411eebb5(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bdea46c375aa57e6245c6fb1d2ecb0c6a484328e9ec617aae6d1f46ec143b722(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d430629ca4d978c3cf14632116d782c10a25ed44f678eb5aff4792d0706a0834(
    value: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnBranch.EnvironmentVariableProperty, _IResolvable_a771d0ef]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__903bf6daade000df2db23f9d75490fe010ff0969a220d3db52cadb7d716587c0(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__243c9b879c11e2a81997242fb14de7627070a0bc396117ab8507fa113fe65124(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1b90995678806d4268be9becd79e024c4daa59d185d36547bda43acfc2bb5d2f(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0147d3cc5c7cdbb6b5faa2607b976c71e93c3e4aa0025eb73772eba56c26b3e3(
    *,
    password: builtins.str,
    username: builtins.str,
    enable_basic_auth: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fea7d77d1bd8b1fa5dab055dee38eac5b174641a05f335cc737ecc327f8f4ff(
    *,
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24f17b52e1d63abdc4a206fd2a13a8c94c1f92fe5fc5ca837b11f5ae50c7a552(
    *,
    app_id: builtins.str,
    branch_name: builtins.str,
    basic_auth_config: typing.Optional[typing.Union[typing.Union[CfnBranch.BasicAuthConfigProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]] = None,
    build_spec: typing.Optional[builtins.str] = None,
    description: typing.Optional[builtins.str] = None,
    enable_auto_build: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_performance_mode: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    enable_pull_request_preview: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
    environment_variables: typing.Optional[typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnBranch.EnvironmentVariableProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]]] = None,
    framework: typing.Optional[builtins.str] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    stage: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_CfnTag_95fbdc29, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a612a4128896bb966b8ef1945fcb8bae3ca1ea3de63ccba9c7ab998d401a48ee(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain_settings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
    enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f6ebaf849f6a4b3da1a4d6fbf3982a9b12334bdcf529423b1e5ac0aa01a0154(
    inspector: _TreeInspector_1cd1894e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8976d6ef36cae5f579630d3044cdf17e594d31501251bcfcc2cd085b4bd8468a(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca667eb08871111d25c9213b4468b694b42ac7067adca0a7d104a85537d52c27(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a17079458a6f870ed963a275e80113d43a19893575da51f25bbcfdc72f266e01(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1806885de5be192c9e16b247cdcdc44a7b3bc351328d588dfd13b60673004039(
    value: typing.Union[_IResolvable_a771d0ef, typing.List[typing.Union[CfnDomain.SubDomainSettingProperty, _IResolvable_a771d0ef]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__be33644166d41cc01397ca93000e26dbaf34d48e0b8b2607eb12337df9297d43(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0eb326101c1aad0647ab4fb2e8ac7f377cf9e1036b89a4f8a8db01b7be1e6e8c(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da9d0350be0ca93fc88cccef74512d96d01e8b09386799600d3696125d6b32d6(
    value: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d244440484546b32ae4623efb4089d13990dd070ab694600d8fc32df2242743a(
    *,
    branch_name: builtins.str,
    prefix: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__da8febeb0d0a7befa7e9382025b5656388988688f9e0662e34454cf204a4a4bf(
    *,
    app_id: builtins.str,
    domain_name: builtins.str,
    sub_domain_settings: typing.Union[_IResolvable_a771d0ef, typing.Sequence[typing.Union[typing.Union[CfnDomain.SubDomainSettingProperty, typing.Dict[builtins.str, typing.Any]], _IResolvable_a771d0ef]]],
    auto_sub_domain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    auto_sub_domain_iam_role: typing.Optional[builtins.str] = None,
    enable_auto_sub_domain: typing.Optional[typing.Union[builtins.bool, _IResolvable_a771d0ef]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5852be3beca47e381e011a9bfca854d7f75b0e81705c3489e2f0ee797290c952(
    *,
    repository: _IRepository_cdb2a3c0,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f9c327c9a6b08787ccd6806194d7ba422fc108ab1416697df50be5e2464f12e(
    *,
    headers: typing.Mapping[builtins.str, builtins.str],
    pattern: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d00fc5f798f803310b7ba418930b31919f8b8d9e308e4bb9baaed6f55c3f1367(
    *,
    source: builtins.str,
    target: builtins.str,
    condition: typing.Optional[builtins.str] = None,
    status: typing.Optional[RedirectStatus] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e8092228538277a79a30edbb0b3a26474e47f93d98d37bb95371c32c2c59ba2e(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_IRole_59af6f50] = None,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2dc6fb652f4a13cbc17a9729c2741ca3a9b9dd661a6334d7401824cd7a0a77af(
    branch: IBranch,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__24450ddf502a17c78cda483f35858e07ee28d3458d4567453bd3eb983218f8ad(
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7250a71dde68e5a45257b779ec6ca0fe50a1b50dcc5b076d638ec13c0a10344d(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b81eee0f9442b5fd8115685a5dd279fc18205b5f29fd20db7e28a961040c19e0(
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
    app: IApp,
    auto_sub_domain_iam_role: typing.Optional[_IRole_59af6f50] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__71709197ed7b4dacbbdda6e3f7d9c8a0592e66716e0288f2d8b4fc37d7606db0(
    *,
    oauth_token: _SecretValue_c18506ef,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b5030802eab58f0d1cce5ccdbc7c633f63ccbddd76ad6443f24f90069c62bc56(
    *,
    oauth_token: _SecretValue_c18506ef,
    owner: builtins.str,
    repository: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c92443503479ba23727d684d5fb140a6d6cb6e5322a229d0c9c8ba655f49eaed(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1cc076493484abfa9208f91039353a73e013f10ac61617e1fa9bb4fb98a03cb8(
    *,
    repository: builtins.str,
    access_token: typing.Optional[_SecretValue_c18506ef] = None,
    oauth_token: typing.Optional[_SecretValue_c18506ef] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd5a132a499029eea877f8448bb2a355b95e4b65fd5f983108cd1ddb458a8698(
    *,
    branch: IBranch,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__56a3027633886462440d9711ae64b6b0266f1ddcafb8abc3553758ca0d81bba4(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app_name: typing.Optional[builtins.str] = None,
    auto_branch_creation: typing.Optional[typing.Union[AutoBranchCreation, typing.Dict[builtins.str, typing.Any]]] = None,
    auto_branch_deletion: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    custom_response_headers: typing.Optional[typing.Sequence[typing.Union[CustomResponseHeader, typing.Dict[builtins.str, typing.Any]]]] = None,
    custom_rules: typing.Optional[typing.Sequence[CustomRule]] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    source_code_provider: typing.Optional[ISourceCodeProvider] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__84d7ffb8cd5281aaad35b02e166f1524091922bb8019458be60d7f0288d4ca42(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    app_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ab225937b70a3468893f4b338550c1e03f39d358ffd2cbbfbc29505c17738e4(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a5e574853f21f489daf4f6ed4dbfd0b5b21800d67cfb4a066638c5a41ae27bcd(
    id: builtins.str,
    *,
    asset: typing.Optional[_Asset_d07e8c00] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f9fcf80c120c5e149883e9cad67aa44011806d3951848501953d3d7cfac19d9f(
    rule: CustomRule,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5422655ecee9bc71dfca63c7b69dea00a3e9d846e442b79e70b64b1ce51694a8(
    id: builtins.str,
    *,
    auto_subdomain_creation_patterns: typing.Optional[typing.Sequence[builtins.str]] = None,
    domain_name: typing.Optional[builtins.str] = None,
    enable_auto_subdomain: typing.Optional[builtins.bool] = None,
    sub_domains: typing.Optional[typing.Sequence[typing.Union[SubDomain, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b74cf945f7de715193137a5bf206f75e4735d2636c7831654cf9f7e498f19cd(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__10ee070971d47b4cf5bdb23407ae8e5b9d9bb77ec466ba6ef0571196048365f0(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    app: IApp,
    asset: typing.Optional[_Asset_d07e8c00] = None,
    auto_build: typing.Optional[builtins.bool] = None,
    basic_auth: typing.Optional[BasicAuth] = None,
    branch_name: typing.Optional[builtins.str] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    description: typing.Optional[builtins.str] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    performance_mode: typing.Optional[builtins.bool] = None,
    pull_request_environment_name: typing.Optional[builtins.str] = None,
    pull_request_preview: typing.Optional[builtins.bool] = None,
    stage: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e264d47e0fec34da9ad37df148f875636925737b031b3356109ce15828b80ad6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    branch_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35113950b120739f77f7fda77f4d45a1aa34a1328b0aa1f2af8b483c6a0f75e1(
    name: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a82a2b88b3da6a96fc72a4927f6f29660802641e102567bd4e4091392ef00c78(
    app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1fc94697438547ad019064569a1b73de73c06ef622e975c18a62cac7cd500be8(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9df7d127d3fe5f641af76fb6fdea99ac056b4d541b4a4638ff0d97fccf811942(
    _app: App,
) -> None:
    """Type checking stubs"""
    pass
