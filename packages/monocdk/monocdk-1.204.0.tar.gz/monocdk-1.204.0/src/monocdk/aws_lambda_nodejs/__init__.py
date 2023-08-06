'''
# Amazon Lambda Node.js Library

This library provides constructs for Node.js Lambda functions.

## Node.js Function

The `NodejsFunction` construct creates a Lambda function with automatic transpiling and bundling
of TypeScript or Javascript code. This results in smaller Lambda packages that contain only the
code and dependencies needed to run the function.

It uses [esbuild](https://esbuild.github.io/) under the hood.

## Reference project architecture

The `NodejsFunction` allows you to define your CDK and runtime dependencies in a single
package.json and to collocate your runtime code with your infrastructure code:

```plaintext
.
├── lib
│   ├── my-construct.api.ts # Lambda handler for API
│   ├── my-construct.auth.ts # Lambda handler for Auth
│   └── my-construct.ts # CDK construct with two Lambda functions
├── package-lock.json # single lock file
├── package.json # CDK and runtime dependencies defined in a single package.json
└── tsconfig.json
```

By default, the construct will use the name of the defining file and the construct's
id to look up the entry file. In `my-construct.ts` above we have:

```python
# automatic entry look up
api_handler = lambda_.NodejsFunction(self, "api")
auth_handler = lambda_.NodejsFunction(self, "auth")
```

Alternatively, an entry file and handler can be specified:

```python
lambda_.NodejsFunction(self, "MyFunction",
    entry="/path/to/my/file.ts",  # accepts .js, .jsx, .ts, .tsx and .mjs files
    handler="myExportedFunc"
)
```

For monorepos, the reference architecture becomes:

```plaintext
.
├── packages
│   ├── cool-package
│   │   ├── lib
│   │   │   ├── cool-construct.api.ts
│   │   │   ├── cool-construct.auth.ts
│   │   │   └── cool-construct.ts
│   │   ├── package.json # CDK and runtime dependencies for cool-package
│   │   └── tsconfig.json
│   └── super-package
│       ├── lib
│       │   ├── super-construct.handler.ts
│       │   └── super-construct.ts
│       ├── package.json # CDK and runtime dependencies for super-package
│       └── tsconfig.json
├── package-lock.json # single lock file
├── package.json # root dependencies
└── tsconfig.json
```

## Customizing the underlying Lambda function

All properties of `lambda.Function` can be used to customize the underlying `lambda.Function`.

See also the [AWS Lambda construct library](https://github.com/aws/aws-cdk/tree/master/packages/%40aws-cdk/aws-lambda).

The `NodejsFunction` construct automatically [reuses existing connections](https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html)
when working with the AWS SDK for JavaScript. Set the `awsSdkConnectionReuse` prop to `false` to disable it.

## Lock file

The `NodejsFunction` requires a dependencies lock file (`yarn.lock`, `pnpm-lock.yaml` or
`package-lock.json`). When bundling in a Docker container, the path containing this lock file is
used as the source (`/asset-input`) for the volume mounted in the container.

By default, the construct will try to automatically determine your project lock file.
Alternatively, you can specify the `depsLockFilePath` prop manually. In this
case you need to ensure that this path includes `entry` and any module/dependencies
used by your function. Otherwise bundling will fail.

## Local bundling

If `esbuild` is available it will be used to bundle your code in your environment. Otherwise,
bundling will happen in a [Lambda compatible Docker container](https://gallery.ecr.aws/sam/build-nodejs12.x)
with the Docker platform based on the target architecture of the Lambda function.

For macOS the recommended approach is to install `esbuild` as Docker volume performance is really poor.

`esbuild` can be installed with:

```console
$ npm install --save-dev esbuild@0
```

OR

```console
$ yarn add --dev esbuild@0
```

If you're using a monorepo layout, the `esbuild` dependency needs to be installed in the "root" `package.json` file,
not in the workspace. From the reference architecture described [above](#reference-project-architecture), the `esbuild`
dev dependency needs to be in `./package.json`, not `packages/cool-package/package.json` or
`packages/super-package/package.json`.

To force bundling in a Docker container even if `esbuild` is available in your environment,
set `bundling.forceDockerBundling` to `true`. This is useful if your function relies on node
modules that should be installed (`nodeModules` prop, see [below](#install-modules)) in a Lambda
compatible environment. This is usually the case with modules using native dependencies.

## Working with modules

### Externals

By default, all node modules are bundled except for `aws-sdk`. This can be configured by specifying
`bundling.externalModules`:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        external_modules=["aws-sdk", "cool-module"
        ]
    )
)
```

### Install modules

By default, all node modules referenced in your Lambda code will be bundled by `esbuild`.
Use the `nodeModules` prop under `bundling` to specify a list of modules that should not be
bundled but instead included in the `node_modules` folder of the Lambda package. This is useful
when working with native dependencies or when `esbuild` fails to bundle a module.

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        node_modules=["native-module", "other-module"]
    )
)
```

The modules listed in `nodeModules` must be present in the `package.json`'s dependencies or
installed. The same version will be used for installation. The lock file (`yarn.lock`,
`pnpm-lock.yaml` or `package-lock.json`) will be used along with the right installer (`yarn`,
`pnpm` or `npm`).

When working with `nodeModules` using native dependencies, you might want to force bundling in a
Docker container even if `esbuild` is available in your environment. This can be done by setting
`bundling.forceDockerBundling` to `true`.

## Configuring `esbuild`

The `NodejsFunction` construct exposes [esbuild options](https://esbuild.github.io/api/#build-api)
via properties under `bundling`:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        minify=True,  # minify code, defaults to false
        source_map=True,  # include source map, defaults to false
        source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
        sources_content=False,  # do not include original source into source map, defaults to true
        target="es2020",  # target environment for the generated JavaScript code
        loader={ # Use the 'dataurl' loader for '.png' files
            ".png": "dataurl"},
        define={ # Replace strings during build time
            "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
            "process.env.PRODUCTION": JSON.stringify(True),
            "process.env.NUMBER": JSON.stringify(123)},
        log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
        keep_names=True,  # defaults to false
        tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
        metafile=True,  # include meta file, defaults to false
        banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
        footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
        charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
        format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
        main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
        inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
        esbuild_args={ # Pass additional arguments to esbuild
            "--log-limit": "0",
            "--splitting": True}
    )
)
```

## Command hooks

It is possible to run additional commands by specifying the `commandHooks` prop:

```text
// This example only available in TypeScript
// Run additional props via `commandHooks`
new lambda.NodejsFunction(this, 'my-handler-with-commands', {
  bundling: {
    commandHooks: {
      beforeBundling(inputDir: string, outputDir: string): string[] {
        return [
          `echo hello > ${inputDir}/a.txt`,
          `cp ${inputDir}/a.txt ${outputDir}`,
        ];
      },
      afterBundling(inputDir: string, outputDir: string): string[] {
        return [`cp ${inputDir}/b.txt ${outputDir}/txt`];
      },
      beforeInstall() {
        return [];
      },
      // ...
    },
    // ...
  },
});
```

The following hooks are available:

* `beforeBundling`: runs before all bundling commands
* `beforeInstall`: runs before node modules installation
* `afterBundling`: runs after all bundling commands

They all receive the directory containing the lock file (`inputDir`) and the
directory where the bundled asset will be output (`outputDir`). They must return
an array of commands to run. Commands are chained with `&&`.

The commands will run in the environment in which bundling occurs: inside the
container for Docker bundling or on the host OS for local bundling.

## Pre Compilation with TSC

In some cases, `esbuild` may not yet support some newer features of the typescript language, such as,
[`emitDecoratorMetadata`](https://www.typescriptlang.org/tsconfig#emitDecoratorMetadata).
In such cases, it is possible to run pre-compilation using `tsc` by setting the `preCompilation` flag.

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        pre_compilation=True
    )
)
```

Note: A [`tsconfig.json` file](https://www.typescriptlang.org/docs/handbook/tsconfig-json.html) is required

## Customizing Docker bundling

Use `bundling.environment` to define environments variables when `esbuild` runs:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        environment={
            "NODE_ENV": "production"
        }
    )
)
```

Use `bundling.buildArgs` to pass build arguments when building the Docker bundling image:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        build_args={
            "HTTPS_PROXY": "https://127.0.0.1:3001"
        }
    )
)
```

Use `bundling.dockerImage` to use a custom Docker bundling image:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        docker_image=DockerImage.from_build("/path/to/Dockerfile")
    )
)
```

This image should have `esbuild` installed **globally**. If you plan to use `nodeModules` it
should also have `npm`, `yarn` or `pnpm` depending on the lock file you're using.

Use the [default image provided by `@aws-cdk/aws-lambda-nodejs`](https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile)
as a source of inspiration.

## Asset hash

By default the asset hash will be calculated based on the bundled output (`AssetHashType.OUTPUT`).

Use the `assetHash` prop to pass a custom hash:

```python
lambda_.NodejsFunction(self, "my-handler",
    bundling=lambda.aws_lambda_nodejs.BundlingOptions(
        asset_hash="my-custom-hash"
    )
)
```

If you chose to customize the hash, you will need to make sure it is updated every time the asset
changes, or otherwise it is possible that some deployments will not be invalidated.
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
    Construct as _Construct_e78e779f,
    DockerImage as _DockerImage_d5f0ad8e,
    Duration as _Duration_070aa057,
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
    LogRetentionRetryOptions as _LogRetentionRetryOptions_7acc40ab,
    Runtime as _Runtime_932d369a,
    Tracing as _Tracing_b7f4a8b6,
    VersionOptions as _VersionOptions_085bb455,
)
from ..aws_logs import RetentionDays as _RetentionDays_6c560d31
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.data_type(
    jsii_type="monocdk.aws_lambda_nodejs.BundlingOptions",
    jsii_struct_bases=[],
    name_mapping={
        "asset_hash": "assetHash",
        "banner": "banner",
        "build_args": "buildArgs",
        "charset": "charset",
        "command_hooks": "commandHooks",
        "define": "define",
        "docker_image": "dockerImage",
        "environment": "environment",
        "esbuild_args": "esbuildArgs",
        "esbuild_version": "esbuildVersion",
        "external_modules": "externalModules",
        "footer": "footer",
        "force_docker_bundling": "forceDockerBundling",
        "format": "format",
        "inject": "inject",
        "keep_names": "keepNames",
        "loader": "loader",
        "log_level": "logLevel",
        "main_fields": "mainFields",
        "metafile": "metafile",
        "minify": "minify",
        "node_modules": "nodeModules",
        "pre_compilation": "preCompilation",
        "source_map": "sourceMap",
        "source_map_mode": "sourceMapMode",
        "sources_content": "sourcesContent",
        "target": "target",
        "tsconfig": "tsconfig",
    },
)
class BundlingOptions:
    def __init__(
        self,
        *,
        asset_hash: typing.Optional[builtins.str] = None,
        banner: typing.Optional[builtins.str] = None,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        charset: typing.Optional["Charset"] = None,
        command_hooks: typing.Optional["ICommandHooks"] = None,
        define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_image: typing.Optional[_DockerImage_d5f0ad8e] = None,
        environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        esbuild_args: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
        esbuild_version: typing.Optional[builtins.str] = None,
        external_modules: typing.Optional[typing.Sequence[builtins.str]] = None,
        footer: typing.Optional[builtins.str] = None,
        force_docker_bundling: typing.Optional[builtins.bool] = None,
        format: typing.Optional["OutputFormat"] = None,
        inject: typing.Optional[typing.Sequence[builtins.str]] = None,
        keep_names: typing.Optional[builtins.bool] = None,
        loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        log_level: typing.Optional["LogLevel"] = None,
        main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
        metafile: typing.Optional[builtins.bool] = None,
        minify: typing.Optional[builtins.bool] = None,
        node_modules: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_compilation: typing.Optional[builtins.bool] = None,
        source_map: typing.Optional[builtins.bool] = None,
        source_map_mode: typing.Optional["SourceMapMode"] = None,
        sources_content: typing.Optional[builtins.bool] = None,
        target: typing.Optional[builtins.str] = None,
        tsconfig: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Bundling options.

        :param asset_hash: (experimental) Specify a custom hash for this asset. For consistency, this custom hash will be SHA256 hashed and encoded as hex. The resulting hash will be the asset hash. NOTE: the hash is used in order to identify a specific revision of the asset, and used for optimizing and caching deployment activities related to this asset such as packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will need to make sure it is updated every time the asset changes, or otherwise it is possible that some deployments will not be invalidated. Default: - asset hash is calculated based on the bundled output
        :param banner: (experimental) Use this to insert an arbitrary string at the beginning of generated JavaScript files. This is similar to footer which inserts at the end instead of the beginning. This is commonly used to insert comments: Default: - no comments are passed
        :param build_args: (experimental) Build arguments to pass when building the bundling image. Default: - no build arguments are passed
        :param charset: (experimental) The charset to use for esbuild's output. By default esbuild's output is ASCII-only. Any non-ASCII characters are escaped using backslash escape sequences. Using escape sequences makes the generated output slightly bigger, and also makes it harder to read. If you would like for esbuild to print the original characters without using escape sequences, use ``Charset.UTF8``. Default: Charset.ASCII
        :param command_hooks: (experimental) Command hooks. Default: - do not run additional commands
        :param define: (experimental) Replace global identifiers with constant expressions. For example, ``{ 'process.env.DEBUG': 'true' }``. Another example, ``{ 'process.env.API_KEY': JSON.stringify('xxx-xxxx-xxx') }``. Default: - no replacements are made
        :param docker_image: (experimental) A custom bundling Docker image. This image should have esbuild installed globally. If you plan to use ``nodeModules`` it should also have ``npm`` or ``yarn`` depending on the lock file you're using. See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile for the default image provided by @aws-cdk/aws-lambda-nodejs. Default: - use the Docker image provided by
        :param environment: (experimental) Environment variables defined when bundling runs. Default: - no environment variables are defined.
        :param esbuild_args: (experimental) Build arguments to pass into esbuild. For example, to add the `--log-limit <https://esbuild.github.io/api/#log-limit>`_ flag:: new NodejsFunction(scope, id, { ... bundling: { esbuildArgs: { "--log-limit": "0", } } }); Default: - no additional esbuild arguments are passed
        :param esbuild_version: (experimental) The version of esbuild to use when running in a Docker container. Default: - latest v0
        :param external_modules: (experimental) A list of modules that should be considered as externals (already available in the runtime). Default: ['aws-sdk']
        :param footer: (experimental) Use this to insert an arbitrary string at the end of generated JavaScript files. This is similar to banner which inserts at the beginning instead of the end. This is commonly used to insert comments Default: - no comments are passed
        :param force_docker_bundling: (experimental) Force bundling in a Docker container even if local bundling is possible. This is useful if your function relies on node modules that should be installed (``nodeModules``) in a Lambda compatible environment. Default: false
        :param format: (experimental) Output format for the generated JavaScript files. Default: OutputFormat.CJS
        :param inject: (experimental) This option allows you to automatically replace a global variable with an import from another file. Default: - no code is injected
        :param keep_names: (experimental) Whether to preserve the original ``name`` values even in minified code. In JavaScript the ``name`` property on functions and classes defaults to a nearby identifier in the source code. However, minification renames symbols to reduce code size and bundling sometimes need to rename symbols to avoid collisions. That changes value of the ``name`` property for many of these cases. This is usually fine because the ``name`` property is normally only used for debugging. However, some frameworks rely on the ``name`` property for registration and binding purposes. If this is the case, you can enable this option to preserve the original ``name`` values even in minified code. Default: false
        :param loader: (experimental) Use loaders to change how a given input file is interpreted. Configuring a loader for a given file type lets you load that file type with an ``import`` statement or a ``require`` call. Default: - use esbuild default loaders
        :param log_level: (experimental) Log level for esbuild. This is also propagated to the package manager and applies to its specific install command. Default: LogLevel.WARNING
        :param main_fields: (experimental) How to determine the entry point for modules. Try ['module', 'main'] to default to ES module versions. Default: ['main', 'module']
        :param metafile: (experimental) This option tells esbuild to write out a JSON file relative to output directory with metadata about the build. The metadata in this JSON file follows this schema (specified using TypeScript syntax):: { outputs: { [path: string]: { bytes: number inputs: { [path: string]: { bytesInOutput: number } } imports: { path: string }[] exports: string[] } } } This data can then be analyzed by other tools. For example, bundle buddy can consume esbuild's metadata format and generates a treemap visualization of the modules in your bundle and how much space each one takes up. Default: false
        :param minify: (experimental) Whether to minify files when bundling. Default: false
        :param node_modules: (experimental) A list of modules that should be installed instead of bundled. Modules are installed in a Lambda compatible environment only when bundling runs in Docker. Default: - all modules are bundled
        :param pre_compilation: (experimental) Run compilation using tsc before running file through bundling step. This usually is not required unless you are using new experimental features that are only supported by typescript's ``tsc`` compiler. One example of such feature is ``emitDecoratorMetadata``. Default: false
        :param source_map: (experimental) Whether to include source maps when bundling. Default: false
        :param source_map_mode: (experimental) Source map mode to be used when bundling. Default: SourceMapMode.DEFAULT
        :param sources_content: (experimental) Whether to include original source code in source maps when bundling. Default: true
        :param target: (experimental) Target environment for the generated JavaScript code. Default: - the node version of the runtime
        :param tsconfig: (experimental) Normally the esbuild automatically discovers ``tsconfig.json`` files and reads their contents during a build. However, you can also configure a custom ``tsconfig.json`` file to use instead. This is similar to entry path, you need to provide path to your custom ``tsconfig.json``. This can be useful if you need to do multiple builds of the same code with different settings. For example, ``{ 'tsconfig': 'path/custom.tsconfig.json' }``. Default: - automatically discovered by ``esbuild``

        :stability: experimental
        :exampleMetadata: infused

        Example::

            lambda_.NodejsFunction(self, "my-handler",
                bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                    docker_image=DockerImage.from_build("/path/to/Dockerfile")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98e846d4f4d28d2be609bd4cfe151c0673af5111339d568a5f4366dac6b98fb0)
            check_type(argname="argument asset_hash", value=asset_hash, expected_type=type_hints["asset_hash"])
            check_type(argname="argument banner", value=banner, expected_type=type_hints["banner"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument charset", value=charset, expected_type=type_hints["charset"])
            check_type(argname="argument command_hooks", value=command_hooks, expected_type=type_hints["command_hooks"])
            check_type(argname="argument define", value=define, expected_type=type_hints["define"])
            check_type(argname="argument docker_image", value=docker_image, expected_type=type_hints["docker_image"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument esbuild_args", value=esbuild_args, expected_type=type_hints["esbuild_args"])
            check_type(argname="argument esbuild_version", value=esbuild_version, expected_type=type_hints["esbuild_version"])
            check_type(argname="argument external_modules", value=external_modules, expected_type=type_hints["external_modules"])
            check_type(argname="argument footer", value=footer, expected_type=type_hints["footer"])
            check_type(argname="argument force_docker_bundling", value=force_docker_bundling, expected_type=type_hints["force_docker_bundling"])
            check_type(argname="argument format", value=format, expected_type=type_hints["format"])
            check_type(argname="argument inject", value=inject, expected_type=type_hints["inject"])
            check_type(argname="argument keep_names", value=keep_names, expected_type=type_hints["keep_names"])
            check_type(argname="argument loader", value=loader, expected_type=type_hints["loader"])
            check_type(argname="argument log_level", value=log_level, expected_type=type_hints["log_level"])
            check_type(argname="argument main_fields", value=main_fields, expected_type=type_hints["main_fields"])
            check_type(argname="argument metafile", value=metafile, expected_type=type_hints["metafile"])
            check_type(argname="argument minify", value=minify, expected_type=type_hints["minify"])
            check_type(argname="argument node_modules", value=node_modules, expected_type=type_hints["node_modules"])
            check_type(argname="argument pre_compilation", value=pre_compilation, expected_type=type_hints["pre_compilation"])
            check_type(argname="argument source_map", value=source_map, expected_type=type_hints["source_map"])
            check_type(argname="argument source_map_mode", value=source_map_mode, expected_type=type_hints["source_map_mode"])
            check_type(argname="argument sources_content", value=sources_content, expected_type=type_hints["sources_content"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
            check_type(argname="argument tsconfig", value=tsconfig, expected_type=type_hints["tsconfig"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if asset_hash is not None:
            self._values["asset_hash"] = asset_hash
        if banner is not None:
            self._values["banner"] = banner
        if build_args is not None:
            self._values["build_args"] = build_args
        if charset is not None:
            self._values["charset"] = charset
        if command_hooks is not None:
            self._values["command_hooks"] = command_hooks
        if define is not None:
            self._values["define"] = define
        if docker_image is not None:
            self._values["docker_image"] = docker_image
        if environment is not None:
            self._values["environment"] = environment
        if esbuild_args is not None:
            self._values["esbuild_args"] = esbuild_args
        if esbuild_version is not None:
            self._values["esbuild_version"] = esbuild_version
        if external_modules is not None:
            self._values["external_modules"] = external_modules
        if footer is not None:
            self._values["footer"] = footer
        if force_docker_bundling is not None:
            self._values["force_docker_bundling"] = force_docker_bundling
        if format is not None:
            self._values["format"] = format
        if inject is not None:
            self._values["inject"] = inject
        if keep_names is not None:
            self._values["keep_names"] = keep_names
        if loader is not None:
            self._values["loader"] = loader
        if log_level is not None:
            self._values["log_level"] = log_level
        if main_fields is not None:
            self._values["main_fields"] = main_fields
        if metafile is not None:
            self._values["metafile"] = metafile
        if minify is not None:
            self._values["minify"] = minify
        if node_modules is not None:
            self._values["node_modules"] = node_modules
        if pre_compilation is not None:
            self._values["pre_compilation"] = pre_compilation
        if source_map is not None:
            self._values["source_map"] = source_map
        if source_map_mode is not None:
            self._values["source_map_mode"] = source_map_mode
        if sources_content is not None:
            self._values["sources_content"] = sources_content
        if target is not None:
            self._values["target"] = target
        if tsconfig is not None:
            self._values["tsconfig"] = tsconfig

    @builtins.property
    def asset_hash(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specify a custom hash for this asset.

        For consistency, this custom hash will
        be SHA256 hashed and encoded as hex. The resulting hash will be the asset
        hash.

        NOTE: the hash is used in order to identify a specific revision of the asset, and
        used for optimizing and caching deployment activities related to this asset such as
        packaging, uploading to Amazon S3, etc. If you chose to customize the hash, you will
        need to make sure it is updated every time the asset changes, or otherwise it is
        possible that some deployments will not be invalidated.

        :default: - asset hash is calculated based on the bundled output

        :stability: experimental
        '''
        result = self._values.get("asset_hash")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def banner(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use this to insert an arbitrary string at the beginning of generated JavaScript files.

        This is similar to footer which inserts at the end instead of the beginning.

        This is commonly used to insert comments:

        :default: - no comments are passed

        :stability: experimental
        '''
        result = self._values.get("banner")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build arguments to pass when building the bundling image.

        :default: - no build arguments are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def charset(self) -> typing.Optional["Charset"]:
        '''(experimental) The charset to use for esbuild's output.

        By default esbuild's output is ASCII-only. Any non-ASCII characters are escaped
        using backslash escape sequences. Using escape sequences makes the generated output
        slightly bigger, and also makes it harder to read. If you would like for esbuild to print
        the original characters without using escape sequences, use ``Charset.UTF8``.

        :default: Charset.ASCII

        :see: https://esbuild.github.io/api/#charset
        :stability: experimental
        '''
        result = self._values.get("charset")
        return typing.cast(typing.Optional["Charset"], result)

    @builtins.property
    def command_hooks(self) -> typing.Optional["ICommandHooks"]:
        '''(experimental) Command hooks.

        :default: - do not run additional commands

        :stability: experimental
        '''
        result = self._values.get("command_hooks")
        return typing.cast(typing.Optional["ICommandHooks"], result)

    @builtins.property
    def define(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Replace global identifiers with constant expressions.

        For example, ``{ 'process.env.DEBUG': 'true' }``.

        Another example, ``{ 'process.env.API_KEY': JSON.stringify('xxx-xxxx-xxx') }``.

        :default: - no replacements are made

        :stability: experimental
        '''
        result = self._values.get("define")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_image(self) -> typing.Optional[_DockerImage_d5f0ad8e]:
        '''(experimental) A custom bundling Docker image.

        This image should have esbuild installed globally. If you plan to use ``nodeModules``
        it should also have ``npm`` or ``yarn`` depending on the lock file you're using.

        See https://github.com/aws/aws-cdk/blob/master/packages/%40aws-cdk/aws-lambda-nodejs/lib/Dockerfile
        for the default image provided by @aws-cdk/aws-lambda-nodejs.

        :default: - use the Docker image provided by

        :stability: experimental
        :aws-cdk: /aws-lambda-nodejs
        '''
        result = self._values.get("docker_image")
        return typing.cast(typing.Optional[_DockerImage_d5f0ad8e], result)

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
    def esbuild_args(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]]:
        '''(experimental) Build arguments to pass into esbuild.

        For example, to add the `--log-limit <https://esbuild.github.io/api/#log-limit>`_ flag::

           new NodejsFunction(scope, id, {
              ...
              bundling: {
                esbuildArgs: {
                  "--log-limit": "0",
                }
              }
           });

        :default: - no additional esbuild arguments are passed

        :stability: experimental
        '''
        result = self._values.get("esbuild_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]], result)

    @builtins.property
    def esbuild_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) The version of esbuild to use when running in a Docker container.

        :default: - latest v0

        :stability: experimental
        '''
        result = self._values.get("esbuild_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def external_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of modules that should be considered as externals (already available in the runtime).

        :default: ['aws-sdk']

        :stability: experimental
        '''
        result = self._values.get("external_modules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def footer(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use this to insert an arbitrary string at the end of generated JavaScript files.

        This is similar to banner which inserts at the beginning instead of the end.

        This is commonly used to insert comments

        :default: - no comments are passed

        :stability: experimental
        '''
        result = self._values.get("footer")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def force_docker_bundling(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force bundling in a Docker container even if local bundling is possible.

        This is useful if your function relies on node modules
        that should be installed (``nodeModules``) in a Lambda compatible
        environment.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force_docker_bundling")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def format(self) -> typing.Optional["OutputFormat"]:
        '''(experimental) Output format for the generated JavaScript files.

        :default: OutputFormat.CJS

        :stability: experimental
        '''
        result = self._values.get("format")
        return typing.cast(typing.Optional["OutputFormat"], result)

    @builtins.property
    def inject(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) This option allows you to automatically replace a global variable with an import from another file.

        :default: - no code is injected

        :see: https://esbuild.github.io/api/#inject
        :stability: experimental
        '''
        result = self._values.get("inject")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def keep_names(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to preserve the original ``name`` values even in minified code.

        In JavaScript the ``name`` property on functions and classes defaults to a
        nearby identifier in the source code.

        However, minification renames symbols to reduce code size and bundling
        sometimes need to rename symbols to avoid collisions. That changes value of
        the ``name`` property for many of these cases. This is usually fine because
        the ``name`` property is normally only used for debugging. However, some
        frameworks rely on the ``name`` property for registration and binding purposes.
        If this is the case, you can enable this option to preserve the original
        ``name`` values even in minified code.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("keep_names")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def loader(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Use loaders to change how a given input file is interpreted.

        Configuring a loader for a given file type lets you load that file type with
        an ``import`` statement or a ``require`` call.

        :default: - use esbuild default loaders

        :see:

        https://esbuild.github.io/api/#loader

        For example, ``{ '.png': 'dataurl' }``.
        :stability: experimental
        '''
        result = self._values.get("loader")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def log_level(self) -> typing.Optional["LogLevel"]:
        '''(experimental) Log level for esbuild.

        This is also propagated to the package manager and
        applies to its specific install command.

        :default: LogLevel.WARNING

        :stability: experimental
        '''
        result = self._values.get("log_level")
        return typing.cast(typing.Optional["LogLevel"], result)

    @builtins.property
    def main_fields(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) How to determine the entry point for modules.

        Try ['module', 'main'] to default to ES module versions.

        :default: ['main', 'module']

        :stability: experimental
        '''
        result = self._values.get("main_fields")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def metafile(self) -> typing.Optional[builtins.bool]:
        '''(experimental) This option tells esbuild to write out a JSON file relative to output directory with metadata about the build.

        The metadata in this JSON file follows this schema (specified using TypeScript syntax)::

           {
              outputs: {
                [path: string]: {
                  bytes: number
                  inputs: {
                    [path: string]: { bytesInOutput: number }
                  }
                  imports: { path: string }[]
                  exports: string[]
                }
              }
           }

        This data can then be analyzed by other tools. For example,
        bundle buddy can consume esbuild's metadata format and generates a treemap visualization
        of the modules in your bundle and how much space each one takes up.

        :default: false

        :see: https://esbuild.github.io/api/#metafile
        :stability: experimental
        '''
        result = self._values.get("metafile")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def minify(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to minify files when bundling.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("minify")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def node_modules(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A list of modules that should be installed instead of bundled.

        Modules are
        installed in a Lambda compatible environment only when bundling runs in
        Docker.

        :default: - all modules are bundled

        :stability: experimental
        '''
        result = self._values.get("node_modules")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_compilation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run compilation using tsc before running file through bundling step.

        This usually is not required unless you are using new experimental features that
        are only supported by typescript's ``tsc`` compiler.
        One example of such feature is ``emitDecoratorMetadata``.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("pre_compilation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_map(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include source maps when bundling.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("source_map")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_map_mode(self) -> typing.Optional["SourceMapMode"]:
        '''(experimental) Source map mode to be used when bundling.

        :default: SourceMapMode.DEFAULT

        :see: https://esbuild.github.io/api/#sourcemap
        :stability: experimental
        '''
        result = self._values.get("source_map_mode")
        return typing.cast(typing.Optional["SourceMapMode"], result)

    @builtins.property
    def sources_content(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to include original source code in source maps when bundling.

        :default: true

        :see: https://esbuild.github.io/api/#sources-content
        :stability: experimental
        '''
        result = self._values.get("sources_content")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target environment for the generated JavaScript code.

        :default: - the node version of the runtime

        :see: https://esbuild.github.io/api/#target
        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tsconfig(self) -> typing.Optional[builtins.str]:
        '''(experimental) Normally the esbuild automatically discovers ``tsconfig.json`` files and reads their contents during a build.

        However, you can also configure a custom ``tsconfig.json`` file to use instead.

        This is similar to entry path, you need to provide path to your custom ``tsconfig.json``.

        This can be useful if you need to do multiple builds of the same code with different settings.

        For example, ``{ 'tsconfig': 'path/custom.tsconfig.json' }``.

        :default: - automatically discovered by ``esbuild``

        :stability: experimental
        '''
        result = self._values.get("tsconfig")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BundlingOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_lambda_nodejs.Charset")
class Charset(enum.Enum):
    '''(experimental) Charset for esbuild's output.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.NodejsFunction(self, "my-handler",
            bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                minify=True,  # minify code, defaults to false
                source_map=True,  # include source map, defaults to false
                source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
                sources_content=False,  # do not include original source into source map, defaults to true
                target="es2020",  # target environment for the generated JavaScript code
                loader={ # Use the 'dataurl' loader for '.png' files
                    ".png": "dataurl"},
                define={ # Replace strings during build time
                    "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
                    "process.env.PRODUCTION": JSON.stringify(True),
                    "process.env.NUMBER": JSON.stringify(123)},
                log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
                keep_names=True,  # defaults to false
                tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
                metafile=True,  # include meta file, defaults to false
                banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
                format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
                main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
                inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
                esbuild_args={ # Pass additional arguments to esbuild
                    "--log-limit": "0",
                    "--splitting": True}
            )
        )
    '''

    ASCII = "ASCII"
    '''(experimental) ASCII.

    Any non-ASCII characters are escaped using backslash escape sequences

    :stability: experimental
    '''
    UTF8 = "UTF8"
    '''(experimental) UTF-8.

    Keep original characters without using escape sequences

    :stability: experimental
    '''


@jsii.interface(jsii_type="monocdk.aws_lambda_nodejs.ICommandHooks")
class ICommandHooks(typing_extensions.Protocol):
    '''(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    The following example (specified in TypeScript) copies a file from the input
    directory to the output directory to include it in the bundled asset::

       afterBundling(inputDir: string, outputDir: string): string[]{
          return [`cp ${inputDir}/my-binary.node ${outputDir}`];
       }

    :stability: experimental
    '''

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        ...


class _ICommandHooksProxy:
    '''(experimental) Command hooks.

    These commands will run in the environment in which bundling occurs: inside
    the container for Docker bundling or on the host OS for local bundling.

    Commands are chained with ``&&``.

    The following example (specified in TypeScript) copies a file from the input
    directory to the output directory to include it in the bundled asset::

       afterBundling(inputDir: string, outputDir: string): string[]{
          return [`cp ${inputDir}/my-binary.node ${outputDir}`];
       }

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.aws_lambda_nodejs.ICommandHooks"

    @jsii.member(jsii_name="afterBundling")
    def after_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run after bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4671893e321c1a777a610baf6c60fbe44dd747ece6e0d849eb3ad613b63b774c)
            check_type(argname="argument input_dir", value=input_dir, expected_type=type_hints["input_dir"])
            check_type(argname="argument output_dir", value=output_dir, expected_type=type_hints["output_dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "afterBundling", [input_dir, output_dir]))

    @jsii.member(jsii_name="beforeBundling")
    def before_bundling(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before bundling.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f5010ad80d31f2f01542b5d0fd0e889a0ab62b6d278a944b5a31a92e8c26e32c)
            check_type(argname="argument input_dir", value=input_dir, expected_type=type_hints["input_dir"])
            check_type(argname="argument output_dir", value=output_dir, expected_type=type_hints["output_dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "beforeBundling", [input_dir, output_dir]))

    @jsii.member(jsii_name="beforeInstall")
    def before_install(
        self,
        input_dir: builtins.str,
        output_dir: builtins.str,
    ) -> typing.List[builtins.str]:
        '''(experimental) Returns commands to run before installing node modules.

        This hook only runs when node modules are installed.

        Commands are chained with ``&&``.

        :param input_dir: -
        :param output_dir: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a31571778fae41b7f3124ccf4449af662face8e3163647b95e71d0e1315992f1)
            check_type(argname="argument input_dir", value=input_dir, expected_type=type_hints["input_dir"])
            check_type(argname="argument output_dir", value=output_dir, expected_type=type_hints["output_dir"])
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "beforeInstall", [input_dir, output_dir]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICommandHooks).__jsii_proxy_class__ = lambda : _ICommandHooksProxy


@jsii.enum(jsii_type="monocdk.aws_lambda_nodejs.LogLevel")
class LogLevel(enum.Enum):
    '''(experimental) Log levels for esbuild and package managers' install commands.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.NodejsFunction(self, "my-handler",
            bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                minify=True,  # minify code, defaults to false
                source_map=True,  # include source map, defaults to false
                source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
                sources_content=False,  # do not include original source into source map, defaults to true
                target="es2020",  # target environment for the generated JavaScript code
                loader={ # Use the 'dataurl' loader for '.png' files
                    ".png": "dataurl"},
                define={ # Replace strings during build time
                    "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
                    "process.env.PRODUCTION": JSON.stringify(True),
                    "process.env.NUMBER": JSON.stringify(123)},
                log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
                keep_names=True,  # defaults to false
                tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
                metafile=True,  # include meta file, defaults to false
                banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
                format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
                main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
                inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
                esbuild_args={ # Pass additional arguments to esbuild
                    "--log-limit": "0",
                    "--splitting": True}
            )
        )
    '''

    INFO = "INFO"
    '''(experimental) Show everything.

    :stability: experimental
    '''
    WARNING = "WARNING"
    '''(experimental) Show warnings and errors.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Show errors only.

    :stability: experimental
    '''
    SILENT = "SILENT"
    '''(experimental) Show nothing.

    :stability: experimental
    '''


class NodejsFunction(
    _Function_40b20aa5,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunction",
):
    '''(experimental) A Node.js Lambda function bundled using esbuild.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.NodejsFunction(self, "my-handler",
            bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                docker_image=DockerImage.from_build("/path/to/Dockerfile")
            )
        )
    '''

    def __init__(
        self,
        scope: _Construct_e78e779f,
        id: builtins.str,
        *,
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        project_root: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
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
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param project_root: (experimental) The path to the directory containing project config files (``package.json`` or ``tsconfig.json``). Default: - the directory containing the ``depsLockFilePath``
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: Runtime.NODEJS_14_X
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
            type_hints = typing.get_type_hints(_typecheckingstub__50005495ed98ad74d38cc48ef08451eb4ad250e160548016eca0f7fb9d65535f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = NodejsFunctionProps(
            aws_sdk_connection_reuse=aws_sdk_connection_reuse,
            bundling=bundling,
            deps_lock_file_path=deps_lock_file_path,
            entry=entry,
            handler=handler,
            project_root=project_root,
            runtime=runtime,
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
    jsii_type="monocdk.aws_lambda_nodejs.NodejsFunctionProps",
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
        "aws_sdk_connection_reuse": "awsSdkConnectionReuse",
        "bundling": "bundling",
        "deps_lock_file_path": "depsLockFilePath",
        "entry": "entry",
        "handler": "handler",
        "project_root": "projectRoot",
        "runtime": "runtime",
    },
)
class NodejsFunctionProps(_FunctionOptions_dc75a392):
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
        aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
        bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        deps_lock_file_path: typing.Optional[builtins.str] = None,
        entry: typing.Optional[builtins.str] = None,
        handler: typing.Optional[builtins.str] = None,
        project_root: typing.Optional[builtins.str] = None,
        runtime: typing.Optional[_Runtime_932d369a] = None,
    ) -> None:
        '''(experimental) Properties for a NodejsFunction.

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
        :param aws_sdk_connection_reuse: (experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript. This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable to ``1``. Default: true
        :param bundling: (experimental) Bundling options. Default: - use default bundling options: no minify, no sourcemap, all modules are bundled.
        :param deps_lock_file_path: (experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``). This will be used as the source for the volume mounted in the Docker container. Modules specified in ``nodeModules`` will be installed using the right installer (``npm`` or ``yarn``) along with this lock file. Default: - the path is found by walking up parent directories searching for a ``yarn.lock`` or ``package-lock.json`` file
        :param entry: (experimental) Path to the entry file (JavaScript or TypeScript). Default: - Derived from the name of the defining file and the construct's id. If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts`` and ``stack.my-handler.js``.
        :param handler: (experimental) The name of the exported handler in the entry file. Default: handler
        :param project_root: (experimental) The path to the directory containing project config files (``package.json`` or ``tsconfig.json``). Default: - the directory containing the ``depsLockFilePath``
        :param runtime: (experimental) The runtime environment. Only runtimes of the Node.js family are supported. Default: Runtime.NODEJS_14_X

        :stability: experimental
        :exampleMetadata: infused

        Example::

            lambda_.NodejsFunction(self, "my-handler",
                bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                    minify=True,  # minify code, defaults to false
                    source_map=True,  # include source map, defaults to false
                    source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
                    sources_content=False,  # do not include original source into source map, defaults to true
                    target="es2020",  # target environment for the generated JavaScript code
                    loader={ # Use the 'dataurl' loader for '.png' files
                        ".png": "dataurl"},
                    define={ # Replace strings during build time
                        "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
                        "process.env.PRODUCTION": JSON.stringify(True),
                        "process.env.NUMBER": JSON.stringify(123)},
                    log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
                    keep_names=True,  # defaults to false
                    tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
                    metafile=True,  # include meta file, defaults to false
                    banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                    footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                    charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
                    format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
                    main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
                    inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
                    esbuild_args={ # Pass additional arguments to esbuild
                        "--log-limit": "0",
                        "--splitting": True}
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
            type_hints = typing.get_type_hints(_typecheckingstub__1b9a97293c9974766f841ed6cfa58d24852542837d455793cb55fd22c0a96798)
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
            check_type(argname="argument aws_sdk_connection_reuse", value=aws_sdk_connection_reuse, expected_type=type_hints["aws_sdk_connection_reuse"])
            check_type(argname="argument bundling", value=bundling, expected_type=type_hints["bundling"])
            check_type(argname="argument deps_lock_file_path", value=deps_lock_file_path, expected_type=type_hints["deps_lock_file_path"])
            check_type(argname="argument entry", value=entry, expected_type=type_hints["entry"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument project_root", value=project_root, expected_type=type_hints["project_root"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
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
        if aws_sdk_connection_reuse is not None:
            self._values["aws_sdk_connection_reuse"] = aws_sdk_connection_reuse
        if bundling is not None:
            self._values["bundling"] = bundling
        if deps_lock_file_path is not None:
            self._values["deps_lock_file_path"] = deps_lock_file_path
        if entry is not None:
            self._values["entry"] = entry
        if handler is not None:
            self._values["handler"] = handler
        if project_root is not None:
            self._values["project_root"] = project_root
        if runtime is not None:
            self._values["runtime"] = runtime

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
    def aws_sdk_connection_reuse(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to automatically reuse TCP connections when working with the AWS SDK for JavaScript.

        This sets the ``AWS_NODEJS_CONNECTION_REUSE_ENABLED`` environment variable
        to ``1``.

        :default: true

        :see: https://docs.aws.amazon.com/sdk-for-javascript/v2/developer-guide/node-reusing-connections.html
        :stability: experimental
        '''
        result = self._values.get("aws_sdk_connection_reuse")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def bundling(self) -> typing.Optional[BundlingOptions]:
        '''(experimental) Bundling options.

        :default:

        - use default bundling options: no minify, no sourcemap, all
        modules are bundled.

        :stability: experimental
        '''
        result = self._values.get("bundling")
        return typing.cast(typing.Optional[BundlingOptions], result)

    @builtins.property
    def deps_lock_file_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the dependencies lock file (``yarn.lock`` or ``package-lock.json``).

        This will be used as the source for the volume mounted in the Docker
        container.

        Modules specified in ``nodeModules`` will be installed using the right
        installer (``npm`` or ``yarn``) along with this lock file.

        :default:

        - the path is found by walking up parent directories searching for
        a ``yarn.lock`` or ``package-lock.json`` file

        :stability: experimental
        '''
        result = self._values.get("deps_lock_file_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def entry(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the entry file (JavaScript or TypeScript).

        :default:

        - Derived from the name of the defining file and the construct's id.
        If the ``NodejsFunction`` is defined in ``stack.ts`` with ``my-handler`` as id
        (``new NodejsFunction(this, 'my-handler')``), the construct will look at ``stack.my-handler.ts``
        and ``stack.my-handler.js``.

        :stability: experimental
        '''
        result = self._values.get("entry")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def handler(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the exported handler in the entry file.

        :default: handler

        :stability: experimental
        '''
        result = self._values.get("handler")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def project_root(self) -> typing.Optional[builtins.str]:
        '''(experimental) The path to the directory containing project config files (``package.json`` or ``tsconfig.json``).

        :default: - the directory containing the ``depsLockFilePath``

        :stability: experimental
        '''
        result = self._values.get("project_root")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runtime(self) -> typing.Optional[_Runtime_932d369a]:
        '''(experimental) The runtime environment.

        Only runtimes of the Node.js family are
        supported.

        :default: Runtime.NODEJS_14_X

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional[_Runtime_932d369a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NodejsFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.aws_lambda_nodejs.OutputFormat")
class OutputFormat(enum.Enum):
    '''(experimental) Output format for the generated JavaScript files.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.NodejsFunction(self, "my-handler",
            bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                minify=True,  # minify code, defaults to false
                source_map=True,  # include source map, defaults to false
                source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
                sources_content=False,  # do not include original source into source map, defaults to true
                target="es2020",  # target environment for the generated JavaScript code
                loader={ # Use the 'dataurl' loader for '.png' files
                    ".png": "dataurl"},
                define={ # Replace strings during build time
                    "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
                    "process.env.PRODUCTION": JSON.stringify(True),
                    "process.env.NUMBER": JSON.stringify(123)},
                log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
                keep_names=True,  # defaults to false
                tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
                metafile=True,  # include meta file, defaults to false
                banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
                format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
                main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
                inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
                esbuild_args={ # Pass additional arguments to esbuild
                    "--log-limit": "0",
                    "--splitting": True}
            )
        )
    '''

    CJS = "CJS"
    '''(experimental) CommonJS.

    :stability: experimental
    '''
    ESM = "ESM"
    '''(experimental) ECMAScript module.

    Requires a running environment that supports ``import`` and ``export`` syntax.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.aws_lambda_nodejs.SourceMapMode")
class SourceMapMode(enum.Enum):
    '''(experimental) SourceMap mode for esbuild.

    :see: https://esbuild.github.io/api/#sourcemap
    :stability: experimental
    :exampleMetadata: infused

    Example::

        lambda_.NodejsFunction(self, "my-handler",
            bundling=lambda.aws_lambda_nodejs.BundlingOptions(
                minify=True,  # minify code, defaults to false
                source_map=True,  # include source map, defaults to false
                source_map_mode=lambda_.SourceMapMode.INLINE,  # defaults to SourceMapMode.DEFAULT
                sources_content=False,  # do not include original source into source map, defaults to true
                target="es2020",  # target environment for the generated JavaScript code
                loader={ # Use the 'dataurl' loader for '.png' files
                    ".png": "dataurl"},
                define={ # Replace strings during build time
                    "process.env.API_KEY": JSON.stringify("xxx-xxxx-xxx"),
                    "process.env.PRODUCTION": JSON.stringify(True),
                    "process.env.NUMBER": JSON.stringify(123)},
                log_level=lambda_.LogLevel.SILENT,  # defaults to LogLevel.WARNING
                keep_names=True,  # defaults to false
                tsconfig="custom-tsconfig.json",  # use custom-tsconfig.json instead of default,
                metafile=True,  # include meta file, defaults to false
                banner="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                footer="/* comments */",  # requires esbuild >= 0.9.0, defaults to none
                charset=lambda_.Charset.UTF8,  # do not escape non-ASCII characters, defaults to Charset.ASCII
                format=lambda_.OutputFormat.ESM,  # ECMAScript module output format, defaults to OutputFormat.CJS (OutputFormat.ESM requires Node.js 14.x)
                main_fields=["module", "main"],  # prefer ECMAScript versions of dependencies
                inject=["./my-shim.js", "./other-shim.js"],  # allows to automatically replace a global variable with an import from another file
                esbuild_args={ # Pass additional arguments to esbuild
                    "--log-limit": "0",
                    "--splitting": True}
            )
        )
    '''

    DEFAULT = "DEFAULT"
    '''(experimental) Default sourceMap mode - will generate a .js.map file alongside any generated .js file and add a special //# sourceMappingURL= comment to the bottom of the .js file pointing to the .js.map file.

    :stability: experimental
    '''
    EXTERNAL = "EXTERNAL"
    '''(experimental) External sourceMap mode - If you want to omit the special //# sourceMappingURL= comment from the generated .js file but you still want to generate the .js.map files.

    :stability: experimental
    '''
    INLINE = "INLINE"
    '''(experimental) Inline sourceMap mode - If you want to insert the entire source map into the .js file instead of generating a separate .js.map file.

    :stability: experimental
    '''
    BOTH = "BOTH"
    '''(experimental) Both sourceMap mode - If you want to have the effect of both inline and external simultaneously.

    :stability: experimental
    '''


__all__ = [
    "BundlingOptions",
    "Charset",
    "ICommandHooks",
    "LogLevel",
    "NodejsFunction",
    "NodejsFunctionProps",
    "OutputFormat",
    "SourceMapMode",
]

publication.publish()

def _typecheckingstub__98e846d4f4d28d2be609bd4cfe151c0673af5111339d568a5f4366dac6b98fb0(
    *,
    asset_hash: typing.Optional[builtins.str] = None,
    banner: typing.Optional[builtins.str] = None,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    charset: typing.Optional[Charset] = None,
    command_hooks: typing.Optional[ICommandHooks] = None,
    define: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_image: typing.Optional[_DockerImage_d5f0ad8e] = None,
    environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    esbuild_args: typing.Optional[typing.Mapping[builtins.str, typing.Union[builtins.str, builtins.bool]]] = None,
    esbuild_version: typing.Optional[builtins.str] = None,
    external_modules: typing.Optional[typing.Sequence[builtins.str]] = None,
    footer: typing.Optional[builtins.str] = None,
    force_docker_bundling: typing.Optional[builtins.bool] = None,
    format: typing.Optional[OutputFormat] = None,
    inject: typing.Optional[typing.Sequence[builtins.str]] = None,
    keep_names: typing.Optional[builtins.bool] = None,
    loader: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    log_level: typing.Optional[LogLevel] = None,
    main_fields: typing.Optional[typing.Sequence[builtins.str]] = None,
    metafile: typing.Optional[builtins.bool] = None,
    minify: typing.Optional[builtins.bool] = None,
    node_modules: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_compilation: typing.Optional[builtins.bool] = None,
    source_map: typing.Optional[builtins.bool] = None,
    source_map_mode: typing.Optional[SourceMapMode] = None,
    sources_content: typing.Optional[builtins.bool] = None,
    target: typing.Optional[builtins.str] = None,
    tsconfig: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4671893e321c1a777a610baf6c60fbe44dd747ece6e0d849eb3ad613b63b774c(
    input_dir: builtins.str,
    output_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f5010ad80d31f2f01542b5d0fd0e889a0ab62b6d278a944b5a31a92e8c26e32c(
    input_dir: builtins.str,
    output_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a31571778fae41b7f3124ccf4449af662face8e3163647b95e71d0e1315992f1(
    input_dir: builtins.str,
    output_dir: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50005495ed98ad74d38cc48ef08451eb4ad250e160548016eca0f7fb9d65535f(
    scope: _Construct_e78e779f,
    id: builtins.str,
    *,
    aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps_lock_file_path: typing.Optional[builtins.str] = None,
    entry: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    project_root: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[_Runtime_932d369a] = None,
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

def _typecheckingstub__1b9a97293c9974766f841ed6cfa58d24852542837d455793cb55fd22c0a96798(
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
    aws_sdk_connection_reuse: typing.Optional[builtins.bool] = None,
    bundling: typing.Optional[typing.Union[BundlingOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    deps_lock_file_path: typing.Optional[builtins.str] = None,
    entry: typing.Optional[builtins.str] = None,
    handler: typing.Optional[builtins.str] = None,
    project_root: typing.Optional[builtins.str] = None,
    runtime: typing.Optional[_Runtime_932d369a] = None,
) -> None:
    """Type checking stubs"""
    pass
