'''
# Cloud Assembly Schema

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Cloud Assembly

The *Cloud Assembly* is the output of the synthesis operation. It is produced as part of the
[`cdk synth`](https://github.com/aws/aws-cdk/tree/master/packages/aws-cdk#cdk-synthesize)
command, or the [`app.synth()`](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/core/lib/app.ts#L135) method invocation.

Its essentially a set of files and directories, one of which is the `manifest.json` file. It defines the set of instructions that are
needed in order to deploy the assembly directory.

> For example, when `cdk deploy` is executed, the CLI reads this file and performs its instructions:
>
> * Build container images.
> * Upload assets.
> * Deploy CloudFormation templates.

Therefore, the assembly is how the CDK class library and CDK CLI (or any other consumer) communicate. To ensure compatibility
between the assembly and its consumers, we treat the manifest file as a well defined, versioned schema.

## Schema

This module contains the typescript structs that comprise the `manifest.json` file, as well as the
generated [*json-schema*](./schema/cloud-assembly.schema.json).

## Versioning

The schema version is specified in the [`cloud-assembly.version.json`](./schema/cloud-assembly.schema.json) file, under the `version` property.
It follows semantic versioning, but with a small twist.

When we add instructions to the assembly, they are reflected in the manifest file and the *json-schema* accordingly.
Every such instruction, is crucial for ensuring the correct deployment behavior. This means that to properly deploy a cloud assembly,
consumers must be aware of every such instruction modification.

For this reason, every change to the schema, even though it might not strictly break validation of the *json-schema* format,
is considered `major` version bump.

## How to consume

If you'd like to consume the [schema file](./schema/cloud-assembly.schema.json) in order to do validations on `manifest.json` files,
simply download it from this repo and run it against standard *json-schema* validators, such as [jsonschema](https://www.npmjs.com/package/jsonschema).

Consumers must take into account the `major` version of the schema they are consuming. They should reject cloud assemblies
with a `major` version that is higher than what they expect. While schema validation might pass on such assemblies, the deployment integrity
cannot be guaranteed because some instructions will be ignored.

> For example, if your consumer was built when the schema version was 2.0.0, you should reject deploying cloud assemblies with a
> manifest version of 3.0.0.

## Contributing

See [Contribution Guide](./CONTRIBUTING.md)
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


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AmiContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "filters": "filters",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
        "owners": "owners",
    },
)
class AmiContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        filters: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
        owners: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Query to AMI context provider.

        :param account: (experimental) Account to query.
        :param filters: (experimental) Filters to DescribeImages call.
        :param region: (experimental) Region to query.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None
        :param owners: (experimental) Owners to DescribeImages call. Default: - All owners

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            ami_context_query = cloud_assembly_schema.AmiContextQuery(
                account="account",
                filters={
                    "filters_key": ["filters"]
                },
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn",
                owners=["owners"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8f2a94285068509b87a6e46df77bbf8877588baa46f3d664d316eb5cd15d7911)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
            check_type(argname="argument owners", value=owners, expected_type=type_hints["owners"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "filters": filters,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn
        if owners is not None:
            self._values["owners"] = owners

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Account to query.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filters(self) -> typing.Mapping[builtins.str, typing.List[builtins.str]]:
        '''(experimental) Filters to DescribeImages call.

        :stability: experimental
        '''
        result = self._values.get("filters")
        assert result is not None, "Required property 'filters' is missing"
        return typing.cast(typing.Mapping[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Region to query.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def owners(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Owners to DescribeImages call.

        :default: - All owners

        :stability: experimental
        '''
        result = self._values.get("owners")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AmiContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.ArtifactManifest",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "dependencies": "dependencies",
        "display_name": "displayName",
        "environment": "environment",
        "metadata": "metadata",
        "properties": "properties",
    },
)
class ArtifactManifest:
    def __init__(
        self,
        *,
        type: "ArtifactType",
        dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
        display_name: typing.Optional[builtins.str] = None,
        environment: typing.Optional[builtins.str] = None,
        metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union["MetadataEntry", typing.Dict[builtins.str, typing.Any]]]]] = None,
        properties: typing.Optional[typing.Union[typing.Union["AwsCloudFormationStackProperties", typing.Dict[builtins.str, typing.Any]], typing.Union["AssetManifestProperties", typing.Dict[builtins.str, typing.Any]], typing.Union["TreeArtifactProperties", typing.Dict[builtins.str, typing.Any]], typing.Union["NestedCloudAssemblyProperties", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) A manifest for a single artifact within the cloud assembly.

        :param type: (experimental) The type of artifact.
        :param dependencies: (experimental) IDs of artifacts that must be deployed before this artifact. Default: - no dependencies.
        :param display_name: (experimental) A string that represents this artifact. Should only be used in user interfaces. Default: - no display name
        :param environment: (experimental) The environment into which this artifact is deployed. Default: - no envrionment.
        :param metadata: (experimental) Associated metadata. Default: - no metadata.
        :param properties: (experimental) The set of properties for this artifact (depends on type). Default: - no properties.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            artifact_manifest = cloud_assembly_schema.ArtifactManifest(
                type=cloud_assembly_schema.ArtifactType.NONE,
            
                # the properties below are optional
                dependencies=["dependencies"],
                display_name="displayName",
                environment="environment",
                metadata={
                    "metadata_key": [cloud_assembly_schema.MetadataEntry(
                        type="type",
            
                        # the properties below are optional
                        data="data",
                        trace=["trace"]
                    )]
                },
                properties=cloud_assembly_schema.AwsCloudFormationStackProperties(
                    template_file="templateFile",
            
                    # the properties below are optional
                    assume_role_arn="assumeRoleArn",
                    assume_role_external_id="assumeRoleExternalId",
                    bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                    cloud_formation_execution_role_arn="cloudFormationExecutionRoleArn",
                    lookup_role=cloud_assembly_schema.BootstrapRole(
                        arn="arn",
            
                        # the properties below are optional
                        assume_role_external_id="assumeRoleExternalId",
                        bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                        requires_bootstrap_stack_version=123
                    ),
                    parameters={
                        "parameters_key": "parameters"
                    },
                    requires_bootstrap_stack_version=123,
                    stack_name="stackName",
                    stack_template_asset_object_url="stackTemplateAssetObjectUrl",
                    tags={
                        "tags_key": "tags"
                    },
                    termination_protection=False,
                    validate_on_synth=False
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2432006d5d04f100829a91ebe1f4bed220c293772b8d7048ecf07ba71b9af9)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument dependencies", value=dependencies, expected_type=type_hints["dependencies"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument metadata", value=metadata, expected_type=type_hints["metadata"])
            check_type(argname="argument properties", value=properties, expected_type=type_hints["properties"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if dependencies is not None:
            self._values["dependencies"] = dependencies
        if display_name is not None:
            self._values["display_name"] = display_name
        if environment is not None:
            self._values["environment"] = environment
        if metadata is not None:
            self._values["metadata"] = metadata
        if properties is not None:
            self._values["properties"] = properties

    @builtins.property
    def type(self) -> "ArtifactType":
        '''(experimental) The type of artifact.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast("ArtifactType", result)

    @builtins.property
    def dependencies(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) IDs of artifacts that must be deployed before this artifact.

        :default: - no dependencies.

        :stability: experimental
        '''
        result = self._values.get("dependencies")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) A string that represents this artifact.

        Should only be used in user interfaces.

        :default: - no display name

        :stability: experimental
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The environment into which this artifact is deployed.

        :default: - no envrionment.

        :stability: experimental
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def metadata(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List["MetadataEntry"]]]:
        '''(experimental) Associated metadata.

        :default: - no metadata.

        :stability: experimental
        '''
        result = self._values.get("metadata")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List["MetadataEntry"]]], result)

    @builtins.property
    def properties(
        self,
    ) -> typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]]:
        '''(experimental) The set of properties for this artifact (depends on type).

        :default: - no properties.

        :stability: experimental
        '''
        result = self._values.get("properties")
        return typing.cast(typing.Optional[typing.Union["AwsCloudFormationStackProperties", "AssetManifestProperties", "TreeArtifactProperties", "NestedCloudAssemblyProperties"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ArtifactManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.ArtifactMetadataEntryType")
class ArtifactMetadataEntryType(enum.Enum):
    '''(experimental) Type of artifact metadata entry.

    :stability: experimental
    '''

    ASSET = "ASSET"
    '''(experimental) Asset in metadata.

    :stability: experimental
    '''
    INFO = "INFO"
    '''(experimental) Metadata key used to print INFO-level messages by the toolkit when an app is syntheized.

    :stability: experimental
    '''
    WARN = "WARN"
    '''(experimental) Metadata key used to print WARNING-level messages by the toolkit when an app is syntheized.

    :stability: experimental
    '''
    ERROR = "ERROR"
    '''(experimental) Metadata key used to print ERROR-level messages by the toolkit when an app is syntheized.

    :stability: experimental
    '''
    LOGICAL_ID = "LOGICAL_ID"
    '''(experimental) Represents the CloudFormation logical ID of a resource at a certain path.

    :stability: experimental
    '''
    STACK_TAGS = "STACK_TAGS"
    '''(experimental) Represents tags of a stack.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.ArtifactType")
class ArtifactType(enum.Enum):
    '''(experimental) Type of cloud artifact.

    :stability: experimental
    '''

    NONE = "NONE"
    '''(experimental) Stub required because of JSII.

    :stability: experimental
    '''
    AWS_CLOUDFORMATION_STACK = "AWS_CLOUDFORMATION_STACK"
    '''(experimental) The artifact is an AWS CloudFormation stack.

    :stability: experimental
    '''
    CDK_TREE = "CDK_TREE"
    '''(experimental) The artifact contains the CDK application's construct tree.

    :stability: experimental
    '''
    ASSET_MANIFEST = "ASSET_MANIFEST"
    '''(experimental) Manifest for all assets in the Cloud Assembly.

    :stability: experimental
    '''
    NESTED_CLOUD_ASSEMBLY = "NESTED_CLOUD_ASSEMBLY"
    '''(experimental) Nested Cloud Assembly.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AssemblyManifest",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "artifacts": "artifacts",
        "missing": "missing",
        "runtime": "runtime",
    },
)
class AssemblyManifest:
    def __init__(
        self,
        *,
        version: builtins.str,
        artifacts: typing.Optional[typing.Mapping[builtins.str, typing.Union[ArtifactManifest, typing.Dict[builtins.str, typing.Any]]]] = None,
        missing: typing.Optional[typing.Sequence[typing.Union["MissingContext", typing.Dict[builtins.str, typing.Any]]]] = None,
        runtime: typing.Optional[typing.Union["RuntimeInfo", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) A manifest which describes the cloud assembly.

        :param version: (experimental) Protocol version.
        :param artifacts: (experimental) The set of artifacts in this assembly. Default: - no artifacts.
        :param missing: (experimental) Missing context information. If this field has values, it means that the cloud assembly is not complete and should not be deployed. Default: - no missing context.
        :param runtime: (experimental) Runtime information. Default: - no info.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            assembly_manifest = cloud_assembly_schema.AssemblyManifest(
                version="version",
            
                # the properties below are optional
                artifacts={
                    "artifacts_key": cloud_assembly_schema.ArtifactManifest(
                        type=cloud_assembly_schema.ArtifactType.NONE,
            
                        # the properties below are optional
                        dependencies=["dependencies"],
                        display_name="displayName",
                        environment="environment",
                        metadata={
                            "metadata_key": [cloud_assembly_schema.MetadataEntry(
                                type="type",
            
                                # the properties below are optional
                                data="data",
                                trace=["trace"]
                            )]
                        },
                        properties=cloud_assembly_schema.AwsCloudFormationStackProperties(
                            template_file="templateFile",
            
                            # the properties below are optional
                            assume_role_arn="assumeRoleArn",
                            assume_role_external_id="assumeRoleExternalId",
                            bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                            cloud_formation_execution_role_arn="cloudFormationExecutionRoleArn",
                            lookup_role=cloud_assembly_schema.BootstrapRole(
                                arn="arn",
            
                                # the properties below are optional
                                assume_role_external_id="assumeRoleExternalId",
                                bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                                requires_bootstrap_stack_version=123
                            ),
                            parameters={
                                "parameters_key": "parameters"
                            },
                            requires_bootstrap_stack_version=123,
                            stack_name="stackName",
                            stack_template_asset_object_url="stackTemplateAssetObjectUrl",
                            tags={
                                "tags_key": "tags"
                            },
                            termination_protection=False,
                            validate_on_synth=False
                        )
                    )
                },
                missing=[cloud_assembly_schema.MissingContext(
                    key="key",
                    props=cloud_assembly_schema.AmiContextQuery(
                        account="account",
                        filters={
                            "filters_key": ["filters"]
                        },
                        region="region",
            
                        # the properties below are optional
                        lookup_role_arn="lookupRoleArn",
                        owners=["owners"]
                    ),
                    provider=cloud_assembly_schema.ContextProvider.AMI_PROVIDER
                )],
                runtime=cloud_assembly_schema.RuntimeInfo(
                    libraries={
                        "libraries_key": "libraries"
                    }
                )
            )
        '''
        if isinstance(runtime, dict):
            runtime = RuntimeInfo(**runtime)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2b85c4f7731874e306253a41ce60384ca15cbb300d41778f681e47a3fe65b472)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument missing", value=missing, expected_type=type_hints["missing"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if artifacts is not None:
            self._values["artifacts"] = artifacts
        if missing is not None:
            self._values["missing"] = missing
        if runtime is not None:
            self._values["runtime"] = runtime

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Protocol version.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ArtifactManifest]]:
        '''(experimental) The set of artifacts in this assembly.

        :default: - no artifacts.

        :stability: experimental
        '''
        result = self._values.get("artifacts")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ArtifactManifest]], result)

    @builtins.property
    def missing(self) -> typing.Optional[typing.List["MissingContext"]]:
        '''(experimental) Missing context information.

        If this field has values, it means that the
        cloud assembly is not complete and should not be deployed.

        :default: - no missing context.

        :stability: experimental
        '''
        result = self._values.get("missing")
        return typing.cast(typing.Optional[typing.List["MissingContext"]], result)

    @builtins.property
    def runtime(self) -> typing.Optional["RuntimeInfo"]:
        '''(experimental) Runtime information.

        :default: - no info.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        return typing.cast(typing.Optional["RuntimeInfo"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssemblyManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AssetManifest",
    jsii_struct_bases=[],
    name_mapping={
        "version": "version",
        "docker_images": "dockerImages",
        "files": "files",
    },
)
class AssetManifest:
    def __init__(
        self,
        *,
        version: builtins.str,
        docker_images: typing.Optional[typing.Mapping[builtins.str, typing.Union["DockerImageAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
        files: typing.Optional[typing.Mapping[builtins.str, typing.Union["FileAsset", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Definitions for the asset manifest.

        :param version: (experimental) Version of the manifest.
        :param docker_images: (experimental) The Docker image assets in this manifest. Default: - No Docker images
        :param files: (experimental) The file assets in this manifest. Default: - No files

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            asset_manifest = cloud_assembly_schema.AssetManifest(
                version="version",
            
                # the properties below are optional
                docker_images={
                    "docker_images_key": cloud_assembly_schema.DockerImageAsset(
                        destinations={
                            "destinations_key": cloud_assembly_schema.DockerImageDestination(
                                image_tag="imageTag",
                                repository_name="repositoryName",
            
                                # the properties below are optional
                                assume_role_arn="assumeRoleArn",
                                assume_role_external_id="assumeRoleExternalId",
                                region="region"
                            )
                        },
                        source=cloud_assembly_schema.DockerImageSource(
                            directory="directory",
                            docker_build_args={
                                "docker_build_args_key": "dockerBuildArgs"
                            },
                            docker_build_target="dockerBuildTarget",
                            docker_file="dockerFile",
                            executable=["executable"],
                            network_mode="networkMode",
                            platform="platform"
                        )
                    )
                },
                files={
                    "files_key": cloud_assembly_schema.FileAsset(
                        destinations={
                            "destinations_key": cloud_assembly_schema.FileDestination(
                                bucket_name="bucketName",
                                object_key="objectKey",
            
                                # the properties below are optional
                                assume_role_arn="assumeRoleArn",
                                assume_role_external_id="assumeRoleExternalId",
                                region="region"
                            )
                        },
                        source=cloud_assembly_schema.FileSource(
                            executable=["executable"],
                            packaging=cloud_assembly_schema.FileAssetPackaging.FILE,
                            path="path"
                        )
                    )
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3f137c27eef0c5d528b8056a661fb2dd1e87a7fe7b9b631b4f2a3d34d9fcb6ab)
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument docker_images", value=docker_images, expected_type=type_hints["docker_images"])
            check_type(argname="argument files", value=files, expected_type=type_hints["files"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "version": version,
        }
        if docker_images is not None:
            self._values["docker_images"] = docker_images
        if files is not None:
            self._values["files"] = files

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Version of the manifest.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def docker_images(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "DockerImageAsset"]]:
        '''(experimental) The Docker image assets in this manifest.

        :default: - No Docker images

        :stability: experimental
        '''
        result = self._values.get("docker_images")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "DockerImageAsset"]], result)

    @builtins.property
    def files(self) -> typing.Optional[typing.Mapping[builtins.str, "FileAsset"]]:
        '''(experimental) The file assets in this manifest.

        :default: - No files

        :stability: experimental
        '''
        result = self._values.get("files")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "FileAsset"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AssetManifestProperties",
    jsii_struct_bases=[],
    name_mapping={
        "file": "file",
        "bootstrap_stack_version_ssm_parameter": "bootstrapStackVersionSsmParameter",
        "requires_bootstrap_stack_version": "requiresBootstrapStackVersion",
    },
)
class AssetManifestProperties:
    def __init__(
        self,
        *,
        file: builtins.str,
        bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
        requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Artifact properties for the Asset Manifest.

        :param file: (experimental) Filename of the asset manifest.
        :param bootstrap_stack_version_ssm_parameter: (experimental) SSM parameter where the bootstrap stack version number can be found. - If this value is not set, the bootstrap stack name must be known at deployment time so the stack version can be looked up from the stack outputs. - If this value is set, the bootstrap stack can have any name because we won't need to look it up. Default: - Bootstrap stack version number looked up
        :param requires_bootstrap_stack_version: (experimental) Version of bootstrap stack required to deploy this stack. Default: - Version 1 (basic modern bootstrap stack)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            asset_manifest_properties = cloud_assembly_schema.AssetManifestProperties(
                file="file",
            
                # the properties below are optional
                bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                requires_bootstrap_stack_version=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__387089bdef8ecbb6f514cc4ce3a76d1f595d51bda2855168a6a43b1aee7dbdae)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument bootstrap_stack_version_ssm_parameter", value=bootstrap_stack_version_ssm_parameter, expected_type=type_hints["bootstrap_stack_version_ssm_parameter"])
            check_type(argname="argument requires_bootstrap_stack_version", value=requires_bootstrap_stack_version, expected_type=type_hints["requires_bootstrap_stack_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
        }
        if bootstrap_stack_version_ssm_parameter is not None:
            self._values["bootstrap_stack_version_ssm_parameter"] = bootstrap_stack_version_ssm_parameter
        if requires_bootstrap_stack_version is not None:
            self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version

    @builtins.property
    def file(self) -> builtins.str:
        '''(experimental) Filename of the asset manifest.

        :stability: experimental
        '''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def bootstrap_stack_version_ssm_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSM parameter where the bootstrap stack version number can be found.

        - If this value is not set, the bootstrap stack name must be known at
          deployment time so the stack version can be looked up from the stack
          outputs.
        - If this value is set, the bootstrap stack can have any name because
          we won't need to look it up.

        :default: - Bootstrap stack version number looked up

        :stability: experimental
        '''
        result = self._values.get("bootstrap_stack_version_ssm_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of bootstrap stack required to deploy this stack.

        :default: - Version 1 (basic modern bootstrap stack)

        :stability: experimental
        '''
        result = self._values.get("requires_bootstrap_stack_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetManifestProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AvailabilityZonesContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class AvailabilityZonesContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query to availability zone context provider.

        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            availability_zones_context_query = cloud_assembly_schema.AvailabilityZonesContextQuery(
                account="account",
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__484a0ae5d95e7545a4d8aa23b962078607c6b75b66ebd14ac72f9344756da7af)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AvailabilityZonesContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AwsCloudFormationStackProperties",
    jsii_struct_bases=[],
    name_mapping={
        "template_file": "templateFile",
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "bootstrap_stack_version_ssm_parameter": "bootstrapStackVersionSsmParameter",
        "cloud_formation_execution_role_arn": "cloudFormationExecutionRoleArn",
        "lookup_role": "lookupRole",
        "parameters": "parameters",
        "requires_bootstrap_stack_version": "requiresBootstrapStackVersion",
        "stack_name": "stackName",
        "stack_template_asset_object_url": "stackTemplateAssetObjectUrl",
        "tags": "tags",
        "termination_protection": "terminationProtection",
        "validate_on_synth": "validateOnSynth",
    },
)
class AwsCloudFormationStackProperties:
    def __init__(
        self,
        *,
        template_file: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
        cloud_formation_execution_role_arn: typing.Optional[builtins.str] = None,
        lookup_role: typing.Optional[typing.Union["BootstrapRole", typing.Dict[builtins.str, typing.Any]]] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
        stack_name: typing.Optional[builtins.str] = None,
        stack_template_asset_object_url: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        termination_protection: typing.Optional[builtins.bool] = None,
        validate_on_synth: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Artifact properties for CloudFormation stacks.

        :param template_file: (experimental) A file relative to the assembly root which contains the CloudFormation template for this stack.
        :param assume_role_arn: (experimental) The role that needs to be assumed to deploy the stack. Default: - No role is assumed (current credentials are used)
        :param assume_role_external_id: (experimental) External ID to use when assuming role for cloudformation deployments. Default: - No external ID
        :param bootstrap_stack_version_ssm_parameter: (experimental) SSM parameter where the bootstrap stack version number can be found. Only used if ``requiresBootstrapStackVersion`` is set. - If this value is not set, the bootstrap stack name must be known at deployment time so the stack version can be looked up from the stack outputs. - If this value is set, the bootstrap stack can have any name because we won't need to look it up. Default: - Bootstrap stack version number looked up
        :param cloud_formation_execution_role_arn: (experimental) The role that is passed to CloudFormation to execute the change set. Default: - No role is passed (currently assumed role/credentials are used)
        :param lookup_role: (experimental) The role to use to look up values from the target AWS account. Default: - No role is assumed (current credentials are used)
        :param parameters: (experimental) Values for CloudFormation stack parameters that should be passed when the stack is deployed. Default: - No parameters
        :param requires_bootstrap_stack_version: (experimental) Version of bootstrap stack required to deploy this stack. Default: - No bootstrap stack required
        :param stack_name: (experimental) The name to use for the CloudFormation stack. Default: - name derived from artifact ID
        :param stack_template_asset_object_url: (experimental) If the stack template has already been included in the asset manifest, its asset URL. Default: - Not uploaded yet, upload just before deploying
        :param tags: (experimental) Values for CloudFormation stack tags that should be passed when the stack is deployed. Default: - No tags
        :param termination_protection: (experimental) Whether to enable termination protection for this stack. Default: false
        :param validate_on_synth: (experimental) Whether this stack should be validated by the CLI after synthesis. Default: - false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            aws_cloud_formation_stack_properties = cloud_assembly_schema.AwsCloudFormationStackProperties(
                template_file="templateFile",
            
                # the properties below are optional
                assume_role_arn="assumeRoleArn",
                assume_role_external_id="assumeRoleExternalId",
                bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                cloud_formation_execution_role_arn="cloudFormationExecutionRoleArn",
                lookup_role=cloud_assembly_schema.BootstrapRole(
                    arn="arn",
            
                    # the properties below are optional
                    assume_role_external_id="assumeRoleExternalId",
                    bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                    requires_bootstrap_stack_version=123
                ),
                parameters={
                    "parameters_key": "parameters"
                },
                requires_bootstrap_stack_version=123,
                stack_name="stackName",
                stack_template_asset_object_url="stackTemplateAssetObjectUrl",
                tags={
                    "tags_key": "tags"
                },
                termination_protection=False,
                validate_on_synth=False
            )
        '''
        if isinstance(lookup_role, dict):
            lookup_role = BootstrapRole(**lookup_role)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8360008dbc98119effa4cbbb84f73ccc3be2fc630e9bdfaa0e36433554394fdf)
            check_type(argname="argument template_file", value=template_file, expected_type=type_hints["template_file"])
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument assume_role_external_id", value=assume_role_external_id, expected_type=type_hints["assume_role_external_id"])
            check_type(argname="argument bootstrap_stack_version_ssm_parameter", value=bootstrap_stack_version_ssm_parameter, expected_type=type_hints["bootstrap_stack_version_ssm_parameter"])
            check_type(argname="argument cloud_formation_execution_role_arn", value=cloud_formation_execution_role_arn, expected_type=type_hints["cloud_formation_execution_role_arn"])
            check_type(argname="argument lookup_role", value=lookup_role, expected_type=type_hints["lookup_role"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument requires_bootstrap_stack_version", value=requires_bootstrap_stack_version, expected_type=type_hints["requires_bootstrap_stack_version"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument stack_template_asset_object_url", value=stack_template_asset_object_url, expected_type=type_hints["stack_template_asset_object_url"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument termination_protection", value=termination_protection, expected_type=type_hints["termination_protection"])
            check_type(argname="argument validate_on_synth", value=validate_on_synth, expected_type=type_hints["validate_on_synth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "template_file": template_file,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if bootstrap_stack_version_ssm_parameter is not None:
            self._values["bootstrap_stack_version_ssm_parameter"] = bootstrap_stack_version_ssm_parameter
        if cloud_formation_execution_role_arn is not None:
            self._values["cloud_formation_execution_role_arn"] = cloud_formation_execution_role_arn
        if lookup_role is not None:
            self._values["lookup_role"] = lookup_role
        if parameters is not None:
            self._values["parameters"] = parameters
        if requires_bootstrap_stack_version is not None:
            self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version
        if stack_name is not None:
            self._values["stack_name"] = stack_name
        if stack_template_asset_object_url is not None:
            self._values["stack_template_asset_object_url"] = stack_template_asset_object_url
        if tags is not None:
            self._values["tags"] = tags
        if termination_protection is not None:
            self._values["termination_protection"] = termination_protection
        if validate_on_synth is not None:
            self._values["validate_on_synth"] = validate_on_synth

    @builtins.property
    def template_file(self) -> builtins.str:
        '''(experimental) A file relative to the assembly root which contains the CloudFormation template for this stack.

        :stability: experimental
        '''
        result = self._values.get("template_file")
        assert result is not None, "Required property 'template_file' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that needs to be assumed to deploy the stack.

        :default: - No role is assumed (current credentials are used)

        :stability: experimental
        '''
        result = self._values.get("assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) External ID to use when assuming role for cloudformation deployments.

        :default: - No external ID

        :stability: experimental
        '''
        result = self._values.get("assume_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bootstrap_stack_version_ssm_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) SSM parameter where the bootstrap stack version number can be found.

        Only used if ``requiresBootstrapStackVersion`` is set.

        - If this value is not set, the bootstrap stack name must be known at
          deployment time so the stack version can be looked up from the stack
          outputs.
        - If this value is set, the bootstrap stack can have any name because
          we won't need to look it up.

        :default: - Bootstrap stack version number looked up

        :stability: experimental
        '''
        result = self._values.get("bootstrap_stack_version_ssm_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def cloud_formation_execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that is passed to CloudFormation to execute the change set.

        :default: - No role is passed (currently assumed role/credentials are used)

        :stability: experimental
        '''
        result = self._values.get("cloud_formation_execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def lookup_role(self) -> typing.Optional["BootstrapRole"]:
        '''(experimental) The role to use to look up values from the target AWS account.

        :default: - No role is assumed (current credentials are used)

        :stability: experimental
        '''
        result = self._values.get("lookup_role")
        return typing.cast(typing.Optional["BootstrapRole"], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Values for CloudFormation stack parameters that should be passed when the stack is deployed.

        :default: - No parameters

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of bootstrap stack required to deploy this stack.

        :default: - No bootstrap stack required

        :stability: experimental
        '''
        result = self._values.get("requires_bootstrap_stack_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name to use for the CloudFormation stack.

        :default: - name derived from artifact ID

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_template_asset_object_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) If the stack template has already been included in the asset manifest, its asset URL.

        :default: - Not uploaded yet, upload just before deploying

        :stability: experimental
        '''
        result = self._values.get("stack_template_asset_object_url")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Values for CloudFormation stack tags that should be passed when the stack is deployed.

        :default: - No tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def termination_protection(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to enable termination protection for this stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("termination_protection")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def validate_on_synth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether this stack should be validated by the CLI after synthesis.

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("validate_on_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCloudFormationStackProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.AwsDestination",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
    },
)
class AwsDestination:
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Destination for assets that need to be uploaded to AWS.

        :param assume_role_arn: (experimental) The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: (experimental) The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: (experimental) The region where this asset will need to be published. Default: - Current region

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            aws_destination = cloud_assembly_schema.AwsDestination(
                assume_role_arn="assumeRoleArn",
                assume_role_external_id="assumeRoleExternalId",
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1933cfb6bff539b5e63360451650e4155ca2b378e2c47c4ee913043ed1a161ed)
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument assume_role_external_id", value=assume_role_external_id, expected_type=type_hints["assume_role_external_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed

        :stability: experimental
        '''
        result = self._values.get("assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied

        :stability: experimental
        '''
        result = self._values.get("assume_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where this asset will need to be published.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.BootstrapRole",
    jsii_struct_bases=[],
    name_mapping={
        "arn": "arn",
        "assume_role_external_id": "assumeRoleExternalId",
        "bootstrap_stack_version_ssm_parameter": "bootstrapStackVersionSsmParameter",
        "requires_bootstrap_stack_version": "requiresBootstrapStackVersion",
    },
)
class BootstrapRole:
    def __init__(
        self,
        *,
        arn: builtins.str,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
        requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Information needed to access an IAM role created as part of the bootstrap process.

        :param arn: (experimental) The ARN of the IAM role created as part of bootrapping e.g. lookupRoleArn.
        :param assume_role_external_id: (experimental) External ID to use when assuming the bootstrap role. Default: - No external ID
        :param bootstrap_stack_version_ssm_parameter: (experimental) Name of SSM parameter with bootstrap stack version. Default: - Discover SSM parameter by reading stack
        :param requires_bootstrap_stack_version: (experimental) Version of bootstrap stack required to use this role. Default: - No bootstrap stack required

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            bootstrap_role = cloud_assembly_schema.BootstrapRole(
                arn="arn",
            
                # the properties below are optional
                assume_role_external_id="assumeRoleExternalId",
                bootstrap_stack_version_ssm_parameter="bootstrapStackVersionSsmParameter",
                requires_bootstrap_stack_version=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67b6ad8cbe1a229a48cb983133ececa7df5bd0c26da1da0ba401feab61aefff3)
            check_type(argname="argument arn", value=arn, expected_type=type_hints["arn"])
            check_type(argname="argument assume_role_external_id", value=assume_role_external_id, expected_type=type_hints["assume_role_external_id"])
            check_type(argname="argument bootstrap_stack_version_ssm_parameter", value=bootstrap_stack_version_ssm_parameter, expected_type=type_hints["bootstrap_stack_version_ssm_parameter"])
            check_type(argname="argument requires_bootstrap_stack_version", value=requires_bootstrap_stack_version, expected_type=type_hints["requires_bootstrap_stack_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "arn": arn,
        }
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if bootstrap_stack_version_ssm_parameter is not None:
            self._values["bootstrap_stack_version_ssm_parameter"] = bootstrap_stack_version_ssm_parameter
        if requires_bootstrap_stack_version is not None:
            self._values["requires_bootstrap_stack_version"] = requires_bootstrap_stack_version

    @builtins.property
    def arn(self) -> builtins.str:
        '''(experimental) The ARN of the IAM role created as part of bootrapping e.g. lookupRoleArn.

        :stability: experimental
        '''
        result = self._values.get("arn")
        assert result is not None, "Required property 'arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) External ID to use when assuming the bootstrap role.

        :default: - No external ID

        :stability: experimental
        '''
        result = self._values.get("assume_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bootstrap_stack_version_ssm_parameter(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of SSM parameter with bootstrap stack version.

        :default: - Discover SSM parameter by reading stack

        :stability: experimental
        '''
        result = self._values.get("bootstrap_stack_version_ssm_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def requires_bootstrap_stack_version(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Version of bootstrap stack required to use this role.

        :default: - No bootstrap stack required

        :stability: experimental
        '''
        result = self._values.get("requires_bootstrap_stack_version")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BootstrapRole(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.CdkCommand",
    jsii_struct_bases=[],
    name_mapping={
        "enabled": "enabled",
        "expected_message": "expectedMessage",
        "expect_error": "expectError",
    },
)
class CdkCommand:
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        expected_message: typing.Optional[builtins.str] = None,
        expect_error: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Represents a cdk command i.e. ``synth``, ``deploy``, & ``destroy``.

        :param enabled: (experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis. Default: true
        :param expected_message: (experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned. Default: - do not validate message
        :param expect_error: (experimental) If the runner should expect this command to fail. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            cdk_command = cloud_assembly_schema.CdkCommand(
                enabled=False,
                expected_message="expectedMessage",
                expect_error=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a2e3b64d564e502f88cc9aeae0f8aa504a53c55905d2249939e5b71b4538e44)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expected_message", value=expected_message, expected_type=type_hints["expected_message"])
            check_type(argname="argument expect_error", value=expect_error, expected_type=type_hints["expect_error"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if expected_message is not None:
            self._values["expected_message"] = expected_message
        if expect_error is not None:
            self._values["expect_error"] = expect_error

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expected_message(self) -> typing.Optional[builtins.str]:
        '''(experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned.

        :default: - do not validate message

        :stability: experimental
        '''
        result = self._values.get("expected_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expect_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the runner should expect this command to fail.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("expect_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.CdkCommands",
    jsii_struct_bases=[],
    name_mapping={"deploy": "deploy", "destroy": "destroy"},
)
class CdkCommands:
    def __init__(
        self,
        *,
        deploy: typing.Optional[typing.Union["DeployCommand", typing.Dict[builtins.str, typing.Any]]] = None,
        destroy: typing.Optional[typing.Union["DestroyCommand", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Options for specific cdk commands that are run as part of the integration test workflow.

        :param deploy: (experimental) Options to for the cdk deploy command. Default: - default deploy options
        :param destroy: (experimental) Options to for the cdk destroy command. Default: - default destroy options

        :stability: experimental
        :exampleMetadata: infused

        Example::

            app = App()
            
            stack_under_test = Stack(app, "StackUnderTest")
            
            stack = Stack(app, "stack")
            
            test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
                test_cases=[stack_under_test],
                diff_assets=True,
                stack_update_workflow=True,
                cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                    deploy=lambda.cloud_assembly_schema.DeployCommand(
                        args=lambda.cloud_assembly_schema.DeployOptions(
                            require_approval=RequireApproval.NEVER,
                            json=True
                        )
                    ),
                    destroy=lambda.cloud_assembly_schema.DestroyCommand(
                        args=lambda.cloud_assembly_schema.DestroyOptions(
                            force=True
                        )
                    )
                )
            )
        '''
        if isinstance(deploy, dict):
            deploy = DeployCommand(**deploy)
        if isinstance(destroy, dict):
            destroy = DestroyCommand(**destroy)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94b6d49787ca8183c380bd904923fc40e21152903fd019f70a0447d691732e8e)
            check_type(argname="argument deploy", value=deploy, expected_type=type_hints["deploy"])
            check_type(argname="argument destroy", value=destroy, expected_type=type_hints["destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if deploy is not None:
            self._values["deploy"] = deploy
        if destroy is not None:
            self._values["destroy"] = destroy

    @builtins.property
    def deploy(self) -> typing.Optional["DeployCommand"]:
        '''(experimental) Options to for the cdk deploy command.

        :default: - default deploy options

        :stability: experimental
        '''
        result = self._values.get("deploy")
        return typing.cast(typing.Optional["DeployCommand"], result)

    @builtins.property
    def destroy(self) -> typing.Optional["DestroyCommand"]:
        '''(experimental) Options to for the cdk destroy command.

        :default: - default destroy options

        :stability: experimental
        '''
        result = self._values.get("destroy")
        return typing.cast(typing.Optional["DestroyCommand"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkCommands(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.ContainerImageAssetMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "id": "id",
        "packaging": "packaging",
        "path": "path",
        "source_hash": "sourceHash",
        "build_args": "buildArgs",
        "file": "file",
        "image_name_parameter": "imageNameParameter",
        "image_tag": "imageTag",
        "network_mode": "networkMode",
        "platform": "platform",
        "repository_name": "repositoryName",
        "target": "target",
    },
)
class ContainerImageAssetMetadataEntry:
    def __init__(
        self,
        *,
        id: builtins.str,
        packaging: builtins.str,
        path: builtins.str,
        source_hash: builtins.str,
        build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        file: typing.Optional[builtins.str] = None,
        image_name_parameter: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
        network_mode: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
        repository_name: typing.Optional[builtins.str] = None,
        target: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Metadata Entry spec for container images.

        :param id: (experimental) Logical identifier for the asset.
        :param packaging: (experimental) Type of asset.
        :param path: (experimental) Path on disk to the asset.
        :param source_hash: (experimental) The hash of the asset source.
        :param build_args: (experimental) Build args to pass to the ``docker build`` command. Default: no build args are passed
        :param file: (experimental) Path to the Dockerfile (relative to the directory). Default: - no file is passed
        :param image_name_parameter: (deprecated) ECR Repository name and repo digest (separated by "@sha256:") where this image is stored. Default: undefined If not specified, ``repositoryName`` and ``imageTag`` are required because otherwise how will the stack know where to find the asset, ha?
        :param image_tag: (experimental) The docker image tag to use for tagging pushed images. This field is required if ``imageParameterName`` is ommited (otherwise, the app won't be able to find the image). Default: - this parameter is REQUIRED after 1.21.0
        :param network_mode: (experimental) Networking mode for the RUN commands during build. Default: - no networking mode specified
        :param platform: (experimental) Platform to build for. *Requires Docker Buildx*. Default: - current machine platform
        :param repository_name: (experimental) ECR repository name, if omitted a default name based on the asset's ID is used instead. Specify this property if you need to statically address the image, e.g. from a Kubernetes Pod. Note, this is only the repository name, without the registry and the tag parts. Default: - this parameter is REQUIRED after 1.21.0
        :param target: (experimental) Docker target to build to. Default: no build target

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            container_image_asset_metadata_entry = cloud_assembly_schema.ContainerImageAssetMetadataEntry(
                id="id",
                packaging="packaging",
                path="path",
                source_hash="sourceHash",
            
                # the properties below are optional
                build_args={
                    "build_args_key": "buildArgs"
                },
                file="file",
                image_name_parameter="imageNameParameter",
                image_tag="imageTag",
                network_mode="networkMode",
                platform="platform",
                repository_name="repositoryName",
                target="target"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8bcae44b068f34e0af341c79563d929bc81c1dd1ca480d0eb4cb6b38e32380f6)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument source_hash", value=source_hash, expected_type=type_hints["source_hash"])
            check_type(argname="argument build_args", value=build_args, expected_type=type_hints["build_args"])
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
            check_type(argname="argument image_name_parameter", value=image_name_parameter, expected_type=type_hints["image_name_parameter"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "id": id,
            "packaging": packaging,
            "path": path,
            "source_hash": source_hash,
        }
        if build_args is not None:
            self._values["build_args"] = build_args
        if file is not None:
            self._values["file"] = file
        if image_name_parameter is not None:
            self._values["image_name_parameter"] = image_name_parameter
        if image_tag is not None:
            self._values["image_tag"] = image_tag
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform
        if repository_name is not None:
            self._values["repository_name"] = repository_name
        if target is not None:
            self._values["target"] = target

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) Logical identifier for the asset.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def packaging(self) -> builtins.str:
        '''(experimental) Type of asset.

        :stability: experimental
        '''
        result = self._values.get("packaging")
        assert result is not None, "Required property 'packaging' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path on disk to the asset.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_hash(self) -> builtins.str:
        '''(experimental) The hash of the asset source.

        :stability: experimental
        '''
        result = self._values.get("source_hash")
        assert result is not None, "Required property 'source_hash' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_args(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Build args to pass to the ``docker build`` command.

        :default: no build args are passed

        :stability: experimental
        '''
        result = self._values.get("build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to the Dockerfile (relative to the directory).

        :default: - no file is passed

        :stability: experimental
        '''
        result = self._values.get("file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_name_parameter(self) -> typing.Optional[builtins.str]:
        '''(deprecated) ECR Repository name and repo digest (separated by "@sha256:") where this image is stored.

        :default:

        undefined If not specified, ``repositoryName`` and ``imageTag`` are
        required because otherwise how will the stack know where to find the asset,
        ha?

        :deprecated:

        specify ``repositoryName`` and ``imageTag`` instead, and then you
        know where the image will go.

        :stability: deprecated
        '''
        result = self._values.get("image_name_parameter")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The docker image tag to use for tagging pushed images.

        This field is
        required if ``imageParameterName`` is ommited (otherwise, the app won't be
        able to find the image).

        :default: - this parameter is REQUIRED after 1.21.0

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''(experimental) Networking mode for the RUN commands during build.

        :default: - no networking mode specified

        :stability: experimental
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''(experimental) Platform to build for.

        *Requires Docker Buildx*.

        :default: - current machine platform

        :stability: experimental
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def repository_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) ECR repository name, if omitted a default name based on the asset's ID is used instead.

        Specify this property if you need to statically address the
        image, e.g. from a Kubernetes Pod. Note, this is only the repository name,
        without the registry and the tag parts.

        :default: - this parameter is REQUIRED after 1.21.0

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Docker target to build to.

        :default: no build target

        :stability: experimental
        '''
        result = self._values.get("target")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerImageAssetMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.ContextProvider")
class ContextProvider(enum.Enum):
    '''(experimental) Identifier for the context provider.

    :stability: experimental
    '''

    AMI_PROVIDER = "AMI_PROVIDER"
    '''(experimental) AMI provider.

    :stability: experimental
    '''
    AVAILABILITY_ZONE_PROVIDER = "AVAILABILITY_ZONE_PROVIDER"
    '''(experimental) AZ provider.

    :stability: experimental
    '''
    HOSTED_ZONE_PROVIDER = "HOSTED_ZONE_PROVIDER"
    '''(experimental) Route53 Hosted Zone provider.

    :stability: experimental
    '''
    SSM_PARAMETER_PROVIDER = "SSM_PARAMETER_PROVIDER"
    '''(experimental) SSM Parameter Provider.

    :stability: experimental
    '''
    VPC_PROVIDER = "VPC_PROVIDER"
    '''(experimental) VPC Provider.

    :stability: experimental
    '''
    ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER = "ENDPOINT_SERVICE_AVAILABILITY_ZONE_PROVIDER"
    '''(experimental) VPC Endpoint Service AZ Provider.

    :stability: experimental
    '''
    LOAD_BALANCER_PROVIDER = "LOAD_BALANCER_PROVIDER"
    '''(experimental) Load balancer provider.

    :stability: experimental
    '''
    LOAD_BALANCER_LISTENER_PROVIDER = "LOAD_BALANCER_LISTENER_PROVIDER"
    '''(experimental) Load balancer listener provider.

    :stability: experimental
    '''
    SECURITY_GROUP_PROVIDER = "SECURITY_GROUP_PROVIDER"
    '''(experimental) Security group provider.

    :stability: experimental
    '''
    KEY_PROVIDER = "KEY_PROVIDER"
    '''(experimental) KMS Key Provider.

    :stability: experimental
    '''
    PLUGIN = "PLUGIN"
    '''(experimental) A plugin provider (the actual plugin name will be in the properties).

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DefaultCdkOptions",
    jsii_struct_bases=[],
    name_mapping={
        "all": "all",
        "app": "app",
        "asset_metadata": "assetMetadata",
        "ca_bundle_path": "caBundlePath",
        "color": "color",
        "context": "context",
        "debug": "debug",
        "ec2_creds": "ec2Creds",
        "ignore_errors": "ignoreErrors",
        "json": "json",
        "lookups": "lookups",
        "notices": "notices",
        "output": "output",
        "path_metadata": "pathMetadata",
        "profile": "profile",
        "proxy": "proxy",
        "role_arn": "roleArn",
        "stacks": "stacks",
        "staging": "staging",
        "strict": "strict",
        "trace": "trace",
        "verbose": "verbose",
        "version_reporting": "versionReporting",
    },
)
class DefaultCdkOptions:
    def __init__(
        self,
        *,
        all: typing.Optional[builtins.bool] = None,
        app: typing.Optional[builtins.str] = None,
        asset_metadata: typing.Optional[builtins.bool] = None,
        ca_bundle_path: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        debug: typing.Optional[builtins.bool] = None,
        ec2_creds: typing.Optional[builtins.bool] = None,
        ignore_errors: typing.Optional[builtins.bool] = None,
        json: typing.Optional[builtins.bool] = None,
        lookups: typing.Optional[builtins.bool] = None,
        notices: typing.Optional[builtins.bool] = None,
        output: typing.Optional[builtins.str] = None,
        path_metadata: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
        staging: typing.Optional[builtins.bool] = None,
        strict: typing.Optional[builtins.bool] = None,
        trace: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
        version_reporting: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Default CDK CLI options that apply to all commands.

        :param all: (experimental) Deploy all stacks. Requried if ``stacks`` is not set Default: - false
        :param app: (experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out". Default: - read from cdk.json
        :param asset_metadata: (experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets. Default: true
        :param ca_bundle_path: (experimental) Path to CA certificate to use when validating HTTPS requests. Default: - read from AWS_CA_BUNDLE environment variable
        :param color: (experimental) Show colors and other style from console output. Default: true
        :param context: (experimental) Additional context. Default: - no additional context
        :param debug: (experimental) enable emission of additional debugging information, such as creation stack traces of tokens. Default: false
        :param ec2_creds: (experimental) Force trying to fetch EC2 instance credentials. Default: - guess EC2 instance status
        :param ignore_errors: (experimental) Ignores synthesis errors, which will likely produce an invalid output. Default: false
        :param json: (experimental) Use JSON output instead of YAML when templates are printed to STDOUT. Default: false
        :param lookups: (experimental) Perform context lookups. Synthesis fails if this is disabled and context lookups need to be performed Default: true
        :param notices: (experimental) Show relevant notices. Default: true
        :param output: (experimental) Emits the synthesized cloud assembly into a directory. Default: cdk.out
        :param path_metadata: (experimental) Include "aws:cdk:path" CloudFormation metadata for each resource. Default: true
        :param profile: (experimental) Use the indicated AWS profile as the default environment. Default: - no profile is used
        :param proxy: (experimental) Use the indicated proxy. Will read from HTTPS_PROXY environment if specified Default: - no proxy
        :param role_arn: (experimental) Role to pass to CloudFormation for deployment. Default: - use the bootstrap cfn-exec role
        :param stacks: (experimental) List of stacks to deploy. Requried if ``all`` is not set Default: - []
        :param staging: (experimental) Copy assets to the output directory. Needed for local debugging the source files with SAM CLI Default: false
        :param strict: (experimental) Do not construct stacks with warnings. Default: false
        :param trace: (experimental) Print trace for stack warnings. Default: false
        :param verbose: (experimental) show debug logs. Default: false
        :param version_reporting: (experimental) Include "AWS::CDK::Metadata" resource in synthesized templates. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            default_cdk_options = cloud_assembly_schema.DefaultCdkOptions(
                all=False,
                app="app",
                asset_metadata=False,
                ca_bundle_path="caBundlePath",
                color=False,
                context={
                    "context_key": "context"
                },
                debug=False,
                ec2_creds=False,
                ignore_errors=False,
                json=False,
                lookups=False,
                notices=False,
                output="output",
                path_metadata=False,
                profile="profile",
                proxy="proxy",
                role_arn="roleArn",
                stacks=["stacks"],
                staging=False,
                strict=False,
                trace=False,
                verbose=False,
                version_reporting=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a7ea7ec5f9890ce22bc988e235e5f8b8364322fe6ae34349030821e8f2e43810)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument asset_metadata", value=asset_metadata, expected_type=type_hints["asset_metadata"])
            check_type(argname="argument ca_bundle_path", value=ca_bundle_path, expected_type=type_hints["ca_bundle_path"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument ec2_creds", value=ec2_creds, expected_type=type_hints["ec2_creds"])
            check_type(argname="argument ignore_errors", value=ignore_errors, expected_type=type_hints["ignore_errors"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument lookups", value=lookups, expected_type=type_hints["lookups"])
            check_type(argname="argument notices", value=notices, expected_type=type_hints["notices"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument path_metadata", value=path_metadata, expected_type=type_hints["path_metadata"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument staging", value=staging, expected_type=type_hints["staging"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument version_reporting", value=version_reporting, expected_type=type_hints["version_reporting"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if app is not None:
            self._values["app"] = app
        if asset_metadata is not None:
            self._values["asset_metadata"] = asset_metadata
        if ca_bundle_path is not None:
            self._values["ca_bundle_path"] = ca_bundle_path
        if color is not None:
            self._values["color"] = color
        if context is not None:
            self._values["context"] = context
        if debug is not None:
            self._values["debug"] = debug
        if ec2_creds is not None:
            self._values["ec2_creds"] = ec2_creds
        if ignore_errors is not None:
            self._values["ignore_errors"] = ignore_errors
        if json is not None:
            self._values["json"] = json
        if lookups is not None:
            self._values["lookups"] = lookups
        if notices is not None:
            self._values["notices"] = notices
        if output is not None:
            self._values["output"] = output
        if path_metadata is not None:
            self._values["path_metadata"] = path_metadata
        if profile is not None:
            self._values["profile"] = profile
        if proxy is not None:
            self._values["proxy"] = proxy
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stacks is not None:
            self._values["stacks"] = stacks
        if staging is not None:
            self._values["staging"] = staging
        if strict is not None:
            self._values["strict"] = strict
        if trace is not None:
            self._values["trace"] = trace
        if verbose is not None:
            self._values["verbose"] = verbose
        if version_reporting is not None:
            self._values["version_reporting"] = version_reporting

    @builtins.property
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Deploy all stacks.

        Requried if ``stacks`` is not set

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app(self) -> typing.Optional[builtins.str]:
        '''(experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out".

        :default: - read from cdk.json

        :stability: experimental
        '''
        result = self._values.get("app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("asset_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ca_bundle_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to CA certificate to use when validating HTTPS requests.

        :default: - read from AWS_CA_BUNDLE environment variable

        :stability: experimental
        '''
        result = self._values.get("ca_bundle_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show colors and other style from console output.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional context.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        '''(experimental) enable emission of additional debugging information, such as creation stack traces of tokens.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ec2_creds(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force trying to fetch EC2 instance credentials.

        :default: - guess EC2 instance status

        :stability: experimental
        '''
        result = self._values.get("ec2_creds")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignores synthesis errors, which will likely produce an invalid output.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use JSON output instead of YAML when templates are printed to STDOUT.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lookups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Perform context lookups.

        Synthesis fails if this is disabled and context lookups need
        to be performed

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lookups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notices(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show relevant notices.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("notices")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output(self) -> typing.Optional[builtins.str]:
        '''(experimental) Emits the synthesized cloud assembly into a directory.

        :default: cdk.out

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:cdk:path" CloudFormation metadata for each resource.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("path_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated AWS profile as the default environment.

        :default: - no profile is used

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated proxy.

        Will read from
        HTTPS_PROXY environment if specified

        :default: - no proxy

        :stability: experimental
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role to pass to CloudFormation for deployment.

        :default: - use the bootstrap cfn-exec role

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stacks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of stacks to deploy.

        Requried if ``all`` is not set

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("stacks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def staging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Copy assets to the output directory.

        Needed for local debugging the source files with SAM CLI

        :default: false

        :stability: experimental
        '''
        result = self._values.get("staging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not construct stacks with warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Print trace for stack warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''(experimental) show debug logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_reporting(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "AWS::CDK::Metadata" resource in synthesized templates.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("version_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DefaultCdkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DeployCommand",
    jsii_struct_bases=[CdkCommand],
    name_mapping={
        "enabled": "enabled",
        "expected_message": "expectedMessage",
        "expect_error": "expectError",
        "args": "args",
    },
)
class DeployCommand(CdkCommand):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        expected_message: typing.Optional[builtins.str] = None,
        expect_error: typing.Optional[builtins.bool] = None,
        args: typing.Optional[typing.Union["DeployOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Represents a cdk deploy command.

        :param enabled: (experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis. Default: true
        :param expected_message: (experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned. Default: - do not validate message
        :param expect_error: (experimental) If the runner should expect this command to fail. Default: false
        :param args: (experimental) Additional arguments to pass to the command This can be used to test specific CLI functionality. Default: - only default args are used

        :stability: experimental
        :exampleMetadata: infused

        Example::

            app = App()
            
            stack_under_test = Stack(app, "StackUnderTest")
            
            stack = Stack(app, "stack")
            
            test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
                test_cases=[stack_under_test],
                diff_assets=True,
                stack_update_workflow=True,
                cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                    deploy=lambda.cloud_assembly_schema.DeployCommand(
                        args=lambda.cloud_assembly_schema.DeployOptions(
                            require_approval=RequireApproval.NEVER,
                            json=True
                        )
                    ),
                    destroy=lambda.cloud_assembly_schema.DestroyCommand(
                        args=lambda.cloud_assembly_schema.DestroyOptions(
                            force=True
                        )
                    )
                )
            )
        '''
        if isinstance(args, dict):
            args = DeployOptions(**args)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__aa9e8152bcee65bbee0162599ae487529471054cee5218ed4ebfc52da00dc6ac)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expected_message", value=expected_message, expected_type=type_hints["expected_message"])
            check_type(argname="argument expect_error", value=expect_error, expected_type=type_hints["expect_error"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if expected_message is not None:
            self._values["expected_message"] = expected_message
        if expect_error is not None:
            self._values["expect_error"] = expect_error
        if args is not None:
            self._values["args"] = args

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expected_message(self) -> typing.Optional[builtins.str]:
        '''(experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned.

        :default: - do not validate message

        :stability: experimental
        '''
        result = self._values.get("expected_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expect_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the runner should expect this command to fail.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("expect_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def args(self) -> typing.Optional["DeployOptions"]:
        '''(experimental) Additional arguments to pass to the command This can be used to test specific CLI functionality.

        :default: - only default args are used

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional["DeployOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DeployOptions",
    jsii_struct_bases=[DefaultCdkOptions],
    name_mapping={
        "all": "all",
        "app": "app",
        "asset_metadata": "assetMetadata",
        "ca_bundle_path": "caBundlePath",
        "color": "color",
        "context": "context",
        "debug": "debug",
        "ec2_creds": "ec2Creds",
        "ignore_errors": "ignoreErrors",
        "json": "json",
        "lookups": "lookups",
        "notices": "notices",
        "output": "output",
        "path_metadata": "pathMetadata",
        "profile": "profile",
        "proxy": "proxy",
        "role_arn": "roleArn",
        "stacks": "stacks",
        "staging": "staging",
        "strict": "strict",
        "trace": "trace",
        "verbose": "verbose",
        "version_reporting": "versionReporting",
        "change_set_name": "changeSetName",
        "ci": "ci",
        "exclusively": "exclusively",
        "execute": "execute",
        "force": "force",
        "notification_arns": "notificationArns",
        "outputs_file": "outputsFile",
        "parameters": "parameters",
        "require_approval": "requireApproval",
        "reuse_assets": "reuseAssets",
        "rollback": "rollback",
        "toolkit_stack_name": "toolkitStackName",
        "use_previous_parameters": "usePreviousParameters",
    },
)
class DeployOptions(DefaultCdkOptions):
    def __init__(
        self,
        *,
        all: typing.Optional[builtins.bool] = None,
        app: typing.Optional[builtins.str] = None,
        asset_metadata: typing.Optional[builtins.bool] = None,
        ca_bundle_path: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        debug: typing.Optional[builtins.bool] = None,
        ec2_creds: typing.Optional[builtins.bool] = None,
        ignore_errors: typing.Optional[builtins.bool] = None,
        json: typing.Optional[builtins.bool] = None,
        lookups: typing.Optional[builtins.bool] = None,
        notices: typing.Optional[builtins.bool] = None,
        output: typing.Optional[builtins.str] = None,
        path_metadata: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
        staging: typing.Optional[builtins.bool] = None,
        strict: typing.Optional[builtins.bool] = None,
        trace: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
        version_reporting: typing.Optional[builtins.bool] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        ci: typing.Optional[builtins.bool] = None,
        exclusively: typing.Optional[builtins.bool] = None,
        execute: typing.Optional[builtins.bool] = None,
        force: typing.Optional[builtins.bool] = None,
        notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs_file: typing.Optional[builtins.str] = None,
        parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        require_approval: typing.Optional["RequireApproval"] = None,
        reuse_assets: typing.Optional[typing.Sequence[builtins.str]] = None,
        rollback: typing.Optional[builtins.bool] = None,
        toolkit_stack_name: typing.Optional[builtins.str] = None,
        use_previous_parameters: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to use with cdk deploy.

        :param all: (experimental) Deploy all stacks. Requried if ``stacks`` is not set Default: - false
        :param app: (experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out". Default: - read from cdk.json
        :param asset_metadata: (experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets. Default: true
        :param ca_bundle_path: (experimental) Path to CA certificate to use when validating HTTPS requests. Default: - read from AWS_CA_BUNDLE environment variable
        :param color: (experimental) Show colors and other style from console output. Default: true
        :param context: (experimental) Additional context. Default: - no additional context
        :param debug: (experimental) enable emission of additional debugging information, such as creation stack traces of tokens. Default: false
        :param ec2_creds: (experimental) Force trying to fetch EC2 instance credentials. Default: - guess EC2 instance status
        :param ignore_errors: (experimental) Ignores synthesis errors, which will likely produce an invalid output. Default: false
        :param json: (experimental) Use JSON output instead of YAML when templates are printed to STDOUT. Default: false
        :param lookups: (experimental) Perform context lookups. Synthesis fails if this is disabled and context lookups need to be performed Default: true
        :param notices: (experimental) Show relevant notices. Default: true
        :param output: (experimental) Emits the synthesized cloud assembly into a directory. Default: cdk.out
        :param path_metadata: (experimental) Include "aws:cdk:path" CloudFormation metadata for each resource. Default: true
        :param profile: (experimental) Use the indicated AWS profile as the default environment. Default: - no profile is used
        :param proxy: (experimental) Use the indicated proxy. Will read from HTTPS_PROXY environment if specified Default: - no proxy
        :param role_arn: (experimental) Role to pass to CloudFormation for deployment. Default: - use the bootstrap cfn-exec role
        :param stacks: (experimental) List of stacks to deploy. Requried if ``all`` is not set Default: - []
        :param staging: (experimental) Copy assets to the output directory. Needed for local debugging the source files with SAM CLI Default: false
        :param strict: (experimental) Do not construct stacks with warnings. Default: false
        :param trace: (experimental) Print trace for stack warnings. Default: false
        :param verbose: (experimental) show debug logs. Default: false
        :param version_reporting: (experimental) Include "AWS::CDK::Metadata" resource in synthesized templates. Default: true
        :param change_set_name: (experimental) Optional name to use for the CloudFormation change set. If not provided, a name will be generated automatically. Default: - auto generate a name
        :param ci: (experimental) Whether we are on a CI system. Default: false
        :param exclusively: (experimental) Only perform action on the given stack. Default: false
        :param execute: (experimental) Whether to execute the ChangeSet Not providing ``execute`` parameter will result in execution of ChangeSet. Default: true
        :param force: (experimental) Always deploy, even if templates are identical. Default: false
        :param notification_arns: (experimental) ARNs of SNS topics that CloudFormation will notify with stack related events. Default: - no notifications
        :param outputs_file: (experimental) Path to file where stack outputs will be written after a successful deploy as JSON. Default: - Outputs are not written to any file
        :param parameters: (experimental) Additional parameters for CloudFormation at deploy time. Default: {}
        :param require_approval: (experimental) What kind of security changes require approval. Default: RequireApproval.Never
        :param reuse_assets: (experimental) Reuse the assets with the given asset IDs. Default: - do not reuse assets
        :param rollback: (experimental) Rollback failed deployments. Default: true
        :param toolkit_stack_name: (experimental) Name of the toolkit stack to use/deploy. Default: CDKToolkit
        :param use_previous_parameters: (experimental) Use previous values for unspecified parameters. If not set, all parameters must be specified for every deployment. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            app = App()
            
            stack_under_test = Stack(app, "StackUnderTest")
            
            stack = Stack(app, "stack")
            
            test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
                test_cases=[stack_under_test],
                diff_assets=True,
                stack_update_workflow=True,
                cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                    deploy=lambda.cloud_assembly_schema.DeployCommand(
                        args=lambda.cloud_assembly_schema.DeployOptions(
                            require_approval=RequireApproval.NEVER,
                            json=True
                        )
                    ),
                    destroy=lambda.cloud_assembly_schema.DestroyCommand(
                        args=lambda.cloud_assembly_schema.DestroyOptions(
                            force=True
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__218d47322e5c35ac480e1d317ee9da5f5250ad3b7905cbea9c6fdbc588d73fa7)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument asset_metadata", value=asset_metadata, expected_type=type_hints["asset_metadata"])
            check_type(argname="argument ca_bundle_path", value=ca_bundle_path, expected_type=type_hints["ca_bundle_path"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument ec2_creds", value=ec2_creds, expected_type=type_hints["ec2_creds"])
            check_type(argname="argument ignore_errors", value=ignore_errors, expected_type=type_hints["ignore_errors"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument lookups", value=lookups, expected_type=type_hints["lookups"])
            check_type(argname="argument notices", value=notices, expected_type=type_hints["notices"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument path_metadata", value=path_metadata, expected_type=type_hints["path_metadata"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument staging", value=staging, expected_type=type_hints["staging"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument version_reporting", value=version_reporting, expected_type=type_hints["version_reporting"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument ci", value=ci, expected_type=type_hints["ci"])
            check_type(argname="argument exclusively", value=exclusively, expected_type=type_hints["exclusively"])
            check_type(argname="argument execute", value=execute, expected_type=type_hints["execute"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
            check_type(argname="argument notification_arns", value=notification_arns, expected_type=type_hints["notification_arns"])
            check_type(argname="argument outputs_file", value=outputs_file, expected_type=type_hints["outputs_file"])
            check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
            check_type(argname="argument require_approval", value=require_approval, expected_type=type_hints["require_approval"])
            check_type(argname="argument reuse_assets", value=reuse_assets, expected_type=type_hints["reuse_assets"])
            check_type(argname="argument rollback", value=rollback, expected_type=type_hints["rollback"])
            check_type(argname="argument toolkit_stack_name", value=toolkit_stack_name, expected_type=type_hints["toolkit_stack_name"])
            check_type(argname="argument use_previous_parameters", value=use_previous_parameters, expected_type=type_hints["use_previous_parameters"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if app is not None:
            self._values["app"] = app
        if asset_metadata is not None:
            self._values["asset_metadata"] = asset_metadata
        if ca_bundle_path is not None:
            self._values["ca_bundle_path"] = ca_bundle_path
        if color is not None:
            self._values["color"] = color
        if context is not None:
            self._values["context"] = context
        if debug is not None:
            self._values["debug"] = debug
        if ec2_creds is not None:
            self._values["ec2_creds"] = ec2_creds
        if ignore_errors is not None:
            self._values["ignore_errors"] = ignore_errors
        if json is not None:
            self._values["json"] = json
        if lookups is not None:
            self._values["lookups"] = lookups
        if notices is not None:
            self._values["notices"] = notices
        if output is not None:
            self._values["output"] = output
        if path_metadata is not None:
            self._values["path_metadata"] = path_metadata
        if profile is not None:
            self._values["profile"] = profile
        if proxy is not None:
            self._values["proxy"] = proxy
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stacks is not None:
            self._values["stacks"] = stacks
        if staging is not None:
            self._values["staging"] = staging
        if strict is not None:
            self._values["strict"] = strict
        if trace is not None:
            self._values["trace"] = trace
        if verbose is not None:
            self._values["verbose"] = verbose
        if version_reporting is not None:
            self._values["version_reporting"] = version_reporting
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if ci is not None:
            self._values["ci"] = ci
        if exclusively is not None:
            self._values["exclusively"] = exclusively
        if execute is not None:
            self._values["execute"] = execute
        if force is not None:
            self._values["force"] = force
        if notification_arns is not None:
            self._values["notification_arns"] = notification_arns
        if outputs_file is not None:
            self._values["outputs_file"] = outputs_file
        if parameters is not None:
            self._values["parameters"] = parameters
        if require_approval is not None:
            self._values["require_approval"] = require_approval
        if reuse_assets is not None:
            self._values["reuse_assets"] = reuse_assets
        if rollback is not None:
            self._values["rollback"] = rollback
        if toolkit_stack_name is not None:
            self._values["toolkit_stack_name"] = toolkit_stack_name
        if use_previous_parameters is not None:
            self._values["use_previous_parameters"] = use_previous_parameters

    @builtins.property
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Deploy all stacks.

        Requried if ``stacks`` is not set

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app(self) -> typing.Optional[builtins.str]:
        '''(experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out".

        :default: - read from cdk.json

        :stability: experimental
        '''
        result = self._values.get("app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("asset_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ca_bundle_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to CA certificate to use when validating HTTPS requests.

        :default: - read from AWS_CA_BUNDLE environment variable

        :stability: experimental
        '''
        result = self._values.get("ca_bundle_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show colors and other style from console output.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional context.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        '''(experimental) enable emission of additional debugging information, such as creation stack traces of tokens.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ec2_creds(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force trying to fetch EC2 instance credentials.

        :default: - guess EC2 instance status

        :stability: experimental
        '''
        result = self._values.get("ec2_creds")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignores synthesis errors, which will likely produce an invalid output.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use JSON output instead of YAML when templates are printed to STDOUT.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lookups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Perform context lookups.

        Synthesis fails if this is disabled and context lookups need
        to be performed

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lookups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notices(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show relevant notices.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("notices")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output(self) -> typing.Optional[builtins.str]:
        '''(experimental) Emits the synthesized cloud assembly into a directory.

        :default: cdk.out

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:cdk:path" CloudFormation metadata for each resource.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("path_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated AWS profile as the default environment.

        :default: - no profile is used

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated proxy.

        Will read from
        HTTPS_PROXY environment if specified

        :default: - no proxy

        :stability: experimental
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role to pass to CloudFormation for deployment.

        :default: - use the bootstrap cfn-exec role

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stacks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of stacks to deploy.

        Requried if ``all`` is not set

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("stacks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def staging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Copy assets to the output directory.

        Needed for local debugging the source files with SAM CLI

        :default: false

        :stability: experimental
        '''
        result = self._values.get("staging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not construct stacks with warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Print trace for stack warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''(experimental) show debug logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_reporting(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "AWS::CDK::Metadata" resource in synthesized templates.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("version_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional name to use for the CloudFormation change set.

        If not provided, a name will be generated automatically.

        :default: - auto generate a name

        :stability: experimental
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def ci(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether we are on a CI system.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ci")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclusively(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Only perform action on the given stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclusively")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def execute(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to execute the ChangeSet Not providing ``execute`` parameter will result in execution of ChangeSet.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("execute")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Always deploy, even if templates are identical.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notification_arns(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) ARNs of SNS topics that CloudFormation will notify with stack related events.

        :default: - no notifications

        :stability: experimental
        '''
        result = self._values.get("notification_arns")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to file where stack outputs will be written after a successful deploy as JSON.

        :default: - Outputs are not written to any file

        :stability: experimental
        '''
        result = self._values.get("outputs_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def parameters(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional parameters for CloudFormation at deploy time.

        :default: {}

        :stability: experimental
        '''
        result = self._values.get("parameters")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def require_approval(self) -> typing.Optional["RequireApproval"]:
        '''(experimental) What kind of security changes require approval.

        :default: RequireApproval.Never

        :stability: experimental
        '''
        result = self._values.get("require_approval")
        return typing.cast(typing.Optional["RequireApproval"], result)

    @builtins.property
    def reuse_assets(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Reuse the assets with the given asset IDs.

        :default: - do not reuse assets

        :stability: experimental
        '''
        result = self._values.get("reuse_assets")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def rollback(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Rollback failed deployments.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("rollback")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def toolkit_stack_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name of the toolkit stack to use/deploy.

        :default: CDKToolkit

        :stability: experimental
        '''
        result = self._values.get("toolkit_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def use_previous_parameters(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use previous values for unspecified parameters.

        If not set, all parameters must be specified for every deployment.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("use_previous_parameters")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DestroyCommand",
    jsii_struct_bases=[CdkCommand],
    name_mapping={
        "enabled": "enabled",
        "expected_message": "expectedMessage",
        "expect_error": "expectError",
        "args": "args",
    },
)
class DestroyCommand(CdkCommand):
    def __init__(
        self,
        *,
        enabled: typing.Optional[builtins.bool] = None,
        expected_message: typing.Optional[builtins.str] = None,
        expect_error: typing.Optional[builtins.bool] = None,
        args: typing.Optional[typing.Union["DestroyOptions", typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Represents a cdk destroy command.

        :param enabled: (experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis. Default: true
        :param expected_message: (experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned. Default: - do not validate message
        :param expect_error: (experimental) If the runner should expect this command to fail. Default: false
        :param args: (experimental) Additional arguments to pass to the command This can be used to test specific CLI functionality. Default: - only default args are used

        :stability: experimental
        :exampleMetadata: infused

        Example::

            app = App()
            
            stack_under_test = Stack(app, "StackUnderTest")
            
            stack = Stack(app, "stack")
            
            test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
                test_cases=[stack_under_test],
                diff_assets=True,
                stack_update_workflow=True,
                cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                    deploy=lambda.cloud_assembly_schema.DeployCommand(
                        args=lambda.cloud_assembly_schema.DeployOptions(
                            require_approval=RequireApproval.NEVER,
                            json=True
                        )
                    ),
                    destroy=lambda.cloud_assembly_schema.DestroyCommand(
                        args=lambda.cloud_assembly_schema.DestroyOptions(
                            force=True
                        )
                    )
                )
            )
        '''
        if isinstance(args, dict):
            args = DestroyOptions(**args)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f703a7f4a1ad8887fb5a7e86baa2e101dcdb823fc437ba4d0d28adbe8134b7d4)
            check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
            check_type(argname="argument expected_message", value=expected_message, expected_type=type_hints["expected_message"])
            check_type(argname="argument expect_error", value=expect_error, expected_type=type_hints["expect_error"])
            check_type(argname="argument args", value=args, expected_type=type_hints["args"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if enabled is not None:
            self._values["enabled"] = enabled
        if expected_message is not None:
            self._values["expected_message"] = expected_message
        if expect_error is not None:
            self._values["expect_error"] = expect_error
        if args is not None:
            self._values["args"] = args

    @builtins.property
    def enabled(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to run this command as part of the workflow This can be used if you only want to test some of the workflow for example enable ``synth`` and disable ``deploy`` & ``destroy`` in order to limit the test to synthesis.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("enabled")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def expected_message(self) -> typing.Optional[builtins.str]:
        '''(experimental) This can be used in combination with ``expectedError`` to validate that a specific message is returned.

        :default: - do not validate message

        :stability: experimental
        '''
        result = self._values.get("expected_message")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def expect_error(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If the runner should expect this command to fail.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("expect_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def args(self) -> typing.Optional["DestroyOptions"]:
        '''(experimental) Additional arguments to pass to the command This can be used to test specific CLI functionality.

        :default: - only default args are used

        :stability: experimental
        '''
        result = self._values.get("args")
        return typing.cast(typing.Optional["DestroyOptions"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestroyCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DestroyOptions",
    jsii_struct_bases=[DefaultCdkOptions],
    name_mapping={
        "all": "all",
        "app": "app",
        "asset_metadata": "assetMetadata",
        "ca_bundle_path": "caBundlePath",
        "color": "color",
        "context": "context",
        "debug": "debug",
        "ec2_creds": "ec2Creds",
        "ignore_errors": "ignoreErrors",
        "json": "json",
        "lookups": "lookups",
        "notices": "notices",
        "output": "output",
        "path_metadata": "pathMetadata",
        "profile": "profile",
        "proxy": "proxy",
        "role_arn": "roleArn",
        "stacks": "stacks",
        "staging": "staging",
        "strict": "strict",
        "trace": "trace",
        "verbose": "verbose",
        "version_reporting": "versionReporting",
        "exclusively": "exclusively",
        "force": "force",
    },
)
class DestroyOptions(DefaultCdkOptions):
    def __init__(
        self,
        *,
        all: typing.Optional[builtins.bool] = None,
        app: typing.Optional[builtins.str] = None,
        asset_metadata: typing.Optional[builtins.bool] = None,
        ca_bundle_path: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.bool] = None,
        context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        debug: typing.Optional[builtins.bool] = None,
        ec2_creds: typing.Optional[builtins.bool] = None,
        ignore_errors: typing.Optional[builtins.bool] = None,
        json: typing.Optional[builtins.bool] = None,
        lookups: typing.Optional[builtins.bool] = None,
        notices: typing.Optional[builtins.bool] = None,
        output: typing.Optional[builtins.str] = None,
        path_metadata: typing.Optional[builtins.bool] = None,
        profile: typing.Optional[builtins.str] = None,
        proxy: typing.Optional[builtins.str] = None,
        role_arn: typing.Optional[builtins.str] = None,
        stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
        staging: typing.Optional[builtins.bool] = None,
        strict: typing.Optional[builtins.bool] = None,
        trace: typing.Optional[builtins.bool] = None,
        verbose: typing.Optional[builtins.bool] = None,
        version_reporting: typing.Optional[builtins.bool] = None,
        exclusively: typing.Optional[builtins.bool] = None,
        force: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options to use with cdk destroy.

        :param all: (experimental) Deploy all stacks. Requried if ``stacks`` is not set Default: - false
        :param app: (experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out". Default: - read from cdk.json
        :param asset_metadata: (experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets. Default: true
        :param ca_bundle_path: (experimental) Path to CA certificate to use when validating HTTPS requests. Default: - read from AWS_CA_BUNDLE environment variable
        :param color: (experimental) Show colors and other style from console output. Default: true
        :param context: (experimental) Additional context. Default: - no additional context
        :param debug: (experimental) enable emission of additional debugging information, such as creation stack traces of tokens. Default: false
        :param ec2_creds: (experimental) Force trying to fetch EC2 instance credentials. Default: - guess EC2 instance status
        :param ignore_errors: (experimental) Ignores synthesis errors, which will likely produce an invalid output. Default: false
        :param json: (experimental) Use JSON output instead of YAML when templates are printed to STDOUT. Default: false
        :param lookups: (experimental) Perform context lookups. Synthesis fails if this is disabled and context lookups need to be performed Default: true
        :param notices: (experimental) Show relevant notices. Default: true
        :param output: (experimental) Emits the synthesized cloud assembly into a directory. Default: cdk.out
        :param path_metadata: (experimental) Include "aws:cdk:path" CloudFormation metadata for each resource. Default: true
        :param profile: (experimental) Use the indicated AWS profile as the default environment. Default: - no profile is used
        :param proxy: (experimental) Use the indicated proxy. Will read from HTTPS_PROXY environment if specified Default: - no proxy
        :param role_arn: (experimental) Role to pass to CloudFormation for deployment. Default: - use the bootstrap cfn-exec role
        :param stacks: (experimental) List of stacks to deploy. Requried if ``all`` is not set Default: - []
        :param staging: (experimental) Copy assets to the output directory. Needed for local debugging the source files with SAM CLI Default: false
        :param strict: (experimental) Do not construct stacks with warnings. Default: false
        :param trace: (experimental) Print trace for stack warnings. Default: false
        :param verbose: (experimental) show debug logs. Default: false
        :param version_reporting: (experimental) Include "AWS::CDK::Metadata" resource in synthesized templates. Default: true
        :param exclusively: (experimental) Only destroy the given stack. Default: false
        :param force: (experimental) Do not ask for permission before destroying stacks. Default: false

        :stability: experimental
        :exampleMetadata: infused

        Example::

            app = App()
            
            stack_under_test = Stack(app, "StackUnderTest")
            
            stack = Stack(app, "stack")
            
            test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
                test_cases=[stack_under_test],
                diff_assets=True,
                stack_update_workflow=True,
                cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                    deploy=lambda.cloud_assembly_schema.DeployCommand(
                        args=lambda.cloud_assembly_schema.DeployOptions(
                            require_approval=RequireApproval.NEVER,
                            json=True
                        )
                    ),
                    destroy=lambda.cloud_assembly_schema.DestroyCommand(
                        args=lambda.cloud_assembly_schema.DestroyOptions(
                            force=True
                        )
                    )
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fe413e27463eb24cbad97073db059059c3dd4e70317ceaa323e9b7e3718c10c)
            check_type(argname="argument all", value=all, expected_type=type_hints["all"])
            check_type(argname="argument app", value=app, expected_type=type_hints["app"])
            check_type(argname="argument asset_metadata", value=asset_metadata, expected_type=type_hints["asset_metadata"])
            check_type(argname="argument ca_bundle_path", value=ca_bundle_path, expected_type=type_hints["ca_bundle_path"])
            check_type(argname="argument color", value=color, expected_type=type_hints["color"])
            check_type(argname="argument context", value=context, expected_type=type_hints["context"])
            check_type(argname="argument debug", value=debug, expected_type=type_hints["debug"])
            check_type(argname="argument ec2_creds", value=ec2_creds, expected_type=type_hints["ec2_creds"])
            check_type(argname="argument ignore_errors", value=ignore_errors, expected_type=type_hints["ignore_errors"])
            check_type(argname="argument json", value=json, expected_type=type_hints["json"])
            check_type(argname="argument lookups", value=lookups, expected_type=type_hints["lookups"])
            check_type(argname="argument notices", value=notices, expected_type=type_hints["notices"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument path_metadata", value=path_metadata, expected_type=type_hints["path_metadata"])
            check_type(argname="argument profile", value=profile, expected_type=type_hints["profile"])
            check_type(argname="argument proxy", value=proxy, expected_type=type_hints["proxy"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument staging", value=staging, expected_type=type_hints["staging"])
            check_type(argname="argument strict", value=strict, expected_type=type_hints["strict"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
            check_type(argname="argument verbose", value=verbose, expected_type=type_hints["verbose"])
            check_type(argname="argument version_reporting", value=version_reporting, expected_type=type_hints["version_reporting"])
            check_type(argname="argument exclusively", value=exclusively, expected_type=type_hints["exclusively"])
            check_type(argname="argument force", value=force, expected_type=type_hints["force"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if all is not None:
            self._values["all"] = all
        if app is not None:
            self._values["app"] = app
        if asset_metadata is not None:
            self._values["asset_metadata"] = asset_metadata
        if ca_bundle_path is not None:
            self._values["ca_bundle_path"] = ca_bundle_path
        if color is not None:
            self._values["color"] = color
        if context is not None:
            self._values["context"] = context
        if debug is not None:
            self._values["debug"] = debug
        if ec2_creds is not None:
            self._values["ec2_creds"] = ec2_creds
        if ignore_errors is not None:
            self._values["ignore_errors"] = ignore_errors
        if json is not None:
            self._values["json"] = json
        if lookups is not None:
            self._values["lookups"] = lookups
        if notices is not None:
            self._values["notices"] = notices
        if output is not None:
            self._values["output"] = output
        if path_metadata is not None:
            self._values["path_metadata"] = path_metadata
        if profile is not None:
            self._values["profile"] = profile
        if proxy is not None:
            self._values["proxy"] = proxy
        if role_arn is not None:
            self._values["role_arn"] = role_arn
        if stacks is not None:
            self._values["stacks"] = stacks
        if staging is not None:
            self._values["staging"] = staging
        if strict is not None:
            self._values["strict"] = strict
        if trace is not None:
            self._values["trace"] = trace
        if verbose is not None:
            self._values["verbose"] = verbose
        if version_reporting is not None:
            self._values["version_reporting"] = version_reporting
        if exclusively is not None:
            self._values["exclusively"] = exclusively
        if force is not None:
            self._values["force"] = force

    @builtins.property
    def all(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Deploy all stacks.

        Requried if ``stacks`` is not set

        :default: - false

        :stability: experimental
        '''
        result = self._values.get("all")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def app(self) -> typing.Optional[builtins.str]:
        '''(experimental) command-line for executing your app or a cloud assembly directory e.g. "node bin/my-app.js" or "cdk.out".

        :default: - read from cdk.json

        :stability: experimental
        '''
        result = self._values.get("app")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def asset_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:asset:*" CloudFormation metadata for resources that use assets.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("asset_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ca_bundle_path(self) -> typing.Optional[builtins.str]:
        '''(experimental) Path to CA certificate to use when validating HTTPS requests.

        :default: - read from AWS_CA_BUNDLE environment variable

        :stability: experimental
        '''
        result = self._values.get("ca_bundle_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def color(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show colors and other style from console output.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("color")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def context(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional context.

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def debug(self) -> typing.Optional[builtins.bool]:
        '''(experimental) enable emission of additional debugging information, such as creation stack traces of tokens.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("debug")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ec2_creds(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Force trying to fetch EC2 instance credentials.

        :default: - guess EC2 instance status

        :stability: experimental
        '''
        result = self._values.get("ec2_creds")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def ignore_errors(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Ignores synthesis errors, which will likely produce an invalid output.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("ignore_errors")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def json(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Use JSON output instead of YAML when templates are printed to STDOUT.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("json")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def lookups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Perform context lookups.

        Synthesis fails if this is disabled and context lookups need
        to be performed

        :default: true

        :stability: experimental
        '''
        result = self._values.get("lookups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def notices(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Show relevant notices.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("notices")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def output(self) -> typing.Optional[builtins.str]:
        '''(experimental) Emits the synthesized cloud assembly into a directory.

        :default: cdk.out

        :stability: experimental
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def path_metadata(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "aws:cdk:path" CloudFormation metadata for each resource.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("path_metadata")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def profile(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated AWS profile as the default environment.

        :default: - no profile is used

        :stability: experimental
        '''
        result = self._values.get("profile")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def proxy(self) -> typing.Optional[builtins.str]:
        '''(experimental) Use the indicated proxy.

        Will read from
        HTTPS_PROXY environment if specified

        :default: - no proxy

        :stability: experimental
        '''
        result = self._values.get("proxy")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role to pass to CloudFormation for deployment.

        :default: - use the bootstrap cfn-exec role

        :stability: experimental
        '''
        result = self._values.get("role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stacks(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of stacks to deploy.

        Requried if ``all`` is not set

        :default: - []

        :stability: experimental
        '''
        result = self._values.get("stacks")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def staging(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Copy assets to the output directory.

        Needed for local debugging the source files with SAM CLI

        :default: false

        :stability: experimental
        '''
        result = self._values.get("staging")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def strict(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not construct stacks with warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("strict")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trace(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Print trace for stack warnings.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def verbose(self) -> typing.Optional[builtins.bool]:
        '''(experimental) show debug logs.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("verbose")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def version_reporting(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Include "AWS::CDK::Metadata" resource in synthesized templates.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("version_reporting")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def exclusively(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Only destroy the given stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("exclusively")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def force(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Do not ask for permission before destroying stacks.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("force")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DestroyOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DockerImageAsset",
    jsii_struct_bases=[],
    name_mapping={"destinations": "destinations", "source": "source"},
)
class DockerImageAsset:
    def __init__(
        self,
        *,
        destinations: typing.Mapping[builtins.str, typing.Union["DockerImageDestination", typing.Dict[builtins.str, typing.Any]]],
        source: typing.Union["DockerImageSource", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) A file asset.

        :param destinations: (experimental) Destinations for this file asset.
        :param source: (experimental) Source description for file assets.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            docker_image_asset = cloud_assembly_schema.DockerImageAsset(
                destinations={
                    "destinations_key": cloud_assembly_schema.DockerImageDestination(
                        image_tag="imageTag",
                        repository_name="repositoryName",
            
                        # the properties below are optional
                        assume_role_arn="assumeRoleArn",
                        assume_role_external_id="assumeRoleExternalId",
                        region="region"
                    )
                },
                source=cloud_assembly_schema.DockerImageSource(
                    directory="directory",
                    docker_build_args={
                        "docker_build_args_key": "dockerBuildArgs"
                    },
                    docker_build_target="dockerBuildTarget",
                    docker_file="dockerFile",
                    executable=["executable"],
                    network_mode="networkMode",
                    platform="platform"
                )
            )
        '''
        if isinstance(source, dict):
            source = DockerImageSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a058bb5ca7e30fd740d2f099779a473d25b9af3acd7fcd93b8fdecc9a7381c2d)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destinations": destinations,
            "source": source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[builtins.str, "DockerImageDestination"]:
        '''(experimental) Destinations for this file asset.

        :stability: experimental
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.Mapping[builtins.str, "DockerImageDestination"], result)

    @builtins.property
    def source(self) -> "DockerImageSource":
        '''(experimental) Source description for file assets.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("DockerImageSource", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DockerImageDestination",
    jsii_struct_bases=[AwsDestination],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
        "image_tag": "imageTag",
        "repository_name": "repositoryName",
    },
)
class DockerImageDestination(AwsDestination):
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        image_tag: builtins.str,
        repository_name: builtins.str,
    ) -> None:
        '''(experimental) Where to publish docker images.

        :param assume_role_arn: (experimental) The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: (experimental) The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: (experimental) The region where this asset will need to be published. Default: - Current region
        :param image_tag: (experimental) Tag of the image to publish.
        :param repository_name: (experimental) Name of the ECR repository to publish to.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            docker_image_destination = cloud_assembly_schema.DockerImageDestination(
                image_tag="imageTag",
                repository_name="repositoryName",
            
                # the properties below are optional
                assume_role_arn="assumeRoleArn",
                assume_role_external_id="assumeRoleExternalId",
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e124c79400a0a76e2c2bd2f467f4bfc6fa0c435c459ebd7eb06bd9db57d6897)
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument assume_role_external_id", value=assume_role_external_id, expected_type=type_hints["assume_role_external_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
            check_type(argname="argument repository_name", value=repository_name, expected_type=type_hints["repository_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "image_tag": image_tag,
            "repository_name": repository_name,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed

        :stability: experimental
        '''
        result = self._values.get("assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied

        :stability: experimental
        '''
        result = self._values.get("assume_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where this asset will need to be published.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> builtins.str:
        '''(experimental) Tag of the image to publish.

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        assert result is not None, "Required property 'image_tag' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def repository_name(self) -> builtins.str:
        '''(experimental) Name of the ECR repository to publish to.

        :stability: experimental
        '''
        result = self._values.get("repository_name")
        assert result is not None, "Required property 'repository_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.DockerImageSource",
    jsii_struct_bases=[],
    name_mapping={
        "directory": "directory",
        "docker_build_args": "dockerBuildArgs",
        "docker_build_target": "dockerBuildTarget",
        "docker_file": "dockerFile",
        "executable": "executable",
        "network_mode": "networkMode",
        "platform": "platform",
    },
)
class DockerImageSource:
    def __init__(
        self,
        *,
        directory: typing.Optional[builtins.str] = None,
        docker_build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        docker_build_target: typing.Optional[builtins.str] = None,
        docker_file: typing.Optional[builtins.str] = None,
        executable: typing.Optional[typing.Sequence[builtins.str]] = None,
        network_mode: typing.Optional[builtins.str] = None,
        platform: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for how to produce a Docker image from a source.

        :param directory: (experimental) The directory containing the Docker image build instructions. This path is relative to the asset manifest location. Default: - Exactly one of ``directory`` and ``executable`` is required
        :param docker_build_args: (experimental) Additional build arguments. Only allowed when ``directory`` is set. Default: - No additional build arguments
        :param docker_build_target: (experimental) Target build stage in a Dockerfile with multiple build stages. Only allowed when ``directory`` is set. Default: - The last stage in the Dockerfile
        :param docker_file: (experimental) The name of the file with build instructions. Only allowed when ``directory`` is set. Default: "Dockerfile"
        :param executable: (experimental) A command-line executable that returns the name of a local Docker image on stdout after being run. Default: - Exactly one of ``directory`` and ``executable`` is required
        :param network_mode: (experimental) Networking mode for the RUN commands during build. *Requires Docker Engine API v1.25+*. Specify this property to build images on a specific networking mode. Default: - no networking mode specified
        :param platform: (experimental) Platform to build for. *Requires Docker Buildx*. Specify this property to build images on a specific platform/architecture. Default: - current machine platform

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            docker_image_source = cloud_assembly_schema.DockerImageSource(
                directory="directory",
                docker_build_args={
                    "docker_build_args_key": "dockerBuildArgs"
                },
                docker_build_target="dockerBuildTarget",
                docker_file="dockerFile",
                executable=["executable"],
                network_mode="networkMode",
                platform="platform"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__104edb7ee38860ee04a1fde6703c74c5815f414ceb63086ff228f8ca4b34a9bc)
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument docker_build_args", value=docker_build_args, expected_type=type_hints["docker_build_args"])
            check_type(argname="argument docker_build_target", value=docker_build_target, expected_type=type_hints["docker_build_target"])
            check_type(argname="argument docker_file", value=docker_file, expected_type=type_hints["docker_file"])
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument network_mode", value=network_mode, expected_type=type_hints["network_mode"])
            check_type(argname="argument platform", value=platform, expected_type=type_hints["platform"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if directory is not None:
            self._values["directory"] = directory
        if docker_build_args is not None:
            self._values["docker_build_args"] = docker_build_args
        if docker_build_target is not None:
            self._values["docker_build_target"] = docker_build_target
        if docker_file is not None:
            self._values["docker_file"] = docker_file
        if executable is not None:
            self._values["executable"] = executable
        if network_mode is not None:
            self._values["network_mode"] = network_mode
        if platform is not None:
            self._values["platform"] = platform

    @builtins.property
    def directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory containing the Docker image build instructions.

        This path is relative to the asset manifest location.

        :default: - Exactly one of ``directory`` and ``executable`` is required

        :stability: experimental
        '''
        result = self._values.get("directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_build_args(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional build arguments.

        Only allowed when ``directory`` is set.

        :default: - No additional build arguments

        :stability: experimental
        '''
        result = self._values.get("docker_build_args")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def docker_build_target(self) -> typing.Optional[builtins.str]:
        '''(experimental) Target build stage in a Dockerfile with multiple build stages.

        Only allowed when ``directory`` is set.

        :default: - The last stage in the Dockerfile

        :stability: experimental
        '''
        result = self._values.get("docker_build_target")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_file(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the file with build instructions.

        Only allowed when ``directory`` is set.

        :default: "Dockerfile"

        :stability: experimental
        '''
        result = self._values.get("docker_file")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def executable(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A command-line executable that returns the name of a local Docker image on stdout after being run.

        :default: - Exactly one of ``directory`` and ``executable`` is required

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def network_mode(self) -> typing.Optional[builtins.str]:
        '''(experimental) Networking mode for the RUN commands during build. *Requires Docker Engine API v1.25+*.

        Specify this property to build images on a specific networking mode.

        :default: - no networking mode specified

        :stability: experimental
        '''
        result = self._values.get("network_mode")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def platform(self) -> typing.Optional[builtins.str]:
        '''(experimental) Platform to build for. *Requires Docker Buildx*.

        Specify this property to build images on a specific platform/architecture.

        :default: - current machine platform

        :stability: experimental
        '''
        result = self._values.get("platform")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerImageSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.EndpointServiceAvailabilityZonesContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "service_name": "serviceName",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class EndpointServiceAvailabilityZonesContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        region: builtins.str,
        service_name: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query to endpoint service context provider.

        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param service_name: (experimental) Query service name.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            endpoint_service_availability_zones_context_query = cloud_assembly_schema.EndpointServiceAvailabilityZonesContextQuery(
                account="account",
                region="region",
                service_name="serviceName",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__61789c9f65bf8cbf7c0f744a3aaa5f93aa65164be9576583fd2bb9561e9450e1)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument service_name", value=service_name, expected_type=type_hints["service_name"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "region": region,
            "service_name": service_name,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def service_name(self) -> builtins.str:
        '''(experimental) Query service name.

        :stability: experimental
        '''
        result = self._values.get("service_name")
        assert result is not None, "Required property 'service_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EndpointServiceAvailabilityZonesContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.FileAsset",
    jsii_struct_bases=[],
    name_mapping={"destinations": "destinations", "source": "source"},
)
class FileAsset:
    def __init__(
        self,
        *,
        destinations: typing.Mapping[builtins.str, typing.Union["FileDestination", typing.Dict[builtins.str, typing.Any]]],
        source: typing.Union["FileSource", typing.Dict[builtins.str, typing.Any]],
    ) -> None:
        '''(experimental) A file asset.

        :param destinations: (experimental) Destinations for this file asset.
        :param source: (experimental) Source description for file assets.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            file_asset = cloud_assembly_schema.FileAsset(
                destinations={
                    "destinations_key": cloud_assembly_schema.FileDestination(
                        bucket_name="bucketName",
                        object_key="objectKey",
            
                        # the properties below are optional
                        assume_role_arn="assumeRoleArn",
                        assume_role_external_id="assumeRoleExternalId",
                        region="region"
                    )
                },
                source=cloud_assembly_schema.FileSource(
                    executable=["executable"],
                    packaging=cloud_assembly_schema.FileAssetPackaging.FILE,
                    path="path"
                )
            )
        '''
        if isinstance(source, dict):
            source = FileSource(**source)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a43b845fc9b5119ae995164ceb987384abea2587c952dc4ec9023ca057a702dc)
            check_type(argname="argument destinations", value=destinations, expected_type=type_hints["destinations"])
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destinations": destinations,
            "source": source,
        }

    @builtins.property
    def destinations(self) -> typing.Mapping[builtins.str, "FileDestination"]:
        '''(experimental) Destinations for this file asset.

        :stability: experimental
        '''
        result = self._values.get("destinations")
        assert result is not None, "Required property 'destinations' is missing"
        return typing.cast(typing.Mapping[builtins.str, "FileDestination"], result)

    @builtins.property
    def source(self) -> "FileSource":
        '''(experimental) Source description for file assets.

        :stability: experimental
        '''
        result = self._values.get("source")
        assert result is not None, "Required property 'source' is missing"
        return typing.cast("FileSource", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.FileAssetMetadataEntry",
    jsii_struct_bases=[],
    name_mapping={
        "artifact_hash_parameter": "artifactHashParameter",
        "id": "id",
        "packaging": "packaging",
        "path": "path",
        "s3_bucket_parameter": "s3BucketParameter",
        "s3_key_parameter": "s3KeyParameter",
        "source_hash": "sourceHash",
    },
)
class FileAssetMetadataEntry:
    def __init__(
        self,
        *,
        artifact_hash_parameter: builtins.str,
        id: builtins.str,
        packaging: builtins.str,
        path: builtins.str,
        s3_bucket_parameter: builtins.str,
        s3_key_parameter: builtins.str,
        source_hash: builtins.str,
    ) -> None:
        '''(experimental) Metadata Entry spec for files.

        :param artifact_hash_parameter: (experimental) The name of the parameter where the hash of the bundled asset should be passed in.
        :param id: (experimental) Logical identifier for the asset.
        :param packaging: (experimental) Requested packaging style.
        :param path: (experimental) Path on disk to the asset.
        :param s3_bucket_parameter: (experimental) Name of parameter where S3 bucket should be passed in.
        :param s3_key_parameter: (experimental) Name of parameter where S3 key should be passed in.
        :param source_hash: (experimental) The hash of the asset source.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # Example automatically generated from non-compiling source. May contain errors.
            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            file_asset_metadata_entry = cloud_assembly_schema.FileAssetMetadataEntry(
                artifact_hash_parameter="artifactHashParameter",
                id="id",
                packaging="packaging",
                path="path",
                s3_bucket_parameter="s3BucketParameter",
                s3_key_parameter="s3KeyParameter",
                source_hash="sourceHash"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2459ad59dfbc1ef3868ee67e7fd1da30ce9cc0907258260abecd2114c24d9ca4)
            check_type(argname="argument artifact_hash_parameter", value=artifact_hash_parameter, expected_type=type_hints["artifact_hash_parameter"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument s3_bucket_parameter", value=s3_bucket_parameter, expected_type=type_hints["s3_bucket_parameter"])
            check_type(argname="argument s3_key_parameter", value=s3_key_parameter, expected_type=type_hints["s3_key_parameter"])
            check_type(argname="argument source_hash", value=source_hash, expected_type=type_hints["source_hash"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact_hash_parameter": artifact_hash_parameter,
            "id": id,
            "packaging": packaging,
            "path": path,
            "s3_bucket_parameter": s3_bucket_parameter,
            "s3_key_parameter": s3_key_parameter,
            "source_hash": source_hash,
        }

    @builtins.property
    def artifact_hash_parameter(self) -> builtins.str:
        '''(experimental) The name of the parameter where the hash of the bundled asset should be passed in.

        :stability: experimental
        '''
        result = self._values.get("artifact_hash_parameter")
        assert result is not None, "Required property 'artifact_hash_parameter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def id(self) -> builtins.str:
        '''(experimental) Logical identifier for the asset.

        :stability: experimental
        '''
        result = self._values.get("id")
        assert result is not None, "Required property 'id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def packaging(self) -> builtins.str:
        '''(experimental) Requested packaging style.

        :stability: experimental
        '''
        result = self._values.get("packaging")
        assert result is not None, "Required property 'packaging' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def path(self) -> builtins.str:
        '''(experimental) Path on disk to the asset.

        :stability: experimental
        '''
        result = self._values.get("path")
        assert result is not None, "Required property 'path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_bucket_parameter(self) -> builtins.str:
        '''(experimental) Name of parameter where S3 bucket should be passed in.

        :stability: experimental
        '''
        result = self._values.get("s3_bucket_parameter")
        assert result is not None, "Required property 's3_bucket_parameter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def s3_key_parameter(self) -> builtins.str:
        '''(experimental) Name of parameter where S3 key should be passed in.

        :stability: experimental
        '''
        result = self._values.get("s3_key_parameter")
        assert result is not None, "Required property 's3_key_parameter' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def source_hash(self) -> builtins.str:
        '''(experimental) The hash of the asset source.

        :stability: experimental
        '''
        result = self._values.get("source_hash")
        assert result is not None, "Required property 'source_hash' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileAssetMetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.FileAssetPackaging")
class FileAssetPackaging(enum.Enum):
    '''(experimental) Packaging strategy for file assets.

    :stability: experimental
    '''

    FILE = "FILE"
    '''(experimental) Upload the given path as a file.

    :stability: experimental
    '''
    ZIP_DIRECTORY = "ZIP_DIRECTORY"
    '''(experimental) The given path is a directory, zip it and upload.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.FileDestination",
    jsii_struct_bases=[AwsDestination],
    name_mapping={
        "assume_role_arn": "assumeRoleArn",
        "assume_role_external_id": "assumeRoleExternalId",
        "region": "region",
        "bucket_name": "bucketName",
        "object_key": "objectKey",
    },
)
class FileDestination(AwsDestination):
    def __init__(
        self,
        *,
        assume_role_arn: typing.Optional[builtins.str] = None,
        assume_role_external_id: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        bucket_name: builtins.str,
        object_key: builtins.str,
    ) -> None:
        '''(experimental) Where in S3 a file asset needs to be published.

        :param assume_role_arn: (experimental) The role that needs to be assumed while publishing this asset. Default: - No role will be assumed
        :param assume_role_external_id: (experimental) The ExternalId that needs to be supplied while assuming this role. Default: - No ExternalId will be supplied
        :param region: (experimental) The region where this asset will need to be published. Default: - Current region
        :param bucket_name: (experimental) The name of the bucket.
        :param object_key: (experimental) The destination object key.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            file_destination = cloud_assembly_schema.FileDestination(
                bucket_name="bucketName",
                object_key="objectKey",
            
                # the properties below are optional
                assume_role_arn="assumeRoleArn",
                assume_role_external_id="assumeRoleExternalId",
                region="region"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__480c6a6ac88167c38aa2fee76f5a82756a7ae673810ae852380ebd9ca7536537)
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument assume_role_external_id", value=assume_role_external_id, expected_type=type_hints["assume_role_external_id"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
            check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "bucket_name": bucket_name,
            "object_key": object_key,
        }
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if assume_role_external_id is not None:
            self._values["assume_role_external_id"] = assume_role_external_id
        if region is not None:
            self._values["region"] = region

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The role that needs to be assumed while publishing this asset.

        :default: - No role will be assumed

        :stability: experimental
        '''
        result = self._values.get("assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assume_role_external_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ExternalId that needs to be supplied while assuming this role.

        :default: - No ExternalId will be supplied

        :stability: experimental
        '''
        result = self._values.get("assume_role_external_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) The region where this asset will need to be published.

        :default: - Current region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def bucket_name(self) -> builtins.str:
        '''(experimental) The name of the bucket.

        :stability: experimental
        '''
        result = self._values.get("bucket_name")
        assert result is not None, "Required property 'bucket_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def object_key(self) -> builtins.str:
        '''(experimental) The destination object key.

        :stability: experimental
        '''
        result = self._values.get("object_key")
        assert result is not None, "Required property 'object_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileDestination(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.FileSource",
    jsii_struct_bases=[],
    name_mapping={
        "executable": "executable",
        "packaging": "packaging",
        "path": "path",
    },
)
class FileSource:
    def __init__(
        self,
        *,
        executable: typing.Optional[typing.Sequence[builtins.str]] = None,
        packaging: typing.Optional[FileAssetPackaging] = None,
        path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Describe the source of a file asset.

        :param executable: (experimental) External command which will produce the file asset to upload. Default: - Exactly one of ``executable`` and ``path`` is required.
        :param packaging: (experimental) Packaging method. Only allowed when ``path`` is specified. Default: FILE
        :param path: (experimental) The filesystem object to upload. This path is relative to the asset manifest location. Default: - Exactly one of ``executable`` and ``path`` is required.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            file_source = cloud_assembly_schema.FileSource(
                executable=["executable"],
                packaging=cloud_assembly_schema.FileAssetPackaging.FILE,
                path="path"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f951c5369c28990fc35ca311fe7d7d4af410301a880bf4a3b91bd666dfed6476)
            check_type(argname="argument executable", value=executable, expected_type=type_hints["executable"])
            check_type(argname="argument packaging", value=packaging, expected_type=type_hints["packaging"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if executable is not None:
            self._values["executable"] = executable
        if packaging is not None:
            self._values["packaging"] = packaging
        if path is not None:
            self._values["path"] = path

    @builtins.property
    def executable(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) External command which will produce the file asset to upload.

        :default: - Exactly one of ``executable`` and ``path`` is required.

        :stability: experimental
        '''
        result = self._values.get("executable")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def packaging(self) -> typing.Optional[FileAssetPackaging]:
        '''(experimental) Packaging method.

        Only allowed when ``path`` is specified.

        :default: FILE

        :stability: experimental
        '''
        result = self._values.get("packaging")
        return typing.cast(typing.Optional[FileAssetPackaging], result)

    @builtins.property
    def path(self) -> typing.Optional[builtins.str]:
        '''(experimental) The filesystem object to upload.

        This path is relative to the asset manifest location.

        :default: - Exactly one of ``executable`` and ``path`` is required.

        :stability: experimental
        '''
        result = self._values.get("path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSource(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.Hooks",
    jsii_struct_bases=[],
    name_mapping={
        "post_deploy": "postDeploy",
        "post_destroy": "postDestroy",
        "pre_deploy": "preDeploy",
        "pre_destroy": "preDestroy",
    },
)
class Hooks:
    def __init__(
        self,
        *,
        post_deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
        post_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
        pre_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) Commands to run at predefined points during the integration test workflow.

        :param post_deploy: (experimental) Commands to run prior after deploying the cdk stacks in the integration test. Default: - no commands
        :param post_destroy: (experimental) Commands to run after destroying the cdk stacks in the integration test. Default: - no commands
        :param pre_deploy: (experimental) Commands to run prior to deploying the cdk stacks in the integration test. Default: - no commands
        :param pre_destroy: (experimental) Commands to run prior to destroying the cdk stacks in the integration test. Default: - no commands

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            hooks = cloud_assembly_schema.Hooks(
                post_deploy=["postDeploy"],
                post_destroy=["postDestroy"],
                pre_deploy=["preDeploy"],
                pre_destroy=["preDestroy"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__910fdf7f70801aee3e341900ae5774a4b8ae93545d58996faaecef06bada8e4c)
            check_type(argname="argument post_deploy", value=post_deploy, expected_type=type_hints["post_deploy"])
            check_type(argname="argument post_destroy", value=post_destroy, expected_type=type_hints["post_destroy"])
            check_type(argname="argument pre_deploy", value=pre_deploy, expected_type=type_hints["pre_deploy"])
            check_type(argname="argument pre_destroy", value=pre_destroy, expected_type=type_hints["pre_destroy"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post_deploy is not None:
            self._values["post_deploy"] = post_deploy
        if post_destroy is not None:
            self._values["post_destroy"] = post_destroy
        if pre_deploy is not None:
            self._values["pre_deploy"] = pre_deploy
        if pre_destroy is not None:
            self._values["pre_destroy"] = pre_destroy

    @builtins.property
    def post_deploy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run prior after deploying the cdk stacks in the integration test.

        :default: - no commands

        :stability: experimental
        '''
        result = self._values.get("post_deploy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def post_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run after destroying the cdk stacks in the integration test.

        :default: - no commands

        :stability: experimental
        '''
        result = self._values.get("post_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_deploy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run prior to deploying the cdk stacks in the integration test.

        :default: - no commands

        :stability: experimental
        '''
        result = self._values.get("pre_deploy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def pre_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Commands to run prior to destroying the cdk stacks in the integration test.

        :default: - no commands

        :stability: experimental
        '''
        result = self._values.get("pre_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Hooks(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.HostedZoneContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "domain_name": "domainName",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
        "private_zone": "privateZone",
        "vpc_id": "vpcId",
    },
)
class HostedZoneContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        domain_name: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
        private_zone: typing.Optional[builtins.bool] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query to hosted zone context provider.

        :param account: (experimental) Query account.
        :param domain_name: (experimental) The domain name e.g. example.com to lookup.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None
        :param private_zone: (experimental) True if the zone you want to find is a private hosted zone. Default: false
        :param vpc_id: (experimental) The VPC ID to that the private zone must be associated with. If you provide VPC ID and privateZone is false, this will return no results and raise an error. Default: - Required if privateZone=true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            hosted_zone_context_query = cloud_assembly_schema.HostedZoneContextQuery(
                account="account",
                domain_name="domainName",
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn",
                private_zone=False,
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7f67a4a8a0193498879ad71d01f369e35e92cbdeb3a1b1ecb87b8d2e6d857a1d)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
            check_type(argname="argument private_zone", value=private_zone, expected_type=type_hints["private_zone"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "domain_name": domain_name,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn
        if private_zone is not None:
            self._values["private_zone"] = private_zone
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def domain_name(self) -> builtins.str:
        '''(experimental) The domain name e.g. example.com to lookup.

        :stability: experimental
        '''
        result = self._values.get("domain_name")
        assert result is not None, "Required property 'domain_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def private_zone(self) -> typing.Optional[builtins.bool]:
        '''(experimental) True if the zone you want to find is a private hosted zone.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("private_zone")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The VPC ID to that the private zone must be associated with.

        If you provide VPC ID and privateZone is false, this will return no results
        and raise an error.

        :default: - Required if privateZone=true

        :stability: experimental
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HostedZoneContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.IntegManifest",
    jsii_struct_bases=[],
    name_mapping={
        "test_cases": "testCases",
        "version": "version",
        "enable_lookups": "enableLookups",
        "synth_context": "synthContext",
    },
)
class IntegManifest:
    def __init__(
        self,
        *,
        test_cases: typing.Mapping[builtins.str, typing.Union["TestCase", typing.Dict[builtins.str, typing.Any]]],
        version: builtins.str,
        enable_lookups: typing.Optional[builtins.bool] = None,
        synth_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''(experimental) Definitions for the integration testing manifest.

        :param test_cases: (experimental) test cases.
        :param version: (experimental) Version of the manifest.
        :param enable_lookups: (experimental) Enable lookups for this test. If lookups are enabled then ``stackUpdateWorkflow`` must be set to false. Lookups should only be enabled when you are explicitely testing lookups. Default: false
        :param synth_context: (experimental) Additional context to use when performing a synth. Any context provided here will override any default context Default: - no additional context

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            integ_manifest = cloud_assembly_schema.IntegManifest(
                test_cases={
                    "test_cases_key": cloud_assembly_schema.TestCase(
                        stacks=["stacks"],
            
                        # the properties below are optional
                        allow_destroy=["allowDestroy"],
                        assertion_stack="assertionStack",
                        cdk_command_options=cloud_assembly_schema.CdkCommands(
                            deploy=cloud_assembly_schema.DeployCommand(
                                args=cloud_assembly_schema.DeployOptions(
                                    all=False,
                                    app="app",
                                    asset_metadata=False,
                                    ca_bundle_path="caBundlePath",
                                    change_set_name="changeSetName",
                                    ci=False,
                                    color=False,
                                    context={
                                        "context_key": "context"
                                    },
                                    debug=False,
                                    ec2_creds=False,
                                    exclusively=False,
                                    execute=False,
                                    force=False,
                                    ignore_errors=False,
                                    json=False,
                                    lookups=False,
                                    notices=False,
                                    notification_arns=["notificationArns"],
                                    output="output",
                                    outputs_file="outputsFile",
                                    parameters={
                                        "parameters_key": "parameters"
                                    },
                                    path_metadata=False,
                                    profile="profile",
                                    proxy="proxy",
                                    require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                                    reuse_assets=["reuseAssets"],
                                    role_arn="roleArn",
                                    rollback=False,
                                    stacks=["stacks"],
                                    staging=False,
                                    strict=False,
                                    toolkit_stack_name="toolkitStackName",
                                    trace=False,
                                    use_previous_parameters=False,
                                    verbose=False,
                                    version_reporting=False
                                ),
                                enabled=False,
                                expected_message="expectedMessage",
                                expect_error=False
                            ),
                            destroy=cloud_assembly_schema.DestroyCommand(
                                args=cloud_assembly_schema.DestroyOptions(
                                    all=False,
                                    app="app",
                                    asset_metadata=False,
                                    ca_bundle_path="caBundlePath",
                                    color=False,
                                    context={
                                        "context_key": "context"
                                    },
                                    debug=False,
                                    ec2_creds=False,
                                    exclusively=False,
                                    force=False,
                                    ignore_errors=False,
                                    json=False,
                                    lookups=False,
                                    notices=False,
                                    output="output",
                                    path_metadata=False,
                                    profile="profile",
                                    proxy="proxy",
                                    role_arn="roleArn",
                                    stacks=["stacks"],
                                    staging=False,
                                    strict=False,
                                    trace=False,
                                    verbose=False,
                                    version_reporting=False
                                ),
                                enabled=False,
                                expected_message="expectedMessage",
                                expect_error=False
                            )
                        ),
                        diff_assets=False,
                        hooks=cloud_assembly_schema.Hooks(
                            post_deploy=["postDeploy"],
                            post_destroy=["postDestroy"],
                            pre_deploy=["preDeploy"],
                            pre_destroy=["preDestroy"]
                        ),
                        regions=["regions"],
                        stack_update_workflow=False
                    )
                },
                version="version",
            
                # the properties below are optional
                enable_lookups=False,
                synth_context={
                    "synth_context_key": "synthContext"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d4f9fe52a44507be12304f6e9783c36b8d643163178af5d0d7188d7e2e7196e8)
            check_type(argname="argument test_cases", value=test_cases, expected_type=type_hints["test_cases"])
            check_type(argname="argument version", value=version, expected_type=type_hints["version"])
            check_type(argname="argument enable_lookups", value=enable_lookups, expected_type=type_hints["enable_lookups"])
            check_type(argname="argument synth_context", value=synth_context, expected_type=type_hints["synth_context"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "test_cases": test_cases,
            "version": version,
        }
        if enable_lookups is not None:
            self._values["enable_lookups"] = enable_lookups
        if synth_context is not None:
            self._values["synth_context"] = synth_context

    @builtins.property
    def test_cases(self) -> typing.Mapping[builtins.str, "TestCase"]:
        '''(experimental) test cases.

        :stability: experimental
        '''
        result = self._values.get("test_cases")
        assert result is not None, "Required property 'test_cases' is missing"
        return typing.cast(typing.Mapping[builtins.str, "TestCase"], result)

    @builtins.property
    def version(self) -> builtins.str:
        '''(experimental) Version of the manifest.

        :stability: experimental
        '''
        result = self._values.get("version")
        assert result is not None, "Required property 'version' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def enable_lookups(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable lookups for this test.

        If lookups are enabled
        then ``stackUpdateWorkflow`` must be set to false.
        Lookups should only be enabled when you are explicitely testing
        lookups.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("enable_lookups")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synth_context(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Additional context to use when performing a synth.

        Any context provided here will override
        any default context

        :default: - no additional context

        :stability: experimental
        '''
        result = self._values.get("synth_context")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegManifest(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.KeyContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "alias_name": "aliasName",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class KeyContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        alias_name: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query input for looking up a KMS Key.

        :param account: (experimental) Query account.
        :param alias_name: (experimental) Alias name used to search the Key.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            key_context_query = cloud_assembly_schema.KeyContextQuery(
                account="account",
                alias_name="aliasName",
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d7ee6469151c451820b41eb1f38f20269d2d84fdcbd30e2d240d47028f768e7f)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "alias_name": alias_name,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def alias_name(self) -> builtins.str:
        '''(experimental) Alias name used to search the Key.

        :stability: experimental
        '''
        result = self._values.get("alias_name")
        assert result is not None, "Required property 'alias_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "KeyContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.LoadBalancerFilter",
    jsii_struct_bases=[],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
    },
)
class LoadBalancerFilter:
    def __init__(
        self,
        *,
        load_balancer_type: "LoadBalancerType",
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Filters for selecting load balancers.

        :param load_balancer_type: (experimental) Filter load balancers by their type.
        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            load_balancer_filter = cloud_assembly_schema.LoadBalancerFilter(
                load_balancer_type=cloud_assembly_schema.LoadBalancerType.NETWORK,
            
                # the properties below are optional
                load_balancer_arn="loadBalancerArn",
                load_balancer_tags=[cloud_assembly_schema.Tag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__38c5568223c5face9dcf7c7da7bafb4fe4f911e234a66832dac4ab9968d65b9f)
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument load_balancer_tags", value=load_balancer_tags, expected_type=type_hints["load_balancer_tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags

    @builtins.property
    def load_balancer_type(self) -> "LoadBalancerType":
        '''(experimental) Filter load balancers by their type.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast("LoadBalancerType", result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerFilter(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.LoadBalancerListenerContextQuery",
    jsii_struct_bases=[LoadBalancerFilter],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "account": "account",
        "region": "region",
        "listener_arn": "listenerArn",
        "listener_port": "listenerPort",
        "listener_protocol": "listenerProtocol",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class LoadBalancerListenerContextQuery(LoadBalancerFilter):
    def __init__(
        self,
        *,
        load_balancer_type: "LoadBalancerType",
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]] = None,
        account: builtins.str,
        region: builtins.str,
        listener_arn: typing.Optional[builtins.str] = None,
        listener_port: typing.Optional[jsii.Number] = None,
        listener_protocol: typing.Optional["LoadBalancerListenerProtocol"] = None,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query input for looking up a load balancer listener.

        :param load_balancer_type: (experimental) Filter load balancers by their type.
        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags
        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param listener_arn: (experimental) Find by listener's arn. Default: - does not find by listener arn
        :param listener_port: (experimental) Filter listeners by listener port. Default: - does not filter by a listener port
        :param listener_protocol: (experimental) Filter by listener protocol. Default: - does not filter by listener protocol
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            load_balancer_listener_context_query = cloud_assembly_schema.LoadBalancerListenerContextQuery(
                account="account",
                load_balancer_type=cloud_assembly_schema.LoadBalancerType.NETWORK,
                region="region",
            
                # the properties below are optional
                listener_arn="listenerArn",
                listener_port=123,
                listener_protocol=cloud_assembly_schema.LoadBalancerListenerProtocol.HTTP,
                load_balancer_arn="loadBalancerArn",
                load_balancer_tags=[cloud_assembly_schema.Tag(
                    key="key",
                    value="value"
                )],
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ce1111745c92a8dde1c598d93b77da6716573ad8de29c30f000a3815b978727e)
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument load_balancer_tags", value=load_balancer_tags, expected_type=type_hints["load_balancer_tags"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument listener_arn", value=listener_arn, expected_type=type_hints["listener_arn"])
            check_type(argname="argument listener_port", value=listener_port, expected_type=type_hints["listener_port"])
            check_type(argname="argument listener_protocol", value=listener_protocol, expected_type=type_hints["listener_protocol"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
            "account": account,
            "region": region,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if listener_arn is not None:
            self._values["listener_arn"] = listener_arn
        if listener_port is not None:
            self._values["listener_port"] = listener_port
        if listener_protocol is not None:
            self._values["listener_protocol"] = listener_protocol
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def load_balancer_type(self) -> "LoadBalancerType":
        '''(experimental) Filter load balancers by their type.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast("LoadBalancerType", result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List["Tag"]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.List["Tag"]], result)

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def listener_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by listener's arn.

        :default: - does not find by listener arn

        :stability: experimental
        '''
        result = self._values.get("listener_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def listener_port(self) -> typing.Optional[jsii.Number]:
        '''(experimental) Filter listeners by listener port.

        :default: - does not filter by a listener port

        :stability: experimental
        '''
        result = self._values.get("listener_port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def listener_protocol(self) -> typing.Optional["LoadBalancerListenerProtocol"]:
        '''(experimental) Filter by listener protocol.

        :default: - does not filter by listener protocol

        :stability: experimental
        '''
        result = self._values.get("listener_protocol")
        return typing.cast(typing.Optional["LoadBalancerListenerProtocol"], result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerListenerContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.LoadBalancerListenerProtocol")
class LoadBalancerListenerProtocol(enum.Enum):
    '''(experimental) The protocol for connections from clients to the load balancer.

    :stability: experimental
    '''

    HTTP = "HTTP"
    '''(experimental) HTTP protocol.

    :stability: experimental
    '''
    HTTPS = "HTTPS"
    '''(experimental) HTTPS protocol.

    :stability: experimental
    '''
    TCP = "TCP"
    '''(experimental) TCP protocol.

    :stability: experimental
    '''
    TLS = "TLS"
    '''(experimental) TLS protocol.

    :stability: experimental
    '''
    UDP = "UDP"
    '''(experimental) UDP protocol.

    :stability: experimental
    '''
    TCP_UDP = "TCP_UDP"
    '''(experimental) TCP and UDP protocol.

    :stability: experimental
    '''


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.LoadBalancerType")
class LoadBalancerType(enum.Enum):
    '''(experimental) Type of load balancer.

    :stability: experimental
    '''

    NETWORK = "NETWORK"
    '''(experimental) Network load balancer.

    :stability: experimental
    '''
    APPLICATION = "APPLICATION"
    '''(experimental) Application load balancer.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.LoadManifestOptions",
    jsii_struct_bases=[],
    name_mapping={
        "skip_enum_check": "skipEnumCheck",
        "skip_version_check": "skipVersionCheck",
    },
)
class LoadManifestOptions:
    def __init__(
        self,
        *,
        skip_enum_check: typing.Optional[builtins.bool] = None,
        skip_version_check: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Options for the loadManifest operation.

        :param skip_enum_check: (experimental) Skip enum checks. This means you may read enum values you don't know about yet. Make sure to always check the values of enums you encounter in the manifest. Default: false
        :param skip_version_check: (experimental) Skip the version check. This means you may read a newer cloud assembly than the CX API is designed to support, and your application may not be aware of all features that in use in the Cloud Assembly. Default: false

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            load_manifest_options = cloud_assembly_schema.LoadManifestOptions(
                skip_enum_check=False,
                skip_version_check=False
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__356e2b51b940724005f4d816b60902c571d28579650fc00dc287283c2c83f88c)
            check_type(argname="argument skip_enum_check", value=skip_enum_check, expected_type=type_hints["skip_enum_check"])
            check_type(argname="argument skip_version_check", value=skip_version_check, expected_type=type_hints["skip_version_check"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if skip_enum_check is not None:
            self._values["skip_enum_check"] = skip_enum_check
        if skip_version_check is not None:
            self._values["skip_version_check"] = skip_version_check

    @builtins.property
    def skip_enum_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Skip enum checks.

        This means you may read enum values you don't know about yet. Make sure to always
        check the values of enums you encounter in the manifest.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("skip_enum_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def skip_version_check(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Skip the version check.

        This means you may read a newer cloud assembly than the CX API is designed
        to support, and your application may not be aware of all features that in use
        in the Cloud Assembly.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("skip_version_check")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadManifestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Manifest(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.cloud_assembly_schema.Manifest",
):
    '''(experimental) Protocol utility class.

    :stability: experimental
    '''

    @jsii.member(jsii_name="load")
    @builtins.classmethod
    def load(cls, file_path: builtins.str) -> AssemblyManifest:
        '''(deprecated) Deprecated.

        :param file_path: -

        :deprecated: use ``loadAssemblyManifest()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__078e52672b5074804e1112222ee4da699db48d2a060886035e384130eb111d75)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(AssemblyManifest, jsii.sinvoke(cls, "load", [file_path]))

    @jsii.member(jsii_name="loadAssemblyManifest")
    @builtins.classmethod
    def load_assembly_manifest(
        cls,
        file_path: builtins.str,
        *,
        skip_enum_check: typing.Optional[builtins.bool] = None,
        skip_version_check: typing.Optional[builtins.bool] = None,
    ) -> AssemblyManifest:
        '''(experimental) Load and validates the cloud assembly manifest from file.

        :param file_path: - path to the manifest file.
        :param skip_enum_check: (experimental) Skip enum checks. This means you may read enum values you don't know about yet. Make sure to always check the values of enums you encounter in the manifest. Default: false
        :param skip_version_check: (experimental) Skip the version check. This means you may read a newer cloud assembly than the CX API is designed to support, and your application may not be aware of all features that in use in the Cloud Assembly. Default: false

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c05faad83b24dfdb41efdaebc292291c68f49b6f211778f7dbccc93d158cb9d3)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = LoadManifestOptions(
            skip_enum_check=skip_enum_check, skip_version_check=skip_version_check
        )

        return typing.cast(AssemblyManifest, jsii.sinvoke(cls, "loadAssemblyManifest", [file_path, options]))

    @jsii.member(jsii_name="loadAssetManifest")
    @builtins.classmethod
    def load_asset_manifest(cls, file_path: builtins.str) -> AssetManifest:
        '''(experimental) Load and validates the asset manifest from file.

        :param file_path: - path to the manifest file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d4c0d3d26f8774b5c5122edbc2e8ee5bc73d0dd26743265038e81a1151420f1)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(AssetManifest, jsii.sinvoke(cls, "loadAssetManifest", [file_path]))

    @jsii.member(jsii_name="loadIntegManifest")
    @builtins.classmethod
    def load_integ_manifest(cls, file_path: builtins.str) -> IntegManifest:
        '''(experimental) Load and validates the integ manifest from file.

        :param file_path: - path to the manifest file.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bcc032aa406e5c3e313713dc9d6bd3f7e9caa9dfe8f510f1148886716574c7f)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(IntegManifest, jsii.sinvoke(cls, "loadIntegManifest", [file_path]))

    @jsii.member(jsii_name="save")
    @builtins.classmethod
    def save(
        cls,
        manifest: typing.Union[AssemblyManifest, typing.Dict[builtins.str, typing.Any]],
        file_path: builtins.str,
    ) -> None:
        '''(deprecated) Deprecated.

        :param manifest: -
        :param file_path: -

        :deprecated: use ``saveAssemblyManifest()``

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__53bfd6a4d13d9da4fc98af1e035d44e848b43b9eb05e2a047c9c184f02c96dc9)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.sinvoke(cls, "save", [manifest, file_path]))

    @jsii.member(jsii_name="saveAssemblyManifest")
    @builtins.classmethod
    def save_assembly_manifest(
        cls,
        manifest: typing.Union[AssemblyManifest, typing.Dict[builtins.str, typing.Any]],
        file_path: builtins.str,
    ) -> None:
        '''(experimental) Validates and saves the cloud assembly manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2792aafd5993157bb80140e436929cebc6178d83dfe7eadf67203313bd49ae5)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.sinvoke(cls, "saveAssemblyManifest", [manifest, file_path]))

    @jsii.member(jsii_name="saveAssetManifest")
    @builtins.classmethod
    def save_asset_manifest(
        cls,
        manifest: typing.Union[AssetManifest, typing.Dict[builtins.str, typing.Any]],
        file_path: builtins.str,
    ) -> None:
        '''(experimental) Validates and saves the asset manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eb1a8c94170d30e4479c4f849dd3292a2f57058319e55030b8d60fa7a7d8a929)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.sinvoke(cls, "saveAssetManifest", [manifest, file_path]))

    @jsii.member(jsii_name="saveIntegManifest")
    @builtins.classmethod
    def save_integ_manifest(
        cls,
        manifest: typing.Union[IntegManifest, typing.Dict[builtins.str, typing.Any]],
        file_path: builtins.str,
    ) -> None:
        '''(experimental) Validates and saves the integ manifest to file.

        :param manifest: - manifest.
        :param file_path: - output file path.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3bd2315da6f244d87cb4139f718914c1addb25b339dcb06267176efea1d427f3)
            check_type(argname="argument manifest", value=manifest, expected_type=type_hints["manifest"])
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        return typing.cast(None, jsii.sinvoke(cls, "saveIntegManifest", [manifest, file_path]))

    @jsii.member(jsii_name="version")
    @builtins.classmethod
    def version(cls) -> builtins.str:
        '''(experimental) Fetch the current schema version number.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.sinvoke(cls, "version", []))


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.MetadataEntry",
    jsii_struct_bases=[],
    name_mapping={"type": "type", "data": "data", "trace": "trace"},
)
class MetadataEntry:
    def __init__(
        self,
        *,
        type: builtins.str,
        data: typing.Optional[typing.Union[builtins.str, typing.Union[FileAssetMetadataEntry, typing.Dict[builtins.str, typing.Any]], typing.Union[ContainerImageAssetMetadataEntry, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union["Tag", typing.Dict[builtins.str, typing.Any]]]]] = None,
        trace: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(experimental) A metadata entry in a cloud assembly artifact.

        :param type: (experimental) The type of the metadata entry.
        :param data: (experimental) The data. Default: - no data.
        :param trace: (experimental) A stack trace for when the entry was created. Default: - no trace.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            metadata_entry = cloud_assembly_schema.MetadataEntry(
                type="type",
            
                # the properties below are optional
                data="data",
                trace=["trace"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c2fe54c7940001232e95d22a4826fa4c17b23a00832f918a74bafd894a25d31f)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument data", value=data, expected_type=type_hints["data"])
            check_type(argname="argument trace", value=trace, expected_type=type_hints["trace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if data is not None:
            self._values["data"] = data
        if trace is not None:
            self._values["trace"] = trace

    @builtins.property
    def type(self) -> builtins.str:
        '''(experimental) The type of the metadata entry.

        :stability: experimental
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def data(
        self,
    ) -> typing.Optional[typing.Union[builtins.str, FileAssetMetadataEntry, ContainerImageAssetMetadataEntry, typing.List["Tag"]]]:
        '''(experimental) The data.

        :default: - no data.

        :stability: experimental
        '''
        result = self._values.get("data")
        return typing.cast(typing.Optional[typing.Union[builtins.str, FileAssetMetadataEntry, ContainerImageAssetMetadataEntry, typing.List["Tag"]]], result)

    @builtins.property
    def trace(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) A stack trace for when the entry was created.

        :default: - no trace.

        :stability: experimental
        '''
        result = self._values.get("trace")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MetadataEntry(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.MissingContext",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "props": "props", "provider": "provider"},
)
class MissingContext:
    def __init__(
        self,
        *,
        key: builtins.str,
        props: typing.Union[typing.Union[AmiContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[AvailabilityZonesContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[HostedZoneContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union["SSMParameterContextQuery", typing.Dict[builtins.str, typing.Any]], typing.Union["VpcContextQuery", typing.Dict[builtins.str, typing.Any]], typing.Union[EndpointServiceAvailabilityZonesContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union["LoadBalancerContextQuery", typing.Dict[builtins.str, typing.Any]], typing.Union[LoadBalancerListenerContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union["SecurityGroupContextQuery", typing.Dict[builtins.str, typing.Any]], typing.Union[KeyContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union["PluginContextQuery", typing.Dict[builtins.str, typing.Any]]],
        provider: ContextProvider,
    ) -> None:
        '''(experimental) Represents a missing piece of context.

        :param key: (experimental) The missing context key.
        :param props: (experimental) A set of provider-specific options.
        :param provider: (experimental) The provider from which we expect this context key to be obtained.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            missing_context = cloud_assembly_schema.MissingContext(
                key="key",
                props=cloud_assembly_schema.AmiContextQuery(
                    account="account",
                    filters={
                        "filters_key": ["filters"]
                    },
                    region="region",
            
                    # the properties below are optional
                    lookup_role_arn="lookupRoleArn",
                    owners=["owners"]
                ),
                provider=cloud_assembly_schema.ContextProvider.AMI_PROVIDER
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fbb5a3a8ed9c74cab3cb25d2a5c935444cecf040374f769326fd44a6a01a21a8)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "props": props,
            "provider": provider,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) The missing context key.

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def props(
        self,
    ) -> typing.Union[AmiContextQuery, AvailabilityZonesContextQuery, HostedZoneContextQuery, "SSMParameterContextQuery", "VpcContextQuery", EndpointServiceAvailabilityZonesContextQuery, "LoadBalancerContextQuery", LoadBalancerListenerContextQuery, "SecurityGroupContextQuery", KeyContextQuery, "PluginContextQuery"]:
        '''(experimental) A set of provider-specific options.

        :stability: experimental
        '''
        result = self._values.get("props")
        assert result is not None, "Required property 'props' is missing"
        return typing.cast(typing.Union[AmiContextQuery, AvailabilityZonesContextQuery, HostedZoneContextQuery, "SSMParameterContextQuery", "VpcContextQuery", EndpointServiceAvailabilityZonesContextQuery, "LoadBalancerContextQuery", LoadBalancerListenerContextQuery, "SecurityGroupContextQuery", KeyContextQuery, "PluginContextQuery"], result)

    @builtins.property
    def provider(self) -> ContextProvider:
        '''(experimental) The provider from which we expect this context key to be obtained.

        :stability: experimental
        '''
        result = self._values.get("provider")
        assert result is not None, "Required property 'provider' is missing"
        return typing.cast(ContextProvider, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MissingContext(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.NestedCloudAssemblyProperties",
    jsii_struct_bases=[],
    name_mapping={"directory_name": "directoryName", "display_name": "displayName"},
)
class NestedCloudAssemblyProperties:
    def __init__(
        self,
        *,
        directory_name: builtins.str,
        display_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Artifact properties for nested cloud assemblies.

        :param directory_name: (experimental) Relative path to the nested cloud assembly.
        :param display_name: (experimental) Display name for the cloud assembly. Default: - The artifact ID

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            nested_cloud_assembly_properties = cloud_assembly_schema.NestedCloudAssemblyProperties(
                directory_name="directoryName",
            
                # the properties below are optional
                display_name="displayName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__47c6f4765040c92065811eeed277c21fa9bed1067ddb178a6ef5d4b7860703e2)
            check_type(argname="argument directory_name", value=directory_name, expected_type=type_hints["directory_name"])
            check_type(argname="argument display_name", value=display_name, expected_type=type_hints["display_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory_name": directory_name,
        }
        if display_name is not None:
            self._values["display_name"] = display_name

    @builtins.property
    def directory_name(self) -> builtins.str:
        '''(experimental) Relative path to the nested cloud assembly.

        :stability: experimental
        '''
        result = self._values.get("directory_name")
        assert result is not None, "Required property 'directory_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def display_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Display name for the cloud assembly.

        :default: - The artifact ID

        :stability: experimental
        '''
        result = self._values.get("display_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "NestedCloudAssemblyProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.PluginContextQuery",
    jsii_struct_bases=[],
    name_mapping={"plugin_name": "pluginName"},
)
class PluginContextQuery:
    def __init__(self, *, plugin_name: builtins.str) -> None:
        '''(experimental) Query input for plugins.

        This alternate branch is necessary because it needs to be able to escape all type checking
        we do on on the cloud assembly -- we cannot know the properties that will be used a priori.

        :param plugin_name: (experimental) The name of the plugin.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            plugin_context_query = cloud_assembly_schema.PluginContextQuery(
                plugin_name="pluginName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__68ab40467f54bd40390364ba9698d22124890b45a97bd554418a75f04676b227)
            check_type(argname="argument plugin_name", value=plugin_name, expected_type=type_hints["plugin_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "plugin_name": plugin_name,
        }

    @builtins.property
    def plugin_name(self) -> builtins.str:
        '''(experimental) The name of the plugin.

        :stability: experimental
        '''
        result = self._values.get("plugin_name")
        assert result is not None, "Required property 'plugin_name' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PluginContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.cloud_assembly_schema.RequireApproval")
class RequireApproval(enum.Enum):
    '''(experimental) In what scenarios should the CLI ask for approval.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        app = App()
        
        stack_under_test = Stack(app, "StackUnderTest")
        
        stack = Stack(app, "stack")
        
        test_case = IntegTest(app, "CustomizedDeploymentWorkflow",
            test_cases=[stack_under_test],
            diff_assets=True,
            stack_update_workflow=True,
            cdk_command_options=lambda.cloud_assembly_schema.CdkCommands(
                deploy=lambda.cloud_assembly_schema.DeployCommand(
                    args=lambda.cloud_assembly_schema.DeployOptions(
                        require_approval=RequireApproval.NEVER,
                        json=True
                    )
                ),
                destroy=lambda.cloud_assembly_schema.DestroyCommand(
                    args=lambda.cloud_assembly_schema.DestroyOptions(
                        force=True
                    )
                )
            )
        )
    '''

    NEVER = "NEVER"
    '''(experimental) Never ask for approval.

    :stability: experimental
    '''
    ANYCHANGE = "ANYCHANGE"
    '''(experimental) Prompt for approval for any type  of change to the stack.

    :stability: experimental
    '''
    BROADENING = "BROADENING"
    '''(experimental) Only prompt for approval if there are security related changes.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.RuntimeInfo",
    jsii_struct_bases=[],
    name_mapping={"libraries": "libraries"},
)
class RuntimeInfo:
    def __init__(
        self,
        *,
        libraries: typing.Mapping[builtins.str, builtins.str],
    ) -> None:
        '''(experimental) Information about the application's runtime components.

        :param libraries: (experimental) The list of libraries loaded in the application, associated with their versions.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            runtime_info = cloud_assembly_schema.RuntimeInfo(
                libraries={
                    "libraries_key": "libraries"
                }
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a3409338bda06c93ef1c3a51190d9a6056e4fba9608b9390156bf81f9cc5f80)
            check_type(argname="argument libraries", value=libraries, expected_type=type_hints["libraries"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "libraries": libraries,
        }

    @builtins.property
    def libraries(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) The list of libraries loaded in the application, associated with their versions.

        :stability: experimental
        '''
        result = self._values.get("libraries")
        assert result is not None, "Required property 'libraries' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RuntimeInfo(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.SSMParameterContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "parameter_name": "parameterName",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class SSMParameterContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        parameter_name: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query to SSM Parameter Context Provider.

        :param account: (experimental) Query account.
        :param parameter_name: (experimental) Parameter name to query.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            s_sMParameter_context_query = cloud_assembly_schema.SSMParameterContextQuery(
                account="account",
                parameter_name="parameterName",
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466cc9a8785ae419ca2bc107b5a6dc6ef392bf526d5704d92be2c9422af02b96)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument parameter_name", value=parameter_name, expected_type=type_hints["parameter_name"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "parameter_name": parameter_name,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def parameter_name(self) -> builtins.str:
        '''(experimental) Parameter name to query.

        :stability: experimental
        '''
        result = self._values.get("parameter_name")
        assert result is not None, "Required property 'parameter_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SSMParameterContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.SecurityGroupContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
        "security_group_id": "securityGroupId",
        "security_group_name": "securityGroupName",
        "vpc_id": "vpcId",
    },
)
class SecurityGroupContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
        security_group_id: typing.Optional[builtins.str] = None,
        security_group_name: typing.Optional[builtins.str] = None,
        vpc_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query input for looking up a security group.

        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None
        :param security_group_id: (experimental) Security group id. Default: - None
        :param security_group_name: (experimental) Security group name. Default: - None
        :param vpc_id: (experimental) VPC ID. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            security_group_context_query = cloud_assembly_schema.SecurityGroupContextQuery(
                account="account",
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn",
                security_group_id="securityGroupId",
                security_group_name="securityGroupName",
                vpc_id="vpcId"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8b2115c05554177b7a9ed032a57901a7629ce70fb7a935f594139a51deb30c41)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
            check_type(argname="argument security_group_id", value=security_group_id, expected_type=type_hints["security_group_id"])
            check_type(argname="argument security_group_name", value=security_group_name, expected_type=type_hints["security_group_name"])
            check_type(argname="argument vpc_id", value=vpc_id, expected_type=type_hints["vpc_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn
        if security_group_id is not None:
            self._values["security_group_id"] = security_group_id
        if security_group_name is not None:
            self._values["security_group_name"] = security_group_name
        if vpc_id is not None:
            self._values["vpc_id"] = vpc_id

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) Security group id.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("security_group_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def security_group_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Security group name.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("security_group_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) VPC ID.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("vpc_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SecurityGroupContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.Tag",
    jsii_struct_bases=[],
    name_mapping={"key": "key", "value": "value"},
)
class Tag:
    def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
        '''(experimental) Metadata Entry spec for stack tag.

        :param key: (experimental) Tag key. (In the actual file on disk this will be cased as "Key", and the structure is patched to match this structure upon loading: https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)
        :param value: (experimental) Tag value. (In the actual file on disk this will be cased as "Value", and the structure is patched to match this structure upon loading: https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            tag = cloud_assembly_schema.Tag(
                key="key",
                value="value"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d20f2662570c724ec244ca64311059808596fdc6c7097d15f60d3a1fdedc7c2)
            check_type(argname="argument key", value=key, expected_type=type_hints["key"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "key": key,
            "value": value,
        }

    @builtins.property
    def key(self) -> builtins.str:
        '''(experimental) Tag key.

        (In the actual file on disk this will be cased as "Key", and the structure is
        patched to match this structure upon loading:
        https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)

        :stability: experimental
        '''
        result = self._values.get("key")
        assert result is not None, "Required property 'key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def value(self) -> builtins.str:
        '''(experimental) Tag value.

        (In the actual file on disk this will be cased as "Value", and the structure is
        patched to match this structure upon loading:
        https://github.com/aws/aws-cdk/blob/4aadaa779b48f35838cccd4e25107b2338f05547/packages/%40aws-cdk/cloud-assembly-schema/lib/manifest.ts#L137)

        :stability: experimental
        '''
        result = self._values.get("value")
        assert result is not None, "Required property 'value' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Tag(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.TestOptions",
    jsii_struct_bases=[],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
    },
)
class TestOptions:
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) The set of options to control the workflow of the test runner.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            test_options = cloud_assembly_schema.TestOptions(
                allow_destroy=["allowDestroy"],
                cdk_command_options=cloud_assembly_schema.CdkCommands(
                    deploy=cloud_assembly_schema.DeployCommand(
                        args=cloud_assembly_schema.DeployOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            change_set_name="changeSetName",
                            ci=False,
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            execute=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            notification_arns=["notificationArns"],
                            output="output",
                            outputs_file="outputsFile",
                            parameters={
                                "parameters_key": "parameters"
                            },
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                            reuse_assets=["reuseAssets"],
                            role_arn="roleArn",
                            rollback=False,
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            toolkit_stack_name="toolkitStackName",
                            trace=False,
                            use_previous_parameters=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    ),
                    destroy=cloud_assembly_schema.DestroyCommand(
                        args=cloud_assembly_schema.DestroyOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            output="output",
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            role_arn="roleArn",
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            trace=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    )
                ),
                diff_assets=False,
                hooks=cloud_assembly_schema.Hooks(
                    post_deploy=["postDeploy"],
                    post_destroy=["postDestroy"],
                    pre_deploy=["preDeploy"],
                    pre_destroy=["preDestroy"]
                ),
                regions=["regions"],
                stack_update_workflow=False
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = Hooks(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f424e01de7bc625307165fa76410bf4b13c8a5afcc615147237345f26edc80c1)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[CdkCommands]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[Hooks]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.TreeArtifactProperties",
    jsii_struct_bases=[],
    name_mapping={"file": "file"},
)
class TreeArtifactProperties:
    def __init__(self, *, file: builtins.str) -> None:
        '''(experimental) Artifact properties for the Construct Tree Artifact.

        :param file: (experimental) Filename of the tree artifact.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            tree_artifact_properties = cloud_assembly_schema.TreeArtifactProperties(
                file="file"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3688393ecfb640a030aef1c444a34c2ace6219bcac35ba4359f492bb74e84b7)
            check_type(argname="argument file", value=file, expected_type=type_hints["file"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "file": file,
        }

    @builtins.property
    def file(self) -> builtins.str:
        '''(experimental) Filename of the tree artifact.

        :stability: experimental
        '''
        result = self._values.get("file")
        assert result is not None, "Required property 'file' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TreeArtifactProperties(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.VpcContextQuery",
    jsii_struct_bases=[],
    name_mapping={
        "account": "account",
        "filter": "filter",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
        "return_asymmetric_subnets": "returnAsymmetricSubnets",
        "subnet_group_name_tag": "subnetGroupNameTag",
    },
)
class VpcContextQuery:
    def __init__(
        self,
        *,
        account: builtins.str,
        filter: typing.Mapping[builtins.str, builtins.str],
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
        return_asymmetric_subnets: typing.Optional[builtins.bool] = None,
        subnet_group_name_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query input for looking up a VPC.

        :param account: (experimental) Query account.
        :param filter: (experimental) Filters to apply to the VPC. Filter parameters are the same as passed to DescribeVpcs.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None
        :param return_asymmetric_subnets: (experimental) Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups. Default: false
        :param subnet_group_name_tag: (experimental) Optional tag for subnet group name. If not provided, we'll look at the aws-cdk:subnet-name tag. If the subnet does not have the specified tag, we'll use its type as the name. Default: 'aws-cdk:subnet-name'

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            vpc_context_query = cloud_assembly_schema.VpcContextQuery(
                account="account",
                filter={
                    "filter_key": "filter"
                },
                region="region",
            
                # the properties below are optional
                lookup_role_arn="lookupRoleArn",
                return_asymmetric_subnets=False,
                subnet_group_name_tag="subnetGroupNameTag"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__87126abc6f788a536398e855f488e93825556db9cfcf5ad70b46d0eb7f82f564)
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument filter", value=filter, expected_type=type_hints["filter"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
            check_type(argname="argument return_asymmetric_subnets", value=return_asymmetric_subnets, expected_type=type_hints["return_asymmetric_subnets"])
            check_type(argname="argument subnet_group_name_tag", value=subnet_group_name_tag, expected_type=type_hints["subnet_group_name_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "account": account,
            "filter": filter,
            "region": region,
        }
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn
        if return_asymmetric_subnets is not None:
            self._values["return_asymmetric_subnets"] = return_asymmetric_subnets
        if subnet_group_name_tag is not None:
            self._values["subnet_group_name_tag"] = subnet_group_name_tag

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def filter(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Filters to apply to the VPC.

        Filter parameters are the same as passed to DescribeVpcs.

        :see: https://docs.aws.amazon.com/AWSEC2/latest/APIReference/API_DescribeVpcs.html
        :stability: experimental
        '''
        result = self._values.get("filter")
        assert result is not None, "Required property 'filter' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def return_asymmetric_subnets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether to populate the subnetGroups field of the {@link VpcContextResponse}, which contains potentially asymmetric subnet groups.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("return_asymmetric_subnets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def subnet_group_name_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) Optional tag for subnet group name.

        If not provided, we'll look at the aws-cdk:subnet-name tag.
        If the subnet does not have the specified tag,
        we'll use its type as the name.

        :default: 'aws-cdk:subnet-name'

        :stability: experimental
        '''
        result = self._values.get("subnet_group_name_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "VpcContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.LoadBalancerContextQuery",
    jsii_struct_bases=[LoadBalancerFilter],
    name_mapping={
        "load_balancer_type": "loadBalancerType",
        "load_balancer_arn": "loadBalancerArn",
        "load_balancer_tags": "loadBalancerTags",
        "account": "account",
        "region": "region",
        "lookup_role_arn": "lookupRoleArn",
    },
)
class LoadBalancerContextQuery(LoadBalancerFilter):
    def __init__(
        self,
        *,
        load_balancer_type: LoadBalancerType,
        load_balancer_arn: typing.Optional[builtins.str] = None,
        load_balancer_tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
        account: builtins.str,
        region: builtins.str,
        lookup_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Query input for looking up a load balancer.

        :param load_balancer_type: (experimental) Filter load balancers by their type.
        :param load_balancer_arn: (experimental) Find by load balancer's ARN. Default: - does not search by load balancer arn
        :param load_balancer_tags: (experimental) Match load balancer tags. Default: - does not match load balancers by tags
        :param account: (experimental) Query account.
        :param region: (experimental) Query region.
        :param lookup_role_arn: (experimental) The ARN of the role that should be used to look up the missing values. Default: - None

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            load_balancer_context_query = cloud_assembly_schema.LoadBalancerContextQuery(
                account="account",
                load_balancer_type=cloud_assembly_schema.LoadBalancerType.NETWORK,
                region="region",
            
                # the properties below are optional
                load_balancer_arn="loadBalancerArn",
                load_balancer_tags=[cloud_assembly_schema.Tag(
                    key="key",
                    value="value"
                )],
                lookup_role_arn="lookupRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4a606c971fce244eb23ffb3725b7bb05e8f6a068c26b9be8e3fae68bff9f8a02)
            check_type(argname="argument load_balancer_type", value=load_balancer_type, expected_type=type_hints["load_balancer_type"])
            check_type(argname="argument load_balancer_arn", value=load_balancer_arn, expected_type=type_hints["load_balancer_arn"])
            check_type(argname="argument load_balancer_tags", value=load_balancer_tags, expected_type=type_hints["load_balancer_tags"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument lookup_role_arn", value=lookup_role_arn, expected_type=type_hints["lookup_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "load_balancer_type": load_balancer_type,
            "account": account,
            "region": region,
        }
        if load_balancer_arn is not None:
            self._values["load_balancer_arn"] = load_balancer_arn
        if load_balancer_tags is not None:
            self._values["load_balancer_tags"] = load_balancer_tags
        if lookup_role_arn is not None:
            self._values["lookup_role_arn"] = lookup_role_arn

    @builtins.property
    def load_balancer_type(self) -> LoadBalancerType:
        '''(experimental) Filter load balancers by their type.

        :stability: experimental
        '''
        result = self._values.get("load_balancer_type")
        assert result is not None, "Required property 'load_balancer_type' is missing"
        return typing.cast(LoadBalancerType, result)

    @builtins.property
    def load_balancer_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Find by load balancer's ARN.

        :default: - does not search by load balancer arn

        :stability: experimental
        '''
        result = self._values.get("load_balancer_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def load_balancer_tags(self) -> typing.Optional[typing.List[Tag]]:
        '''(experimental) Match load balancer tags.

        :default: - does not match load balancers by tags

        :stability: experimental
        '''
        result = self._values.get("load_balancer_tags")
        return typing.cast(typing.Optional[typing.List[Tag]], result)

    @builtins.property
    def account(self) -> builtins.str:
        '''(experimental) Query account.

        :stability: experimental
        '''
        result = self._values.get("account")
        assert result is not None, "Required property 'account' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def region(self) -> builtins.str:
        '''(experimental) Query region.

        :stability: experimental
        '''
        result = self._values.get("region")
        assert result is not None, "Required property 'region' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def lookup_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) The ARN of the role that should be used to look up the missing values.

        :default: - None

        :stability: experimental
        '''
        result = self._values.get("lookup_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LoadBalancerContextQuery(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.cloud_assembly_schema.TestCase",
    jsii_struct_bases=[TestOptions],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "stacks": "stacks",
        "assertion_stack": "assertionStack",
    },
)
class TestCase(TestOptions):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[typing.Union[CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[typing.Union[Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        stacks: typing.Sequence[builtins.str],
        assertion_stack: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Represents an integration test case.

        :param allow_destroy: (experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: (experimental) Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: (experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: (experimental) Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: (experimental) Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: (experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param stacks: (experimental) Stacks that should be tested as part of this test case The stackNames will be passed as args to the cdk commands so dependent stacks will be automatically deployed unless ``exclusively`` is passed.
        :param assertion_stack: (experimental) The name of the stack that contains assertions. Default: - no assertion stack

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import cloud_assembly_schema
            
            test_case = cloud_assembly_schema.TestCase(
                stacks=["stacks"],
            
                # the properties below are optional
                allow_destroy=["allowDestroy"],
                assertion_stack="assertionStack",
                cdk_command_options=cloud_assembly_schema.CdkCommands(
                    deploy=cloud_assembly_schema.DeployCommand(
                        args=cloud_assembly_schema.DeployOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            change_set_name="changeSetName",
                            ci=False,
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            execute=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            notification_arns=["notificationArns"],
                            output="output",
                            outputs_file="outputsFile",
                            parameters={
                                "parameters_key": "parameters"
                            },
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            require_approval=cloud_assembly_schema.RequireApproval.NEVER,
                            reuse_assets=["reuseAssets"],
                            role_arn="roleArn",
                            rollback=False,
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            toolkit_stack_name="toolkitStackName",
                            trace=False,
                            use_previous_parameters=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    ),
                    destroy=cloud_assembly_schema.DestroyCommand(
                        args=cloud_assembly_schema.DestroyOptions(
                            all=False,
                            app="app",
                            asset_metadata=False,
                            ca_bundle_path="caBundlePath",
                            color=False,
                            context={
                                "context_key": "context"
                            },
                            debug=False,
                            ec2_creds=False,
                            exclusively=False,
                            force=False,
                            ignore_errors=False,
                            json=False,
                            lookups=False,
                            notices=False,
                            output="output",
                            path_metadata=False,
                            profile="profile",
                            proxy="proxy",
                            role_arn="roleArn",
                            stacks=["stacks"],
                            staging=False,
                            strict=False,
                            trace=False,
                            verbose=False,
                            version_reporting=False
                        ),
                        enabled=False,
                        expected_message="expectedMessage",
                        expect_error=False
                    )
                ),
                diff_assets=False,
                hooks=cloud_assembly_schema.Hooks(
                    post_deploy=["postDeploy"],
                    post_destroy=["postDestroy"],
                    pre_deploy=["preDeploy"],
                    pre_destroy=["preDestroy"]
                ),
                regions=["regions"],
                stack_update_workflow=False
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = Hooks(**hooks)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e2bcb1af621bcc749988f3e214d943189bc8f00f66eaa898ec5097c721786fee)
            check_type(argname="argument allow_destroy", value=allow_destroy, expected_type=type_hints["allow_destroy"])
            check_type(argname="argument cdk_command_options", value=cdk_command_options, expected_type=type_hints["cdk_command_options"])
            check_type(argname="argument diff_assets", value=diff_assets, expected_type=type_hints["diff_assets"])
            check_type(argname="argument hooks", value=hooks, expected_type=type_hints["hooks"])
            check_type(argname="argument regions", value=regions, expected_type=type_hints["regions"])
            check_type(argname="argument stack_update_workflow", value=stack_update_workflow, expected_type=type_hints["stack_update_workflow"])
            check_type(argname="argument stacks", value=stacks, expected_type=type_hints["stacks"])
            check_type(argname="argument assertion_stack", value=assertion_stack, expected_type=type_hints["assertion_stack"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stacks": stacks,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow
        if assertion_stack is not None:
            self._values["assertion_stack"] = assertion_stack

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update

        :stability: experimental
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(self) -> typing.Optional[CdkCommands]:
        '''(experimental) Additional options to use for each CDK command.

        :default: - runner default options

        :stability: experimental
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false

        :stability: experimental
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[Hooks]:
        '''(experimental) Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks

        :stability: experimental
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Limit deployment to these regions.

        :default: - can run in any region

        :stability: experimental
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacks(self) -> typing.List[builtins.str]:
        '''(experimental) Stacks that should be tested as part of this test case The stackNames will be passed as args to the cdk commands so dependent stacks will be automatically deployed unless ``exclusively`` is passed.

        :stability: experimental
        '''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def assertion_stack(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the stack that contains assertions.

        :default: - no assertion stack

        :stability: experimental
        '''
        result = self._values.get("assertion_stack")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "TestCase(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AmiContextQuery",
    "ArtifactManifest",
    "ArtifactMetadataEntryType",
    "ArtifactType",
    "AssemblyManifest",
    "AssetManifest",
    "AssetManifestProperties",
    "AvailabilityZonesContextQuery",
    "AwsCloudFormationStackProperties",
    "AwsDestination",
    "BootstrapRole",
    "CdkCommand",
    "CdkCommands",
    "ContainerImageAssetMetadataEntry",
    "ContextProvider",
    "DefaultCdkOptions",
    "DeployCommand",
    "DeployOptions",
    "DestroyCommand",
    "DestroyOptions",
    "DockerImageAsset",
    "DockerImageDestination",
    "DockerImageSource",
    "EndpointServiceAvailabilityZonesContextQuery",
    "FileAsset",
    "FileAssetMetadataEntry",
    "FileAssetPackaging",
    "FileDestination",
    "FileSource",
    "Hooks",
    "HostedZoneContextQuery",
    "IntegManifest",
    "KeyContextQuery",
    "LoadBalancerContextQuery",
    "LoadBalancerFilter",
    "LoadBalancerListenerContextQuery",
    "LoadBalancerListenerProtocol",
    "LoadBalancerType",
    "LoadManifestOptions",
    "Manifest",
    "MetadataEntry",
    "MissingContext",
    "NestedCloudAssemblyProperties",
    "PluginContextQuery",
    "RequireApproval",
    "RuntimeInfo",
    "SSMParameterContextQuery",
    "SecurityGroupContextQuery",
    "Tag",
    "TestCase",
    "TestOptions",
    "TreeArtifactProperties",
    "VpcContextQuery",
]

publication.publish()

def _typecheckingstub__8f2a94285068509b87a6e46df77bbf8877588baa46f3d664d316eb5cd15d7911(
    *,
    account: builtins.str,
    filters: typing.Mapping[builtins.str, typing.Sequence[builtins.str]],
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
    owners: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2432006d5d04f100829a91ebe1f4bed220c293772b8d7048ecf07ba71b9af9(
    *,
    type: ArtifactType,
    dependencies: typing.Optional[typing.Sequence[builtins.str]] = None,
    display_name: typing.Optional[builtins.str] = None,
    environment: typing.Optional[builtins.str] = None,
    metadata: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[typing.Union[MetadataEntry, typing.Dict[builtins.str, typing.Any]]]]] = None,
    properties: typing.Optional[typing.Union[typing.Union[AwsCloudFormationStackProperties, typing.Dict[builtins.str, typing.Any]], typing.Union[AssetManifestProperties, typing.Dict[builtins.str, typing.Any]], typing.Union[TreeArtifactProperties, typing.Dict[builtins.str, typing.Any]], typing.Union[NestedCloudAssemblyProperties, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2b85c4f7731874e306253a41ce60384ca15cbb300d41778f681e47a3fe65b472(
    *,
    version: builtins.str,
    artifacts: typing.Optional[typing.Mapping[builtins.str, typing.Union[ArtifactManifest, typing.Dict[builtins.str, typing.Any]]]] = None,
    missing: typing.Optional[typing.Sequence[typing.Union[MissingContext, typing.Dict[builtins.str, typing.Any]]]] = None,
    runtime: typing.Optional[typing.Union[RuntimeInfo, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3f137c27eef0c5d528b8056a661fb2dd1e87a7fe7b9b631b4f2a3d34d9fcb6ab(
    *,
    version: builtins.str,
    docker_images: typing.Optional[typing.Mapping[builtins.str, typing.Union[DockerImageAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    files: typing.Optional[typing.Mapping[builtins.str, typing.Union[FileAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__387089bdef8ecbb6f514cc4ce3a76d1f595d51bda2855168a6a43b1aee7dbdae(
    *,
    file: builtins.str,
    bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
    requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__484a0ae5d95e7545a4d8aa23b962078607c6b75b66ebd14ac72f9344756da7af(
    *,
    account: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8360008dbc98119effa4cbbb84f73ccc3be2fc630e9bdfaa0e36433554394fdf(
    *,
    template_file: builtins.str,
    assume_role_arn: typing.Optional[builtins.str] = None,
    assume_role_external_id: typing.Optional[builtins.str] = None,
    bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
    cloud_formation_execution_role_arn: typing.Optional[builtins.str] = None,
    lookup_role: typing.Optional[typing.Union[BootstrapRole, typing.Dict[builtins.str, typing.Any]]] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
    stack_name: typing.Optional[builtins.str] = None,
    stack_template_asset_object_url: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    termination_protection: typing.Optional[builtins.bool] = None,
    validate_on_synth: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1933cfb6bff539b5e63360451650e4155ca2b378e2c47c4ee913043ed1a161ed(
    *,
    assume_role_arn: typing.Optional[builtins.str] = None,
    assume_role_external_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67b6ad8cbe1a229a48cb983133ececa7df5bd0c26da1da0ba401feab61aefff3(
    *,
    arn: builtins.str,
    assume_role_external_id: typing.Optional[builtins.str] = None,
    bootstrap_stack_version_ssm_parameter: typing.Optional[builtins.str] = None,
    requires_bootstrap_stack_version: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a2e3b64d564e502f88cc9aeae0f8aa504a53c55905d2249939e5b71b4538e44(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    expected_message: typing.Optional[builtins.str] = None,
    expect_error: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94b6d49787ca8183c380bd904923fc40e21152903fd019f70a0447d691732e8e(
    *,
    deploy: typing.Optional[typing.Union[DeployCommand, typing.Dict[builtins.str, typing.Any]]] = None,
    destroy: typing.Optional[typing.Union[DestroyCommand, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8bcae44b068f34e0af341c79563d929bc81c1dd1ca480d0eb4cb6b38e32380f6(
    *,
    id: builtins.str,
    packaging: builtins.str,
    path: builtins.str,
    source_hash: builtins.str,
    build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    file: typing.Optional[builtins.str] = None,
    image_name_parameter: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
    network_mode: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
    repository_name: typing.Optional[builtins.str] = None,
    target: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a7ea7ec5f9890ce22bc988e235e5f8b8364322fe6ae34349030821e8f2e43810(
    *,
    all: typing.Optional[builtins.bool] = None,
    app: typing.Optional[builtins.str] = None,
    asset_metadata: typing.Optional[builtins.bool] = None,
    ca_bundle_path: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    debug: typing.Optional[builtins.bool] = None,
    ec2_creds: typing.Optional[builtins.bool] = None,
    ignore_errors: typing.Optional[builtins.bool] = None,
    json: typing.Optional[builtins.bool] = None,
    lookups: typing.Optional[builtins.bool] = None,
    notices: typing.Optional[builtins.bool] = None,
    output: typing.Optional[builtins.str] = None,
    path_metadata: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
    staging: typing.Optional[builtins.bool] = None,
    strict: typing.Optional[builtins.bool] = None,
    trace: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
    version_reporting: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__aa9e8152bcee65bbee0162599ae487529471054cee5218ed4ebfc52da00dc6ac(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    expected_message: typing.Optional[builtins.str] = None,
    expect_error: typing.Optional[builtins.bool] = None,
    args: typing.Optional[typing.Union[DeployOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__218d47322e5c35ac480e1d317ee9da5f5250ad3b7905cbea9c6fdbc588d73fa7(
    *,
    all: typing.Optional[builtins.bool] = None,
    app: typing.Optional[builtins.str] = None,
    asset_metadata: typing.Optional[builtins.bool] = None,
    ca_bundle_path: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    debug: typing.Optional[builtins.bool] = None,
    ec2_creds: typing.Optional[builtins.bool] = None,
    ignore_errors: typing.Optional[builtins.bool] = None,
    json: typing.Optional[builtins.bool] = None,
    lookups: typing.Optional[builtins.bool] = None,
    notices: typing.Optional[builtins.bool] = None,
    output: typing.Optional[builtins.str] = None,
    path_metadata: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
    staging: typing.Optional[builtins.bool] = None,
    strict: typing.Optional[builtins.bool] = None,
    trace: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
    version_reporting: typing.Optional[builtins.bool] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    ci: typing.Optional[builtins.bool] = None,
    exclusively: typing.Optional[builtins.bool] = None,
    execute: typing.Optional[builtins.bool] = None,
    force: typing.Optional[builtins.bool] = None,
    notification_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    outputs_file: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    require_approval: typing.Optional[RequireApproval] = None,
    reuse_assets: typing.Optional[typing.Sequence[builtins.str]] = None,
    rollback: typing.Optional[builtins.bool] = None,
    toolkit_stack_name: typing.Optional[builtins.str] = None,
    use_previous_parameters: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f703a7f4a1ad8887fb5a7e86baa2e101dcdb823fc437ba4d0d28adbe8134b7d4(
    *,
    enabled: typing.Optional[builtins.bool] = None,
    expected_message: typing.Optional[builtins.str] = None,
    expect_error: typing.Optional[builtins.bool] = None,
    args: typing.Optional[typing.Union[DestroyOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fe413e27463eb24cbad97073db059059c3dd4e70317ceaa323e9b7e3718c10c(
    *,
    all: typing.Optional[builtins.bool] = None,
    app: typing.Optional[builtins.str] = None,
    asset_metadata: typing.Optional[builtins.bool] = None,
    ca_bundle_path: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.bool] = None,
    context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    debug: typing.Optional[builtins.bool] = None,
    ec2_creds: typing.Optional[builtins.bool] = None,
    ignore_errors: typing.Optional[builtins.bool] = None,
    json: typing.Optional[builtins.bool] = None,
    lookups: typing.Optional[builtins.bool] = None,
    notices: typing.Optional[builtins.bool] = None,
    output: typing.Optional[builtins.str] = None,
    path_metadata: typing.Optional[builtins.bool] = None,
    profile: typing.Optional[builtins.str] = None,
    proxy: typing.Optional[builtins.str] = None,
    role_arn: typing.Optional[builtins.str] = None,
    stacks: typing.Optional[typing.Sequence[builtins.str]] = None,
    staging: typing.Optional[builtins.bool] = None,
    strict: typing.Optional[builtins.bool] = None,
    trace: typing.Optional[builtins.bool] = None,
    verbose: typing.Optional[builtins.bool] = None,
    version_reporting: typing.Optional[builtins.bool] = None,
    exclusively: typing.Optional[builtins.bool] = None,
    force: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a058bb5ca7e30fd740d2f099779a473d25b9af3acd7fcd93b8fdecc9a7381c2d(
    *,
    destinations: typing.Mapping[builtins.str, typing.Union[DockerImageDestination, typing.Dict[builtins.str, typing.Any]]],
    source: typing.Union[DockerImageSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e124c79400a0a76e2c2bd2f467f4bfc6fa0c435c459ebd7eb06bd9db57d6897(
    *,
    assume_role_arn: typing.Optional[builtins.str] = None,
    assume_role_external_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    image_tag: builtins.str,
    repository_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__104edb7ee38860ee04a1fde6703c74c5815f414ceb63086ff228f8ca4b34a9bc(
    *,
    directory: typing.Optional[builtins.str] = None,
    docker_build_args: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    docker_build_target: typing.Optional[builtins.str] = None,
    docker_file: typing.Optional[builtins.str] = None,
    executable: typing.Optional[typing.Sequence[builtins.str]] = None,
    network_mode: typing.Optional[builtins.str] = None,
    platform: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__61789c9f65bf8cbf7c0f744a3aaa5f93aa65164be9576583fd2bb9561e9450e1(
    *,
    account: builtins.str,
    region: builtins.str,
    service_name: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a43b845fc9b5119ae995164ceb987384abea2587c952dc4ec9023ca057a702dc(
    *,
    destinations: typing.Mapping[builtins.str, typing.Union[FileDestination, typing.Dict[builtins.str, typing.Any]]],
    source: typing.Union[FileSource, typing.Dict[builtins.str, typing.Any]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2459ad59dfbc1ef3868ee67e7fd1da30ce9cc0907258260abecd2114c24d9ca4(
    *,
    artifact_hash_parameter: builtins.str,
    id: builtins.str,
    packaging: builtins.str,
    path: builtins.str,
    s3_bucket_parameter: builtins.str,
    s3_key_parameter: builtins.str,
    source_hash: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__480c6a6ac88167c38aa2fee76f5a82756a7ae673810ae852380ebd9ca7536537(
    *,
    assume_role_arn: typing.Optional[builtins.str] = None,
    assume_role_external_id: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    bucket_name: builtins.str,
    object_key: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f951c5369c28990fc35ca311fe7d7d4af410301a880bf4a3b91bd666dfed6476(
    *,
    executable: typing.Optional[typing.Sequence[builtins.str]] = None,
    packaging: typing.Optional[FileAssetPackaging] = None,
    path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__910fdf7f70801aee3e341900ae5774a4b8ae93545d58996faaecef06bada8e4c(
    *,
    post_deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
    post_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_deploy: typing.Optional[typing.Sequence[builtins.str]] = None,
    pre_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7f67a4a8a0193498879ad71d01f369e35e92cbdeb3a1b1ecb87b8d2e6d857a1d(
    *,
    account: builtins.str,
    domain_name: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
    private_zone: typing.Optional[builtins.bool] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4f9fe52a44507be12304f6e9783c36b8d643163178af5d0d7188d7e2e7196e8(
    *,
    test_cases: typing.Mapping[builtins.str, typing.Union[TestCase, typing.Dict[builtins.str, typing.Any]]],
    version: builtins.str,
    enable_lookups: typing.Optional[builtins.bool] = None,
    synth_context: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d7ee6469151c451820b41eb1f38f20269d2d84fdcbd30e2d240d47028f768e7f(
    *,
    account: builtins.str,
    alias_name: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__38c5568223c5face9dcf7c7da7bafb4fe4f911e234a66832dac4ab9968d65b9f(
    *,
    load_balancer_type: LoadBalancerType,
    load_balancer_arn: typing.Optional[builtins.str] = None,
    load_balancer_tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ce1111745c92a8dde1c598d93b77da6716573ad8de29c30f000a3815b978727e(
    *,
    load_balancer_type: LoadBalancerType,
    load_balancer_arn: typing.Optional[builtins.str] = None,
    load_balancer_tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: builtins.str,
    region: builtins.str,
    listener_arn: typing.Optional[builtins.str] = None,
    listener_port: typing.Optional[jsii.Number] = None,
    listener_protocol: typing.Optional[LoadBalancerListenerProtocol] = None,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__356e2b51b940724005f4d816b60902c571d28579650fc00dc287283c2c83f88c(
    *,
    skip_enum_check: typing.Optional[builtins.bool] = None,
    skip_version_check: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__078e52672b5074804e1112222ee4da699db48d2a060886035e384130eb111d75(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c05faad83b24dfdb41efdaebc292291c68f49b6f211778f7dbccc93d158cb9d3(
    file_path: builtins.str,
    *,
    skip_enum_check: typing.Optional[builtins.bool] = None,
    skip_version_check: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d4c0d3d26f8774b5c5122edbc2e8ee5bc73d0dd26743265038e81a1151420f1(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bcc032aa406e5c3e313713dc9d6bd3f7e9caa9dfe8f510f1148886716574c7f(
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__53bfd6a4d13d9da4fc98af1e035d44e848b43b9eb05e2a047c9c184f02c96dc9(
    manifest: typing.Union[AssemblyManifest, typing.Dict[builtins.str, typing.Any]],
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2792aafd5993157bb80140e436929cebc6178d83dfe7eadf67203313bd49ae5(
    manifest: typing.Union[AssemblyManifest, typing.Dict[builtins.str, typing.Any]],
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eb1a8c94170d30e4479c4f849dd3292a2f57058319e55030b8d60fa7a7d8a929(
    manifest: typing.Union[AssetManifest, typing.Dict[builtins.str, typing.Any]],
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3bd2315da6f244d87cb4139f718914c1addb25b339dcb06267176efea1d427f3(
    manifest: typing.Union[IntegManifest, typing.Dict[builtins.str, typing.Any]],
    file_path: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c2fe54c7940001232e95d22a4826fa4c17b23a00832f918a74bafd894a25d31f(
    *,
    type: builtins.str,
    data: typing.Optional[typing.Union[builtins.str, typing.Union[FileAssetMetadataEntry, typing.Dict[builtins.str, typing.Any]], typing.Union[ContainerImageAssetMetadataEntry, typing.Dict[builtins.str, typing.Any]], typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]]] = None,
    trace: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fbb5a3a8ed9c74cab3cb25d2a5c935444cecf040374f769326fd44a6a01a21a8(
    *,
    key: builtins.str,
    props: typing.Union[typing.Union[AmiContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[AvailabilityZonesContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[HostedZoneContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[SSMParameterContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[VpcContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[EndpointServiceAvailabilityZonesContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[LoadBalancerContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[LoadBalancerListenerContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[SecurityGroupContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[KeyContextQuery, typing.Dict[builtins.str, typing.Any]], typing.Union[PluginContextQuery, typing.Dict[builtins.str, typing.Any]]],
    provider: ContextProvider,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__47c6f4765040c92065811eeed277c21fa9bed1067ddb178a6ef5d4b7860703e2(
    *,
    directory_name: builtins.str,
    display_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__68ab40467f54bd40390364ba9698d22124890b45a97bd554418a75f04676b227(
    *,
    plugin_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a3409338bda06c93ef1c3a51190d9a6056e4fba9608b9390156bf81f9cc5f80(
    *,
    libraries: typing.Mapping[builtins.str, builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466cc9a8785ae419ca2bc107b5a6dc6ef392bf526d5704d92be2c9422af02b96(
    *,
    account: builtins.str,
    parameter_name: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8b2115c05554177b7a9ed032a57901a7629ce70fb7a935f594139a51deb30c41(
    *,
    account: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
    security_group_id: typing.Optional[builtins.str] = None,
    security_group_name: typing.Optional[builtins.str] = None,
    vpc_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d20f2662570c724ec244ca64311059808596fdc6c7097d15f60d3a1fdedc7c2(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f424e01de7bc625307165fa76410bf4b13c8a5afcc615147237345f26edc80c1(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3688393ecfb640a030aef1c444a34c2ace6219bcac35ba4359f492bb74e84b7(
    *,
    file: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__87126abc6f788a536398e855f488e93825556db9cfcf5ad70b46d0eb7f82f564(
    *,
    account: builtins.str,
    filter: typing.Mapping[builtins.str, builtins.str],
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
    return_asymmetric_subnets: typing.Optional[builtins.bool] = None,
    subnet_group_name_tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a606c971fce244eb23ffb3725b7bb05e8f6a068c26b9be8e3fae68bff9f8a02(
    *,
    load_balancer_type: LoadBalancerType,
    load_balancer_arn: typing.Optional[builtins.str] = None,
    load_balancer_tags: typing.Optional[typing.Sequence[typing.Union[Tag, typing.Dict[builtins.str, typing.Any]]]] = None,
    account: builtins.str,
    region: builtins.str,
    lookup_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e2bcb1af621bcc749988f3e214d943189bc8f00f66eaa898ec5097c721786fee(
    *,
    allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_command_options: typing.Optional[typing.Union[CdkCommands, typing.Dict[builtins.str, typing.Any]]] = None,
    diff_assets: typing.Optional[builtins.bool] = None,
    hooks: typing.Optional[typing.Union[Hooks, typing.Dict[builtins.str, typing.Any]]] = None,
    regions: typing.Optional[typing.Sequence[builtins.str]] = None,
    stack_update_workflow: typing.Optional[builtins.bool] = None,
    stacks: typing.Sequence[builtins.str],
    assertion_stack: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
