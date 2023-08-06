'''
# Amazon Lambda Python Library

This library provides constructs for Python Lambda functions.

To use this module, you will need to have Docker installed.

## Python Function

Define a `PythonFunction`:

```python
lambda_.PythonFunction(self, "MyFunction",
    entry="/path/to/my/function",  # required
    runtime=Runtime.PYTHON_3_8,  # required
    index="my_index.py",  # optional, defaults to 'index.py'
    handler="my_exported_func"
)
```

All other properties of `lambda.Function` are supported, see also the [AWS Lambda construct library](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-lambda).

## Python Layer

You may create a python-based lambda layer with `PythonLayerVersion`. If `PythonLayerVersion` detects a `requirements.txt`
or `Pipfile` or `poetry.lock` with the associated `pyproject.toml` at the entry path, then `PythonLayerVersion` will include the dependencies inline with your code in the
layer.

Define a `PythonLayerVersion`:

```python
lambda_.PythonLayerVersion(self, "MyLayer",
    entry="/path/to/my/layer"
)
```

A layer can also be used as a part of a `PythonFunction`:

```python
lambda_.PythonFunction(self, "MyFunction",
    entry="/path/to/my/function",
    runtime=Runtime.PYTHON_3_8,
    layers=[
        lambda_.PythonLayerVersion(self, "MyLayer",
            entry="/path/to/my/layer"
        )
    ]
)
```

## Packaging

If `requirements.txt`, `Pipfile` or `poetry.lock` exists at the entry path, the construct will handle installing all required modules in a [Lambda compatible Docker container](https://gallery.ecr.aws/sam/build-python3.7) according to the `runtime` and with the Docker platform based on the target architecture of the Lambda function.

Python bundles are only recreated and published when a file in a source directory has changed.
Therefore (and as a general best-practice), it is highly recommended to commit a lockfile with a
list of all transitive dependencies and their exact versions. This will ensure that when any dependency version is updated, the bundle asset is recreated and uploaded.

To that end, we recommend using [`pipenv`] or [`poetry`] which have lockfile support.

* [`pipenv`](https://pipenv-fork.readthedocs.io/en/latest/basics.html#example-pipfile-lock)
* [`poetry`](https://python-poetry.org/docs/basic-usage/#commit-your-poetrylock-file-to-version-control)

Packaging is executed using the `Packaging` class, which:

1. Infers the packaging type based on the files present.
2. If it sees a `Pipfile` or a `poetry.lock` file, it exports it to a compatible `requirements.txt` file with credentials (if they're available in the source files or in the bundling container).
3. Installs dependencies using `pip`.
4. Copies the dependencies into an asset that is bundled for the Lambda package.

**Lambda with a requirements.txt**

```plaintext
.
├── lambda_function.py # exports a function named 'handler'
├── requirements.txt # has to be present at the entry path
```

**Lambda with a Pipfile**

```plaintext
.
├── lambda_function.py # exports a function named 'handler'
├── Pipfile # has to be present at the entry path
├── Pipfile.lock # your lock file
```

**Lambda with a poetry.lock**

```plaintext
.
├── lambda_function.py # exports a function named 'handler'
├── pyproject.toml # your poetry project definition
├── poetry.lock # your poetry lock file has to be present at the entry path
```

## Custom Bundling

Custom bundling can be performed by passing in additional build arguments that point to index URLs to private repos, or by using an entirely custom Docker images for bundling dependencies. The build args currently supported are:

* `PIP_INDEX_URL`
* `PIP_EXTRA_INDEX_URL`
* `HTTPS_PROXY`

Additional build args for bundling that refer to PyPI indexes can be specified as:

```python
entry = "/path/to/function"
image = DockerImage.from_build(entry)

lambda_.PythonFunction(self, "function",
    entry=entry,
    runtime=Runtime.PYTHON_3_8,
    bundling=lambda.aws_lambda_python.BundlingOptions(
        build_args={"PIP_INDEX_URL": "https://your.index.url/simple/", "PIP_EXTRA_INDEX_URL": "https://your.extra-index.url/simple/"}
    )
)
```

If using a custom Docker image for bundling, the dependencies are installed with `pip`, `pipenv` or `poetry` by using the `Packaging` class. A different bundling Docker image that is in the same directory as the function can be specified as:

```python
entry = "/path/to/function"
image = DockerImage.from_build(entry)

lambda_.PythonFunction(self, "function",
    entry=entry,
    runtime=Runtime.PYTHON_3_8,
    bundling=lambda.aws_lambda_python.BundlingOptions(image=image)
)
```

## Custom Bundling with Code Artifact

To use a Code Artifact PyPI repo, the `PIP_INDEX_URL` for bundling the function can be customized (requires AWS CLI in the build environment):

```python
from child_process import exec_sync


entry = "/path/to/function"
image = DockerImage.from_build(entry)

domain = "my-domain"
domain_owner = "111122223333"
repo_name = "my_repo"
region = "us-east-1"
code_artifact_auth_token = exec_sync(f"aws codeartifact get-authorization-token --domain {domain} --domain-owner {domainOwner} --query authorizationToken --output text").to_string().trim()

index_url = f"https://aws:{codeArtifactAuthToken}@{domain}-{domainOwner}.d.codeartifact.{region}.amazonaws.com/pypi/{repoName}/simple/"

lambda_.PythonFunction(self, "function",
    entry=entry,
    runtime=Runtime.PYTHON_3_8,
    bundling=lambda.aws_lambda_python.BundlingOptions(
        environment={"PIP_INDEX_URL": index_url}
    )
)
```

The index URL or the token are only used during bundling and thus not included in the final asset. Setting only environment variable for `PIP_INDEX_URL` or `PIP_EXTRA_INDEX_URL` should work for accesing private Python repositories with `pip`, `pipenv` and `poetry` based dependencies.

If you also want to use the Code Artifact repo for building the base Docker image for bundling, use `buildArgs`. However, note that setting custom build args for bundling will force the base bundling image to be rebuilt every time (i.e. skip the Docker cache). Build args can be customized as:

```python
from child_process import exec_sync


entry = "/path/to/function"
image = DockerImage.from_build(entry)

domain = "my-domain"
domain_owner = "111122223333"
repo_name = "my_repo"
region = "us-east-1"
code_artifact_auth_token = exec_sync(f"aws codeartifact get-authorization-token --domain {domain} --domain-owner {domainOwner} --query authorizationToken --output text").to_string().trim()

index_url = f"https://aws:{codeArtifactAuthToken}@{domain}-{domainOwner}.d.codeartifact.{region}.amazonaws.com/pypi/{repoName}/simple/"

lambda_.PythonFunction(self, "function",
    entry=entry,
    runtime=Runtime.PYTHON_3_8,
    bundling=lambda.aws_lambda_python.BundlingOptions(
        build_args={"PIP_INDEX_URL": index_url}
    )
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

from .. import (
    AssetHashType as _AssetHashType_49193809,
    Construct as _Construct_e78e779f,
    DockerImage as _DockerImage_d5f0ad8e,
    Duration as _Duration_070aa057,
    RemovalPolicy as _RemovalPolicy_c97e7a20,
    Size as _Size_7fbd4337,
)
from ..aws_codeguruprofiler import IProfilingGroup as _IProfilingGroup_418eb20c
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_iam import (
    IRole as _IRole_59af6f50, PolicyStatement as _PolicyStatement_296fe8a3
)
from ..aws_kms import IKey as _IKey_36930160
from ..aws_lambda import (
    Architecture as _Architecture_24056b62,
    FileSystem as _FileSystem_17be1f4c,
    Function as _Function_40b20aa5,
    FunctionOptions as _FunctionOptions_dc75a392,
    ICodeSigningConfig as _ICodeSigningConfig_5d77bccf,
    IDestination as _IDestination_7f253ff1,
    IEventSource as _IEventSource_7914870e,
    ILayerVersion as _ILayerVersion_b2b86380,
    LambdaInsightsVersion as _LambdaInsightsVersion_2966e73b,
    LayerVersion as _LayerVersion_34d6006f,
    LayerVersionOptions as _LayerVersionOptions_15d6ea62,
    LogRetentionRetryOptions as _LogRetentionRetryOptions_7acc40ab,
    Runtime as _Runtime_932d369a,
    Tracing as _Tracing_b7f4a8b6,
    VersionOptions as _VersionOptions_085bb455,
)
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_python.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset_hash": "assetHash",
        "asset_hash_type": "assetHashType",
        "build_args": "buildArgs",
        "environment": "environment",
        "image": "image",
        "output_path_suffix": "outputPathSuffix",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        image: typing.Optional[_DockerImage_d5f0ad8e] = None,
        output_path_suffix: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for bundling.

        :param asset_hash: (experimental) Specify a custom hash for this asset. If ``assetHashType`` is set it must be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - Based on ``assetHashType``
        :param asset_hash_type: (experimental) Determines how asset hash is calculated. Assets will get rebuild and uploaded only if their hash has changed. If asset hash is set to ``SOURCE`` (default), then only changes to the source directory will cause the asset to rebuild. This means, for example, that in order to pick up a new dependency version, a change must be made to the source tree. Ideally, this can be implemented by including a dependency lockfile in your source tree or using fixed dependencies. If the asset hash is set to ``OUTPUT``, the hash is calculated after bundling. This means that any change in the output will cause the asset to be invalidated and uploaded. Bear in mind that ``pip`` adds timestamps to dependencies it installs, which implies that in this mode Python bundles will *always* get rebuild and uploaded. Normally this is an anti-pattern since build Default: AssetHashType.SOURCE By default, hash is calculated based on the contents of the source directory. This means that only updates to the source will cause the asset to rebuild.
        :param build_args: (experimental) Optional build arguments to pass to the default container. This can be used to customize the index URLs used for installing dependencies. This is not used if a custom image is provided. Default: - No build arguments.
        :param environment: (experimental) Environment variables defined when bundling runs. Default: - no environment variables are defined.
        :param image: (experimental) Docker image to use for bundling. If no options are provided, the default bundling image will be used. Dependencies will be installed using the default packaging commands and copied over from into the Lambda asset. Default: - Default bundling image.
        :param output_path_suffix: (experimental) Output path suffix: the suffix for the directory into which the bundled output is written. Default: - 'python' for a layer, empty string otherwise.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            entry = "/path/to/function"
            image = DockerImage.from_build(entry)
            
            lambda_.PythonFunction(self, "function",
                entry=entry,
                runtime=Runtime.PYTHON_3_8,
                bundling=lambda.aws_lambda_python.BundlingOptions(
                    build_args={"PIP_INDEX_URL": "https://your.index.url/simple/", "PIP_EXTRA_INDEX_URL": "https://your.extra-index.url/simple/"}
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ac4e0436c2309daa08b5de4d684582f00c5585d82ea6af18f9e4d2b7518ce1)
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument asset_hash_type", value=asset_hash_type, expected_type=type_hints["asset_hash_type"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument output_path_suffix", value=output_path_suffix, expected_type=type_hints["output_path_suffix"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if asset_hash_type is not None:
            self._values["asset_hash_type"] = asset_hash_type
        if build_args is not None:
            self._values["build_args"] = build_args
        if environment is not None:
            self._values["environment"] = environment
        if image is not None:
            self._values["image"] = image
        if output_path_suffix is not None:
            self._values["output_path_suffix"] = output_path_suffix

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify a custom hash for this asset.

        If ``assetHashType`` is set it must
        be set to ``AssetHashType.CUSTOM``. For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - Based on ``assetHashType``

        :stability: experimental
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_hash_type(self) -> typing.Optional[_AssetHashType_49193809]:
        '''(experimental) Determines how asset hash is calculated. Assets will get rebuild and uploaded only if their hash has changed.

        If asset hash is set to ``SOURCE`` (default), then only changes to the source
        directory will cause the asset to rebuild. This means, for example, that in
        order to pick up a new dependency version, a change must be made to the
        source tree. Ideally, this can be implemented by including a dependency
        lockfile in your source tree or using fixed dependencies.

        If the asset hash is set to ``OUTPUT``, the hash is calculated after
        bundling. This means that any change in the output will cause the asset to
        be invalidated and uploaded. Bear in mind that ``pip`` adds timestamps to
        dependencies it installs, which implies that in this mode Python bundles
        will *always* get rebuild and uploaded. Normally this is an anti-pattern
        since build

        :default:

        AssetHashType.SOURCE By default, hash is calculated based on the
        contents of the source directory. This means that only updates to the
        source will cause the asset to rebuild.

        :stability: experimental
        '''
        result = self._values.get("asset_hash_type")
        return typing.cast(typing.Optional[_AssetHashType_49193809], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Optional build arguments to pass to the default container.

        This can be used to customize
        the index URLs used for installing dependencies.
        This is not used if a custom image is provided.

        :default: - No build arguments.

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables defined when bundling runs.

        :default: - no environment variables are defined.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def image(self) -> typing.Optional[_DockerImage_d5f0ad8e]:
        '''(experimental) Docker image to use for bundling.

        If no options are provided, the default bundling image
        will be used. Dependencies will be installed using the default packaging commands
        and copied over from into the Lambda asset.

        :default: - Default bundling image.

        :stability: experimental
        '''
        result = self._values.get("image")
        return typing.cast(typing.Optional[_DockerImage_d5f0ad8e], result)

    @builtins.property
    def output_path_suffix(self) -> typing.Optional[builtins.str]:
        '''(experimental) Output path suffix: the suffix for the directory into which the bundled output is written.

        :default: - 'python' for a layer, empty string otherwise.

        :stability: experimental
        '''
        result = self._values.get("output_path_suffix")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PythonFunction(
    _Function_40b20aa5,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_python.PythonFunction",
):
    '''(experimental) A Python Lambda function.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        entry = "/path/to/function"
        image = DockerImage.from_build(entry)
        
        lambda_.PythonFunction(self, "function",
            entry=entry,
            runtime=Runtime.PYTHON_3_8,
            bundling=lambda.aws_lambda_python.BundlingOptions(
                build_args={"PIP_INDEX_URL": "https://your.index.url/simple/", "PIP_EXTRA_INDEX_URL": "https://your.extra-index.url/simple/"}
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        entry: builtins.str,
        runtime: _Runtime_932d369a,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        handler: typing.Optional[builtins.str] = None,
        index: typing.Optional[builtins.str] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_Architecture_24056b62] = None,
        architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
        code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
        current_version_options: typing.Optional[typing.Union[_VersionOptions_085bb455, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_ITopic_465e36b9] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_IKey_36930160] = None,
        ephemeral_storage_size: typing.Optional[_Size_7fbd4337] = None,
        events: typing.Optional[typing.Sequence[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        insights_version: typing.Optional[_LambdaInsightsVersion_2966e73b] = None,
        layers: typing.Optional[typing.Sequence[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_7acc40ab, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param entry: (experimental) Path to the source of the function or the location for dependencies.
        :param runtime: (experimental) The runtime environment. Only runtimes of the Python family are supported. Default: Runtime.PYTHON_3_7
        :param bundling: (experimental) Bundling options to use for this function. Use this to specify custom bundling options like the bundling Docker image, asset hash type, custom hash, architecture, etc. Default: - Use the default bundling Docker image, with x86_64 architecture.
        :param handler: (experimental) The name of the exported handler in the index file. Default: handler
        :param index: (experimental) The path (relative to entry) to the index file containing the exported handler. Default: index.py
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: (experimental) The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param architectures: (deprecated) DEPRECATED. Default: [Architecture.X86_64]
        :param code_signing_config: (experimental) Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: (experimental) The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: (experimental) The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: (experimental) Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c58e355407c7c5a9786cf52b1d8ae59413c33f40e092fa9cbac5746fcf7ca763)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PythonFunctionProps(
            entry=entry,
            runtime=runtime,
            bundling=bundling,
            handler=handler,
            index=index,
            allow_all_outbound=allow_all_outbound,
            allow_public_subnet=allow_public_subnet,
            architecture=architecture,
            architectures=architectures,
            code_signing_config=code_signing_config,
            current_version_options=current_version_options,
            dead_letter_queue=dead_letter_queue,
            dead_letter_queue_enabled=dead_letter_queue_enabled,
            dead_letter_topic=dead_letter_topic,
            description=description,
            environment=environment,
            environment_encryption=environment_encryption,
            ephemeral_storage_size=ephemeral_storage_size,
            events=events,
            filesystem=filesystem,
            function_name=function_name,
            initial_policy=initial_policy,
            insights_version=insights_version,
            layers=layers,
            log_retention=log_retention,
            log_retention_retry_options=log_retention_retry_options,
            log_retention_role=log_retention_role,
            memory_size=memory_size,
            profiling=profiling,
            profiling_group=profiling_group,
            reserved_concurrent_executions=reserved_concurrent_executions,
            role=role,
            security_group=security_group,
            security_groups=security_groups,
            timeout=timeout,
            tracing=tracing,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_python.PythonFunctionProps",
    jsii_struct_bases=[_FunctionOptions_dc75a392],
    name_mapping={
        "max_event_age": "maxEventAge",
        "on_failure": "onFailure",
        "on_success": "onSuccess",
        "retry_attempts": "retryAttempts",
        "allow_all_outbound": "allowAllOutbound",
        "allow_public_subnet": "allowPublicSubnet",
        "architecture": "architecture",
        "architectures": "architectures",
        "code_signing_config": "codeSigningConfig",
        "current_version_options": "currentVersionOptions",
        "dead_letter_queue": "deadLetterQueue",
        "dead_letter_queue_enabled": "deadLetterQueueEnabled",
        "dead_letter_topic": "deadLetterTopic",
        "description": "description",
        "environment": "environment",
        "environment_encryption": "environmentEncryption",
        "ephemeral_storage_size": "ephemeralStorageSize",
        "events": "events",
        "filesystem": "filesystem",
        "function_name": "functionName",
        "initial_policy": "initialPolicy",
        "insights_version": "insightsVersion",
        "layers": "layers",
        "log_retention": "logRetention",
        "log_retention_retry_options": "logRetentionRetryOptions",
        "log_retention_role": "logRetentionRole",
        "memory_size": "memorySize",
        "profiling": "profiling",
        "profiling_group": "profilingGroup",
        "reserved_concurrent_executions": "reservedConcurrentExecutions",
        "role": "role",
        "security_group": "securityGroup",
        "security_groups": "securityGroups",
        "timeout": "timeout",
        "tracing": "tracing",
        "vpc": "vpc",
        "vpc_subnets": "vpcSubnets",
        "entry": "entry",
        "runtime": "runtime",
        "bundling": "bundling",
        "handler": "handler",
        "index": "index",
    },
)
class PythonFunctionProps(_FunctionOptions_dc75a392):
    def __init__(
        self,
        *,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        allow_all_outbound: typing.Optional[builtins.bool] = None,
        allow_public_subnet: typing.Optional[builtins.bool] = None,
        architecture: typing.Optional[_Architecture_24056b62] = None,
        architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
        code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
        current_version_options: typing.Optional[typing.Union[_VersionOptions_085bb455, typing.Dict[builtins.str, typing.Any]]] = None,
        dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
        dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
        dead_letter_topic: typing.Optional[_ITopic_465e36b9] = None,
        description: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment_encryption: typing.Optional[_IKey_36930160] = None,
        ephemeral_storage_size: typing.Optional[_Size_7fbd4337] = None,
        events: typing.Optional[typing.Sequence[_IEventSource_7914870e]] = None,
        filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
        function_name: typing.Optional[builtins.str] = None,
        initial_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        insights_version: typing.Optional[_LambdaInsightsVersion_2966e73b] = None,
        layers: typing.Optional[typing.Sequence[_ILayerVersion_b2b86380]] = None,
        log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
        log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_7acc40ab, typing.Dict[builtins.str, typing.Any]]] = None,
        log_retention_role: typing.Optional[_IRole_59af6f50] = None,
        memory_size: typing.Optional[jsii.Number] = None,
        profiling: typing.Optional[builtins.bool] = None,
        profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
        reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        entry: builtins.str,
        runtime: _Runtime_932d369a,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        handler: typing.Optional[builtins.str] = None,
        index: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a PythonFunction.

        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2
        :param allow_all_outbound: (experimental) Whether to allow the Lambda to send all network traffic. If set to false, you must individually add traffic rules to allow the Lambda to connect to network targets. Default: true
        :param allow_public_subnet: (experimental) Lambda Functions in a public subnet can NOT access the internet. Use this property to acknowledge this limitation and still place the function in a public subnet. Default: false
        :param architecture: (experimental) The system architectures compatible with this lambda function. Default: Architecture.X86_64
        :param architectures: (deprecated) DEPRECATED. Default: [Architecture.X86_64]
        :param code_signing_config: (experimental) Code signing config associated with this function. Default: - Not Sign the Code
        :param current_version_options: (experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method. Default: - default options as described in ``VersionOptions``
        :param dead_letter_queue: (experimental) The SQS queue to use if DLQ is enabled. If SNS topic is desired, specify ``deadLetterTopic`` property instead. Default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``
        :param dead_letter_queue_enabled: (experimental) Enabled DLQ. If ``deadLetterQueue`` is undefined, an SQS queue with default options will be defined for your Function. Default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.
        :param dead_letter_topic: (experimental) The SNS topic to use as a DLQ. Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly. Default: - no SNS topic
        :param description: (experimental) A description of the function. Default: - No description.
        :param environment: (experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions. Use environment variables to apply configuration changes, such as test and production environment configurations, without changing your Lambda function source code. Default: - No environment variables.
        :param environment_encryption: (experimental) The AWS KMS key that's used to encrypt your function's environment variables. Default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).
        :param ephemeral_storage_size: (experimental) The size of the function’s /tmp directory in MiB. Default: 512 MiB
        :param events: (experimental) Event sources for this function. You can also add event sources using ``addEventSource``. Default: - No event sources.
        :param filesystem: (experimental) The filesystem configuration for the lambda function. Default: - will not mount any filesystem
        :param function_name: (experimental) A name for the function. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the function's name. For more information, see Name Type.
        :param initial_policy: (experimental) Initial policy statements to add to the created Lambda Role. You can call ``addToRolePolicy`` to the created lambda to add statements post creation. Default: - No policy statements are added to the created Lambda role.
        :param insights_version: (experimental) Specify the version of CloudWatch Lambda insights to use for monitoring. Default: - No Lambda Insights
        :param layers: (experimental) A list of layers to add to the function's execution environment. You can configure your Lambda function to pull in additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies that can be used by multiple functions. Default: - No layers.
        :param log_retention: (experimental) The number of days log events are kept in CloudWatch Logs. When updating this property, unsetting it doesn't remove the log retention policy. To remove the retention policy, set the value to ``INFINITE``. Default: logs.RetentionDays.INFINITE
        :param log_retention_retry_options: (experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group. These options control the retry policy when interacting with CloudWatch APIs. Default: - Default AWS SDK retry options.
        :param log_retention_role: (experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy. Default: - A new role is created.
        :param memory_size: (experimental) The amount of memory, in MB, that is allocated to your Lambda function. Lambda uses this value to proportionally allocate the amount of CPU power. For more information, see Resource Model in the AWS Lambda Developer Guide. Default: 128
        :param profiling: (experimental) Enable profiling. Default: - No profiling.
        :param profiling_group: (experimental) Profiling Group. Default: - A new profiling group will be created if ``profiling`` is set.
        :param reserved_concurrent_executions: (experimental) The maximum of concurrent executions you want to reserve for the function. Default: - No specific limit - account limit.
        :param role: (experimental) Lambda execution role. This is the role that will be assumed by the function upon execution. It controls the permissions that the function will have. The Role must be assumable by the 'lambda.amazonaws.com' service principal. The default Role automatically has permissions granted for Lambda execution. If you provide a Role, you must add the relevant AWS managed policies yourself. The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and "service-role/AWSLambdaVPCAccessExecutionRole". Default: - A unique role will be generated for this lambda function. Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.
        :param security_group: (deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead. Only used if 'vpc' is supplied. Use securityGroups property instead. Function constructor will throw an error if both are specified. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroups prop, a dedicated security group will be created for this function.
        :param security_groups: (experimental) The list of security groups to associate with the Lambda's network interfaces. Only used if 'vpc' is supplied. Default: - If the function is placed within a VPC and a security group is not specified, either by this or securityGroup prop, a dedicated security group will be created for this function.
        :param timeout: (experimental) The function execution time (in seconds) after which Lambda terminates the function. Because the execution time affects cost, set this value based on the function's expected execution time. Default: Duration.seconds(3)
        :param tracing: (experimental) Enable AWS X-Ray Tracing for Lambda Function. Default: Tracing.Disabled
        :param vpc: (experimental) VPC network to place Lambda network interfaces. Specify this if the Lambda function needs to access resources in a VPC. Default: - Function is not placed within a VPC.
        :param vpc_subnets: (experimental) Where to place the network interfaces within the VPC. Only used if 'vpc' is supplied. Note: internet access for Lambdas requires a NAT gateway, so picking Public subnets is not allowed. Default: - the Vpc default strategy if not specified
        :param entry: (experimental) Path to the source of the function or the location for dependencies.
        :param runtime: (experimental) The runtime environment. Only runtimes of the Python family are supported. Default: Runtime.PYTHON_3_7
        :param bundling: (experimental) Bundling options to use for this function. Use this to specify custom bundling options like the bundling Docker image, asset hash type, custom hash, architecture, etc. Default: - Use the default bundling Docker image, with x86_64 architecture.
        :param handler: (experimental) The name of the exported handler in the index file. Default: handler
        :param index: (experimental) The path (relative to entry) to the index file containing the exported handler. Default: index.py

        :stability: experimental
        :exampleMetadata: infused

        Example::

            entry = "/path/to/function"
            image = DockerImage.from_build(entry)
            
            lambda_.PythonFunction(self, "function",
                entry=entry,
                runtime=Runtime.PYTHON_3_8,
                bundling=lambda.aws_lambda_python.BundlingOptions(
                    build_args={"PIP_INDEX_URL": "https://your.index.url/simple/", "PIP_EXTRA_INDEX_URL": "https://your.extra-index.url/simple/"}
                )
            )
        '''
        if isinstance(current_version_options, dict):
            current_version_options = _VersionOptions_085bb455(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_7acc40ab(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34d8bafe9c03087f464742d82267bcf9f39e15162da17c40c58240b8669632ba)
            check_type(argname="argument max_event_age", value=max_event_age, expected_type=type_hints["max_event_age"])
            check_type(argname="argument on_failure", value=on_failure, expected_type=type_hints["on_failure"])
            check_type(argname="argument on_success", value=on_success, expected_type=type_hints["on_success"])
            check_type(argname="argument retry_attempts", value=retry_attempts, expected_type=type_hints["retry_attempts"])
            check_type(argname="argument allow_all_outbound", value=allow_all_outbound, expected_type=type_hints["allow_all_outbound"])
            check_type(argname="argument allow_public_subnet", value=allow_public_subnet, expected_type=type_hints["allow_public_subnet"])
            check_type(argname="argument architecture", value=architecture, expected_type=type_hints["architecture"])
            check_type(argname="argument architectures", value=architectures, expected_type=type_hints["architectures"])
            check_type(argname="argument code_signing_config", value=code_signing_config, expected_type=type_hints["code_signing_config"])
            check_type(argname="argument current_version_options", value=current_version_options, expected_type=type_hints["current_version_options"])
            check_type(argname="argument dead_letter_queue", value=dead_letter_queue, expected_type=type_hints["dead_letter_queue"])
            check_type(argname="argument dead_letter_queue_enabled", value=dead_letter_queue_enabled, expected_type=type_hints["dead_letter_queue_enabled"])
            check_type(argname="argument dead_letter_topic", value=dead_letter_topic, expected_type=type_hints["dead_letter_topic"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_encryption", value=environment_encryption, expected_type=type_hints["environment_encryption"])
            check_type(argname="argument ephemeral_storage_size", value=ephemeral_storage_size, expected_type=type_hints["ephemeral_storage_size"])
            check_type(argname="argument events", value=events, expected_type=type_hints["events"])
            check_type(argname="argument filesystem", value=filesystem, expected_type=type_hints["filesystem"])
            check_type(argname="argument function_name", value=function_name, expected_type=type_hints["function_name"])
            check_type(argname="argument initial_policy", value=initial_policy, expected_type=type_hints["initial_policy"])
            check_type(argname="argument insights_version", value=insights_version, expected_type=type_hints["insights_version"])
            check_type(argname="argument layers", value=layers, expected_type=type_hints["layers"])
            check_type(argname="argument log_retention", value=log_retention, expected_type=type_hints["log_retention"])
            check_type(argname="argument log_retention_retry_options", value=log_retention_retry_options, expected_type=type_hints["log_retention_retry_options"])
            check_type(argname="argument log_retention_role", value=log_retention_role, expected_type=type_hints["log_retention_role"])
            check_type(argname="argument memory_size", value=memory_size, expected_type=type_hints["memory_size"])
            check_type(argname="argument profiling", value=profiling, expected_type=type_hints["profiling"])
            check_type(argname="argument profiling_group", value=profiling_group, expected_type=type_hints["profiling_group"])
            check_type(argname="argument reserved_concurrent_executions", value=reserved_concurrent_executions, expected_type=type_hints["reserved_concurrent_executions"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument security_group", value=security_group, expected_type=type_hints["security_group"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument tracing", value=tracing, expected_type=type_hints["tracing"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument vpc_subnets", value=vpc_subnets, expected_type=type_hints["vpc_subnets"])
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument index", value=index, expected_type=type_hints["index"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry": entry,
            "runtime": runtime,
        }
        if max_event_age is not None:
            self._values["max_event_age"] = max_event_age
        if on_failure is not None:
            self._values["on_failure"] = on_failure
        if on_success is not None:
            self._values["on_success"] = on_success
        if retry_attempts is not None:
            self._values["retry_attempts"] = retry_attempts
        if allow_all_outbound is not None:
            self._values["allow_all_outbound"] = allow_all_outbound
        if allow_public_subnet is not None:
            self._values["allow_public_subnet"] = allow_public_subnet
        if architecture is not None:
            self._values["architecture"] = architecture
        if architectures is not None:
            self._values["architectures"] = architectures
        if code_signing_config is not None:
            self._values["code_signing_config"] = code_signing_config
        if current_version_options is not None:
            self._values["current_version_options"] = current_version_options
        if dead_letter_queue is not None:
            self._values["dead_letter_queue"] = dead_letter_queue
        if dead_letter_queue_enabled is not None:
            self._values["dead_letter_queue_enabled"] = dead_letter_queue_enabled
        if dead_letter_topic is not None:
            self._values["dead_letter_topic"] = dead_letter_topic
        if description is not None:
            self._values["description"] = description
        if environment is not None:
            self._values["environment"] = environment
        if environment_encryption is not None:
            self._values["environment_encryption"] = environment_encryption
        if ephemeral_storage_size is not None:
            self._values["ephemeral_storage_size"] = ephemeral_storage_size
        if events is not None:
            self._values["events"] = events
        if filesystem is not None:
            self._values["filesystem"] = filesystem
        if function_name is not None:
            self._values["function_name"] = function_name
        if initial_policy is not None:
            self._values["initial_policy"] = initial_policy
        if insights_version is not None:
            self._values["insights_version"] = insights_version
        if layers is not None:
            self._values["layers"] = layers
        if log_retention is not None:
            self._values["log_retention"] = log_retention
        if log_retention_retry_options is not None:
            self._values["log_retention_retry_options"] = log_retention_retry_options
        if log_retention_role is not None:
            self._values["log_retention_role"] = log_retention_role
        if memory_size is not None:
            self._values["memory_size"] = memory_size
        if profiling is not None:
            self._values["profiling"] = profiling
        if profiling_group is not None:
            self._values["profiling_group"] = profiling_group
        if reserved_concurrent_executions is not None:
            self._values["reserved_concurrent_executions"] = reserved_concurrent_executions
        if role is not None:
            self._values["role"] = role
        if security_group is not None:
            self._values["security_group"] = security_group
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if timeout is not None:
            self._values["timeout"] = timeout
        if tracing is not None:
            self._values["tracing"] = tracing
        if vpc is not None:
            self._values["vpc"] = vpc
        if vpc_subnets is not None:
            self._values["vpc_subnets"] = vpc_subnets
        if bundling is not None:
            self._values["bundling"] = bundling
        if handler is not None:
            self._values["handler"] = handler
        if index is not None:
            self._values["index"] = index

    @builtins.property
    def max_event_age(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The maximum age of a request that Lambda sends to a function for processing.

        Minimum: 60 seconds
        Maximum: 6 hours

        :default: Duration.hours(6)

        :stability: experimental
        '''
        result = self._values.get("max_event_age")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def on_failure(self) -> typing.Optional[_IDestination_7f253ff1]:
        '''(experimental) The destination for failed invocations.

        :default: - no destination

        :stability: experimental
        '''
        result = self._values.get("on_failure")
        return typing.cast(typing.Optional[_IDestination_7f253ff1], result)

    @builtins.property
    def on_success(self) -> typing.Optional[_IDestination_7f253ff1]:
        '''(experimental) The destination for successful invocations.

        :default: - no destination

        :stability: experimental
        '''
        result = self._values.get("on_success")
        return typing.cast(typing.Optional[_IDestination_7f253ff1], result)

    @builtins.property
    def retry_attempts(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum number of times to retry when the function returns an error.

        Minimum: 0
        Maximum: 2

        :default: 2

        :stability: experimental
        '''
        result = self._values.get("retry_attempts")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def allow_all_outbound(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to allow the Lambda to send all network traffic.

        If set to false, you must individually add traffic rules to allow the
        Lambda to connect to network targets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("allow_all_outbound")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def allow_public_subnet(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Lambda Functions in a public subnet can NOT access the internet.

        Use this property to acknowledge this limitation and still place the function in a public subnet.

        :default: false

        :see: https://stackoverflow.com/questions/52992085/why-cant-an-aws-lambda-function-inside-a-public-subnet-in-a-vpc-connect-to-the/52994841#52994841
        :stability: experimental
        '''
        result = self._values.get("allow_public_subnet")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def architecture(self) -> typing.Optional[_Architecture_24056b62]:
        '''(experimental) The system architectures compatible with this lambda function.

        :default: Architecture.X86_64

        :stability: experimental
        '''
        result = self._values.get("architecture")
        return typing.cast(typing.Optional[_Architecture_24056b62], result)

    @builtins.property
    def architectures(self) -> typing.Optional[typing.List[_Architecture_24056b62]]:
        '''(deprecated) DEPRECATED.

        :default: [Architecture.X86_64]

        :deprecated: use ``architecture``

        :stability: deprecated
        '''
        result = self._values.get("architectures")
        return typing.cast(typing.Optional[typing.List[_Architecture_24056b62]], result)

    @builtins.property
    def code_signing_config(self) -> typing.Optional[_ICodeSigningConfig_5d77bccf]:
        '''(experimental) Code signing config associated with this function.

        :default: - Not Sign the Code

        :stability: experimental
        '''
        result = self._values.get("code_signing_config")
        return typing.cast(typing.Optional[_ICodeSigningConfig_5d77bccf], result)

    @builtins.property
    def current_version_options(self) -> typing.Optional[_VersionOptions_085bb455]:
        '''(experimental) Options for the ``lambda.Version`` resource automatically created by the ``fn.currentVersion`` method.

        :default: - default options as described in ``VersionOptions``

        :stability: experimental
        '''
        result = self._values.get("current_version_options")
        return typing.cast(typing.Optional[_VersionOptions_085bb455], result)

    @builtins.property
    def dead_letter_queue(self) -> typing.Optional[_IQueue_45a01ab4]:
        '''(experimental) The SQS queue to use if DLQ is enabled.

        If SNS topic is desired, specify ``deadLetterTopic`` property instead.

        :default: - SQS queue with 14 day retention period if ``deadLetterQueueEnabled`` is ``true``

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue")
        return typing.cast(typing.Optional[_IQueue_45a01ab4], result)

    @builtins.property
    def dead_letter_queue_enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enabled DLQ.

        If ``deadLetterQueue`` is undefined,
        an SQS queue with default options will be defined for your Function.

        :default: - false unless ``deadLetterQueue`` is set, which implies DLQ is enabled.

        :stability: experimental
        '''
        result = self._values.get("dead_letter_queue_enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dead_letter_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) The SNS topic to use as a DLQ.

        Note that if ``deadLetterQueueEnabled`` is set to ``true``, an SQS queue will be created
        rather than an SNS topic. Using an SNS topic as a DLQ requires this property to be set explicitly.

        :default: - no SNS topic

        :stability: experimental
        '''
        result = self._values.get("dead_letter_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) A description of the function.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Key-value pairs that Lambda caches and makes available for your Lambda functions.

        Use environment variables to apply configuration changes, such
        as test and production environment configurations, without changing your
        Lambda function source code.

        :default: - No environment variables.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment_encryption(self) -> typing.Optional[_IKey_36930160]:
        '''(experimental) The AWS KMS key that's used to encrypt your function's environment variables.

        :default: - AWS Lambda creates and uses an AWS managed customer master key (CMK).

        :stability: experimental
        '''
        result = self._values.get("environment_encryption")
        return typing.cast(typing.Optional[_IKey_36930160], result)

    @builtins.property
    def ephemeral_storage_size(self) -> typing.Optional[_Size_7fbd4337]:
        '''(experimental) The size of the function’s /tmp directory in MiB.

        :default: 512 MiB

        :stability: experimental
        '''
        result = self._values.get("ephemeral_storage_size")
        return typing.cast(typing.Optional[_Size_7fbd4337], result)

    @builtins.property
    def events(self) -> typing.Optional[typing.List[_IEventSource_7914870e]]:
        '''(experimental) Event sources for this function.

        You can also add event sources using ``addEventSource``.

        :default: - No event sources.

        :stability: experimental
        '''
        result = self._values.get("events")
        return typing.cast(typing.Optional[typing.List[_IEventSource_7914870e]], result)

    @builtins.property
    def filesystem(self) -> typing.Optional[_FileSystem_17be1f4c]:
        '''(experimental) The filesystem configuration for the lambda function.

        :default: - will not mount any filesystem

        :stability: experimental
        '''
        result = self._values.get("filesystem")
        return typing.cast(typing.Optional[_FileSystem_17be1f4c], result)

    @builtins.property
    def function_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A name for the function.

        :default:

        - AWS CloudFormation generates a unique physical ID and uses that
        ID for the function's name. For more information, see Name Type.

        :stability: experimental
        '''
        result = self._values.get("function_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def initial_policy(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Initial policy statements to add to the created Lambda Role.

        You can call ``addToRolePolicy`` to the created lambda to add statements post creation.

        :default: - No policy statements are added to the created Lambda role.

        :stability: experimental
        '''
        result = self._values.get("initial_policy")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def insights_version(self) -> typing.Optional[_LambdaInsightsVersion_2966e73b]:
        '''(experimental) Specify the version of CloudWatch Lambda insights to use for monitoring.

        :default: - No Lambda Insights

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Lambda-Insights-Getting-Started-docker.html
        :stability: experimental
        '''
        result = self._values.get("insights_version")
        return typing.cast(typing.Optional[_LambdaInsightsVersion_2966e73b], result)

    @builtins.property
    def layers(self) -> typing.Optional[typing.List[_ILayerVersion_b2b86380]]:
        '''(experimental) A list of layers to add to the function's execution environment.

        You can configure your Lambda function to pull in
        additional code during initialization in the form of layers. Layers are packages of libraries or other dependencies
        that can be used by multiple functions.

        :default: - No layers.

        :stability: experimental
        '''
        result = self._values.get("layers")
        return typing.cast(typing.Optional[typing.List[_ILayerVersion_b2b86380]], result)

    @builtins.property
    def log_retention(self) -> typing.Optional[_RetentionDays_6c560d31]:
        '''(experimental) The number of days log events are kept in CloudWatch Logs.

        When updating
        this property, unsetting it doesn't remove the log retention policy. To
        remove the retention policy, set the value to ``INFINITE``.

        :default: logs.RetentionDays.INFINITE

        :stability: experimental
        '''
        result = self._values.get("log_retention")
        return typing.cast(typing.Optional[_RetentionDays_6c560d31], result)

    @builtins.property
    def log_retention_retry_options(
        self,
    ) -> typing.Optional[_LogRetentionRetryOptions_7acc40ab]:
        '''(experimental) When log retention is specified, a custom resource attempts to create the CloudWatch log group.

        These options control the retry policy when interacting with CloudWatch APIs.

        :default: - Default AWS SDK retry options.

        :stability: experimental
        '''
        result = self._values.get("log_retention_retry_options")
        return typing.cast(typing.Optional[_LogRetentionRetryOptions_7acc40ab], result)

    @builtins.property
    def log_retention_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role for the Lambda function associated with the custom resource that sets the retention policy.

        :default: - A new role is created.

        :stability: experimental
        '''
        result = self._values.get("log_retention_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def memory_size(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The amount of memory, in MB, that is allocated to your Lambda function.

        Lambda uses this value to proportionally allocate the amount of CPU
        power. For more information, see Resource Model in the AWS Lambda
        Developer Guide.

        :default: 128

        :stability: experimental
        '''
        result = self._values.get("memory_size")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def profiling(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable profiling.

        :default: - No profiling.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        '''
        result = self._values.get("profiling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profiling_group(self) -> typing.Optional[_IProfilingGroup_418eb20c]:
        '''(experimental) Profiling Group.

        :default: - A new profiling group will be created if ``profiling`` is set.

        :see: https://docs.aws.amazon.com/codeguru/latest/profiler-ug/setting-up-lambda.html
        :stability: experimental
        '''
        result = self._values.get("profiling_group")
        return typing.cast(typing.Optional[_IProfilingGroup_418eb20c], result)

    @builtins.property
    def reserved_concurrent_executions(self) -> typing.Optional[jsii.Number]:
        '''(experimental) The maximum of concurrent executions you want to reserve for the function.

        :default: - No specific limit - account limit.

        :see: https://docs.aws.amazon.com/lambda/latest/dg/concurrent-executions.html
        :stability: experimental
        '''
        result = self._values.get("reserved_concurrent_executions")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Lambda execution role.

        This is the role that will be assumed by the function upon execution.
        It controls the permissions that the function will have. The Role must
        be assumable by the 'lambda.amazonaws.com' service principal.

        The default Role automatically has permissions granted for Lambda execution. If you
        provide a Role, you must add the relevant AWS managed policies yourself.

        The relevant managed policies are "service-role/AWSLambdaBasicExecutionRole" and
        "service-role/AWSLambdaVPCAccessExecutionRole".

        :default:

        - A unique role will be generated for this lambda function.
        Both supplied and generated roles can always be changed by calling ``addToRolePolicy``.

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def security_group(self) -> typing.Optional[_ISecurityGroup_cdbba9d3]:
        '''(deprecated) What security group to associate with the Lambda's network interfaces. This property is being deprecated, consider using securityGroups instead.

        Only used if 'vpc' is supplied.

        Use securityGroups property instead.
        Function constructor will throw an error if both are specified.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroups prop, a dedicated security
        group will be created for this function.

        :deprecated: - This property is deprecated, use securityGroups instead

        :stability: deprecated
        '''
        result = self._values.get("security_group")
        return typing.cast(typing.Optional[_ISecurityGroup_cdbba9d3], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) The list of security groups to associate with the Lambda's network interfaces.

        Only used if 'vpc' is supplied.

        :default:

        - If the function is placed within a VPC and a security group is
        not specified, either by this or securityGroup prop, a dedicated security
        group will be created for this function.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The function execution time (in seconds) after which Lambda terminates the function.

        Because the execution time affects cost, set this value
        based on the function's expected execution time.

        :default: Duration.seconds(3)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def tracing(self) -> typing.Optional[_Tracing_b7f4a8b6]:
        '''(experimental) Enable AWS X-Ray Tracing for Lambda Function.

        :default: Tracing.Disabled

        :stability: experimental
        '''
        result = self._values.get("tracing")
        return typing.cast(typing.Optional[_Tracing_b7f4a8b6], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) VPC network to place Lambda network interfaces.

        Specify this if the Lambda function needs to access resources in a VPC.

        :default: - Function is not placed within a VPC.

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def vpc_subnets(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Where to place the network interfaces within the VPC.

        Only used if 'vpc' is supplied. Note: internet access for Lambdas
        requires a NAT gateway, so picking Public subnets is not allowed.

        :default: - the Vpc default strategy if not specified

        :stability: experimental
        '''
        result = self._values.get("vpc_subnets")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def entry(self) -> builtins.str:
        '''(experimental) Path to the source of the function or the location for dependencies.

        :stability: experimental
        '''
        result = self._values.get("entry")
        assert result is not None, "Required property 'entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> _Runtime_932d369a:
        '''(experimental) The runtime environment.

        Only runtimes of the Python family are
        supported.

        :default: Runtime.PYTHON_3_7

        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(_Runtime_932d369a, result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''(experimental) Bundling options to use for this function.

        Use this to specify custom bundling options like
        the bundling Docker image, asset hash type, custom hash, architecture, etc.

        :default: - Use the default bundling Docker image, with x86_64 architecture.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the exported handler in the index file.

        :default: handler

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def index(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path (relative to entry) to the index file containing the exported handler.

        :default: index.py

        :stability: experimental
        '''
        result = self._values.get("index")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PythonLayerVersion(
    _LayerVersion_34d6006f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_python.PythonLayerVersion",
):
    '''(experimental) A lambda layer version.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.PythonLayerVersion(self, "MyLayer",
            entry="/path/to/my/layer"
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        entry: builtins.str,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        compatible_architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
        compatible_runtimes: typing.Optional[typing.Sequence[_Runtime_932d369a]] = None,
        description: typing.Optional[builtins.str] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param entry: (experimental) The path to the root directory of the lambda layer.
        :param bundling: (experimental) Bundling options to use for this function. Use this to specify custom bundling options like the bundling Docker image, asset hash type, custom hash, architecture, etc. Default: - Use the default bundling Docker image, with x86_64 architecture.
        :param compatible_architectures: (experimental) The system architectures compatible with this layer. Default: [Architecture.X86_64]
        :param compatible_runtimes: (experimental) The runtimes compatible with the python layer. Default: - Only Python 3.7 is supported.
        :param description: (experimental) The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: (experimental) The name of the layer. Default: - A name will be generated.
        :param license: (experimental) The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.
        :param removal_policy: (experimental) Whether to retain this version of the layer when a new version is added or when the stack is deleted. Default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef47be1f1c1c4cf9c38df358c993a97146749e8abc5cd2b2655e052fb5770cdc)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PythonLayerVersionProps(
            entry=entry,
            bundling=bundling,
            compatible_architectures=compatible_architectures,
            compatible_runtimes=compatible_runtimes,
            description=description,
            layer_version_name=layer_version_name,
            license=license,
            removal_policy=removal_policy,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_python.PythonLayerVersionProps",
    jsii_struct_bases=[_LayerVersionOptions_15d6ea62],
    name_mapping={
        "description": "description",
        "layer_version_name": "layerVersionName",
        "license": "license",
        "removal_policy": "removalPolicy",
        "entry": "entry",
        "bundling": "bundling",
        "compatible_architectures": "compatibleArchitectures",
        "compatible_runtimes": "compatibleRuntimes",
    },
)
class PythonLayerVersionProps(_LayerVersionOptions_15d6ea62):
    def __init__(
        self,
        *,
        description: typing.Optional[builtins.str] = None,
        layer_version_name: typing.Optional[builtins.str] = None,
        license: typing.Optional[builtins.str] = None,
        removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
        entry: builtins.str,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        compatible_architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
        compatible_runtimes: typing.Optional[typing.Sequence[_Runtime_932d369a]] = None,
    ) -> None:
        '''(experimental) Properties for PythonLayerVersion.

        :param description: (experimental) The description the this Lambda Layer. Default: - No description.
        :param layer_version_name: (experimental) The name of the layer. Default: - A name will be generated.
        :param license: (experimental) The SPDX licence identifier or URL to the license file for this layer. Default: - No license information will be recorded.
        :param removal_policy: (experimental) Whether to retain this version of the layer when a new version is added or when the stack is deleted. Default: RemovalPolicy.DESTROY
        :param entry: (experimental) The path to the root directory of the lambda layer.
        :param bundling: (experimental) Bundling options to use for this function. Use this to specify custom bundling options like the bundling Docker image, asset hash type, custom hash, architecture, etc. Default: - Use the default bundling Docker image, with x86_64 architecture.
        :param compatible_architectures: (experimental) The system architectures compatible with this layer. Default: [Architecture.X86_64]
        :param compatible_runtimes: (experimental) The runtimes compatible with the python layer. Default: - Only Python 3.7 is supported.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            lambda_.PythonLayerVersion(self, "MyLayer",
                entry="/path/to/my/layer"
            )
        '''
        if isinstance(bundling, dict):
            bundling = BundlingOptions(**bundling)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f86e1762362e28c8cfbd30e96bcb231919a73662acd9e2e127753b8ffb71bab2)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument layer_version_name", value=layer_version_name, expected_type=type_hints["layer_version_name"])
            check_type(argname="argument license", value=license, expected_type=type_hints["license"])
            check_type(argname="argument removal_policy", value=removal_policy, expected_type=type_hints["removal_policy"])
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument compatible_architectures", value=compatible_architectures, expected_type=type_hints["compatible_architectures"])
            check_type(argname="argument compatible_runtimes", value=compatible_runtimes, expected_type=type_hints["compatible_runtimes"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "entry": entry,
        }
        if description is not None:
            self._values["description"] = description
        if layer_version_name is not None:
            self._values["layer_version_name"] = layer_version_name
        if license is not None:
            self._values["license"] = license
        if removal_policy is not None:
            self._values["removal_policy"] = removal_policy
        if bundling is not None:
            self._values["bundling"] = bundling
        if compatible_architectures is not None:
            self._values["compatible_architectures"] = compatible_architectures
        if compatible_runtimes is not None:
            self._values["compatible_runtimes"] = compatible_runtimes

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''(experimental) The description the this Lambda Layer.

        :default: - No description.

        :stability: experimental
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def layer_version_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the layer.

        :default: - A name will be generated.

        :stability: experimental
        '''
        result = self._values.get("layer_version_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def license(self) -> typing.Optional[builtins.str]:
        '''(experimental) The SPDX licence identifier or URL to the license file for this layer.

        :default: - No license information will be recorded.

        :stability: experimental
        '''
        result = self._values.get("license")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def removal_policy(self) -> typing.Optional[_RemovalPolicy_c97e7a20]:
        '''(experimental) Whether to retain this version of the layer when a new version is added or when the stack is deleted.

        :default: RemovalPolicy.DESTROY

        :stability: experimental
        '''
        result = self._values.get("removal_policy")
        return typing.cast(typing.Optional[_RemovalPolicy_c97e7a20], result)

    @builtins.property
    def entry(self) -> builtins.str:
        '''(experimental) The path to the root directory of the lambda layer.

        :stability: experimental
        '''
        result = self._values.get("entry")
        assert result is not None, "Required property 'entry' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''(experimental) Bundling options to use for this function.

        Use this to specify custom bundling options like
        the bundling Docker image, asset hash type, custom hash, architecture, etc.

        :default: - Use the default bundling Docker image, with x86_64 architecture.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def compatible_architectures(
        self,
    ) -> typing.Optional[typing.List[_Architecture_24056b62]]:
        '''(experimental) The system architectures compatible with this layer.

        :default: [Architecture.X86_64]

        :stability: experimental
        '''
        result = self._values.get("compatible_architectures")
        return typing.cast(typing.Optional[typing.List[_Architecture_24056b62]], result)

    @builtins.property
    def compatible_runtimes(self) -> typing.Optional[typing.List[_Runtime_932d369a]]:
        '''(experimental) The runtimes compatible with the python layer.

        :default: - Only Python 3.7 is supported.

        :stability: experimental
        '''
        result = self._values.get("compatible_runtimes")
        return typing.cast(typing.Optional[typing.List[_Runtime_932d369a]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PythonLayerVersionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "BundlingOptions",
    "PythonFunction",
    "PythonFunctionProps",
    "PythonLayerVersion",
    "PythonLayerVersionProps",
]

publication.publish()

def _typecheckingstub__a8ac4e0436c2309daa08b5de4d684582f00c5585d82ea6af18f9e4d2b7518ce1(
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    asset_hash_type: typing.Optional[_AssetHashType_49193809] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    image: typing.Optional[_DockerImage_d5f0ad8e] = None,
    output_path_suffix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c58e355407c7c5a9786cf52b1d8ae59413c33f40e092fa9cbac5746fcf7ca763(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    entry: builtins.str,
    runtime: _Runtime_932d369a,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    handler: typing.Optional[builtins.str] = None,
    index: typing.Optional[builtins.str] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_Architecture_24056b62] = None,
    architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
    code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
    current_version_options: typing.Optional[typing.Union[_VersionOptions_085bb455, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_ITopic_465e36b9] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_IKey_36930160] = None,
    ephemeral_storage_size: typing.Optional[_Size_7fbd4337] = None,
    events: typing.Optional[typing.Sequence[_IEventSource_7914870e]] = None,
    filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    insights_version: typing.Optional[_LambdaInsightsVersion_2966e73b] = None,
    layers: typing.Optional[typing.Sequence[_ILayerVersion_b2b86380]] = None,
    log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_7acc40ab, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_IRole_59af6f50] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    max_event_age: typing.Optional[_Duration_070aa057] = None,
    on_failure: typing.Optional[_IDestination_7f253ff1] = None,
    on_success: typing.Optional[_IDestination_7f253ff1] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34d8bafe9c03087f464742d82267bcf9f39e15162da17c40c58240b8669632ba(
    *,
    max_event_age: typing.Optional[_Duration_070aa057] = None,
    on_failure: typing.Optional[_IDestination_7f253ff1] = None,
    on_success: typing.Optional[_IDestination_7f253ff1] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    allow_all_outbound: typing.Optional[builtins.bool] = None,
    allow_public_subnet: typing.Optional[builtins.bool] = None,
    architecture: typing.Optional[_Architecture_24056b62] = None,
    architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
    code_signing_config: typing.Optional[_ICodeSigningConfig_5d77bccf] = None,
    current_version_options: typing.Optional[typing.Union[_VersionOptions_085bb455, typing.Dict[builtins.str, typing.Any]]] = None,
    dead_letter_queue: typing.Optional[_IQueue_45a01ab4] = None,
    dead_letter_queue_enabled: typing.Optional[builtins.bool] = None,
    dead_letter_topic: typing.Optional[_ITopic_465e36b9] = None,
    description: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    environment_encryption: typing.Optional[_IKey_36930160] = None,
    ephemeral_storage_size: typing.Optional[_Size_7fbd4337] = None,
    events: typing.Optional[typing.Sequence[_IEventSource_7914870e]] = None,
    filesystem: typing.Optional[_FileSystem_17be1f4c] = None,
    function_name: typing.Optional[builtins.str] = None,
    initial_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    insights_version: typing.Optional[_LambdaInsightsVersion_2966e73b] = None,
    layers: typing.Optional[typing.Sequence[_ILayerVersion_b2b86380]] = None,
    log_retention: typing.Optional[_RetentionDays_6c560d31] = None,
    log_retention_retry_options: typing.Optional[typing.Union[_LogRetentionRetryOptions_7acc40ab, typing.Dict[builtins.str, typing.Any]]] = None,
    log_retention_role: typing.Optional[_IRole_59af6f50] = None,
    memory_size: typing.Optional[jsii.Number] = None,
    profiling: typing.Optional[builtins.bool] = None,
    profiling_group: typing.Optional[_IProfilingGroup_418eb20c] = None,
    reserved_concurrent_executions: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    security_group: typing.Optional[_ISecurityGroup_cdbba9d3] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    tracing: typing.Optional[_Tracing_b7f4a8b6] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    vpc_subnets: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    entry: builtins.str,
    runtime: _Runtime_932d369a,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    handler: typing.Optional[builtins.str] = None,
    index: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef47be1f1c1c4cf9c38df358c993a97146749e8abc5cd2b2655e052fb5770cdc(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    entry: builtins.str,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compatible_architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
    compatible_runtimes: typing.Optional[typing.Sequence[_Runtime_932d369a]] = None,
    description: typing.Optional[builtins.str] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f86e1762362e28c8cfbd30e96bcb231919a73662acd9e2e127753b8ffb71bab2(
    *,
    description: typing.Optional[builtins.str] = None,
    layer_version_name: typing.Optional[builtins.str] = None,
    license: typing.Optional[builtins.str] = None,
    removal_policy: typing.Optional[_RemovalPolicy_c97e7a20] = None,
    entry: builtins.str,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    compatible_architectures: typing.Optional[typing.Sequence[_Architecture_24056b62]] = None,
    compatible_runtimes: typing.Optional[typing.Sequence[_Runtime_932d369a]] = None,
) -> None:
    """Type checking stubs"""
    pass
