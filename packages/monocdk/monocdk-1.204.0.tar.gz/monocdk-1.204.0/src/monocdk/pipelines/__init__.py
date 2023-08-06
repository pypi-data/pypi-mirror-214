'''
# CDK Pipelines

A construct library for painless Continuous Delivery of CDK applications.

CDK Pipelines is an *opinionated construct library*. It is purpose-built to
deploy one or more copies of your CDK applications using CloudFormation with a
minimal amount of effort on your part. It is *not* intended to support arbitrary
deployment pipelines, and very specifically it is not built to use CodeDeploy to
applications to instances, or deploy your custom-built ECR images to an ECS
cluster directly: use CDK file assets with CloudFormation Init for instances, or
CDK container assets for ECS clusters instead.

Give the CDK Pipelines way of doing things a shot first: you might find it does
everything you need. If you want or need more control, we recommend you drop
down to using the `aws-codepipeline` construct library directly.

> This module contains two sets of APIs: an **original** and a **modern** version of
> CDK Pipelines. The *modern* API has been updated to be easier to work with and
> customize, and will be the preferred API going forward. The *original* version
> of the API is still available for backwards compatibility, but we recommend migrating
> to the new version if possible.
>
> Compared to the original API, the modern API: has more sensible defaults; is
> more flexible; supports parallel deployments; supports multiple synth inputs;
> allows more control of CodeBuild project generation; supports deployment
> engines other than CodePipeline.
>
> The README for the original API, as well as a migration guide, can be found in [our GitHub repository](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/pipelines/ORIGINAL_API.md).

## At a glance

Deploying your application continuously starts by defining a
`MyApplicationStage`, a subclass of `Stage` that contains the stacks that make
up a single copy of your application.

You then define a `Pipeline`, instantiate as many instances of
`MyApplicationStage` as you want for your test and production environments, with
different parameters for each, and calling `pipeline.addStage()` for each of
them. You can deploy to the same account and Region, or to a different one,
with the same amount of code. The *CDK Pipelines* library takes care of the
details.

CDK Pipelines supports multiple *deployment engines* (see
[Using a different deployment engine](#using-a-different-deployment-engine)),
and comes with a deployment engine that deploys CDK apps using AWS CodePipeline.
To use the CodePipeline engine, define a `CodePipeline` construct.  The following
example creates a CodePipeline that deploys an application from GitHub:

```python
# The stacks for our app are minimally defined here.  The internals of these
# stacks aren't important, except that DatabaseStack exposes an attribute
# "table" for a database table it defines, and ComputeStack accepts a reference
# to this table in its properties.
#
class DatabaseStack(Stack):

    def __init__(self, scope, id):
        super().__init__(scope, id)
        self.table = dynamodb.Table(self, "Table",
            partition_key=cdk.aws_dynamodb.Attribute(name="id", type=dynamodb.AttributeType.STRING)
        )

class ComputeStack(Stack):
    def __init__(self, scope, id, *, table):
        super().__init__(scope, id)

#
# Stack to hold the pipeline
#
class MyPipelineStack(Stack):
    def __init__(self, scope, id, *, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        pipeline = pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.ShellStep("Synth",
                # Use a connection created using the AWS console to authenticate to GitHub
                # Other sources are available.
                input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["npm ci", "npm run build", "npx cdk synth"
                ]
            )
        )

        # 'MyApplication' is defined below. Call `addStage` as many times as
        # necessary with any account and region (may be different from the
        # pipeline's).
        pipeline.add_stage(MyApplication(self, "Prod",
            env=cdk.Environment(
                account="123456789012",
                region="eu-west-1"
            )
        ))

#
# Your application
#
# May consist of one or more Stacks (here, two)
#
# By declaring our DatabaseStack and our ComputeStack inside a Stage,
# we make sure they are deployed together, or not at all.
#
class MyApplication(Stage):
    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)

        db_stack = DatabaseStack(self, "Database")
        ComputeStack(self, "Compute",
            table=db_stack.table
        )

# In your main file
MyPipelineStack(self, "PipelineStack",
    env=cdk.Environment(
        account="123456789012",
        region="eu-west-1"
    )
)
```

The pipeline is **self-mutating**, which means that if you add new
application stages in the source code, or new stacks to `MyApplication`, the
pipeline will automatically reconfigure itself to deploy those new stages and
stacks.

(Note that you have to *bootstrap* all environments before the above code
will work, and switch on "Modern synthesis" if you are using
CDKv1. See the section **CDK Environment Bootstrapping** below for
more information).

## Provisioning the pipeline

To provision the pipeline you have defined, make sure the target environment
has been bootstrapped (see below), and then execute deploying the
`PipelineStack` *once*. Afterwards, the pipeline will keep itself up-to-date.

> **Important**: be sure to `git commit` and `git push` before deploying the
> Pipeline stack using `cdk deploy`!
>
> The reason is that the pipeline will start deploying and self-mutating
> right away based on the sources in the repository, so the sources it finds
> in there should be the ones you want it to find.

Run the following commands to get the pipeline going:

```console
$ git commit -a
$ git push
$ cdk deploy PipelineStack
```

Administrative permissions to the account are only necessary up until
this point. We recommend you remove access to these credentials after doing this.

### Working on the pipeline

The self-mutation feature of the Pipeline might at times get in the way
of the pipeline development workflow. Each change to the pipeline must be pushed
to git, otherwise, after the pipeline was updated using `cdk deploy`, it will
automatically revert to the state found in git.

To make the development more convenient, the self-mutation feature can be turned
off temporarily, by passing `selfMutation: false` property, example:

```python
# Modern API
modern_pipeline = pipelines.CodePipeline(self, "Pipeline",
    self_mutation=False,
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"
        ]
    )
)

# Original API
cloud_assembly_artifact = codepipeline.Artifact()
original_pipeline = pipelines.CdkPipeline(self, "Pipeline",
    self_mutating=False,
    cloud_assembly_artifact=cloud_assembly_artifact
)
```

## Definining the pipeline

This section of the documentation describes the AWS CodePipeline engine,
which comes with this library. If you want to use a different deployment
engine, read the section
[Using a different deployment engine](#using-a-different-deployment-engine)below.

### Synth and sources

To define a pipeline, instantiate a `CodePipeline` construct from the
`@aws-cdk/pipelines` module. It takes one argument, a `synth` step, which is
expected to produce the CDK Cloud Assembly as its single output (the contents of
the `cdk.out` directory after running `cdk synth`). "Steps" are arbitrary
actions in the pipeline, typically used to run scripts or commands.

For the synth, use a `ShellStep` and specify the commands necessary to install
dependencies, the CDK CLI, build your project and run `cdk synth`; the specific
commands required will depend on the programming language you are using. For a
typical NPM-based project, the synth will look like this:

```python
# source: pipelines.IFileSetProducer
# the repository source

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["npm ci", "npm run build", "npx cdk synth"
        ]
    )
)
```

The pipeline assumes that your `ShellStep` will produce a `cdk.out`
directory in the root, containing the CDK cloud assembly. If your
CDK project lives in a subdirectory, be sure to adjust the
`primaryOutputDirectory` to match:

```python
# source: pipelines.IFileSetProducer
# the repository source

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["cd mysubdir", "npm ci", "npm run build", "npx cdk synth"
        ],
        primary_output_directory="mysubdir/cdk.out"
    )
)
```

The underlying `@aws-cdk/aws-codepipeline.Pipeline` construct will be produced
when `app.synth()` is called. You can also force it to be produced
earlier by calling `pipeline.buildPipeline()`. After you've called
that method, you can inspect the constructs that were produced by
accessing the properties of the `pipeline` object.

#### Commands for other languages and package managers

The commands you pass to `new ShellStep` will be very similar to the commands
you run on your own workstation to install dependencies and synth your CDK
project. Here are some (non-exhaustive) examples for what those commands might
look like in a number of different situations.

For Yarn, the install commands are different:

```python
# source: pipelines.IFileSetProducer
# the repository source

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["yarn install --frozen-lockfile", "yarn build", "npx cdk synth"
        ]
    )
)
```

For Python projects, remember to install the CDK CLI globally (as
there is no `package.json` to automatically install it for you):

```python
# source: pipelines.IFileSetProducer
# the repository source

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["pip install -r requirements.txt", "npm install -g aws-cdk", "cdk synth"
        ]
    )
)
```

For Java projects, remember to install the CDK CLI globally (as
there is no `package.json` to automatically install it for you),
and the Maven compilation step is automatically executed for you
as you run `cdk synth`:

```python
# source: pipelines.IFileSetProducer
# the repository source

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["npm install -g aws-cdk", "cdk synth"
        ]
    )
)
```

You can adapt these examples to your own situation.

#### Migrating from buildspec.yml files

You may currently have the build instructions for your CodeBuild Projects in a
`buildspec.yml` file in your source repository. In addition to your build
commands, the CodeBuild Project's buildspec also controls some information that
CDK Pipelines manages for you, like artifact identifiers, input artifact
locations, Docker authorization, and exported variables.

Since there is no way in general for CDK Pipelines to modify the file in your
resource repository, CDK Pipelines configures the BuildSpec directly on the
CodeBuild Project, instead of loading it from the `buildspec.yml` file.
This requires a pipeline self-mutation to update.

To avoid this, put your build instructions in a separate script, for example
`build.sh`, and call that script from the build `commands` array:

```python
# source: pipelines.IFileSetProducer


pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=source,
        commands=["./build.sh"
        ]
    )
)
```

Doing so keeps your exact build instructions in sync with your source code in
the source repository where it belongs, and provides a convenient build script
for developers at the same time.

#### CodePipeline Sources

In CodePipeline, *Sources* define where the source of your application lives.
When a change to the source is detected, the pipeline will start executing.
Source objects can be created by factory methods on the `CodePipelineSource` class:

##### GitHub, GitHub Enterprise, BitBucket using a connection

The recommended way of connecting to GitHub or BitBucket is by using a *connection*.
You will first use the AWS Console to authenticate to the source control
provider, and then use the connection ARN in your pipeline definition:

```python
pipelines.CodePipelineSource.connection("org/repo", "branch",
    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
)
```

##### GitHub using OAuth

You can also authenticate to GitHub using a personal access token. This expects
that you've created a personal access token and stored it in Secrets Manager.
By default, the source object will look for a secret named **github-token**, but
you can change the name. The token should have the **repo** and **admin:repo_hook**
scopes.

```python
pipelines.CodePipelineSource.git_hub("org/repo", "branch",
    # This is optional
    authentication=cdk.SecretValue.secrets_manager("my-token")
)
```

##### CodeCommit

You can use a CodeCommit repository as the source. Either create or import
that the CodeCommit repository and then use `CodePipelineSource.codeCommit`
to reference it:

```python
repository = codecommit.Repository.from_repository_name(self, "Repository", "my-repository")
pipelines.CodePipelineSource.code_commit(repository, "main")
```

##### S3

You can use a zip file in S3 as the source of the pipeline. The pipeline will be
triggered every time the file in S3 is changed:

```python
bucket = s3.Bucket.from_bucket_name(self, "Bucket", "my-bucket")
pipelines.CodePipelineSource.s3(bucket, "my/source.zip")
```

##### ECR

You can use a Docker image in ECR as the source of the pipeline. The pipeline will be
triggered every time an image is pushed to ECR:

```python
repository = ecr.Repository(self, "Repository")
pipelines.CodePipelineSource.ecr(repository)
```

#### Additional inputs

`ShellStep` allows passing in more than one input: additional
inputs will be placed in the directories you specify. Any step that produces an
output file set can be used as an input, such as a `CodePipelineSource`, but
also other `ShellStep`:

```python
prebuild = pipelines.ShellStep("Prebuild",
    input=pipelines.CodePipelineSource.git_hub("myorg/repo1", "main"),
    primary_output_directory="./build",
    commands=["./build.sh"]
)

pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.git_hub("myorg/repo2", "main"),
        additional_inputs={
            "subdir": pipelines.CodePipelineSource.git_hub("myorg/repo3", "main"),
            "../siblingdir": prebuild
        },

        commands=["./build.sh"]
    )
)
```

### CDK application deployments

After you have defined the pipeline and the `synth` step, you can add one or
more CDK `Stages` which will be deployed to their target environments. To do
so, call `pipeline.addStage()` on the Stage object:

```python
# pipeline: pipelines.CodePipeline

# Do this as many times as necessary with any account and region
# Account and region may different from the pipeline's.
pipeline.add_stage(MyApplicationStage(self, "Prod",
    env=cdk.Environment(
        account="123456789012",
        region="eu-west-1"
    )
))
```

CDK Pipelines will automatically discover all `Stacks` in the given `Stage`
object, determine their dependency order, and add appropriate actions to the
pipeline to publish the assets referenced in those stacks and deploy the stacks
in the right order.

If the `Stacks` are targeted at an environment in a different AWS account or
Region and that environment has been
[bootstrapped](https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html)
, CDK Pipelines will transparently make sure the IAM roles are set up
correctly and any requisite replication Buckets are created.

#### Deploying in parallel

By default, all applications added to CDK Pipelines by calling `addStage()` will
be deployed in sequence, one after the other. If you have a lot of stages, you can
speed up the pipeline by choosing to deploy some stages in parallel. You do this
by calling `addWave()` instead of `addStage()`: a *wave* is a set of stages that
are all deployed in parallel instead of sequentially. Waves themselves are still
deployed in sequence. For example, the following will deploy two copies of your
application to `eu-west-1` and `eu-central-1` in parallel:

```python
# pipeline: pipelines.CodePipeline

europe_wave = pipeline.add_wave("Europe")
europe_wave.add_stage(MyApplicationStage(self, "Ireland",
    env=cdk.Environment(region="eu-west-1")
))
europe_wave.add_stage(MyApplicationStage(self, "Germany",
    env=cdk.Environment(region="eu-central-1")
))
```

#### Deploying to other accounts / encrypting the Artifact Bucket

CDK Pipelines can transparently deploy to other Regions and other accounts
(provided those target environments have been
[*bootstrapped*](https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html)).
However, deploying to another account requires one additional piece of
configuration: you need to enable `crossAccountKeys: true` when creating the
pipeline.

This will encrypt the artifact bucket(s), but incurs a cost for maintaining the
KMS key.

Example:

```python
pipeline = pipelines.CodePipeline(self, "Pipeline",
    # Encrypt artifacts, required for cross-account deployments
    cross_account_keys=True,
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"
        ]
    )
)
```

### Validation

Every `addStage()` and `addWave()` command takes additional options. As part of these options,
you can specify `pre` and `post` steps, which are arbitrary steps that run before or after
the contents of the stage or wave, respectively. You can use these to add validations like
manual or automated gates to your pipeline. We recommend putting manual approval gates in the set of `pre` steps, and automated approval gates in
the set of `post` steps.

The following example shows both an automated approval in the form of a `ShellStep`, and
a manual approval in the form of a `ManualApprovalStep` added to the pipeline. Both must
pass in order to promote from the `PreProd` to the `Prod` environment:

```python
# pipeline: pipelines.CodePipeline

preprod = MyApplicationStage(self, "PreProd")
prod = MyApplicationStage(self, "Prod")

pipeline.add_stage(preprod,
    post=[
        pipelines.ShellStep("Validate Endpoint",
            commands=["curl -Ssf https://my.webservice.com/"]
        )
    ]
)
pipeline.add_stage(prod,
    pre=[
        pipelines.ManualApprovalStep("PromoteToProd")
    ]
)
```

You can also specify steps to be executed at the stack level. To achieve this, you can specify the stack and step via the `stackSteps` property:

```python
# pipeline: pipelines.CodePipeline
class MyStacksStage(Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        self.stack1 = Stack(self, "stack1")
        self.stack2 = Stack(self, "stack2")
prod = MyStacksStage(self, "Prod")

pipeline.add_stage(prod,
    stack_steps=[cdk.pipelines.StackSteps(
        stack=prod.stack1,
        pre=[pipelines.ManualApprovalStep("Pre-Stack Check")],  # Executed before stack is prepared
        change_set=[pipelines.ManualApprovalStep("ChangeSet Approval")],  # Executed after stack is prepared but before the stack is deployed
        post=[pipelines.ManualApprovalStep("Post-Deploy Check")]
    ), cdk.pipelines.StackSteps(
        stack=prod.stack2,
        post=[pipelines.ManualApprovalStep("Post-Deploy Check")]
    )]
)
```

If you specify multiple steps, they will execute in parallel by default. You can add dependencies between them
to if you wish to specify an order. To add a dependency, call `step.addStepDependency()`:

```python
first_step = pipelines.ManualApprovalStep("A")
second_step = pipelines.ManualApprovalStep("B")
second_step.add_step_dependency(first_step)
```

For convenience, `Step.sequence()` will take an array of steps and dependencies between adjacent steps,
so that the whole list executes in order:

```python
# Step A will depend on step B and step B will depend on step C
ordered_steps = pipelines.Step.sequence([
    pipelines.ManualApprovalStep("A"),
    pipelines.ManualApprovalStep("B"),
    pipelines.ManualApprovalStep("C")
])
```

#### Using CloudFormation Stack Outputs in approvals

Because many CloudFormation deployments result in the generation of resources with unpredictable
names, validations have support for reading back CloudFormation Outputs after a deployment. This
makes it possible to pass (for example) the generated URL of a load balancer to the test set.

To use Stack Outputs, expose the `CfnOutput` object you're interested in, and
pass it to `envFromCfnOutputs` of the `ShellStep`:

```python
# pipeline: pipelines.CodePipeline
class MyOutputStage(Stage):

    def __init__(self, scope, id, *, env=None, outdir=None):
        super().__init__(scope, id, env=env, outdir=outdir)
        self.load_balancer_address = CfnOutput(self, "Output", value="value")

lb_app = MyOutputStage(self, "MyApp")
pipeline.add_stage(lb_app,
    post=[
        pipelines.ShellStep("HitEndpoint",
            env_from_cfn_outputs={
                # Make the load balancer address available as $URL inside the commands
                "URL": lb_app.load_balancer_address
            },
            commands=["curl -Ssf $URL"]
        )
    ]
)
```

#### Running scripts compiled during the synth step

As part of a validation, you probably want to run a test suite that's more
elaborate than what can be expressed in a couple of lines of shell script.
You can bring additional files into the shell script validation by supplying
the `input` or `additionalInputs` property of `ShellStep`. The input can
be produced by the `Synth` step, or come from a source or any other build
step.

Here's an example that captures an additional output directory in the synth
step and runs tests from there:

```python
# synth: pipelines.ShellStep

stage = MyApplicationStage(self, "MyApplication")
pipeline = pipelines.CodePipeline(self, "Pipeline", synth=synth)

pipeline.add_stage(stage,
    post=[
        pipelines.ShellStep("Approve",
            # Use the contents of the 'integ' directory from the synth step as the input
            input=synth.add_output_directory("integ"),
            commands=["cd integ && ./run.sh"]
        )
    ]
)
```

### Customizing CodeBuild Projects

CDK pipelines will generate CodeBuild projects for each `ShellStep` you use, and it
will also generate CodeBuild projects to publish assets and perform the self-mutation
of the pipeline. To control the various aspects of the CodeBuild projects that get
generated, use a `CodeBuildStep` instead of a `ShellStep`. This class has a number
of properties that allow you to customize various aspects of the projects:

```python
# vpc: ec2.Vpc
# my_security_group: ec2.SecurityGroup

pipelines.CodeBuildStep("Synth",
    # ...standard ShellStep props...
    commands=[],
    env={},

    # If you are using a CodeBuildStep explicitly, set the 'cdk.out' directory
    # to be the synth step's output.
    primary_output_directory="cdk.out",

    # Control the name of the project
    project_name="MyProject",

    # Control parts of the BuildSpec other than the regular 'build' and 'install' commands
    partial_build_spec=codebuild.BuildSpec.from_object({
        "version": "0.2"
    }),

    # Control the build environment
    build_environment=cdk.aws_codebuild.BuildEnvironment(
        compute_type=codebuild.ComputeType.LARGE
    ),
    timeout=Duration.minutes(90),

    # Control Elastic Network Interface creation
    vpc=vpc,
    subnet_selection=cdk.aws_ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
    security_groups=[my_security_group],

    # Additional policy statements for the execution role
    role_policy_statements=[
        iam.PolicyStatement()
    ]
)
```

You can also configure defaults for *all* CodeBuild projects by passing `codeBuildDefaults`,
or just for the synth, asset publishing, and self-mutation projects by passing `synthCodeBuildDefaults`,
`assetPublishingCodeBuildDefaults`, or `selfMutationCodeBuildDefaults`:

```python
# vpc: ec2.Vpc
# my_security_group: ec2.SecurityGroup

pipelines.CodePipeline(self, "Pipeline",
    # Standard CodePipeline properties
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"
        ]
    ),

    # Defaults for all CodeBuild projects
    code_build_defaults=cdk.pipelines.CodeBuildOptions(
        # Prepend commands and configuration to all projects
        partial_build_spec=codebuild.BuildSpec.from_object({
            "version": "0.2"
        }),

        # Control the build environment
        build_environment=cdk.aws_codebuild.BuildEnvironment(
            compute_type=codebuild.ComputeType.LARGE
        ),

        # Control Elastic Network Interface creation
        vpc=vpc,
        subnet_selection=cdk.aws_ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
        security_groups=[my_security_group],

        # Additional policy statements for the execution role
        role_policy=[
            iam.PolicyStatement()
        ]
    ),

    synth_code_build_defaults=cdk.pipelines.CodeBuildOptions(),
    asset_publishing_code_build_defaults=cdk.pipelines.CodeBuildOptions(),
    self_mutation_code_build_defaults=cdk.pipelines.CodeBuildOptions()
)
```

### Arbitrary CodePipeline actions

If you want to add a type of CodePipeline action to the CDK Pipeline that
doesn't have a matching class yet, you can define your own step class that extends
`Step` and implements `ICodePipelineActionFactory`.

Here's an example that adds a Jenkins step:

```python
class MyJenkinsStep(pipelines.Steppipelines.ICodePipelineActionFactory):
    def __init__(self, provider, input):
        super().__init__("MyJenkinsStep")

        # This is necessary if your step accepts parametres, like environment variables,
        # that may contain outputs from other steps. It doesn't matter what the
        # structure is, as long as it contains the values that may contain outputs.
        self.discover_referenced_outputs({
            "env": {}
        })

    def produce_action(self, stage, *, scope, actionName, runOrder, variablesNamespace=None, artifacts, fallbackArtifact=None, pipeline, codeBuildDefaults=None, beforeSelfMutation=None):

        # This is where you control what type of Action gets added to the
        # CodePipeline
        stage.add_action(cpactions.JenkinsAction(
            # Copy 'actionName' and 'runOrder' from the options
            action_name=action_name,
            run_order=run_order,

            # Jenkins-specific configuration
            type=cpactions.JenkinsActionType.TEST,
            jenkins_provider=self.provider,
            project_name="MyJenkinsProject",

            # Translate the FileSet into a codepipeline.Artifact
            inputs=[artifacts.to_code_pipeline(self.input)]
        ))

        return cdk.pipelines.CodePipelineActionFactoryResult(run_orders_consumed=1)
```

## Using Docker in the pipeline

Docker can be used in 3 different places in the pipeline:

* If you are using Docker image assets in your application stages: Docker will
  run in the asset publishing projects.
* If you are using Docker image assets in your stack (for example as
  images for your CodeBuild projects): Docker will run in the self-mutate project.
* If you are using Docker to bundle file assets anywhere in your project (for
  example, if you are using such construct libraries as
  `@aws-cdk/aws-lambda-nodejs`): Docker will run in the
  *synth* project.

For the first case, you don't need to do anything special. For the other two cases,
you need to make sure that **privileged mode** is enabled on the correct CodeBuild
projects, so that Docker can run correctly. The follow sections describe how to do
that.

You may also need to authenticate to Docker registries to avoid being throttled.
See the section **Authenticating to Docker registries** below for information on how to do
that.

### Using Docker image assets in the pipeline

If your `PipelineStack` is using Docker image assets (as opposed to the application
stacks the pipeline is deploying), for example by the use of `LinuxBuildImage.fromAsset()`,
you need to pass `dockerEnabledForSelfMutation: true` to the pipeline. For example:

```python
pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"]
    ),

    # Turn this on because the pipeline uses Docker image assets
    docker_enabled_for_self_mutation=True
)

pipeline.add_wave("MyWave",
    post=[
        pipelines.CodeBuildStep("RunApproval",
            commands=["command-from-image"],
            build_environment=cdk.aws_codebuild.BuildEnvironment(
                # The user of a Docker image asset in the pipeline requires turning on
                # 'dockerEnabledForSelfMutation'.
                build_image=codebuild.LinuxBuildImage.from_asset(self, "Image",
                    directory="./docker-image"
                )
            )
        )
    ]
)
```

> **Important**: You must turn on the `dockerEnabledForSelfMutation` flag,
> commit and allow the pipeline to self-update *before* adding the actual
> Docker asset.

### Using bundled file assets

If you are using asset bundling anywhere (such as automatically done for you
if you add a construct like `@aws-cdk/aws-lambda-nodejs`), you need to pass
`dockerEnabledForSynth: true` to the pipeline. For example:

```python
pipeline = pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"]
    ),

    # Turn this on because the application uses bundled file assets
    docker_enabled_for_synth=True
)
```

> **Important**: You must turn on the `dockerEnabledForSynth` flag,
> commit and allow the pipeline to self-update *before* adding the actual
> Docker asset.

### Authenticating to Docker registries

You can specify credentials to use for authenticating to Docker registries as part of the
pipeline definition. This can be useful if any Docker image assets — in the pipeline or
any of the application stages — require authentication, either due to being in a
different environment (e.g., ECR repo) or to avoid throttling (e.g., DockerHub).

```python
docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(self, "DHSecret", "arn:aws:...")
custom_reg_secret = secretsmanager.Secret.from_secret_complete_arn(self, "CRSecret", "arn:aws:...")
repo1 = ecr.Repository.from_repository_arn(self, "Repo", "arn:aws:ecr:eu-west-1:0123456789012:repository/Repo1")
repo2 = ecr.Repository.from_repository_arn(self, "Repo", "arn:aws:ecr:eu-west-1:0123456789012:repository/Repo2")

pipeline = pipelines.CodePipeline(self, "Pipeline",
    docker_credentials=[
        pipelines.DockerCredential.docker_hub(docker_hub_secret),
        pipelines.DockerCredential.custom_registry("dockerregistry.example.com", custom_reg_secret),
        pipelines.DockerCredential.ecr([repo1, repo2])
    ],
    synth=pipelines.ShellStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["npm ci", "npm run build", "npx cdk synth"]
    )
)
```

For authenticating to Docker registries that require a username and password combination
(like DockerHub), create a Secrets Manager Secret with fields named `username`
and `secret`, and import it (the field names change be customized).

Authentication to ECR repostories is done using the execution role of the
relevant CodeBuild job. Both types of credentials can be provided with an
optional role to assume before requesting the credentials.

By default, the Docker credentials provided to the pipeline will be available to
the **Synth**, **Self-Update**, and **Asset Publishing** actions within the
*pipeline. The scope of the credentials can be limited via the `DockerCredentialUsage` option.

```python
docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(self, "DHSecret", "arn:aws:...")
# Only the image asset publishing actions will be granted read access to the secret.
creds = pipelines.DockerCredential.docker_hub(docker_hub_secret, usages=[pipelines.DockerCredentialUsage.ASSET_PUBLISHING])
```

## CDK Environment Bootstrapping

An *environment* is an *(account, region)* pair where you want to deploy a
CDK stack (see
[Environments](https://docs.aws.amazon.com/cdk/latest/guide/environments.html)
in the CDK Developer Guide). In a Continuous Deployment pipeline, there are
at least two environments involved: the environment where the pipeline is
provisioned, and the environment where you want to deploy the application (or
different stages of the application). These can be the same, though best
practices recommend you isolate your different application stages from each
other in different AWS accounts or regions.

Before you can provision the pipeline, you have to *bootstrap* the environment you want
to create it in. If you are deploying your application to different environments, you
also have to bootstrap those and be sure to add a *trust* relationship.

After you have bootstrapped an environment and created a pipeline that deploys
to it, it's important that you don't delete the stack or change its *Qualifier*,
or future deployments to this environment will fail. If you want to upgrade
the bootstrap stack to a newer version, do that by updating it in-place.

> This library requires the *modern* bootstrapping stack which has
> been updated specifically to support cross-account continuous delivery.
>
> If you are using CDKv2, you do not need to do anything else. Modern
> bootstrapping and modern stack synthesis (also known as "default stack
> synthesis") is the default.
>
> If you are using CDKv1, you need to opt in to modern bootstrapping and
> modern stack synthesis using a feature flag. Make sure `cdk.json` includes:
>
> ```json
> {
>   "context": {
>     "@aws-cdk/core:newStyleStackSynthesis": true
>   }
> }
> ```
>
> And be sure to run `cdk bootstrap` in the same directory as the `cdk.json`
> file.

To bootstrap an environment for provisioning the pipeline:

```console
$ npx cdk bootstrap \
    [--profile admin-profile-1] \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
    aws://111111111111/us-east-1
```

To bootstrap a different environment for deploying CDK applications into using
a pipeline in account `111111111111`:

```console
$ npx cdk bootstrap \
    [--profile admin-profile-2] \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
    --trust 11111111111 \
    aws://222222222222/us-east-2
```

If you only want to trust an account to do lookups (e.g, when your CDK application has a
`Vpc.fromLookup()` call), use the option `--trust-for-lookup`:

```console
$ npx cdk bootstrap \
    [--profile admin-profile-2] \
    --cloudformation-execution-policies arn:aws:iam::aws:policy/AdministratorAccess \
    --trust-for-lookup 11111111111 \
    aws://222222222222/us-east-2
```

These command lines explained:

* `npx`: means to use the CDK CLI from the current NPM install. If you are using
  a global install of the CDK CLI, leave this out.
* `--profile`: should indicate a profile with administrator privileges that has
  permissions to provision a pipeline in the indicated account. You can leave this
  flag out if either the AWS default credentials or the `AWS_*` environment
  variables confer these permissions.
* `--cloudformation-execution-policies`: ARN of the managed policy that future CDK
  deployments should execute with. By default this is `AdministratorAccess`, but
  if you also specify the `--trust` flag to give another Account permissions to
  deploy into the current account, you must specify a value here.
* `--trust`: indicates which other account(s) should have permissions to deploy
  CDK applications into this account. In this case we indicate the Pipeline's account,
  but you could also use this for developer accounts (don't do that for production
  application accounts though!).
* `--trust-for-lookup`: gives a more limited set of permissions to the
  trusted account, only allowing it to look up values such as availability zones, EC2 images and
  VPCs. `--trust-for-lookup` does not give permissions to modify anything in the account.
  Note that `--trust` implies `--trust-for-lookup`, so you don't need to specify
  the same acocunt twice.
* `aws://222222222222/us-east-2`: the account and region we're bootstrapping.

> Be aware that anyone who has access to the trusted Accounts **effectively has all
> permissions conferred by the configured CloudFormation execution policies**,
> allowing them to do things like read arbitrary S3 buckets and create arbitrary
> infrastructure in the bootstrapped account.  Restrict the list of `--trust`ed Accounts,
> or restrict the policies configured by `--cloudformation-execution-policies`.

<br>

> **Security tip**: we recommend that you use administrative credentials to an
> account only to bootstrap it and provision the initial pipeline. Otherwise,
> access to administrative credentials should be dropped as soon as possible.

<br>

> **On the use of AdministratorAccess**: The use of the `AdministratorAccess` policy
> ensures that your pipeline can deploy every type of AWS resource to your account.
> Make sure you trust all the code and dependencies that make up your CDK app.
> Check with the appropriate department within your organization to decide on the
> proper policy to use.
>
> If your policy includes permissions to create on attach permission to a role,
> developers can escalate their privilege with more permissive permission.
> Thus, we recommend implementing [permissions boundary](https://aws.amazon.com/premiumsupport/knowledge-center/iam-permission-boundaries/)
> in the CDK Execution role. To do this, you can bootstrap with the `--template` option with
> [a customized template](https://github.com/aws-samples/aws-bootstrap-kit-examples/blob/ba28a97d289128281bc9483bcba12c1793f2c27a/source/1-SDLC-organization/lib/cdk-bootstrap-template.yml#L395) that contains a permission boundary.

### Migrating from old bootstrap stack

The bootstrap stack is a CloudFormation stack in your account named
**CDKToolkit** that provisions a set of resources required for the CDK
to deploy into that environment.

The "new" bootstrap stack (obtained by running `cdk bootstrap` with
`CDK_NEW_BOOTSTRAP=1`) is slightly more elaborate than the "old" stack. It
contains:

* An S3 bucket and ECR repository with predictable names, so that we can reference
  assets in these storage locations *without* the use of CloudFormation template
  parameters.
* A set of roles with permissions to access these asset locations and to execute
  CloudFormation, assumable from whatever accounts you specify under `--trust`.

It is possible and safe to migrate from the old bootstrap stack to the new
bootstrap stack. This will create a new S3 file asset bucket in your account
and orphan the old bucket. You should manually delete the orphaned bucket
after you are sure you have redeployed all CDK applications and there are no
more references to the old asset bucket.

## Context Lookups

You might be using CDK constructs that need to look up [runtime
context](https://docs.aws.amazon.com/cdk/latest/guide/context.html#context_methods),
which is information from the target AWS Account and Region the CDK needs to
synthesize CloudFormation templates appropriate for that environment. Examples
of this kind of context lookups are the number of Availability Zones available
to you, a Route53 Hosted Zone ID, or the ID of an AMI in a given region. This
information is automatically looked up when you run `cdk synth`.

By default, a `cdk synth` performed in a pipeline will not have permissions
to perform these lookups, and the lookups will fail. This is by design.

**Our recommended way of using lookups** is by running `cdk synth` on the
developer workstation and checking in the `cdk.context.json` file, which
contains the results of the context lookups. This will make sure your
synthesized infrastructure is consistent and repeatable. If you do not commit
`cdk.context.json`, the results of the lookups may suddenly be different in
unexpected ways, and even produce results that cannot be deployed or will cause
data loss.  To give an account permissions to perform lookups against an
environment, without being able to deploy to it and make changes, run
`cdk bootstrap --trust-for-lookup=<account>`.

If you want to use lookups directly from the pipeline, you either need to accept
the risk of nondeterminism, or make sure you save and load the
`cdk.context.json` file somewhere between synth runs. Finally, you should
give the synth CodeBuild execution role permissions to assume the bootstrapped
lookup roles. As an example, doing so would look like this:

```python
pipelines.CodePipeline(self, "Pipeline",
    synth=pipelines.CodeBuildStep("Synth",
        input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
            connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
        ),
        commands=["...", "npm ci", "npm run build", "npx cdk synth", "..."
        ],
        role_policy_statements=[
            iam.PolicyStatement(
                actions=["sts:AssumeRole"],
                resources=["*"],
                conditions={
                    "StringEquals": {
                        "iam:ResourceTag/aws-cdk:bootstrap-role": "lookup"
                    }
                }
            )
        ]
    )
)
```

The above example requires that the target environments have all
been bootstrapped with bootstrap stack version `8`, released with
CDK CLI `1.114.0`.

## Security Considerations

It's important to stay safe while employing Continuous Delivery. The CDK Pipelines
library comes with secure defaults to the best of our ability, but by its
very nature the library cannot take care of everything.

We therefore expect you to mind the following:

* Maintain dependency hygiene and vet 3rd-party software you use. Any software you
  run on your build machine has the ability to change the infrastructure that gets
  deployed. Be careful with the software you depend on.
* Use dependency locking to prevent accidental upgrades! The default `CdkSynths` that
  come with CDK Pipelines will expect `package-lock.json` and `yarn.lock` to
  ensure your dependencies are the ones you expect.
* Credentials to production environments should be short-lived. After
  bootstrapping and the initial pipeline provisioning, there is no more need for
  developers to have access to any of the account credentials; all further
  changes can be deployed through git. Avoid the chances of credentials leaking
  by not having them in the first place!

### Confirm permissions broadening

To keep tabs on the security impact of changes going out through your pipeline,
you can insert a security check before any stage deployment. This security check
will check if the upcoming deployment would add any new IAM permissions or
security group rules, and if so pause the pipeline and require you to confirm
the changes.

The security check will appear as two distinct actions in your pipeline: first
a CodeBuild project that runs `cdk diff` on the stage that's about to be deployed,
followed by a Manual Approval action that pauses the pipeline. If it so happens
that there no new IAM permissions or security group rules will be added by the deployment,
the manual approval step is automatically satisfied. The pipeline will look like this:

```txt
Pipeline
├── ...
├── MyApplicationStage
│    ├── MyApplicationSecurityCheck       // Security Diff Action
│    ├── MyApplicationManualApproval      // Manual Approval Action
│    ├── Stack.Prepare
│    └── Stack.Deploy
└── ...
```

You can insert the security check by using a `ConfirmPermissionsBroadening` step:

```python
# pipeline: pipelines.CodePipeline

stage = MyApplicationStage(self, "MyApplication")
pipeline.add_stage(stage,
    pre=[
        pipelines.ConfirmPermissionsBroadening("Check", stage=stage)
    ]
)
```

To get notified when there is a change that needs your manual approval,
create an SNS Topic, subscribe your own email address, and pass it in as
as the `notificationTopic` property:

```python
# pipeline: pipelines.CodePipeline

topic = sns.Topic(self, "SecurityChangesTopic")
topic.add_subscription(subscriptions.EmailSubscription("test@email.com"))

stage = MyApplicationStage(self, "MyApplication")
pipeline.add_stage(stage,
    pre=[
        pipelines.ConfirmPermissionsBroadening("Check",
            stage=stage,
            notification_topic=topic
        )
    ]
)
```

**Note**: Manual Approvals notifications only apply when an application has security
check enabled.

## Using a different deployment engine

CDK Pipelines supports multiple *deployment engines*, but this module vends a
construct for only one such engine: AWS CodePipeline. It is also possible to
use CDK Pipelines to build pipelines backed by other deployment engines.

Here is a list of CDK Libraries that integrate CDK Pipelines with
alternative deployment engines:

* GitHub Workflows: [`cdk-pipelines-github`](https://github.com/cdklabs/cdk-pipelines-github)

## Troubleshooting

Here are some common errors you may encounter while using this library.

### Pipeline: Internal Failure

If you see the following error during deployment of your pipeline:

```plaintext
CREATE_FAILED  | AWS::CodePipeline::Pipeline | Pipeline/Pipeline
Internal Failure
```

There's something wrong with your GitHub access token. It might be missing, or not have the
right permissions to access the repository you're trying to access.

### Key: Policy contains a statement with one or more invalid principals

If you see the following error during deployment of your pipeline:

```plaintext
CREATE_FAILED | AWS::KMS::Key | Pipeline/Pipeline/ArtifactsBucketEncryptionKey
Policy contains a statement with one or more invalid principals.
```

One of the target (account, region) environments has not been bootstrapped
with the new bootstrap stack. Check your target environments and make sure
they are all bootstrapped.

### Message: no matching base directory path found for cdk.out

If you see this error during the **Synth** step, it means that CodeBuild
is expecting to find a `cdk.out` directory in the root of your CodeBuild project,
but the directory wasn't there. There are two common causes for this:

* `cdk synth` is not being executed: `cdk synth` used to be run
  implicitly for you, but you now have to explicitly include the command.
  For NPM-based projects, add `npx cdk synth` to the end of the `commands`
  property, for other languages add `npm install -g aws-cdk` and `cdk synth`.
* Your CDK project lives in a subdirectory: you added a `cd <somedirectory>` command
  to the list of commands; don't forget to tell the `ScriptStep` about the
  different location of `cdk.out`, by passing `primaryOutputDirectory: '<somedirectory>/cdk.out'`.

### <Stack> is in ROLLBACK_COMPLETE state and can not be updated

If  you see the following error during execution of your pipeline:

```plaintext
Stack ... is in ROLLBACK_COMPLETE state and can not be updated. (Service:
AmazonCloudFormation; Status Code: 400; Error Code: ValidationError; Request
ID: ...)
```

The stack failed its previous deployment, and is in a non-retryable state.
Go into the CloudFormation console, delete the stack, and retry the deployment.

### Cannot find module 'xxxx' or its corresponding type declarations

You may see this if you are using TypeScript or other NPM-based languages,
when using NPM 7 on your workstation (where you generate `package-lock.json`)
and NPM 6 on the CodeBuild image used for synthesizing.

It looks like NPM 7 has started writing less information to `package-lock.json`,
leading NPM 6 reading that same file to not install all required packages anymore.

Make sure you are using the same NPM version everywhere, either downgrade your
workstation's version or upgrade the CodeBuild version.

### Cannot find module '.../check-node-version.js' (MODULE_NOT_FOUND)

The above error may be produced by `npx` when executing the CDK CLI, or any
project that uses the AWS SDK for JavaScript, without the target application
having been installed yet. For example, it can be triggered by `npx cdk synth`
if `aws-cdk` is not in your `package.json`.

Work around this by either installing the target application using NPM *before*
running `npx`, or set the environment variable `NPM_CONFIG_UNSAFE_PERM=true`.

### Cannot connect to the Docker daemon at unix:///var/run/docker.sock

If, in the 'Synth' action (inside the 'Build' stage) of your pipeline, you get an error like this:

```console
stderr: docker: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?.
See 'docker run --help'.
```

It means that the AWS CodeBuild project for 'Synth' is not configured to run in privileged mode,
which prevents Docker builds from happening. This typically happens if you use a CDK construct
that bundles asset using tools run via Docker, like `aws-lambda-nodejs`, `aws-lambda-python`,
`aws-lambda-go` and others.

Make sure you set the `privileged` environment variable to `true` in the synth definition:

```python
source_artifact = codepipeline.Artifact()
cloud_assembly_artifact = codepipeline.Artifact()
pipeline = pipelines.CdkPipeline(self, "MyPipeline",
    cloud_assembly_artifact=cloud_assembly_artifact,
    synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
        source_artifact=source_artifact,
        cloud_assembly_artifact=cloud_assembly_artifact,
        environment=cdk.aws_codebuild.BuildEnvironment(
            privileged=True
        )
    )
)
```

After turning on `privilegedMode: true`, you will need to do a one-time manual cdk deploy of your
pipeline to get it going again (as with a broken 'synth' the pipeline will not be able to self
update to the right state).

### S3 error: Access Denied

An "S3 Access Denied" error can have two causes:

* Asset hashes have changed, but self-mutation has been disabled in the pipeline.
* You have deleted and recreated the bootstrap stack, or changed its qualifier.

#### Self-mutation step has been removed

Some constructs, such as EKS clusters, generate nested stacks. When CloudFormation tries
to deploy those stacks, it may fail with this error:

```console
S3 error: Access Denied For more information check http://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html
```

This happens because the pipeline is not self-mutating and, as a consequence, the `FileAssetX`
build projects get out-of-sync with the generated templates. To fix this, make sure the
`selfMutating` property is set to `true`:

```python
cloud_assembly_artifact = codepipeline.Artifact()
pipeline = pipelines.CdkPipeline(self, "MyPipeline",
    self_mutating=True,
    cloud_assembly_artifact=cloud_assembly_artifact
)
```

#### Bootstrap roles have been renamed or recreated

While attempting to deploy an application stage, the "Prepare" or "Deploy" stage may fail with a cryptic error like:

`Action execution failed Access Denied (Service: Amazon S3; Status Code: 403; Error Code: AccessDenied; Request ID: 0123456ABCDEFGH; S3 Extended Request ID: 3hWcrVkhFGxfiMb/rTJO0Bk7Qn95x5ll4gyHiFsX6Pmk/NT+uX9+Z1moEcfkL7H3cjH7sWZfeD0=; Proxy: null)`

This generally indicates that the roles necessary to deploy have been deleted (or deleted and re-created);
for example, if the bootstrap stack has been deleted and re-created, this scenario will happen. Under the hood,
the resources that rely on these roles (e.g., `cdk-$qualifier-deploy-role-$account-$region`) point to different
canonical IDs than the recreated versions of these roles, which causes the errors. There are no simple solutions
to this issue, and for that reason we **strongly recommend** that bootstrap stacks not be deleted and re-created
once created.

The most automated way to solve the issue is to introduce a secondary bootstrap stack. By changing the qualifier
that the pipeline stack looks for, a change will be detected and the impacted policies and resources will be updated.
A hypothetical recovery workflow would look something like this:

* First, for all impacted environments, create a secondary bootstrap stack:

```sh
$ env CDK_NEW_BOOTSTRAP=1 npx cdk bootstrap \
    --qualifier random1234 \
    --toolkit-stack-name CDKToolkitTemp \
    aws://111111111111/us-east-1
```

* Update all impacted stacks in the pipeline to use this new qualifier.
  See https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html for more info.

```python
Stack(self, "MyStack",
    # Update this qualifier to match the one used above.
    synthesizer=cdk.DefaultStackSynthesizer(
        qualifier="randchars1234"
    )
)
```

* Deploy the updated stacks. This will update the stacks to use the roles created in the new bootstrap stack.
* (Optional) Restore back to the original state:

  * Revert the change made in step #2 above
  * Re-deploy the pipeline to use the original qualifier.
  * Delete the temporary bootstrap stack(s)

##### Manual Alternative

Alternatively, the errors can be resolved by finding each impacted resource and policy, and correcting the policies
by replacing the canonical IDs (e.g., `AROAYBRETNYCYV6ZF2R93`) with the appropriate ARNs. As an example, the KMS
encryption key policy for the artifacts bucket may have a statement that looks like the following:

```json
{
  "Effect" : "Allow",
  "Principal" : {
    // "AWS" : "AROAYBRETNYCYV6ZF2R93"  // Indicates this issue; replace this value
    "AWS": "arn:aws:iam::0123456789012:role/cdk-hnb659fds-deploy-role-0123456789012-eu-west-1", // Correct value
  },
  "Action" : [ "kms:Decrypt", "kms:DescribeKey" ],
  "Resource" : "*"
}
```

Any resource or policy that references the qualifier (`hnb659fds` by default) will need to be updated.

### This CDK CLI is not compatible with the CDK library used by your application

The CDK CLI version used in your pipeline is too old to read the Cloud Assembly
produced by your CDK app.

Most likely this happens in the `SelfMutate` action, you are passing the `cliVersion`
parameter to control the version of the CDK CLI, and you just updated the CDK
framework version that your application uses. You either forgot to change the
`cliVersion` parameter, or changed the `cliVersion` in the same commit in which
you changed the framework version. Because a change to the pipeline settings needs
a successful run of the `SelfMutate` step to be applied, the next iteration of the
`SelfMutate` step still executes with the *old* CLI version, and that old CLI version
is not able to read the cloud assembly produced by the new framework version.

Solution: change the `cliVersion` first, commit, push and deploy, and only then
change the framework version.

We recommend you avoid specifying the `cliVersion` parameter at all. By default
the pipeline will use the latest CLI version, which will support all cloud assembly
versions.

## Known Issues

There are some usability issues that are caused by underlying technology, and
cannot be remedied by CDK at this point. They are reproduced here for completeness.

* **Console links to other accounts will not work**: the AWS CodePipeline
  console will assume all links are relative to the current account. You will
  not be able to use the pipeline console to click through to a CloudFormation
  stack in a different account.
* **If a change set failed to apply the pipeline must restarted**: if a change
  set failed to apply, it cannot be retried. The pipeline must be restarted from
  the top by clicking **Release Change**.
* **A stack that failed to create must be deleted manually**: if a stack
  failed to create on the first attempt, you must delete it using the
  CloudFormation console before starting the pipeline again by clicking
  **Release Change**.
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
    CfnOutput as _CfnOutput_a4d857a8,
    Construct as _Construct_e78e779f,
    Duration as _Duration_070aa057,
    IDependable as _IDependable_1175c9f7,
    SecretValue as _SecretValue_c18506ef,
    Stack as _Stack_9f43e4a3,
    Stage as _Stage_9729985a,
)
from ..aws_codebuild import (
    BuildEnvironment as _BuildEnvironment_77bc5f50,
    BuildEnvironmentVariable as _BuildEnvironmentVariable_00095c97,
    BuildSpec as _BuildSpec_1d70c5a1,
    IProject as _IProject_6da8803e,
)
from ..aws_codecommit import IRepository as _IRepository_cdb2a3c0
from ..aws_codepipeline import (
    ActionBindOptions as _ActionBindOptions_20e0a317,
    ActionConfig as _ActionConfig_0c698b52,
    ActionProperties as _ActionProperties_c7760ac6,
    Artifact as _Artifact_9905eec2,
    ArtifactPath as _ArtifactPath_a5b79113,
    IAction as _IAction_ecd54a08,
    IStage as _IStage_5a7e7342,
    Pipeline as _Pipeline_7744fe74,
)
from ..aws_codepipeline_actions import (
    Action as _Action_22e6ab5f,
    CodeCommitTrigger as _CodeCommitTrigger_3c8c9539,
    GitHubTrigger as _GitHubTrigger_0a61ded3,
    S3Trigger as _S3Trigger_688e3a4a,
)
from ..aws_ec2 import (
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ..aws_ecr import IRepository as _IRepository_8b4d2894
from ..aws_events import (
    EventPattern as _EventPattern_a23fbf37,
    IEventBus as _IEventBus_2ca38c95,
    IRuleTarget as _IRuleTarget_d45ec729,
    Rule as _Rule_6cfff189,
    RuleProps as _RuleProps_32051f01,
    Schedule as _Schedule_297d3fad,
)
from ..aws_iam import (
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ..aws_s3 import IBucket as _IBucket_73486e29
from ..aws_secretsmanager import ISecret as _ISecret_22fb8757
from ..aws_sns import ITopic as _ITopic_465e36b9
from ..cx_api import (
    CloudFormationStackArtifact as _CloudFormationStackArtifact_45074b84
)


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddManualApprovalOptions",
    jsii_struct_bases=[],
    name_mapping={"action_name": "actionName", "run_order": "runOrder"},
)
class AddManualApprovalOptions:
    def __init__(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Options for addManualApproval.

        :param action_name: (deprecated) The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: (deprecated) The runOrder for this action. Default: - The next sequential runOrder

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            add_manual_approval_options = pipelines.AddManualApprovalOptions(
                action_name="actionName",
                run_order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e53258e8e55f1f48f8e89ec099df484ebf0e21b0f5287fa8c58754651696e903)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the manual approval action.

        :default: 'ManualApproval' with a rolling counter

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The runOrder for this action.

        :default: - The next sequential runOrder

        :stability: deprecated
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddManualApprovalOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddStackOptions",
    jsii_struct_bases=[],
    name_mapping={"execute_run_order": "executeRunOrder", "run_order": "runOrder"},
)
class AddStackOptions:
    def __init__(
        self,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Additional options for adding a stack deployment.

        :param execute_run_order: (deprecated) Base runorder. Default: - runOrder + 1
        :param run_order: (deprecated) Base runorder. Default: - Next sequential runorder

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            add_stack_options = pipelines.AddStackOptions(
                execute_run_order=123,
                run_order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6b0ec1eac8734e21ef987fc6ad8cd13dc3b2ea57aa69cc15b2d89b66087add0)
            check_type(argname="argument execute_run_order", value=execute_run_order, expected_type=type_hints["execute_run_order"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if run_order is not None:
            self._values["run_order"] = run_order

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Base runorder.

        :default: - runOrder + 1

        :stability: deprecated
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Base runorder.

        :default: - Next sequential runorder

        :stability: deprecated
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStackOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddStageOpts",
    jsii_struct_bases=[],
    name_mapping={"post": "post", "pre": "pre", "stack_steps": "stackSteps"},
)
class AddStageOpts:
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union["StackSteps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''(experimental) Options to pass to ``addStage``.

        :param post: (experimental) Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: (experimental) Instructions for stack level steps. Default: - No additional instructions

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # pipeline: pipelines.CodePipeline
            
            preprod = MyApplicationStage(self, "PreProd")
            prod = MyApplicationStage(self, "Prod")
            
            pipeline.add_stage(preprod,
                post=[
                    pipelines.ShellStep("Validate Endpoint",
                        commands=["curl -Ssf https://my.webservice.com/"]
                    )
                ]
            )
            pipeline.add_stage(prod,
                pre=[
                    pipelines.ManualApprovalStep("PromoteToProd")
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cbdd7c9c07f484b32b780bd09df59fb5411ba050e54c7a4a85fa9a4c706823a)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
            check_type(argname="argument stack_steps", value=stack_steps, expected_type=type_hints["stack_steps"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre
        if stack_steps is not None:
            self._values["stack_steps"] = stack_steps

    @builtins.property
    def post(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Additional steps to run after all of the stacks in the stage.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Additional steps to run before any of the stacks in the stage.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def stack_steps(self) -> typing.Optional[typing.List["StackSteps"]]:
        '''(experimental) Instructions for stack level steps.

        :default: - No additional instructions

        :stability: experimental
        '''
        result = self._values.get("stack_steps")
        return typing.cast(typing.Optional[typing.List["StackSteps"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStageOpts(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AdditionalArtifact",
    jsii_struct_bases=[],
    name_mapping={"artifact": "artifact", "directory": "directory"},
)
class AdditionalArtifact:
    def __init__(
        self,
        *,
        artifact: _Artifact_9905eec2,
        directory: builtins.str,
    ) -> None:
        '''(deprecated) Specification of an additional artifact to generate.

        :param artifact: (deprecated) Artifact to represent the build directory in the pipeline.
        :param directory: (deprecated) Directory to be packaged.

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            
            additional_artifact = pipelines.AdditionalArtifact(
                artifact=artifact,
                directory="directory"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01648844dea0ebea986c7ef74a4e0d14916f34667388b56d215d458193819851)
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "artifact": artifact,
            "directory": directory,
        }

    @builtins.property
    def artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) Artifact to represent the build directory in the pipeline.

        :stability: deprecated
        '''
        result = self._values.get("artifact")
        assert result is not None, "Required property 'artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def directory(self) -> builtins.str:
        '''(deprecated) Directory to be packaged.

        :stability: deprecated
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AdditionalArtifact(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class ArtifactMap(metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.ArtifactMap"):
    '''(experimental) Translate FileSets to CodePipeline Artifacts.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import pipelines
        
        artifact_map = pipelines.ArtifactMap()
    '''

    def __init__(self) -> None:
        '''
        :stability: experimental
        '''
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="toCodePipeline")
    def to_code_pipeline(self, x: "FileSet") -> _Artifact_9905eec2:
        '''(experimental) Return the matching CodePipeline artifact for a FileSet.

        :param x: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7ee5722d41e6ff9c6d9dbb16ce0b07bb64b60cd2d275f2a83cc3dbf32c72a2bd)
            check_type(argname="argument x", value=x, expected_type=type_hints["x"])
        return typing.cast(_Artifact_9905eec2, jsii.invoke(self, "toCodePipeline", [x]))


@jsii.data_type(
    jsii_type="monocdk.pipelines.AssetPublishingCommand",
    jsii_struct_bases=[],
    name_mapping={
        "asset_id": "assetId",
        "asset_manifest_path": "assetManifestPath",
        "asset_publishing_role_arn": "assetPublishingRoleArn",
        "asset_selector": "assetSelector",
        "asset_type": "assetType",
    },
)
class AssetPublishingCommand:
    def __init__(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_publishing_role_arn: builtins.str,
        asset_selector: builtins.str,
        asset_type: "AssetType",
    ) -> None:
        '''(deprecated) Instructions to publish certain assets.

        :param asset_id: (deprecated) Asset identifier.
        :param asset_manifest_path: (deprecated) Asset manifest path.
        :param asset_publishing_role_arn: (deprecated) ARN of the IAM Role used to publish this asset.
        :param asset_selector: (deprecated) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (deprecated) Type of asset to publish.

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            asset_publishing_command = pipelines.AssetPublishingCommand(
                asset_id="assetId",
                asset_manifest_path="assetManifestPath",
                asset_publishing_role_arn="assetPublishingRoleArn",
                asset_selector="assetSelector",
                asset_type=pipelines.AssetType.FILE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__794e1417e465e0dcfa5211235a8cd8fc29a100be525e796247e4cb0049908cbb)
            check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
            check_type(argname="argument asset_manifest_path", value=asset_manifest_path, expected_type=type_hints["asset_manifest_path"])
            check_type(argname="argument asset_publishing_role_arn", value=asset_publishing_role_arn, expected_type=type_hints["asset_publishing_role_arn"])
            check_type(argname="argument asset_selector", value=asset_selector, expected_type=type_hints["asset_selector"])
            check_type(argname="argument asset_type", value=asset_type, expected_type=type_hints["asset_type"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_id": asset_id,
            "asset_manifest_path": asset_manifest_path,
            "asset_publishing_role_arn": asset_publishing_role_arn,
            "asset_selector": asset_selector,
            "asset_type": asset_type,
        }

    @builtins.property
    def asset_id(self) -> builtins.str:
        '''(deprecated) Asset identifier.

        :stability: deprecated
        '''
        result = self._values.get("asset_id")
        assert result is not None, "Required property 'asset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_manifest_path(self) -> builtins.str:
        '''(deprecated) Asset manifest path.

        :stability: deprecated
        '''
        result = self._values.get("asset_manifest_path")
        assert result is not None, "Required property 'asset_manifest_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_publishing_role_arn(self) -> builtins.str:
        '''(deprecated) ARN of the IAM Role used to publish this asset.

        :stability: deprecated
        '''
        result = self._values.get("asset_publishing_role_arn")
        assert result is not None, "Required property 'asset_publishing_role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_selector(self) -> builtins.str:
        '''(deprecated) Asset selector to pass to ``cdk-assets``.

        :stability: deprecated
        '''
        result = self._values.get("asset_selector")
        assert result is not None, "Required property 'asset_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> "AssetType":
        '''(deprecated) Type of asset to publish.

        :stability: deprecated
        '''
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast("AssetType", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AssetPublishingCommand(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="monocdk.pipelines.AssetType")
class AssetType(enum.Enum):
    '''(experimental) Type of the asset that is being published.

    :stability: experimental
    '''

    FILE = "FILE"
    '''(experimental) A file.

    :stability: experimental
    '''
    DOCKER_IMAGE = "DOCKER_IMAGE"
    '''(experimental) A Docker image.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.pipelines.BaseStageOptions",
    jsii_struct_bases=[],
    name_mapping={
        "confirm_broadening_permissions": "confirmBroadeningPermissions",
        "security_notification_topic": "securityNotificationTopic",
    },
)
class BaseStageOptions:
    def __init__(
        self,
        *,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(deprecated) Base options for a pipelines stage.

        :param confirm_broadening_permissions: (deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes. If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this property to override the stage configuration. For example, Pipeline Stage "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three applications will run a security check, but if we want to disable the one for "C", we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline stage behavior. Adds 1 to the run order space. Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application. Default: undefined no notification topic for security check manual approval action

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import pipelines
            
            # topic: sns.Topic
            
            base_stage_options = pipelines.BaseStageOptions(
                confirm_broadening_permissions=False,
                security_notification_topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c7ba3195a09ef48eb12384d783971206b5781b004c60fb1f9675a59382afd7bf)
            check_type(argname="argument confirm_broadening_permissions", value=confirm_broadening_permissions, expected_type=type_hints["confirm_broadening_permissions"])
            check_type(argname="argument security_notification_topic", value=security_notification_topic, expected_type=type_hints["security_notification_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confirm_broadening_permissions is not None:
            self._values["confirm_broadening_permissions"] = confirm_broadening_permissions
        if security_notification_topic is not None:
            self._values["security_notification_topic"] = security_notification_topic

    @builtins.property
    def confirm_broadening_permissions(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes.

        If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this
        property to override the stage configuration. For example, Pipeline Stage
        "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three
        applications will run a security check, but if we want to disable the one for "C",
        we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline
        stage behavior.

        Adds 1 to the run order space.

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("confirm_broadening_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application.

        :default: undefined no notification topic for security check manual approval action

        :stability: deprecated
        '''
        result = self._values.get("security_notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BaseStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdkPipeline(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CdkPipeline",
):
    '''(deprecated) A Pipeline to deploy CDK apps.

    Defines an AWS CodePipeline-based Pipeline to deploy CDK applications.

    Automatically manages the following:

    - Stack dependency order.
    - Asset publishing.
    - Keeping the pipeline up-to-date as the CDK apps change.
    - Using stack outputs later on in the pipeline.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()
        pipeline = pipelines.CdkPipeline(self, "MyPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                environment=cdk.aws_codebuild.BuildEnvironment(
                    privileged=True
                )
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        asset_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        asset_pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        docker_credentials: typing.Optional[typing.Sequence["DockerCredential"]] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        self_mutating: typing.Optional[builtins.bool] = None,
        self_mutation_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        single_publisher_per_type: typing.Optional[builtins.bool] = None,
        source_action: typing.Optional[_IAction_ecd54a08] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        support_docker_assets: typing.Optional[builtins.bool] = None,
        synth_action: typing.Optional[_IAction_ecd54a08] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: (deprecated) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param asset_build_spec: (deprecated) Custom BuildSpec that is merged with generated one (for asset publishing actions). Default: - none
        :param asset_pre_install_commands: (deprecated) Additional commands to run before installing cdk-assets during the asset publishing step Use this to setup proxies or npm mirrors. Default: -
        :param cdk_cli_version: (deprecated) CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: (deprecated) Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param cross_account_keys: (deprecated) Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. Can only be set if ``codePipeline`` is not set. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param docker_credentials: (deprecated) A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param enable_key_rotation: (deprecated) Enables KMS key rotation for cross-account keys. Cannot be set if ``crossAccountKeys`` was set to ``false``. Key rotation costs $1/month when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: (deprecated) Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param self_mutating: (deprecated) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_build_spec: (deprecated) Custom BuildSpec that is merged with generated one (for self-mutation stage). Default: - none
        :param single_publisher_per_type: (deprecated) Whether this pipeline creates one asset upload action per asset type or one asset upload per asset. Default: false
        :param source_action: (deprecated) The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param support_docker_assets: (deprecated) Whether the pipeline needs to build Docker images in the UpdatePipeline stage. If the UpdatePipeline stage tries to build a Docker image and this flag is not set to ``true``, the build step will run in non-privileged mode and consequently will fail with a message like: .. epigraph:: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running? This flag has an effect only if ``selfMutating`` is also ``true``. Default: - false
        :param synth_action: (deprecated) The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given
        :param vpc: (deprecated) The VPC where to execute the CdkPipeline actions. Default: - No VPC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__989087d830a094fcb5bc56d06a252db98005b5de8dc8ca23ffdd1558bb9a9266)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CdkPipelineProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            asset_build_spec=asset_build_spec,
            asset_pre_install_commands=asset_pre_install_commands,
            cdk_cli_version=cdk_cli_version,
            code_pipeline=code_pipeline,
            cross_account_keys=cross_account_keys,
            docker_credentials=docker_credentials,
            enable_key_rotation=enable_key_rotation,
            pipeline_name=pipeline_name,
            self_mutating=self_mutating,
            self_mutation_build_spec=self_mutation_build_spec,
            single_publisher_per_type=single_publisher_per_type,
            source_action=source_action,
            subnet_selection=subnet_selection,
            support_docker_assets=support_docker_assets,
            synth_action=synth_action,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addApplicationStage")
    def add_application_stage(
        self,
        app_stage: _Stage_9729985a,
        *,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> "CdkStage":
        '''(deprecated) Add pipeline stage that will deploy the given application stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param extra_run_order_space: (deprecated) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (deprecated) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false
        :param confirm_broadening_permissions: (deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes. If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this property to override the stage configuration. For example, Pipeline Stage "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three applications will run a security check, but if we want to disable the one for "C", we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline stage behavior. Adds 1 to the run order space. Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application. Default: undefined no notification topic for security check manual approval action

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__60667ecd41c7688b8d136a9e85f911265251d9c4c127095a6200a987090a7901)
            check_type(argname="argument app_stage", value=app_stage, expected_type=type_hints["app_stage"])
        options = AddStageOptions(
            extra_run_order_space=extra_run_order_space,
            manual_approvals=manual_approvals,
            confirm_broadening_permissions=confirm_broadening_permissions,
            security_notification_topic=security_notification_topic,
        )

        return typing.cast("CdkStage", jsii.invoke(self, "addApplicationStage", [app_stage, options]))

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage_name: builtins.str,
        *,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> "CdkStage":
        '''(deprecated) Add a new, empty stage to the pipeline.

        Prefer to use ``addApplicationStage`` if you are intended to deploy a CDK
        application, but you can use this method if you want to add other kinds of
        Actions to a pipeline.

        :param stage_name: -
        :param confirm_broadening_permissions: (deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes. If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this property to override the stage configuration. For example, Pipeline Stage "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three applications will run a security check, but if we want to disable the one for "C", we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline stage behavior. Adds 1 to the run order space. Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application. Default: undefined no notification topic for security check manual approval action

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a21b566b5d6896234548128a0ba7342473aaf41024030bc7822b69f1bfbe75fa)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        options = BaseStageOptions(
            confirm_broadening_permissions=confirm_broadening_permissions,
            security_notification_topic=security_notification_topic,
        )

        return typing.cast("CdkStage", jsii.invoke(self, "addStage", [stage_name, options]))

    @jsii.member(jsii_name="stackOutput")
    def stack_output(self, cfn_output: _CfnOutput_a4d857a8) -> "StackOutput":
        '''(deprecated) Get the StackOutput object that holds this CfnOutput's value in this pipeline.

        ``StackOutput`` can be used in validation actions later in the pipeline.

        :param cfn_output: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4d10f3ea6630fe455a878f375963488e94d9692a28b3664284f1004a5d7a0aa1)
            check_type(argname="argument cfn_output", value=cfn_output, expected_type=type_hints["cfn_output"])
        return typing.cast("StackOutput", jsii.invoke(self, "stackOutput", [cfn_output]))

    @jsii.member(jsii_name="stage")
    def stage(self, stage_name: builtins.str) -> _IStage_5a7e7342:
        '''(deprecated) Access one of the pipeline's stages by stage name.

        You can use this to add more Actions to a stage.

        :param stage_name: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40acafbdef3fb1f200a0d9756a6be77e36ee43b979374cbba5b27e24b8215a79)
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        return typing.cast(_IStage_5a7e7342, jsii.invoke(self, "stage", [stage_name]))

    @jsii.member(jsii_name="validate")
    def _validate(self) -> typing.List[builtins.str]:
        '''(deprecated) Validate that we don't have any stacks violating dependency order in the pipeline.

        Our own convenience methods will never generate a pipeline that does that (although
        this is a nice verification), but a user can also add the stacks by hand.

        :stability: deprecated
        '''
        return typing.cast(typing.List[builtins.str], jsii.invoke(self, "validate", []))

    @builtins.property
    @jsii.member(jsii_name="codePipeline")
    def code_pipeline(self) -> _Pipeline_7744fe74:
        '''(deprecated) The underlying CodePipeline object.

        You can use this to add more Stages to the pipeline, or Actions
        to Stages.

        :stability: deprecated
        '''
        return typing.cast(_Pipeline_7744fe74, jsii.get(self, "codePipeline"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkPipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "asset_build_spec": "assetBuildSpec",
        "asset_pre_install_commands": "assetPreInstallCommands",
        "cdk_cli_version": "cdkCliVersion",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "docker_credentials": "dockerCredentials",
        "enable_key_rotation": "enableKeyRotation",
        "pipeline_name": "pipelineName",
        "self_mutating": "selfMutating",
        "self_mutation_build_spec": "selfMutationBuildSpec",
        "single_publisher_per_type": "singlePublisherPerType",
        "source_action": "sourceAction",
        "subnet_selection": "subnetSelection",
        "support_docker_assets": "supportDockerAssets",
        "synth_action": "synthAction",
        "vpc": "vpc",
    },
)
class CdkPipelineProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        asset_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        asset_pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        docker_credentials: typing.Optional[typing.Sequence["DockerCredential"]] = None,
        enable_key_rotation: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        self_mutating: typing.Optional[builtins.bool] = None,
        self_mutation_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        single_publisher_per_type: typing.Optional[builtins.bool] = None,
        source_action: typing.Optional[_IAction_ecd54a08] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        support_docker_assets: typing.Optional[builtins.bool] = None,
        synth_action: typing.Optional[_IAction_ecd54a08] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(deprecated) Properties for a CdkPipeline.

        :param cloud_assembly_artifact: (deprecated) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.
        :param asset_build_spec: (deprecated) Custom BuildSpec that is merged with generated one (for asset publishing actions). Default: - none
        :param asset_pre_install_commands: (deprecated) Additional commands to run before installing cdk-assets during the asset publishing step Use this to setup proxies or npm mirrors. Default: -
        :param cdk_cli_version: (deprecated) CDK CLI version to use in pipeline. Some Actions in the pipeline will download and run a version of the CDK CLI. Specify the version here. Default: - Latest version
        :param code_pipeline: (deprecated) Existing CodePipeline to add deployment stages to. Use this if you want more control over the CodePipeline that gets created. You can choose to not pass this value, in which case a new CodePipeline is created with default settings. If you pass an existing CodePipeline, it should have been created with ``restartExecutionOnUpdate: true``. [disable-awslint:ref-via-interface] Default: - A new CodePipeline is automatically generated
        :param cross_account_keys: (deprecated) Create KMS keys for cross-account deployments. This controls whether the pipeline is enabled for cross-account deployments. Can only be set if ``codePipeline`` is not set. By default cross-account deployments are enabled, but this feature requires that KMS Customer Master Keys are created which have a cost of $1/month. If you do not need cross-account deployments, you can set this to ``false`` to not create those keys and save on that cost (the artifact bucket will be encrypted with an AWS-managed key). However, cross-account deployments will no longer be possible. Default: true
        :param docker_credentials: (deprecated) A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param enable_key_rotation: (deprecated) Enables KMS key rotation for cross-account keys. Cannot be set if ``crossAccountKeys`` was set to ``false``. Key rotation costs $1/month when enabled. Default: - false (key rotation is disabled)
        :param pipeline_name: (deprecated) Name of the pipeline. Can only be set if ``codePipeline`` is not set. Default: - A name is automatically generated
        :param self_mutating: (deprecated) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_build_spec: (deprecated) Custom BuildSpec that is merged with generated one (for self-mutation stage). Default: - none
        :param single_publisher_per_type: (deprecated) Whether this pipeline creates one asset upload action per asset type or one asset upload per asset. Default: false
        :param source_action: (deprecated) The CodePipeline action used to retrieve the CDK app's source. Default: - Required unless ``codePipeline`` is given
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param support_docker_assets: (deprecated) Whether the pipeline needs to build Docker images in the UpdatePipeline stage. If the UpdatePipeline stage tries to build a Docker image and this flag is not set to ``true``, the build step will run in non-privileged mode and consequently will fail with a message like: .. epigraph:: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running? This flag has an effect only if ``selfMutating`` is also ``true``. Default: - false
        :param synth_action: (deprecated) The CodePipeline action build and synthesis step of the CDK app. Default: - Required unless ``codePipeline`` or ``sourceAction`` is given
        :param vpc: (deprecated) The VPC where to execute the CdkPipeline actions. Default: - No VPC

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            source_artifact = codepipeline.Artifact()
            cloud_assembly_artifact = codepipeline.Artifact()
            pipeline = pipelines.CdkPipeline(self, "MyPipeline",
                cloud_assembly_artifact=cloud_assembly_artifact,
                synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                    source_artifact=source_artifact,
                    cloud_assembly_artifact=cloud_assembly_artifact,
                    environment=cdk.aws_codebuild.BuildEnvironment(
                        privileged=True
                    )
                )
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__37f58057546cb907ffff99db5e3d900e2c1fb8278c6f2389f9943aaca1e45637)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument asset_build_spec", value=asset_build_spec, expected_type=type_hints["asset_build_spec"])
            check_type(argname="argument asset_pre_install_commands", value=asset_pre_install_commands, expected_type=type_hints["asset_pre_install_commands"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
            check_type(argname="argument code_pipeline", value=code_pipeline, expected_type=type_hints["code_pipeline"])
            check_type(argname="argument cross_account_keys", value=cross_account_keys, expected_type=type_hints["cross_account_keys"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument enable_key_rotation", value=enable_key_rotation, expected_type=type_hints["enable_key_rotation"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument self_mutating", value=self_mutating, expected_type=type_hints["self_mutating"])
            check_type(argname="argument self_mutation_build_spec", value=self_mutation_build_spec, expected_type=type_hints["self_mutation_build_spec"])
            check_type(argname="argument single_publisher_per_type", value=single_publisher_per_type, expected_type=type_hints["single_publisher_per_type"])
            check_type(argname="argument source_action", value=source_action, expected_type=type_hints["source_action"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument support_docker_assets", value=support_docker_assets, expected_type=type_hints["support_docker_assets"])
            check_type(argname="argument synth_action", value=synth_action, expected_type=type_hints["synth_action"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
        }
        if asset_build_spec is not None:
            self._values["asset_build_spec"] = asset_build_spec
        if asset_pre_install_commands is not None:
            self._values["asset_pre_install_commands"] = asset_pre_install_commands
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if enable_key_rotation is not None:
            self._values["enable_key_rotation"] = enable_key_rotation
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if self_mutating is not None:
            self._values["self_mutating"] = self_mutating
        if self_mutation_build_spec is not None:
            self._values["self_mutation_build_spec"] = self_mutation_build_spec
        if single_publisher_per_type is not None:
            self._values["single_publisher_per_type"] = single_publisher_per_type
        if source_action is not None:
            self._values["source_action"] = source_action
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if support_docker_assets is not None:
            self._values["support_docker_assets"] = support_docker_assets
        if synth_action is not None:
            self._values["synth_action"] = synth_action
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The artifact you have defined to be the artifact to hold the cloudAssemblyArtifact for the synth action.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def asset_build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) Custom BuildSpec that is merged with generated one (for asset publishing actions).

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("asset_build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def asset_pre_install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Additional commands to run before installing cdk-assets during the asset publishing step Use this to setup proxies or npm mirrors.

        :default: -

        :stability: deprecated
        '''
        result = self._values.get("asset_pre_install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(deprecated) CDK CLI version to use in pipeline.

        Some Actions in the pipeline will download and run a version of the CDK
        CLI. Specify the version here.

        :default: - Latest version

        :stability: deprecated
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_pipeline(self) -> typing.Optional[_Pipeline_7744fe74]:
        '''(deprecated) Existing CodePipeline to add deployment stages to.

        Use this if you want more control over the CodePipeline that gets created.
        You can choose to not pass this value, in which case a new CodePipeline is
        created with default settings.

        If you pass an existing CodePipeline, it should have been created
        with ``restartExecutionOnUpdate: true``.

        [disable-awslint:ref-via-interface]

        :default: - A new CodePipeline is automatically generated

        :stability: deprecated
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_Pipeline_7744fe74], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Create KMS keys for cross-account deployments.

        This controls whether the pipeline is enabled for cross-account deployments.

        Can only be set if ``codePipeline`` is not set.

        By default cross-account deployments are enabled, but this feature requires
        that KMS Customer Master Keys are created which have a cost of $1/month.

        If you do not need cross-account deployments, you can set this to ``false`` to
        not create those keys and save on that cost (the artifact bucket will be
        encrypted with an AWS-managed key). However, cross-account deployments will
        no longer be possible.

        :default: true

        :stability: deprecated
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_credentials(self) -> typing.Optional[typing.List["DockerCredential"]]:
        '''(deprecated) A list of credentials used to authenticate to Docker registries.

        Specify any credentials necessary within the pipeline to build, synth, update, or publish assets.

        :default: []

        :stability: deprecated
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List["DockerCredential"]], result)

    @builtins.property
    def enable_key_rotation(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Enables KMS key rotation for cross-account keys.

        Cannot be set if ``crossAccountKeys`` was set to ``false``.

        Key rotation costs $1/month when enabled.

        :default: - false (key rotation is disabled)

        :stability: deprecated
        '''
        result = self._values.get("enable_key_rotation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the pipeline.

        Can only be set if ``codePipeline`` is not set.

        :default: - A name is automatically generated

        :stability: deprecated
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def self_mutating(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true

        :stability: deprecated
        '''
        result = self._values.get("self_mutating")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation_build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) Custom BuildSpec that is merged with generated one (for self-mutation stage).

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("self_mutation_build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def single_publisher_per_type(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether this pipeline creates one asset upload action per asset type or one asset upload per asset.

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("single_publisher_per_type")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def source_action(self) -> typing.Optional[_IAction_ecd54a08]:
        '''(deprecated) The CodePipeline action used to retrieve the CDK app's source.

        :default: - Required unless ``codePipeline`` is given

        :stability: deprecated
        '''
        result = self._values.get("source_action")
        return typing.cast(typing.Optional[_IAction_ecd54a08], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def support_docker_assets(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether the pipeline needs to build Docker images in the UpdatePipeline stage.

        If the UpdatePipeline stage tries to build a Docker image and this flag is not
        set to ``true``, the build step will run in non-privileged mode and consequently
        will fail with a message like:
        .. epigraph::

           Cannot connect to the Docker daemon at unix:///var/run/docker.sock.
           Is the docker daemon running?

        This flag has an effect only if ``selfMutating`` is also ``true``.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("support_docker_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def synth_action(self) -> typing.Optional[_IAction_ecd54a08]:
        '''(deprecated) The CodePipeline action build and synthesis step of the CDK app.

        :default: - Required unless ``codePipeline`` or ``sourceAction`` is given

        :stability: deprecated
        '''
        result = self._values.get("synth_action")
        return typing.cast(typing.Optional[_IAction_ecd54a08], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the CdkPipeline actions.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkPipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CdkStage(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CdkStage",
):
    '''(deprecated) Stage in a CdkPipeline.

    You don't need to instantiate this class directly. Use
    ``cdkPipeline.addStage()`` instead.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import aws_sns as sns
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        # stage: codepipeline.IStage
        # stage_host: pipelines.IStageHost
        # topic: sns.Topic
        
        cdk_stage = pipelines.CdkStage(self, "MyCdkStage",
            cloud_assembly_artifact=artifact,
            host=stage_host,
            pipeline_stage=stage,
            stage_name="stageName",
        
            # the properties below are optional
            confirm_broadening_permissions=False,
            security_notification_topic=topic
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        host: "IStageHost",
        pipeline_stage: _IStage_5a7e7342,
        stage_name: builtins.str,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_artifact: (deprecated) The CodePipeline Artifact with the Cloud Assembly.
        :param host: (deprecated) Features the Stage needs from its environment.
        :param pipeline_stage: (deprecated) The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: (deprecated) Name of the stage that should be created.
        :param confirm_broadening_permissions: (deprecated) Run a security check before every application prepare/deploy actions. Note: Stage level security check can be overriden per application as follows: ``stage.addApplication(app, { confirmBroadeningPermissions: false })`` Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when any security check registers changes within a application. Note: The Stage Notification Topic can be overriden per application as follows: ``stage.addApplication(app, { securityNotificationTopic: newTopic })`` Default: undefined no stage level notification topic

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dcc892f6f4314c93abf00b34101b146bb57a9578dc757b57de68eec784cf5bfd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CdkStageProps(
            cloud_assembly_artifact=cloud_assembly_artifact,
            host=host,
            pipeline_stage=pipeline_stage,
            stage_name=stage_name,
            confirm_broadening_permissions=confirm_broadening_permissions,
            security_notification_topic=security_notification_topic,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addActions")
    def add_actions(self, *actions: _IAction_ecd54a08) -> None:
        '''(deprecated) Add one or more CodePipeline Actions.

        You need to make sure it is created with the right runOrder. Call ``nextSequentialRunOrder()``
        for every action to get actions to execute in sequence.

        :param actions: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e44c877680f4153b7c1f9881e76412aa3418d316db52e4a18c6258423edc07bc)
            check_type(argname="argument actions", value=actions, expected_type=typing.Tuple[type_hints["actions"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addActions", [*actions]))

    @jsii.member(jsii_name="addApplication")
    def add_application(
        self,
        app_stage: _Stage_9729985a,
        *,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(deprecated) Add all stacks in the application Stage to this stage.

        The application construct should subclass ``Stage`` and can contain any
        number of ``Stacks`` inside it that may have dependency relationships
        on one another.

        All stacks in the application will be deployed in the appropriate order,
        and all assets found in the application will be added to the asset
        publishing stage.

        :param app_stage: -
        :param extra_run_order_space: (deprecated) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (deprecated) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false
        :param confirm_broadening_permissions: (deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes. If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this property to override the stage configuration. For example, Pipeline Stage "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three applications will run a security check, but if we want to disable the one for "C", we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline stage behavior. Adds 1 to the run order space. Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application. Default: undefined no notification topic for security check manual approval action

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d902744d394475fde2e3845a01b0e70231c5d650614aa06522a6e4f568f5f419)
            check_type(argname="argument app_stage", value=app_stage, expected_type=type_hints["app_stage"])
        options = AddStageOptions(
            extra_run_order_space=extra_run_order_space,
            manual_approvals=manual_approvals,
            confirm_broadening_permissions=confirm_broadening_permissions,
            security_notification_topic=security_notification_topic,
        )

        return typing.cast(None, jsii.invoke(self, "addApplication", [app_stage, options]))

    @jsii.member(jsii_name="addManualApprovalAction")
    def add_manual_approval_action(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Add a manual approval action.

        If you need more flexibility than what this method offers,
        use ``addAction`` with a ``ManualApprovalAction``.

        :param action_name: (deprecated) The name of the manual approval action. Default: 'ManualApproval' with a rolling counter
        :param run_order: (deprecated) The runOrder for this action. Default: - The next sequential runOrder

        :stability: deprecated
        '''
        options = AddManualApprovalOptions(
            action_name=action_name, run_order=run_order
        )

        return typing.cast(None, jsii.invoke(self, "addManualApprovalAction", [options]))

    @jsii.member(jsii_name="addStackArtifactDeployment")
    def add_stack_artifact_deployment(
        self,
        stack_artifact: _CloudFormationStackArtifact_45074b84,
        *,
        execute_run_order: typing.Optional[jsii.Number] = None,
        run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Add a deployment action based on a stack artifact.

        :param stack_artifact: -
        :param execute_run_order: (deprecated) Base runorder. Default: - runOrder + 1
        :param run_order: (deprecated) Base runorder. Default: - Next sequential runorder

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c65e3001ed993d169c1125c20e8842cd226b968a6b4bba2d69b909ef07ac5cb)
            check_type(argname="argument stack_artifact", value=stack_artifact, expected_type=type_hints["stack_artifact"])
        options = AddStackOptions(
            execute_run_order=execute_run_order, run_order=run_order
        )

        return typing.cast(None, jsii.invoke(self, "addStackArtifactDeployment", [stack_artifact, options]))

    @jsii.member(jsii_name="deploysStack")
    def deploys_stack(self, artifact_id: builtins.str) -> builtins.bool:
        '''(deprecated) Whether this Stage contains an action to deploy the given stack, identified by its artifact ID.

        :param artifact_id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e24ca59156e0d56a199b747248a2332a03baeaeb0221db9542ff539d983505d6)
            check_type(argname="argument artifact_id", value=artifact_id, expected_type=type_hints["artifact_id"])
        return typing.cast(builtins.bool, jsii.invoke(self, "deploysStack", [artifact_id]))

    @jsii.member(jsii_name="nextSequentialRunOrder")
    def next_sequential_run_order(
        self,
        count: typing.Optional[jsii.Number] = None,
    ) -> jsii.Number:
        '''(deprecated) Return the runOrder number necessary to run the next Action in sequence with the rest.

        FIXME: This is here because Actions are immutable and can't be reordered
        after creation, nor is there a way to specify relative priorities, which
        is a limitation that we should take away in the base library.

        :param count: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd1fc645e90737eb0946de226128e7dbda3b2ec36fdf212763ef0ccabfd07be1)
            check_type(argname="argument count", value=count, expected_type=type_hints["count"])
        return typing.cast(jsii.Number, jsii.invoke(self, "nextSequentialRunOrder", [count]))


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkStageProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "host": "host",
        "pipeline_stage": "pipelineStage",
        "stage_name": "stageName",
        "confirm_broadening_permissions": "confirmBroadeningPermissions",
        "security_notification_topic": "securityNotificationTopic",
    },
)
class CdkStageProps:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        host: "IStageHost",
        pipeline_stage: _IStage_5a7e7342,
        stage_name: builtins.str,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(deprecated) Construction properties for a CdkStage.

        :param cloud_assembly_artifact: (deprecated) The CodePipeline Artifact with the Cloud Assembly.
        :param host: (deprecated) Features the Stage needs from its environment.
        :param pipeline_stage: (deprecated) The underlying Pipeline Stage associated with thisCdkStage.
        :param stage_name: (deprecated) Name of the stage that should be created.
        :param confirm_broadening_permissions: (deprecated) Run a security check before every application prepare/deploy actions. Note: Stage level security check can be overriden per application as follows: ``stage.addApplication(app, { confirmBroadeningPermissions: false })`` Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when any security check registers changes within a application. Note: The Stage Notification Topic can be overriden per application as follows: ``stage.addApplication(app, { securityNotificationTopic: newTopic })`` Default: undefined no stage level notification topic

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_sns as sns
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # stage: codepipeline.IStage
            # stage_host: pipelines.IStageHost
            # topic: sns.Topic
            
            cdk_stage_props = pipelines.CdkStageProps(
                cloud_assembly_artifact=artifact,
                host=stage_host,
                pipeline_stage=stage,
                stage_name="stageName",
            
                # the properties below are optional
                confirm_broadening_permissions=False,
                security_notification_topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01a24e3cc881e3e895d7faa2336a1becf55bb39e624e37e5408ad218deeb3eaa)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument host", value=host, expected_type=type_hints["host"])
            check_type(argname="argument pipeline_stage", value=pipeline_stage, expected_type=type_hints["pipeline_stage"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
            check_type(argname="argument confirm_broadening_permissions", value=confirm_broadening_permissions, expected_type=type_hints["confirm_broadening_permissions"])
            check_type(argname="argument security_notification_topic", value=security_notification_topic, expected_type=type_hints["security_notification_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "host": host,
            "pipeline_stage": pipeline_stage,
            "stage_name": stage_name,
        }
        if confirm_broadening_permissions is not None:
            self._values["confirm_broadening_permissions"] = confirm_broadening_permissions
        if security_notification_topic is not None:
            self._values["security_notification_topic"] = security_notification_topic

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline Artifact with the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def host(self) -> "IStageHost":
        '''(deprecated) Features the Stage needs from its environment.

        :stability: deprecated
        '''
        result = self._values.get("host")
        assert result is not None, "Required property 'host' is missing"
        return typing.cast("IStageHost", result)

    @builtins.property
    def pipeline_stage(self) -> _IStage_5a7e7342:
        '''(deprecated) The underlying Pipeline Stage associated with thisCdkStage.

        :stability: deprecated
        '''
        result = self._values.get("pipeline_stage")
        assert result is not None, "Required property 'pipeline_stage' is missing"
        return typing.cast(_IStage_5a7e7342, result)

    @builtins.property
    def stage_name(self) -> builtins.str:
        '''(deprecated) Name of the stage that should be created.

        :stability: deprecated
        '''
        result = self._values.get("stage_name")
        assert result is not None, "Required property 'stage_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def confirm_broadening_permissions(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Run a security check before every application prepare/deploy actions.

        Note: Stage level security check can be overriden per application as follows:
        ``stage.addApplication(app, { confirmBroadeningPermissions: false })``

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("confirm_broadening_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(deprecated) Optional SNS topic to send notifications to when any security check registers changes within a application.

        Note: The Stage Notification Topic can be overriden per application as follows:
        ``stage.addApplication(app, { securityNotificationTopic: newTopic })``

        :default: undefined no stage level notification topic

        :stability: deprecated
        '''
        result = self._values.get("security_notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStageProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CodeBuildOptions",
    jsii_struct_bases=[],
    name_mapping={
        "build_environment": "buildEnvironment",
        "partial_build_spec": "partialBuildSpec",
        "role_policy": "rolePolicy",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildOptions:
    def __init__(
        self,
        *,
        build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        role_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Options for customizing a single CodeBuild project.

        :param build_environment: (experimental) Partial build environment, will be combined with other build environments that apply. Default: - Non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_5_0
        :param partial_build_spec: (experimental) Partial buildspec, will be combined with other buildspecs that apply. The BuildSpec must be available inline--it cannot reference a file on disk. Default: - No initial BuildSpec
        :param role_policy: (experimental) Policy statements to add to role. Default: - No policy statements added to CodeBuild Project Role
        :param security_groups: (experimental) Which security group(s) to associate with the project network interfaces. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) The VPC where to create the CodeBuild network interfaces in. Default: - No VPC

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # vpc: ec2.Vpc
            # my_security_group: ec2.SecurityGroup
            
            pipelines.CodePipeline(self, "Pipeline",
                # Standard CodePipeline properties
                synth=pipelines.ShellStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["npm ci", "npm run build", "npx cdk synth"
                    ]
                ),
            
                # Defaults for all CodeBuild projects
                code_build_defaults=cdk.pipelines.CodeBuildOptions(
                    # Prepend commands and configuration to all projects
                    partial_build_spec=codebuild.BuildSpec.from_object({
                        "version": "0.2"
                    }),
            
                    # Control the build environment
                    build_environment=cdk.aws_codebuild.BuildEnvironment(
                        compute_type=codebuild.ComputeType.LARGE
                    ),
            
                    # Control Elastic Network Interface creation
                    vpc=vpc,
                    subnet_selection=cdk.aws_ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT),
                    security_groups=[my_security_group],
            
                    # Additional policy statements for the execution role
                    role_policy=[
                        iam.PolicyStatement()
                    ]
                ),
            
                synth_code_build_defaults=cdk.pipelines.CodeBuildOptions(),
                asset_publishing_code_build_defaults=cdk.pipelines.CodeBuildOptions(),
                self_mutation_code_build_defaults=cdk.pipelines.CodeBuildOptions()
            )
        '''
        if isinstance(build_environment, dict):
            build_environment = _BuildEnvironment_77bc5f50(**build_environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0e6d8f505c71a5a7594d231c58fd8d71a3d2dde1f874d16412b8113303bb5cee)
            check_type(argname="argument build_environment", value=build_environment, expected_type=type_hints["build_environment"])
            check_type(argname="argument partial_build_spec", value=partial_build_spec, expected_type=type_hints["partial_build_spec"])
            check_type(argname="argument role_policy", value=role_policy, expected_type=type_hints["role_policy"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if build_environment is not None:
            self._values["build_environment"] = build_environment
        if partial_build_spec is not None:
            self._values["partial_build_spec"] = partial_build_spec
        if role_policy is not None:
            self._values["role_policy"] = role_policy
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def build_environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Partial build environment, will be combined with other build environments that apply.

        :default: - Non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_5_0

        :stability: experimental
        '''
        result = self._values.get("build_environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def partial_build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) Partial buildspec, will be combined with other buildspecs that apply.

        The BuildSpec must be available inline--it cannot reference a file
        on disk.

        :default: - No initial BuildSpec

        :stability: experimental
        '''
        result = self._values.get("partial_build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def role_policy(self) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Which security group(s) to associate with the project network interfaces.

        Only used if 'vpc' is supplied.

        :default: - Security group will be automatically created.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to create the CodeBuild network interfaces in.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CodeCommitSourceOptions",
    jsii_struct_bases=[],
    name_mapping={
        "code_build_clone_output": "codeBuildCloneOutput",
        "event_role": "eventRole",
        "trigger": "trigger",
    },
)
class CodeCommitSourceOptions:
    def __init__(
        self,
        *,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
        trigger: typing.Optional[_CodeCommitTrigger_3c8c9539] = None,
    ) -> None:
        '''(experimental) Configuration options for a CodeCommit source.

        :param code_build_clone_output: (experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files). This provides access to repository history, and retains symlinks (symlinks would otherwise be removed by CodePipeline). **Note**: if this option is true, only CodeBuild jobs can use the output artifact. Default: false
        :param event_role: (experimental) Role to be used by on commit event rule. Used only when trigger value is CodeCommitTrigger.EVENTS. Default: a new role will be created.
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline_actions as codepipeline_actions
            from monocdk import aws_iam as iam
            from monocdk import pipelines
            
            # role: iam.Role
            
            code_commit_source_options = pipelines.CodeCommitSourceOptions(
                code_build_clone_output=False,
                event_role=role,
                trigger=codepipeline_actions.CodeCommitTrigger.NONE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42daba2cc573cb139cb9afedb97b9407dc8e2947e5ea960ba7630d9dc96ea10d)
            check_type(argname="argument code_build_clone_output", value=code_build_clone_output, expected_type=type_hints["code_build_clone_output"])
            check_type(argname="argument event_role", value=event_role, expected_type=type_hints["event_role"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if code_build_clone_output is not None:
            self._values["code_build_clone_output"] = code_build_clone_output
        if event_role is not None:
            self._values["event_role"] = event_role
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def code_build_clone_output(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files).

        This provides access to repository history, and retains symlinks (symlinks would otherwise be
        removed by CodePipeline).

        **Note**: if this option is true, only CodeBuild jobs can use the output artifact.

        :default: false

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodeCommit.html
        :stability: experimental
        '''
        result = self._values.get("code_build_clone_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def event_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Role to be used by on commit event rule.

        Used only when trigger value is CodeCommitTrigger.EVENTS.

        :default: a new role will be created.

        :stability: experimental
        '''
        result = self._values.get("event_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def trigger(self) -> typing.Optional[_CodeCommitTrigger_3c8c9539]:
        '''(experimental) How should CodePipeline detect source changes for this Action.

        :default: CodeCommitTrigger.EVENTS

        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional[_CodeCommitTrigger_3c8c9539], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeCommitSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CodePipelineActionFactoryResult",
    jsii_struct_bases=[],
    name_mapping={"run_orders_consumed": "runOrdersConsumed", "project": "project"},
)
class CodePipelineActionFactoryResult:
    def __init__(
        self,
        *,
        run_orders_consumed: jsii.Number,
        project: typing.Optional[_IProject_6da8803e] = None,
    ) -> None:
        '''(experimental) The result of adding actions to the pipeline.

        :param run_orders_consumed: (experimental) How many RunOrders were consumed. If you add 1 action, return the value 1 here.
        :param project: (experimental) If a CodeBuild project got created, the project. Default: - This factory did not create a CodeBuild project

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import pipelines
            
            # project: codebuild.Project
            
            code_pipeline_action_factory_result = pipelines.CodePipelineActionFactoryResult(
                run_orders_consumed=123,
            
                # the properties below are optional
                project=project
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0432247cd51e19450ab87dda01d3544325a396496478d68484f7a7ca057d368c)
            check_type(argname="argument run_orders_consumed", value=run_orders_consumed, expected_type=type_hints["run_orders_consumed"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "run_orders_consumed": run_orders_consumed,
        }
        if project is not None:
            self._values["project"] = project

    @builtins.property
    def run_orders_consumed(self) -> jsii.Number:
        '''(experimental) How many RunOrders were consumed.

        If you add 1 action, return the value 1 here.

        :stability: experimental
        '''
        result = self._values.get("run_orders_consumed")
        assert result is not None, "Required property 'run_orders_consumed' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def project(self) -> typing.Optional[_IProject_6da8803e]:
        '''(experimental) If a CodeBuild project got created, the project.

        :default: - This factory did not create a CodeBuild project

        :stability: experimental
        '''
        result = self._values.get("project")
        return typing.cast(typing.Optional[_IProject_6da8803e], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineActionFactoryResult(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CodePipelineProps",
    jsii_struct_bases=[],
    name_mapping={
        "synth": "synth",
        "asset_publishing_code_build_defaults": "assetPublishingCodeBuildDefaults",
        "cli_version": "cliVersion",
        "code_build_defaults": "codeBuildDefaults",
        "code_pipeline": "codePipeline",
        "cross_account_keys": "crossAccountKeys",
        "docker_credentials": "dockerCredentials",
        "docker_enabled_for_self_mutation": "dockerEnabledForSelfMutation",
        "docker_enabled_for_synth": "dockerEnabledForSynth",
        "pipeline_name": "pipelineName",
        "publish_assets_in_parallel": "publishAssetsInParallel",
        "reuse_cross_region_support_stacks": "reuseCrossRegionSupportStacks",
        "self_mutation": "selfMutation",
        "self_mutation_code_build_defaults": "selfMutationCodeBuildDefaults",
        "synth_code_build_defaults": "synthCodeBuildDefaults",
    },
)
class CodePipelineProps:
    def __init__(
        self,
        *,
        synth: "IFileSetProducer",
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        docker_credentials: typing.Optional[typing.Sequence["DockerCredential"]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''(experimental) Properties for a ``CodePipeline``.

        :param synth: (experimental) The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param asset_publishing_code_build_defaults: (experimental) Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: (experimental) CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: (experimental) Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_5_0
        :param code_pipeline: (experimental) An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: (experimental) Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param docker_credentials: (experimental) A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: (experimental) Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: (experimental) Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``@aws-cdk/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param pipeline_name: (experimental) The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: (experimental) Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: (experimental) Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param self_mutation: (experimental) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: (experimental) Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth_code_build_defaults: (experimental) Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Modern API
            modern_pipeline = pipelines.CodePipeline(self, "Pipeline",
                self_mutation=False,
                synth=pipelines.ShellStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["npm ci", "npm run build", "npx cdk synth"
                    ]
                )
            )
            
            # Original API
            cloud_assembly_artifact = codepipeline.Artifact()
            original_pipeline = pipelines.CdkPipeline(self, "Pipeline",
                self_mutating=False,
                cloud_assembly_artifact=cloud_assembly_artifact
            )
        '''
        if isinstance(asset_publishing_code_build_defaults, dict):
            asset_publishing_code_build_defaults = CodeBuildOptions(**asset_publishing_code_build_defaults)
        if isinstance(code_build_defaults, dict):
            code_build_defaults = CodeBuildOptions(**code_build_defaults)
        if isinstance(self_mutation_code_build_defaults, dict):
            self_mutation_code_build_defaults = CodeBuildOptions(**self_mutation_code_build_defaults)
        if isinstance(synth_code_build_defaults, dict):
            synth_code_build_defaults = CodeBuildOptions(**synth_code_build_defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5919f25f6a406bdbb4545664160a07a5eb12f43540c7fea542192d0c92d5f06c)
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument asset_publishing_code_build_defaults", value=asset_publishing_code_build_defaults, expected_type=type_hints["asset_publishing_code_build_defaults"])
            check_type(argname="argument cli_version", value=cli_version, expected_type=type_hints["cli_version"])
            check_type(argname="argument code_build_defaults", value=code_build_defaults, expected_type=type_hints["code_build_defaults"])
            check_type(argname="argument code_pipeline", value=code_pipeline, expected_type=type_hints["code_pipeline"])
            check_type(argname="argument cross_account_keys", value=cross_account_keys, expected_type=type_hints["cross_account_keys"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument docker_enabled_for_self_mutation", value=docker_enabled_for_self_mutation, expected_type=type_hints["docker_enabled_for_self_mutation"])
            check_type(argname="argument docker_enabled_for_synth", value=docker_enabled_for_synth, expected_type=type_hints["docker_enabled_for_synth"])
            check_type(argname="argument pipeline_name", value=pipeline_name, expected_type=type_hints["pipeline_name"])
            check_type(argname="argument publish_assets_in_parallel", value=publish_assets_in_parallel, expected_type=type_hints["publish_assets_in_parallel"])
            check_type(argname="argument reuse_cross_region_support_stacks", value=reuse_cross_region_support_stacks, expected_type=type_hints["reuse_cross_region_support_stacks"])
            check_type(argname="argument self_mutation", value=self_mutation, expected_type=type_hints["self_mutation"])
            check_type(argname="argument self_mutation_code_build_defaults", value=self_mutation_code_build_defaults, expected_type=type_hints["self_mutation_code_build_defaults"])
            check_type(argname="argument synth_code_build_defaults", value=synth_code_build_defaults, expected_type=type_hints["synth_code_build_defaults"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "synth": synth,
        }
        if asset_publishing_code_build_defaults is not None:
            self._values["asset_publishing_code_build_defaults"] = asset_publishing_code_build_defaults
        if cli_version is not None:
            self._values["cli_version"] = cli_version
        if code_build_defaults is not None:
            self._values["code_build_defaults"] = code_build_defaults
        if code_pipeline is not None:
            self._values["code_pipeline"] = code_pipeline
        if cross_account_keys is not None:
            self._values["cross_account_keys"] = cross_account_keys
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if docker_enabled_for_self_mutation is not None:
            self._values["docker_enabled_for_self_mutation"] = docker_enabled_for_self_mutation
        if docker_enabled_for_synth is not None:
            self._values["docker_enabled_for_synth"] = docker_enabled_for_synth
        if pipeline_name is not None:
            self._values["pipeline_name"] = pipeline_name
        if publish_assets_in_parallel is not None:
            self._values["publish_assets_in_parallel"] = publish_assets_in_parallel
        if reuse_cross_region_support_stacks is not None:
            self._values["reuse_cross_region_support_stacks"] = reuse_cross_region_support_stacks
        if self_mutation is not None:
            self._values["self_mutation"] = self_mutation
        if self_mutation_code_build_defaults is not None:
            self._values["self_mutation_code_build_defaults"] = self_mutation_code_build_defaults
        if synth_code_build_defaults is not None:
            self._values["synth_code_build_defaults"] = synth_code_build_defaults

    @builtins.property
    def synth(self) -> "IFileSetProducer":
        '''(experimental) The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.

        :stability: experimental
        '''
        result = self._values.get("synth")
        assert result is not None, "Required property 'synth' is missing"
        return typing.cast("IFileSetProducer", result)

    @builtins.property
    def asset_publishing_code_build_defaults(self) -> typing.Optional[CodeBuildOptions]:
        '''(experimental) Additional customizations to apply to the asset publishing CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied

        :stability: experimental
        '''
        result = self._values.get("asset_publishing_code_build_defaults")
        return typing.cast(typing.Optional[CodeBuildOptions], result)

    @builtins.property
    def cli_version(self) -> typing.Optional[builtins.str]:
        '''(experimental) CDK CLI version to use in self-mutation and asset publishing steps.

        If you want to lock the CDK CLI version used in the pipeline, by steps
        that are automatically generated for you, specify the version here.

        We recommend you do not specify this value, as not specifying it always
        uses the latest CLI version which is backwards compatible with old versions.

        If you do specify it, be aware that this version should always be equal to or higher than the
        version of the CDK framework used by the CDK app, when the CDK commands are
        run during your pipeline execution. When you change this version, the *next
        time* the ``SelfMutate`` step runs it will still be using the CLI of the the
        *previous* version that was in this property: it will only start using the
        new version after ``SelfMutate`` completes successfully. That means that if
        you want to update both framework and CLI version, you should update the
        CLI version first, commit, push and deploy, and only then update the
        framework version.

        :default: - Latest version

        :stability: experimental
        '''
        result = self._values.get("cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def code_build_defaults(self) -> typing.Optional[CodeBuildOptions]:
        '''(experimental) Customize the CodeBuild projects created for this pipeline.

        :default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_5_0

        :stability: experimental
        '''
        result = self._values.get("code_build_defaults")
        return typing.cast(typing.Optional[CodeBuildOptions], result)

    @builtins.property
    def code_pipeline(self) -> typing.Optional[_Pipeline_7744fe74]:
        '''(experimental) An existing Pipeline to be reused and built upon.

        [disable-awslint:ref-via-interface]

        :default: - a new underlying pipeline is created.

        :stability: experimental
        '''
        result = self._values.get("code_pipeline")
        return typing.cast(typing.Optional[_Pipeline_7744fe74], result)

    @builtins.property
    def cross_account_keys(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Create KMS keys for the artifact buckets, allowing cross-account deployments.

        The artifact buckets have to be encrypted to support deploying CDK apps to
        another account, so if you want to do that or want to have your artifact
        buckets encrypted, be sure to set this value to ``true``.

        Be aware there is a cost associated with maintaining the KMS keys.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("cross_account_keys")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_credentials(self) -> typing.Optional[typing.List["DockerCredential"]]:
        '''(experimental) A list of credentials used to authenticate to Docker registries.

        Specify any credentials necessary within the pipeline to build, synth, update, or publish assets.

        :default: []

        :stability: experimental
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List["DockerCredential"]], result)

    @builtins.property
    def docker_enabled_for_self_mutation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Docker for the self-mutate step.

        Set this to true if the pipeline itself uses Docker container assets
        (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build
        image of a CodeBuild step in the pipeline).

        You do not need to set it if you build Docker image assets in the
        application Stages and Stacks that are *deployed* by this pipeline.

        Configures privileged mode for the self-mutation CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the Docker asset in the pipeline.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("docker_enabled_for_self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def docker_enabled_for_synth(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Enable Docker for the 'synth' step.

        Set this to true if you are using file assets that require
        "bundling" anywhere in your application (meaning an asset
        compilation step will be run with the tools provided by
        a Docker image), both for the Pipeline stack as well as the
        application stacks.

        A common way to use bundling assets in your application is by
        using the ``@aws-cdk/aws-lambda-nodejs`` library.

        Configures privileged mode for the synth CodeBuild action.

        If you are about to turn this on in an already-deployed Pipeline,
        set the value to ``true`` first, commit and allow the pipeline to
        self-update, and only then use the bundled asset.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("docker_enabled_for_synth")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def pipeline_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the CodePipeline pipeline.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("pipeline_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def publish_assets_in_parallel(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Publish assets in multiple CodeBuild projects.

        If set to false, use one Project per type to publish all assets.

        Publishing in parallel improves concurrency and may reduce publishing
        latency, but may also increase overall provisioning time of the CodeBuild
        projects.

        Experiment and see what value works best for you.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("publish_assets_in_parallel")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def reuse_cross_region_support_stacks(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Reuse the same cross region support stack for all pipelines in the App.

        :default: - true (Use the same support stack for all pipelines in App)

        :stability: experimental
        '''
        result = self._values.get("reuse_cross_region_support_stacks")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether the pipeline will update itself.

        This needs to be set to ``true`` to allow the pipeline to reconfigure
        itself when assets or stages are being added to it, and ``true`` is the
        recommended setting.

        You can temporarily set this to ``false`` while you are iterating
        on the pipeline itself and prefer to deploy changes using ``cdk deploy``.

        :default: true

        :stability: experimental
        '''
        result = self._values.get("self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def self_mutation_code_build_defaults(self) -> typing.Optional[CodeBuildOptions]:
        '''(experimental) Additional customizations to apply to the self mutation CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied

        :stability: experimental
        '''
        result = self._values.get("self_mutation_code_build_defaults")
        return typing.cast(typing.Optional[CodeBuildOptions], result)

    @builtins.property
    def synth_code_build_defaults(self) -> typing.Optional[CodeBuildOptions]:
        '''(experimental) Additional customizations to apply to the synthesize CodeBuild projects.

        :default: - Only ``codeBuildDefaults`` are applied

        :stability: experimental
        '''
        result = self._values.get("synth_code_build_defaults")
        return typing.cast(typing.Optional[CodeBuildOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodePipelineProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.ConnectionSourceOptions",
    jsii_struct_bases=[],
    name_mapping={
        "connection_arn": "connectionArn",
        "code_build_clone_output": "codeBuildCloneOutput",
        "trigger_on_push": "triggerOnPush",
    },
)
class ConnectionSourceOptions:
    def __init__(
        self,
        *,
        connection_arn: builtins.str,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        trigger_on_push: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(experimental) Configuration options for CodeStar source.

        :param connection_arn: (experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this GitHub or BitBucket repository.
        :param code_build_clone_output: (experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files). This provides access to repository history, and retains symlinks (symlinks would otherwise be removed by CodePipeline). **Note**: if this option is true, only CodeBuild jobs can use the output artifact. Default: false
        :param trigger_on_push: (experimental) Controls automatically starting your pipeline when a new commit is made on the configured repository and branch. If unspecified, the default value is true, and the field does not display by default. Default: true

        :stability: experimental
        :exampleMetadata: infused

        Example::

            pipeline = pipelines.CodePipeline(self, "Pipeline",
                synth=pipelines.ShellStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["npm ci", "npm run build", "npx cdk synth"]
                ),
            
                # Turn this on because the pipeline uses Docker image assets
                docker_enabled_for_self_mutation=True
            )
            
            pipeline.add_wave("MyWave",
                post=[
                    pipelines.CodeBuildStep("RunApproval",
                        commands=["command-from-image"],
                        build_environment=cdk.aws_codebuild.BuildEnvironment(
                            # The user of a Docker image asset in the pipeline requires turning on
                            # 'dockerEnabledForSelfMutation'.
                            build_image=codebuild.LinuxBuildImage.from_asset(self, "Image",
                                directory="./docker-image"
                            )
                        )
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d503e56d92e6cc70b17815bbb0d8c54b6ba19e381750270bf4cbdc4bf141792e)
            check_type(argname="argument connection_arn", value=connection_arn, expected_type=type_hints["connection_arn"])
            check_type(argname="argument code_build_clone_output", value=code_build_clone_output, expected_type=type_hints["code_build_clone_output"])
            check_type(argname="argument trigger_on_push", value=trigger_on_push, expected_type=type_hints["trigger_on_push"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "connection_arn": connection_arn,
        }
        if code_build_clone_output is not None:
            self._values["code_build_clone_output"] = code_build_clone_output
        if trigger_on_push is not None:
            self._values["trigger_on_push"] = trigger_on_push

    @builtins.property
    def connection_arn(self) -> builtins.str:
        '''(experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this GitHub or BitBucket repository.

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/connections-create.html
        :stability: experimental

        Example::

            "arn:aws:codestar-connections:us-east-1:123456789012:connection/12345678-abcd-12ab-34cdef5678gh"
        '''
        result = self._values.get("connection_arn")
        assert result is not None, "Required property 'connection_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def code_build_clone_output(self) -> typing.Optional[builtins.bool]:
        '''(experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files).

        This provides access to repository history, and retains symlinks (symlinks would otherwise be
        removed by CodePipeline).

        **Note**: if this option is true, only CodeBuild jobs can use the output artifact.

        :default: false

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html#action-reference-CodestarConnectionSource-config
        :stability: experimental
        '''
        result = self._values.get("code_build_clone_output")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def trigger_on_push(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Controls automatically starting your pipeline when a new commit is made on the configured repository and branch.

        If unspecified,
        the default value is true, and the field does not display by default.

        :default: true

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/action-reference-CodestarConnectionSource.html
        :stability: experimental
        '''
        result = self._values.get("trigger_on_push")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ConnectionSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08)
class DeployCdkStackAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.DeployCdkStackAction",
):
    '''(deprecated) Action to deploy a CDK Stack.

    Adds two CodePipeline Actions to the pipeline: one to create a ChangeSet
    and one to execute it.

    You do not need to instantiate this action yourself -- it will automatically
    be added by the pipeline when you add stack artifacts or entire stages.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import aws_iam as iam
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        # role: iam.Role
        
        deploy_cdk_stack_action = pipelines.DeployCdkStackAction(
            action_role=role,
            cloud_assembly_input=artifact,
            stack_name="stackName",
            template_path="templatePath",
        
            # the properties below are optional
            base_action_name="baseActionName",
            change_set_name="changeSetName",
            cloud_formation_execution_role=role,
            dependency_stack_artifact_ids=["dependencyStackArtifactIds"],
            execute_run_order=123,
            output=artifact,
            output_file_name="outputFileName",
            prepare_run_order=123,
            region="region",
            stack_artifact_id="stackArtifactId",
            template_configuration_path="templateConfigurationPath"
        )
    '''

    def __init__(
        self,
        *,
        action_role: _IRole_59af6f50,
        stack_name: builtins.str,
        template_path: builtins.str,
        cloud_formation_execution_role: typing.Optional[_IRole_59af6f50] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_artifact_id: typing.Optional[builtins.str] = None,
        template_configuration_path: typing.Optional[builtins.str] = None,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''
        :param action_role: (deprecated) Role for the action to assume. This controls the account to deploy into
        :param stack_name: (deprecated) The name of the stack that should be created/updated.
        :param template_path: (deprecated) Relative path of template in the input artifact.
        :param cloud_formation_execution_role: (deprecated) Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: (deprecated) Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: (deprecated) Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: (deprecated) Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked
        :param template_configuration_path: (deprecated) Template configuration path relative to the input artifact. Default: - No template configuration
        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (deprecated) Base name of the action. Default: stackName
        :param change_set_name: (deprecated) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the Prepare action. Default: 1

        :stability: deprecated
        '''
        props = DeployCdkStackActionProps(
            action_role=action_role,
            stack_name=stack_name,
            template_path=template_path,
            cloud_formation_execution_role=cloud_formation_execution_role,
            dependency_stack_artifact_ids=dependency_stack_artifact_ids,
            region=region,
            stack_artifact_id=stack_artifact_id,
            template_configuration_path=template_configuration_path,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="fromStackArtifact")
    @builtins.classmethod
    def from_stack_artifact(
        cls,
        scope: _constructs_77d1e7e8.Construct,
        artifact: _CloudFormationStackArtifact_45074b84,
        *,
        stack_name: typing.Optional[builtins.str] = None,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> "DeployCdkStackAction":
        '''(deprecated) Construct a DeployCdkStackAction from a Stack artifact.

        :param scope: -
        :param artifact: -
        :param stack_name: (deprecated) The name of the stack that should be created/updated. Default: - Same as stack artifact
        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (deprecated) Base name of the action. Default: stackName
        :param change_set_name: (deprecated) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the Prepare action. Default: 1

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e289929d9836be1457a5c52f5c987a6ec8b2b32323befa43844034df9df66c73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
        options = CdkStackActionFromArtifactOptions(
            stack_name=stack_name,
            cloud_assembly_input=cloud_assembly_input,
            base_action_name=base_action_name,
            change_set_name=change_set_name,
            execute_run_order=execute_run_order,
            output=output,
            output_file_name=output_file_name,
            prepare_run_order=prepare_run_order,
        )

        return typing.cast("DeployCdkStackAction", jsii.sinvoke(cls, "fromStackArtifact", [scope, artifact, options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(deprecated) Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c7f13cc7af69642e823b9ae4596283bafc1919d6494c3f27e352c811092eb51)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8d1d5b94df4243d1bf6f32e938a2cd4c01b1368e0d38ef428d55d65870b477b)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''(deprecated) Exists to implement IAction.

        :stability: deprecated
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property
    @jsii.member(jsii_name="dependencyStackArtifactIds")
    def dependency_stack_artifact_ids(self) -> typing.List[builtins.str]:
        '''(deprecated) Artifact ids of the artifact this stack artifact depends on.

        :stability: deprecated
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "dependencyStackArtifactIds"))

    @builtins.property
    @jsii.member(jsii_name="executeRunOrder")
    def execute_run_order(self) -> jsii.Number:
        '''(deprecated) The runorder for the execute action.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "executeRunOrder"))

    @builtins.property
    @jsii.member(jsii_name="prepareRunOrder")
    def prepare_run_order(self) -> jsii.Number:
        '''(deprecated) The runorder for the prepare action.

        :stability: deprecated
        '''
        return typing.cast(jsii.Number, jsii.get(self, "prepareRunOrder"))

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''(deprecated) Name of the deployed stack.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @builtins.property
    @jsii.member(jsii_name="stackArtifactId")
    def stack_artifact_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Artifact id of the artifact this action was based on.

        :stability: deprecated
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "stackArtifactId"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.DeployCdkStackActionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class DeployCdkStackActionOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Customization options for a DeployCdkStackAction.

        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (deprecated) Base name of the action. Default: stackName
        :param change_set_name: (deprecated) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the Prepare action. Default: 1

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            
            deploy_cdk_stack_action_options = pipelines.DeployCdkStackActionOptions(
                cloud_assembly_input=artifact,
            
                # the properties below are optional
                base_action_name="baseActionName",
                change_set_name="changeSetName",
                execute_run_order=123,
                output=artifact,
                output_file_name="outputFileName",
                prepare_run_order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__580643b9e49a8d6b994bcc1390d4e1cc15d22bd68ccf64a036deee5b4c2eef2e)
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument base_action_name", value=base_action_name, expected_type=type_hints["base_action_name"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument execute_run_order", value=execute_run_order, expected_type=type_hints["execute_run_order"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument output_file_name", value=output_file_name, expected_type=type_hints["output_file_name"])
            check_type(argname="argument prepare_run_order", value=prepare_run_order, expected_type=type_hints["prepare_run_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Base name of the action.

        :default: stackName

        :stability: deprecated
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: deprecated
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: deprecated
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: deprecated
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: deprecated
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Prepare action.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.DeployCdkStackActionProps",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "action_role": "actionRole",
        "stack_name": "stackName",
        "template_path": "templatePath",
        "cloud_formation_execution_role": "cloudFormationExecutionRole",
        "dependency_stack_artifact_ids": "dependencyStackArtifactIds",
        "region": "region",
        "stack_artifact_id": "stackArtifactId",
        "template_configuration_path": "templateConfigurationPath",
    },
)
class DeployCdkStackActionProps(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        action_role: _IRole_59af6f50,
        stack_name: builtins.str,
        template_path: builtins.str,
        cloud_formation_execution_role: typing.Optional[_IRole_59af6f50] = None,
        dependency_stack_artifact_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        region: typing.Optional[builtins.str] = None,
        stack_artifact_id: typing.Optional[builtins.str] = None,
        template_configuration_path: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Properties for a DeployCdkStackAction.

        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (deprecated) Base name of the action. Default: stackName
        :param change_set_name: (deprecated) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the Prepare action. Default: 1
        :param action_role: (deprecated) Role for the action to assume. This controls the account to deploy into
        :param stack_name: (deprecated) The name of the stack that should be created/updated.
        :param template_path: (deprecated) Relative path of template in the input artifact.
        :param cloud_formation_execution_role: (deprecated) Role to execute CloudFormation under. Default: - Execute CloudFormation using the action role
        :param dependency_stack_artifact_ids: (deprecated) Artifact ID for the stacks this stack depends on. Used for pipeline order checking. Default: - No dependencies
        :param region: (deprecated) Region to deploy into. Default: - Same region as pipeline
        :param stack_artifact_id: (deprecated) Artifact ID for the stack deployed here. Used for pipeline order checking. Default: - Order will not be checked
        :param template_configuration_path: (deprecated) Template configuration path relative to the input artifact. Default: - No template configuration

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_iam as iam
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # role: iam.Role
            
            deploy_cdk_stack_action_props = pipelines.DeployCdkStackActionProps(
                action_role=role,
                cloud_assembly_input=artifact,
                stack_name="stackName",
                template_path="templatePath",
            
                # the properties below are optional
                base_action_name="baseActionName",
                change_set_name="changeSetName",
                cloud_formation_execution_role=role,
                dependency_stack_artifact_ids=["dependencyStackArtifactIds"],
                execute_run_order=123,
                output=artifact,
                output_file_name="outputFileName",
                prepare_run_order=123,
                region="region",
                stack_artifact_id="stackArtifactId",
                template_configuration_path="templateConfigurationPath"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798f30cdb14e8e151292faf76d49af4b82a70ce48063d5e71e1e05e701577e55)
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument base_action_name", value=base_action_name, expected_type=type_hints["base_action_name"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument execute_run_order", value=execute_run_order, expected_type=type_hints["execute_run_order"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument output_file_name", value=output_file_name, expected_type=type_hints["output_file_name"])
            check_type(argname="argument prepare_run_order", value=prepare_run_order, expected_type=type_hints["prepare_run_order"])
            check_type(argname="argument action_role", value=action_role, expected_type=type_hints["action_role"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument template_path", value=template_path, expected_type=type_hints["template_path"])
            check_type(argname="argument cloud_formation_execution_role", value=cloud_formation_execution_role, expected_type=type_hints["cloud_formation_execution_role"])
            check_type(argname="argument dependency_stack_artifact_ids", value=dependency_stack_artifact_ids, expected_type=type_hints["dependency_stack_artifact_ids"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument stack_artifact_id", value=stack_artifact_id, expected_type=type_hints["stack_artifact_id"])
            check_type(argname="argument template_configuration_path", value=template_configuration_path, expected_type=type_hints["template_configuration_path"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
            "action_role": action_role,
            "stack_name": stack_name,
            "template_path": template_path,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if cloud_formation_execution_role is not None:
            self._values["cloud_formation_execution_role"] = cloud_formation_execution_role
        if dependency_stack_artifact_ids is not None:
            self._values["dependency_stack_artifact_ids"] = dependency_stack_artifact_ids
        if region is not None:
            self._values["region"] = region
        if stack_artifact_id is not None:
            self._values["stack_artifact_id"] = stack_artifact_id
        if template_configuration_path is not None:
            self._values["template_configuration_path"] = template_configuration_path

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Base name of the action.

        :default: stackName

        :stability: deprecated
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: deprecated
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: deprecated
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: deprecated
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: deprecated
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Prepare action.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def action_role(self) -> _IRole_59af6f50:
        '''(deprecated) Role for the action to assume.

        This controls the account to deploy into

        :stability: deprecated
        '''
        result = self._values.get("action_role")
        assert result is not None, "Required property 'action_role' is missing"
        return typing.cast(_IRole_59af6f50, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(deprecated) The name of the stack that should be created/updated.

        :stability: deprecated
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def template_path(self) -> builtins.str:
        '''(deprecated) Relative path of template in the input artifact.

        :stability: deprecated
        '''
        result = self._values.get("template_path")
        assert result is not None, "Required property 'template_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def cloud_formation_execution_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(deprecated) Role to execute CloudFormation under.

        :default: - Execute CloudFormation using the action role

        :stability: deprecated
        '''
        result = self._values.get("cloud_formation_execution_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def dependency_stack_artifact_ids(
        self,
    ) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Artifact ID for the stacks this stack depends on.

        Used for pipeline order checking.

        :default: - No dependencies

        :stability: deprecated
        '''
        result = self._values.get("dependency_stack_artifact_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Region to deploy into.

        :default: - Same region as pipeline

        :stability: deprecated
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def stack_artifact_id(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Artifact ID for the stack deployed here.

        Used for pipeline order checking.

        :default: - Order will not be checked

        :stability: deprecated
        '''
        result = self._values.get("stack_artifact_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def template_configuration_path(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Template configuration path relative to the input artifact.

        :default: - No template configuration

        :stability: deprecated
        '''
        result = self._values.get("template_configuration_path")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeployCdkStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerCredential(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.pipelines.DockerCredential",
):
    '''(experimental) Represents credentials used to access a Docker registry.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(self, "DHSecret", "arn:aws:...")
        custom_reg_secret = secretsmanager.Secret.from_secret_complete_arn(self, "CRSecret", "arn:aws:...")
        repo1 = ecr.Repository.from_repository_arn(self, "Repo", "arn:aws:ecr:eu-west-1:0123456789012:repository/Repo1")
        repo2 = ecr.Repository.from_repository_arn(self, "Repo", "arn:aws:ecr:eu-west-1:0123456789012:repository/Repo2")
        
        pipeline = pipelines.CodePipeline(self, "Pipeline",
            docker_credentials=[
                pipelines.DockerCredential.docker_hub(docker_hub_secret),
                pipelines.DockerCredential.custom_registry("dockerregistry.example.com", custom_reg_secret),
                pipelines.DockerCredential.ecr([repo1, repo2])
            ],
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["npm ci", "npm run build", "npx cdk synth"]
            )
        )
    '''

    def __init__(
        self,
        usages: typing.Optional[typing.Sequence["DockerCredentialUsage"]] = None,
    ) -> None:
        '''
        :param usages: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5e76ae688baeaaddaa7fa9734504f555938deb1a93526f10f3f13dfaee2b8b6c)
            check_type(argname="argument usages", value=usages, expected_type=type_hints["usages"])
        jsii.create(self.__class__, self, [usages])

    @jsii.member(jsii_name="customRegistry")
    @builtins.classmethod
    def custom_registry(
        cls,
        registry_domain: builtins.str,
        secret: _ISecret_22fb8757,
        *,
        assume_role: typing.Optional[_IRole_59af6f50] = None,
        secret_password_field: typing.Optional[builtins.str] = None,
        secret_username_field: typing.Optional[builtins.str] = None,
        usages: typing.Optional[typing.Sequence["DockerCredentialUsage"]] = None,
    ) -> "DockerCredential":
        '''(experimental) Creates a DockerCredential for a registry, based on its domain name (e.g., 'www.example.com').

        :param registry_domain: -
        :param secret: -
        :param assume_role: (experimental) An IAM role to assume prior to accessing the secret. Default: - none. The current execution role will be used.
        :param secret_password_field: (experimental) The name of the JSON field of the secret which contains the secret/password. Default: 'secret'
        :param secret_username_field: (experimental) The name of the JSON field of the secret which contains the user/login name. Default: 'username'
        :param usages: (experimental) Defines which stages of the pipeline should be granted access to these credentials. Default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__500861ffeb59a40b6a53b015db083a8adeb677084ce60b91789661aa8cbdffaa)
            check_type(argname="argument registry_domain", value=registry_domain, expected_type=type_hints["registry_domain"])
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        opts = ExternalDockerCredentialOptions(
            assume_role=assume_role,
            secret_password_field=secret_password_field,
            secret_username_field=secret_username_field,
            usages=usages,
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "customRegistry", [registry_domain, secret, opts]))

    @jsii.member(jsii_name="dockerHub")
    @builtins.classmethod
    def docker_hub(
        cls,
        secret: _ISecret_22fb8757,
        *,
        assume_role: typing.Optional[_IRole_59af6f50] = None,
        secret_password_field: typing.Optional[builtins.str] = None,
        secret_username_field: typing.Optional[builtins.str] = None,
        usages: typing.Optional[typing.Sequence["DockerCredentialUsage"]] = None,
    ) -> "DockerCredential":
        '''(experimental) Creates a DockerCredential for DockerHub.

        Convenience method for ``customRegistry('https://index.docker.io/v1/', opts)``.

        :param secret: -
        :param assume_role: (experimental) An IAM role to assume prior to accessing the secret. Default: - none. The current execution role will be used.
        :param secret_password_field: (experimental) The name of the JSON field of the secret which contains the secret/password. Default: 'secret'
        :param secret_username_field: (experimental) The name of the JSON field of the secret which contains the user/login name. Default: 'username'
        :param usages: (experimental) Defines which stages of the pipeline should be granted access to these credentials. Default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8acf161909cdbe772a62d7e23bb291d0e182ef3b916887f5ec841bd3d6b03e5)
            check_type(argname="argument secret", value=secret, expected_type=type_hints["secret"])
        opts = ExternalDockerCredentialOptions(
            assume_role=assume_role,
            secret_password_field=secret_password_field,
            secret_username_field=secret_username_field,
            usages=usages,
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "dockerHub", [secret, opts]))

    @jsii.member(jsii_name="ecr")
    @builtins.classmethod
    def ecr(
        cls,
        repositories: typing.Sequence[_IRepository_8b4d2894],
        *,
        assume_role: typing.Optional[_IRole_59af6f50] = None,
        usages: typing.Optional[typing.Sequence["DockerCredentialUsage"]] = None,
    ) -> "DockerCredential":
        '''(experimental) Creates a DockerCredential for one or more ECR repositories.

        NOTE - All ECR repositories in the same account and region share a domain name
        (e.g., 0123456789012.dkr.ecr.eu-west-1.amazonaws.com), and can only have one associated
        set of credentials (and DockerCredential). Attempting to associate one set of credentials
        with one ECR repo and another with another ECR repo in the same account and region will
        result in failures when using these credentials in the pipeline.

        :param repositories: -
        :param assume_role: (experimental) An IAM role to assume prior to accessing the secret. Default: - none. The current execution role will be used.
        :param usages: (experimental) Defines which stages of the pipeline should be granted access to these credentials. Default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7889ac91b601338be20c192d3dc6673fd9f2b011a31f5d49177c721aea12776d)
            check_type(argname="argument repositories", value=repositories, expected_type=type_hints["repositories"])
        opts = EcrDockerCredentialOptions(assume_role=assume_role, usages=usages)

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "ecr", [repositories, opts]))

    @jsii.member(jsii_name="grantRead")
    @abc.abstractmethod
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        usage: "DockerCredentialUsage",
    ) -> None:
        '''(experimental) Grant read-only access to the registry credentials.

        This grants read access to any secrets, and pull access to any repositories.

        :param grantee: -
        :param usage: -

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="usages")
    def _usages(self) -> typing.Optional[typing.List["DockerCredentialUsage"]]:
        '''
        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List["DockerCredentialUsage"]], jsii.get(self, "usages"))


class _DockerCredentialProxy(DockerCredential):
    @jsii.member(jsii_name="grantRead")
    def grant_read(
        self,
        grantee: _IGrantable_4c5a91d1,
        usage: "DockerCredentialUsage",
    ) -> None:
        '''(experimental) Grant read-only access to the registry credentials.

        This grants read access to any secrets, and pull access to any repositories.

        :param grantee: -
        :param usage: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__77881d6b41b1c44c8d52604541b28a60f92ad1cc2c96066592145107244f5d3d)
            check_type(argname="argument grantee", value=grantee, expected_type=type_hints["grantee"])
            check_type(argname="argument usage", value=usage, expected_type=type_hints["usage"])
        return typing.cast(None, jsii.invoke(self, "grantRead", [grantee, usage]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, DockerCredential).__jsii_proxy_class__ = lambda : _DockerCredentialProxy


@jsii.enum(jsii_type="monocdk.pipelines.DockerCredentialUsage")
class DockerCredentialUsage(enum.Enum):
    '''(experimental) Defines which stages of a pipeline require the specified credentials.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(self, "DHSecret", "arn:aws:...")
        # Only the image asset publishing actions will be granted read access to the secret.
        creds = pipelines.DockerCredential.docker_hub(docker_hub_secret, usages=[pipelines.DockerCredentialUsage.ASSET_PUBLISHING])
    '''

    SYNTH = "SYNTH"
    '''(experimental) Synth/Build.

    :stability: experimental
    '''
    SELF_UPDATE = "SELF_UPDATE"
    '''(experimental) Self-update.

    :stability: experimental
    '''
    ASSET_PUBLISHING = "ASSET_PUBLISHING"
    '''(experimental) Asset publishing.

    :stability: experimental
    '''


@jsii.data_type(
    jsii_type="monocdk.pipelines.ECRSourceOptions",
    jsii_struct_bases=[],
    name_mapping={"action_name": "actionName", "image_tag": "imageTag"},
)
class ECRSourceOptions:
    def __init__(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for ECR sources.

        :param action_name: (experimental) The action name used for this source in the CodePipeline. Default: - The repository name
        :param image_tag: (experimental) The image tag that will be checked for changes. Default: latest

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # repository: ecr.IRepository
            
            pipelines.CodePipelineSource.ecr(repository,
                image_tag="latest"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f3ff22db6310dd4291743f33e7f7cbd2963aaff8816b0f0795c0f67f4aa9a4f7)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument image_tag", value=image_tag, expected_type=type_hints["image_tag"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if image_tag is not None:
            self._values["image_tag"] = image_tag

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The action name used for this source in the CodePipeline.

        :default: - The repository name

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def image_tag(self) -> typing.Optional[builtins.str]:
        '''(experimental) The image tag that will be checked for changes.

        :default: latest

        :stability: experimental
        '''
        result = self._values.get("image_tag")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ECRSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.EcrDockerCredentialOptions",
    jsii_struct_bases=[],
    name_mapping={"assume_role": "assumeRole", "usages": "usages"},
)
class EcrDockerCredentialOptions:
    def __init__(
        self,
        *,
        assume_role: typing.Optional[_IRole_59af6f50] = None,
        usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
    ) -> None:
        '''(experimental) Options for defining access for a Docker Credential composed of ECR repos.

        :param assume_role: (experimental) An IAM role to assume prior to accessing the secret. Default: - none. The current execution role will be used.
        :param usages: (experimental) Defines which stages of the pipeline should be granted access to these credentials. Default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_iam as iam
            from monocdk import pipelines
            
            # role: iam.Role
            
            ecr_docker_credential_options = pipelines.EcrDockerCredentialOptions(
                assume_role=role,
                usages=[pipelines.DockerCredentialUsage.SYNTH]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8645702d045218b4bdadcf05a41b11f8b20878e58f88c246168c0b9bd54bc15)
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument usages", value=usages, expected_type=type_hints["usages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if usages is not None:
            self._values["usages"] = usages

    @builtins.property
    def assume_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) An IAM role to assume prior to accessing the secret.

        :default: - none. The current execution role will be used.

        :stability: experimental
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def usages(self) -> typing.Optional[typing.List[DockerCredentialUsage]]:
        '''(experimental) Defines which stages of the pipeline should be granted access to these credentials.

        :default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        '''
        result = self._values.get("usages")
        return typing.cast(typing.Optional[typing.List[DockerCredentialUsage]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EcrDockerCredentialOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.ExternalDockerCredentialOptions",
    jsii_struct_bases=[],
    name_mapping={
        "assume_role": "assumeRole",
        "secret_password_field": "secretPasswordField",
        "secret_username_field": "secretUsernameField",
        "usages": "usages",
    },
)
class ExternalDockerCredentialOptions:
    def __init__(
        self,
        *,
        assume_role: typing.Optional[_IRole_59af6f50] = None,
        secret_password_field: typing.Optional[builtins.str] = None,
        secret_username_field: typing.Optional[builtins.str] = None,
        usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
    ) -> None:
        '''(experimental) Options for defining credentials for a Docker Credential.

        :param assume_role: (experimental) An IAM role to assume prior to accessing the secret. Default: - none. The current execution role will be used.
        :param secret_password_field: (experimental) The name of the JSON field of the secret which contains the secret/password. Default: 'secret'
        :param secret_username_field: (experimental) The name of the JSON field of the secret which contains the user/login name. Default: 'username'
        :param usages: (experimental) Defines which stages of the pipeline should be granted access to these credentials. Default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            docker_hub_secret = secretsmanager.Secret.from_secret_complete_arn(self, "DHSecret", "arn:aws:...")
            # Only the image asset publishing actions will be granted read access to the secret.
            creds = pipelines.DockerCredential.docker_hub(docker_hub_secret, usages=[pipelines.DockerCredentialUsage.ASSET_PUBLISHING])
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__67479b6a052b7d47efe89a76048dac1dbe326d8bc870d70421741e1d137f2d0f)
            check_type(argname="argument assume_role", value=assume_role, expected_type=type_hints["assume_role"])
            check_type(argname="argument secret_password_field", value=secret_password_field, expected_type=type_hints["secret_password_field"])
            check_type(argname="argument secret_username_field", value=secret_username_field, expected_type=type_hints["secret_username_field"])
            check_type(argname="argument usages", value=usages, expected_type=type_hints["usages"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if assume_role is not None:
            self._values["assume_role"] = assume_role
        if secret_password_field is not None:
            self._values["secret_password_field"] = secret_password_field
        if secret_username_field is not None:
            self._values["secret_username_field"] = secret_username_field
        if usages is not None:
            self._values["usages"] = usages

    @builtins.property
    def assume_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) An IAM role to assume prior to accessing the secret.

        :default: - none. The current execution role will be used.

        :stability: experimental
        '''
        result = self._values.get("assume_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def secret_password_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the JSON field of the secret which contains the secret/password.

        :default: 'secret'

        :stability: experimental
        '''
        result = self._values.get("secret_password_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_username_field(self) -> typing.Optional[builtins.str]:
        '''(experimental) The name of the JSON field of the secret which contains the user/login name.

        :default: 'username'

        :stability: experimental
        '''
        result = self._values.get("secret_username_field")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def usages(self) -> typing.Optional[typing.List[DockerCredentialUsage]]:
        '''(experimental) Defines which stages of the pipeline should be granted access to these credentials.

        :default: - all relevant stages (synth, self-update, asset publishing) are granted access.

        :stability: experimental
        '''
        result = self._values.get("usages")
        return typing.cast(typing.Optional[typing.List[DockerCredentialUsage]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDockerCredentialOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.FileSetLocation",
    jsii_struct_bases=[],
    name_mapping={"directory": "directory", "file_set": "fileSet"},
)
class FileSetLocation:
    def __init__(self, *, directory: builtins.str, file_set: "FileSet") -> None:
        '''(experimental) Location of a FileSet consumed or produced by a ShellStep.

        :param directory: (experimental) The (relative) directory where the FileSet is found.
        :param file_set: (experimental) The FileSet object.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            # file_set: pipelines.FileSet
            
            file_set_location = pipelines.FileSetLocation(
                directory="directory",
                file_set=file_set
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__44274088f5e1908d0356a1eeb98202c75e3be05060c87ac54d8c93a0242fc874)
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
            check_type(argname="argument file_set", value=file_set, expected_type=type_hints["file_set"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "directory": directory,
            "file_set": file_set,
        }

    @builtins.property
    def directory(self) -> builtins.str:
        '''(experimental) The (relative) directory where the FileSet is found.

        :stability: experimental
        '''
        result = self._values.get("directory")
        assert result is not None, "Required property 'directory' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def file_set(self) -> "FileSet":
        '''(experimental) The FileSet object.

        :stability: experimental
        '''
        result = self._values.get("file_set")
        assert result is not None, "Required property 'file_set' is missing"
        return typing.cast("FileSet", result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FileSetLocation(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.FromStackArtifactOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
    },
)
class FromStackArtifactOptions:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(deprecated) Options for CdkDeployAction.fromStackArtifact.

        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the 2 actions that will be created. Default: 1

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            
            from_stack_artifact_options = pipelines.FromStackArtifactOptions(
                cloud_assembly_input=artifact,
            
                # the properties below are optional
                execute_run_order=123,
                output=artifact,
                output_file_name="outputFileName",
                prepare_run_order=123
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59e72826ad96fd840e207fca89ae680da762de7b812dcd831ee6be2535727c9d)
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument execute_run_order", value=execute_run_order, expected_type=type_hints["execute_run_order"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument output_file_name", value=output_file_name, expected_type=type_hints["output_file_name"])
            check_type(argname="argument prepare_run_order", value=prepare_run_order, expected_type=type_hints["prepare_run_order"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: deprecated
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: deprecated
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: deprecated
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the 2 actions that will be created.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "FromStackArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.GitHubSourceOptions",
    jsii_struct_bases=[],
    name_mapping={"authentication": "authentication", "trigger": "trigger"},
)
class GitHubSourceOptions:
    def __init__(
        self,
        *,
        authentication: typing.Optional[_SecretValue_c18506ef] = None,
        trigger: typing.Optional[_GitHubTrigger_0a61ded3] = None,
    ) -> None:
        '''(experimental) Options for GitHub sources.

        :param authentication: (experimental) A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token:: const oauth = cdk.SecretValue.secretsManager('my-github-token'); The GitHub Personal Access Token should have these scopes: - **repo** - to read the repository - **admin:repo_hook** - if you plan to use webhooks (true by default) Default: - SecretValue.secretsManager('github-token')
        :param trigger: (experimental) How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action. With "POLL", CodePipeline periodically checks the source for changes. With "None", the action is not triggered through changes in the source. To use ``WEBHOOK``, your GitHub Personal Access Token should have **admin:repo_hook** scope (in addition to the regular **repo** scope). Default: GitHubTrigger.WEBHOOK

        :stability: experimental
        :exampleMetadata: infused

        Example::

            pipelines.CodePipelineSource.git_hub("org/repo", "branch",
                # This is optional
                authentication=cdk.SecretValue.secrets_manager("my-token")
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1307a9d666c3054703688c68914c5dbffb3aa27bad41a54e05a5484eebc6eaff)
            check_type(argname="argument authentication", value=authentication, expected_type=type_hints["authentication"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if authentication is not None:
            self._values["authentication"] = authentication
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def authentication(self) -> typing.Optional[_SecretValue_c18506ef]:
        '''(experimental) A GitHub OAuth token to use for authentication.

        It is recommended to use a Secrets Manager ``Secret`` to obtain the token::

           oauth = cdk.SecretValue.secrets_manager("my-github-token")

        The GitHub Personal Access Token should have these scopes:

        - **repo** - to read the repository
        - **admin:repo_hook** - if you plan to use webhooks (true by default)

        :default: - SecretValue.secretsManager('github-token')

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/GitHub-create-personal-token-CLI.html
        :stability: experimental
        '''
        result = self._values.get("authentication")
        return typing.cast(typing.Optional[_SecretValue_c18506ef], result)

    @builtins.property
    def trigger(self) -> typing.Optional[_GitHubTrigger_0a61ded3]:
        '''(experimental) How AWS CodePipeline should be triggered.

        With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action.
        With "POLL", CodePipeline periodically checks the source for changes.
        With "None", the action is not triggered through changes in the source.

        To use ``WEBHOOK``, your GitHub Personal Access Token should have
        **admin:repo_hook** scope (in addition to the regular **repo** scope).

        :default: GitHubTrigger.WEBHOOK

        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional[_GitHubTrigger_0a61ded3], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.interface(jsii_type="monocdk.pipelines.ICodePipelineActionFactory")
class ICodePipelineActionFactory(typing_extensions.Protocol):
    '''(experimental) Factory for explicit CodePipeline Actions.

    If you have specific types of Actions you want to add to a
    CodePipeline, write a subclass of ``Step`` that implements this
    interface, and add the action or actions you want in the ``produce`` method.

    There needs to be a level of indirection here, because some aspects of the
    Action creation need to be controlled by the workflow engine (name and
    runOrder). All the rest of the properties are controlled by the factory.

    :stability: experimental
    '''

    @jsii.member(jsii_name="produceAction")
    def produce_action(
        self,
        stage: _IStage_5a7e7342,
        *,
        action_name: builtins.str,
        artifacts: ArtifactMap,
        pipeline: "CodePipeline",
        run_order: jsii.Number,
        scope: _constructs_77d1e7e8.Construct,
        before_self_mutation: typing.Optional[builtins.bool] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> CodePipelineActionFactoryResult:
        '''(experimental) Create the desired Action and add it to the pipeline.

        :param stage: -
        :param action_name: (experimental) Name the action should get.
        :param artifacts: (experimental) Helper object to translate FileSets to CodePipeline Artifacts.
        :param pipeline: (experimental) The pipeline the action is being generated for.
        :param run_order: (experimental) RunOrder the action should get.
        :param scope: (experimental) Scope in which to create constructs.
        :param before_self_mutation: (experimental) Whether or not this action is inserted before self mutation. If it is, the action should take care to reflect some part of its own definition in the pipeline action definition, to trigger a restart after self-mutation (if necessary). Default: false
        :param code_build_defaults: (experimental) If this action factory creates a CodeBuild step, default options to inherit. Default: - No CodeBuild project defaults
        :param fallback_artifact: (experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use. CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If the Project doesn't actually care about its input (it can be anything), it can use the Artifact passed here. Default: - A fallback artifact does not exist
        :param variables_namespace: (experimental) If this step is producing outputs, the variables namespace assigned to it. Pass this on to the Action you are creating. Default: - Step doesn't produce any outputs

        :stability: experimental
        '''
        ...


class _ICodePipelineActionFactoryProxy:
    '''(experimental) Factory for explicit CodePipeline Actions.

    If you have specific types of Actions you want to add to a
    CodePipeline, write a subclass of ``Step`` that implements this
    interface, and add the action or actions you want in the ``produce`` method.

    There needs to be a level of indirection here, because some aspects of the
    Action creation need to be controlled by the workflow engine (name and
    runOrder). All the rest of the properties are controlled by the factory.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.pipelines.ICodePipelineActionFactory"

    @jsii.member(jsii_name="produceAction")
    def produce_action(
        self,
        stage: _IStage_5a7e7342,
        *,
        action_name: builtins.str,
        artifacts: ArtifactMap,
        pipeline: "CodePipeline",
        run_order: jsii.Number,
        scope: _constructs_77d1e7e8.Construct,
        before_self_mutation: typing.Optional[builtins.bool] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> CodePipelineActionFactoryResult:
        '''(experimental) Create the desired Action and add it to the pipeline.

        :param stage: -
        :param action_name: (experimental) Name the action should get.
        :param artifacts: (experimental) Helper object to translate FileSets to CodePipeline Artifacts.
        :param pipeline: (experimental) The pipeline the action is being generated for.
        :param run_order: (experimental) RunOrder the action should get.
        :param scope: (experimental) Scope in which to create constructs.
        :param before_self_mutation: (experimental) Whether or not this action is inserted before self mutation. If it is, the action should take care to reflect some part of its own definition in the pipeline action definition, to trigger a restart after self-mutation (if necessary). Default: false
        :param code_build_defaults: (experimental) If this action factory creates a CodeBuild step, default options to inherit. Default: - No CodeBuild project defaults
        :param fallback_artifact: (experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use. CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If the Project doesn't actually care about its input (it can be anything), it can use the Artifact passed here. Default: - A fallback artifact does not exist
        :param variables_namespace: (experimental) If this step is producing outputs, the variables namespace assigned to it. Pass this on to the Action you are creating. Default: - Step doesn't produce any outputs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65adb69ac9d1c05d47c8eb8994f4f7a62111b5272eb0de742efece996c3ff43b)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = ProduceActionOptions(
            action_name=action_name,
            artifacts=artifacts,
            pipeline=pipeline,
            run_order=run_order,
            scope=scope,
            before_self_mutation=before_self_mutation,
            code_build_defaults=code_build_defaults,
            fallback_artifact=fallback_artifact,
            variables_namespace=variables_namespace,
        )

        return typing.cast(CodePipelineActionFactoryResult, jsii.invoke(self, "produceAction", [stage, options]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, ICodePipelineActionFactory).__jsii_proxy_class__ = lambda : _ICodePipelineActionFactoryProxy


@jsii.interface(jsii_type="monocdk.pipelines.IFileSetProducer")
class IFileSetProducer(typing_extensions.Protocol):
    '''(experimental) Any class that produces, or is itself, a ``FileSet``.

    Steps implicitly produce a primary FileSet as an output.

    :stability: experimental
    '''

    @builtins.property
    @jsii.member(jsii_name="primaryOutput")
    def primary_output(self) -> typing.Optional["FileSet"]:
        '''(experimental) The ``FileSet`` produced by this file set producer.

        :default: - This producer doesn't produce any file set

        :stability: experimental
        '''
        ...


class _IFileSetProducerProxy:
    '''(experimental) Any class that produces, or is itself, a ``FileSet``.

    Steps implicitly produce a primary FileSet as an output.

    :stability: experimental
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.pipelines.IFileSetProducer"

    @builtins.property
    @jsii.member(jsii_name="primaryOutput")
    def primary_output(self) -> typing.Optional["FileSet"]:
        '''(experimental) The ``FileSet`` produced by this file set producer.

        :default: - This producer doesn't produce any file set

        :stability: experimental
        '''
        return typing.cast(typing.Optional["FileSet"], jsii.get(self, "primaryOutput"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IFileSetProducer).__jsii_proxy_class__ = lambda : _IFileSetProducerProxy


@jsii.interface(jsii_type="monocdk.pipelines.IStageHost")
class IStageHost(typing_extensions.Protocol):
    '''(deprecated) Features that the Stage needs from its environment.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    '''

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_publishing_role_arn: builtins.str,
        asset_selector: builtins.str,
        asset_type: AssetType,
    ) -> None:
        '''(deprecated) Make sure all the assets from the given manifest are published.

        :param asset_id: (deprecated) Asset identifier.
        :param asset_manifest_path: (deprecated) Asset manifest path.
        :param asset_publishing_role_arn: (deprecated) ARN of the IAM Role used to publish this asset.
        :param asset_selector: (deprecated) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (deprecated) Type of asset to publish.

        :stability: deprecated
        '''
        ...

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self,
        stack_artifact_id: builtins.str,
    ) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        :stability: deprecated
        '''
        ...


class _IStageHostProxy:
    '''(deprecated) Features that the Stage needs from its environment.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    '''

    __jsii_type__: typing.ClassVar[str] = "monocdk.pipelines.IStageHost"

    @jsii.member(jsii_name="publishAsset")
    def publish_asset(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_publishing_role_arn: builtins.str,
        asset_selector: builtins.str,
        asset_type: AssetType,
    ) -> None:
        '''(deprecated) Make sure all the assets from the given manifest are published.

        :param asset_id: (deprecated) Asset identifier.
        :param asset_manifest_path: (deprecated) Asset manifest path.
        :param asset_publishing_role_arn: (deprecated) ARN of the IAM Role used to publish this asset.
        :param asset_selector: (deprecated) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (deprecated) Type of asset to publish.

        :stability: deprecated
        '''
        command = AssetPublishingCommand(
            asset_id=asset_id,
            asset_manifest_path=asset_manifest_path,
            asset_publishing_role_arn=asset_publishing_role_arn,
            asset_selector=asset_selector,
            asset_type=asset_type,
        )

        return typing.cast(None, jsii.invoke(self, "publishAsset", [command]))

    @jsii.member(jsii_name="stackOutputArtifact")
    def stack_output_artifact(
        self,
        stack_artifact_id: builtins.str,
    ) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Return the Artifact the given stack has to emit its outputs into, if any.

        :param stack_artifact_id: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72651e1cd8c36fc3f2b7264c158060cf2a92d6b76466ad147679d7865920bfcd)
            check_type(argname="argument stack_artifact_id", value=stack_artifact_id, expected_type=type_hints["stack_artifact_id"])
        return typing.cast(typing.Optional[_Artifact_9905eec2], jsii.invoke(self, "stackOutputArtifact", [stack_artifact_id]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IStageHost).__jsii_proxy_class__ = lambda : _IStageHostProxy


@jsii.data_type(
    jsii_type="monocdk.pipelines.ManualApprovalStepProps",
    jsii_struct_bases=[],
    name_mapping={"comment": "comment"},
)
class ManualApprovalStepProps:
    def __init__(self, *, comment: typing.Optional[builtins.str] = None) -> None:
        '''(experimental) Construction properties for a ``ManualApprovalStep``.

        :param comment: (experimental) The comment to display with this manual approval. Default: - No comment

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            manual_approval_step_props = pipelines.ManualApprovalStepProps(
                comment="comment"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4407d3d9237c8acef0cb985742f530d6193ef57265c488c3f4951bf1e53e4b67)
            check_type(argname="argument comment", value=comment, expected_type=type_hints["comment"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if comment is not None:
            self._values["comment"] = comment

    @builtins.property
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The comment to display with this manual approval.

        :default: - No comment

        :stability: experimental
        '''
        result = self._values.get("comment")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ManualApprovalStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.PermissionsBroadeningCheckProps",
    jsii_struct_bases=[],
    name_mapping={"stage": "stage", "notification_topic": "notificationTopic"},
)
class PermissionsBroadeningCheckProps:
    def __init__(
        self,
        *,
        stage: _Stage_9729985a,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''(experimental) Properties for a ``PermissionsBroadeningCheck``.

        :param stage: (experimental) The CDK Stage object to check the stacks of. This should be the same Stage object you are passing to ``addStage()``.
        :param notification_topic: (experimental) Topic to send notifications when a human needs to give manual confirmation. Default: - no notification

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # pipeline: pipelines.CodePipeline
            
            stage = MyApplicationStage(self, "MyApplication")
            pipeline.add_stage(stage,
                pre=[
                    pipelines.ConfirmPermissionsBroadening("Check", stage=stage)
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__de137c3eea148a4e5a972cbfe48d1491c82ed2763990b7a357ec2e199734ca5c)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
            check_type(argname="argument notification_topic", value=notification_topic, expected_type=type_hints["notification_topic"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stage": stage,
        }
        if notification_topic is not None:
            self._values["notification_topic"] = notification_topic

    @builtins.property
    def stage(self) -> _Stage_9729985a:
        '''(experimental) The CDK Stage object to check the stacks of.

        This should be the same Stage object you are passing to ``addStage()``.

        :stability: experimental
        '''
        result = self._values.get("stage")
        assert result is not None, "Required property 'stage' is missing"
        return typing.cast(_Stage_9729985a, result)

    @builtins.property
    def notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(experimental) Topic to send notifications when a human needs to give manual confirmation.

        :default: - no notification

        :stability: experimental
        '''
        result = self._values.get("notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PermissionsBroadeningCheckProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class PipelineBase(
    _Construct_e78e779f,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.pipelines.PipelineBase",
):
    '''(experimental) A generic CDK Pipelines pipeline.

    Different deployment systems will provide subclasses of ``Pipeline`` that generate
    the deployment infrastructure necessary to deploy CDK apps, specific to that system.

    This library comes with the ``CodePipeline`` class, which uses AWS CodePipeline
    to deploy CDK apps.

    The actual pipeline infrastructure is constructed (by invoking the engine)
    when ``buildPipeline()`` is called, or when ``app.synth()`` is called (whichever
    happens first).

    :stability: experimental
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        synth: IFileSetProducer,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param synth: (experimental) The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ebd565b4d620f66756c14cd03cfdd7fbabf44f60b27e556dcbc563303c2abb50)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PipelineBaseProps(synth=synth)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _Stage_9729985a,
        *,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union["StackSteps", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> "StageDeployment":
        '''(experimental) Deploy a single Stage by itself.

        Add a Stage to the pipeline, to be deployed in sequence with other
        Stages added to the pipeline. All Stacks in the stage will be deployed
        in an order automatically determined by their relative dependencies.

        :param stage: -
        :param post: (experimental) Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: (experimental) Instructions for stack level steps. Default: - No additional instructions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92803ad9223ee20ab44b2af82f86d4f006db21e2a4a55f09ac87c15b6afd5552)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = AddStageOpts(post=post, pre=pre, stack_steps=stack_steps)

        return typing.cast("StageDeployment", jsii.invoke(self, "addStage", [stage, options]))

    @jsii.member(jsii_name="addWave")
    def add_wave(
        self,
        id: builtins.str,
        *,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
    ) -> "Wave":
        '''(experimental) Add a Wave to the pipeline, for deploying multiple Stages in parallel.

        Use the return object of this method to deploy multiple stages in parallel.

        Example::

           # pipeline: pipelines.CodePipeline


           wave = pipeline.add_wave("MyWave")
           wave.add_stage(MyApplicationStage(self, "Stage1"))
           wave.add_stage(MyApplicationStage(self, "Stage2"))

        :param id: -
        :param post: (experimental) Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8a671d62de7f5749fc258e0d502e0fda4dc9f8064a58775dd00014db204c0ee3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = WaveOptions(post=post, pre=pre)

        return typing.cast("Wave", jsii.invoke(self, "addWave", [id, options]))

    @jsii.member(jsii_name="buildPipeline")
    def build_pipeline(self) -> None:
        '''(experimental) Send the current pipeline definition to the engine, and construct the pipeline.

        It is not possible to modify the pipeline after calling this method.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "buildPipeline", []))

    @jsii.member(jsii_name="doBuildPipeline")
    @abc.abstractmethod
    def _do_build_pipeline(self) -> None:
        '''(experimental) Implemented by subclasses to do the actual pipeline construction.

        :stability: experimental
        '''
        ...

    @builtins.property
    @jsii.member(jsii_name="cloudAssemblyFileSet")
    def cloud_assembly_file_set(self) -> "FileSet":
        '''(experimental) The FileSet tha contains the cloud assembly.

        This is the primary output of the synth step.

        :stability: experimental
        '''
        return typing.cast("FileSet", jsii.get(self, "cloudAssemblyFileSet"))

    @builtins.property
    @jsii.member(jsii_name="synth")
    def synth(self) -> IFileSetProducer:
        '''(experimental) The build step that produces the CDK Cloud Assembly.

        :stability: experimental
        '''
        return typing.cast(IFileSetProducer, jsii.get(self, "synth"))

    @builtins.property
    @jsii.member(jsii_name="waves")
    def waves(self) -> typing.List["Wave"]:
        '''(experimental) The waves in this pipeline.

        :stability: experimental
        '''
        return typing.cast(typing.List["Wave"], jsii.get(self, "waves"))


class _PipelineBaseProxy(PipelineBase):
    @jsii.member(jsii_name="doBuildPipeline")
    def _do_build_pipeline(self) -> None:
        '''(experimental) Implemented by subclasses to do the actual pipeline construction.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "doBuildPipeline", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, PipelineBase).__jsii_proxy_class__ = lambda : _PipelineBaseProxy


@jsii.data_type(
    jsii_type="monocdk.pipelines.PipelineBaseProps",
    jsii_struct_bases=[],
    name_mapping={"synth": "synth"},
)
class PipelineBaseProps:
    def __init__(self, *, synth: IFileSetProducer) -> None:
        '''(experimental) Properties for a ``Pipeline``.

        :param synth: (experimental) The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            # file_set_producer: pipelines.IFileSetProducer
            
            pipeline_base_props = pipelines.PipelineBaseProps(
                synth=file_set_producer
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__973e6d2cd25db9dfd4ffb41b9e86771ebbddd86d44abded80db56708394849d5)
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "synth": synth,
        }

    @builtins.property
    def synth(self) -> IFileSetProducer:
        '''(experimental) The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.

        :stability: experimental
        '''
        result = self._values.get("synth")
        assert result is not None, "Required property 'synth' is missing"
        return typing.cast(IFileSetProducer, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineBaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.ProduceActionOptions",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "artifacts": "artifacts",
        "pipeline": "pipeline",
        "run_order": "runOrder",
        "scope": "scope",
        "before_self_mutation": "beforeSelfMutation",
        "code_build_defaults": "codeBuildDefaults",
        "fallback_artifact": "fallbackArtifact",
        "variables_namespace": "variablesNamespace",
    },
)
class ProduceActionOptions:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        artifacts: ArtifactMap,
        pipeline: "CodePipeline",
        run_order: jsii.Number,
        scope: _constructs_77d1e7e8.Construct,
        before_self_mutation: typing.Optional[builtins.bool] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Options for the ``CodePipelineActionFactory.produce()`` method.

        :param action_name: (experimental) Name the action should get.
        :param artifacts: (experimental) Helper object to translate FileSets to CodePipeline Artifacts.
        :param pipeline: (experimental) The pipeline the action is being generated for.
        :param run_order: (experimental) RunOrder the action should get.
        :param scope: (experimental) Scope in which to create constructs.
        :param before_self_mutation: (experimental) Whether or not this action is inserted before self mutation. If it is, the action should take care to reflect some part of its own definition in the pipeline action definition, to trigger a restart after self-mutation (if necessary). Default: false
        :param code_build_defaults: (experimental) If this action factory creates a CodeBuild step, default options to inherit. Default: - No CodeBuild project defaults
        :param fallback_artifact: (experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use. CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If the Project doesn't actually care about its input (it can be anything), it can use the Artifact passed here. Default: - A fallback artifact does not exist
        :param variables_namespace: (experimental) If this step is producing outputs, the variables namespace assigned to it. Pass this on to the Action you are creating. Default: - Step doesn't produce any outputs

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import constructs as constructs
            import monocdk as monocdk
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import aws_s3 as s3
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # artifact_map: pipelines.ArtifactMap
            # bucket: s3.Bucket
            # build_image: codebuild.IBuildImage
            # build_spec: codebuild.BuildSpec
            # code_pipeline: pipelines.CodePipeline
            # construct: constructs.Construct
            # duration: monocdk.Duration
            # policy_statement: iam.PolicyStatement
            # security_group: ec2.SecurityGroup
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # value: Any
            # vpc: ec2.Vpc
            
            produce_action_options = pipelines.ProduceActionOptions(
                action_name="actionName",
                artifacts=artifact_map,
                pipeline=code_pipeline,
                run_order=123,
                scope=construct,
            
                # the properties below are optional
                before_self_mutation=False,
                code_build_defaults=pipelines.CodeBuildOptions(
                    build_environment=codebuild.BuildEnvironment(
                        build_image=build_image,
                        certificate=codebuild.BuildEnvironmentCertificate(
                            bucket=bucket,
                            object_key="objectKey"
                        ),
                        compute_type=codebuild.ComputeType.SMALL,
                        environment_variables={
                            "environment_variables_key": codebuild.BuildEnvironmentVariable(
                                value=value,
            
                                # the properties below are optional
                                type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                            )
                        },
                        privileged=False
                    ),
                    partial_build_spec=build_spec,
                    role_policy=[policy_statement],
                    security_groups=[security_group],
                    subnet_selection=ec2.SubnetSelection(
                        availability_zones=["availabilityZones"],
                        one_per_az=False,
                        subnet_filters=[subnet_filter],
                        subnet_group_name="subnetGroupName",
                        subnet_name="subnetName",
                        subnets=[subnet],
                        subnet_type=ec2.SubnetType.ISOLATED
                    ),
                    timeout=duration,
                    vpc=vpc
                ),
                fallback_artifact=artifact,
                variables_namespace="variablesNamespace"
            )
        '''
        if isinstance(code_build_defaults, dict):
            code_build_defaults = CodeBuildOptions(**code_build_defaults)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1ab2583853973cef62592c9fa850b1f25bcfd02e0286dab2b0c75948d35d5d93)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument artifacts", value=artifacts, expected_type=type_hints["artifacts"])
            check_type(argname="argument pipeline", value=pipeline, expected_type=type_hints["pipeline"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument before_self_mutation", value=before_self_mutation, expected_type=type_hints["before_self_mutation"])
            check_type(argname="argument code_build_defaults", value=code_build_defaults, expected_type=type_hints["code_build_defaults"])
            check_type(argname="argument fallback_artifact", value=fallback_artifact, expected_type=type_hints["fallback_artifact"])
            check_type(argname="argument variables_namespace", value=variables_namespace, expected_type=type_hints["variables_namespace"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_name": action_name,
            "artifacts": artifacts,
            "pipeline": pipeline,
            "run_order": run_order,
            "scope": scope,
        }
        if before_self_mutation is not None:
            self._values["before_self_mutation"] = before_self_mutation
        if code_build_defaults is not None:
            self._values["code_build_defaults"] = code_build_defaults
        if fallback_artifact is not None:
            self._values["fallback_artifact"] = fallback_artifact
        if variables_namespace is not None:
            self._values["variables_namespace"] = variables_namespace

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(experimental) Name the action should get.

        :stability: experimental
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def artifacts(self) -> ArtifactMap:
        '''(experimental) Helper object to translate FileSets to CodePipeline Artifacts.

        :stability: experimental
        '''
        result = self._values.get("artifacts")
        assert result is not None, "Required property 'artifacts' is missing"
        return typing.cast(ArtifactMap, result)

    @builtins.property
    def pipeline(self) -> "CodePipeline":
        '''(experimental) The pipeline the action is being generated for.

        :stability: experimental
        '''
        result = self._values.get("pipeline")
        assert result is not None, "Required property 'pipeline' is missing"
        return typing.cast("CodePipeline", result)

    @builtins.property
    def run_order(self) -> jsii.Number:
        '''(experimental) RunOrder the action should get.

        :stability: experimental
        '''
        result = self._values.get("run_order")
        assert result is not None, "Required property 'run_order' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def scope(self) -> _constructs_77d1e7e8.Construct:
        '''(experimental) Scope in which to create constructs.

        :stability: experimental
        '''
        result = self._values.get("scope")
        assert result is not None, "Required property 'scope' is missing"
        return typing.cast(_constructs_77d1e7e8.Construct, result)

    @builtins.property
    def before_self_mutation(self) -> typing.Optional[builtins.bool]:
        '''(experimental) Whether or not this action is inserted before self mutation.

        If it is, the action should take care to reflect some part of
        its own definition in the pipeline action definition, to
        trigger a restart after self-mutation (if necessary).

        :default: false

        :stability: experimental
        '''
        result = self._values.get("before_self_mutation")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def code_build_defaults(self) -> typing.Optional[CodeBuildOptions]:
        '''(experimental) If this action factory creates a CodeBuild step, default options to inherit.

        :default: - No CodeBuild project defaults

        :stability: experimental
        '''
        result = self._values.get("code_build_defaults")
        return typing.cast(typing.Optional[CodeBuildOptions], result)

    @builtins.property
    def fallback_artifact(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use.

        CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If
        the Project doesn't actually care about its input (it can be anything), it can use the
        Artifact passed here.

        :default: - A fallback artifact does not exist

        :stability: experimental
        '''
        result = self._values.get("fallback_artifact")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def variables_namespace(self) -> typing.Optional[builtins.str]:
        '''(experimental) If this step is producing outputs, the variables namespace assigned to it.

        Pass this on to the Action you are creating.

        :default: - Step doesn't produce any outputs

        :stability: experimental
        '''
        result = self._values.get("variables_namespace")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProduceActionOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08)
class PublishAssetsAction(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.PublishAssetsAction",
):
    '''(deprecated) Action to publish an asset in the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to prepare and publish the asset.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline when you add stacks that use assets.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import aws_codebuild as codebuild
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import aws_ec2 as ec2
        from monocdk import aws_iam as iam
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        # build_spec: codebuild.BuildSpec
        # dependable: monocdk.IDependable
        # role: iam.Role
        # subnet: ec2.Subnet
        # subnet_filter: ec2.SubnetFilter
        # vpc: ec2.Vpc
        
        publish_assets_action = pipelines.PublishAssetsAction(self, "MyPublishAssetsAction",
            action_name="actionName",
            asset_type=pipelines.AssetType.FILE,
            cloud_assembly_input=artifact,
        
            # the properties below are optional
            build_spec=build_spec,
            cdk_cli_version="cdkCliVersion",
            create_buildspec_file=False,
            dependable=dependable,
            pre_install_commands=["preInstallCommands"],
            project_name="projectName",
            role=role,
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["availabilityZones"],
                one_per_az=False,
                subnet_filters=[subnet_filter],
                subnet_group_name="subnetGroupName",
                subnet_name="subnetName",
                subnets=[subnet],
                subnet_type=ec2.SubnetType.ISOLATED
            ),
            vpc=vpc
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        action_name: builtins.str,
        asset_type: AssetType,
        cloud_assembly_input: _Artifact_9905eec2,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        create_buildspec_file: typing.Optional[builtins.bool] = None,
        dependable: typing.Optional[_IDependable_1175c9f7] = None,
        pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param action_name: (deprecated) Name of publishing action.
        :param asset_type: (deprecated) AssetType we're publishing.
        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param build_spec: (deprecated) Custom BuildSpec that is merged with generated one. Default: - none
        :param cdk_cli_version: (deprecated) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param create_buildspec_file: (deprecated) Use a file buildspec written to the cloud assembly instead of an inline buildspec. This prevents size limitation errors as inline specs have a max length of 25600 characters Default: false
        :param dependable: (deprecated) Any Dependable construct that the CodeBuild project needs to take a dependency on. Default: - none
        :param pre_install_commands: (deprecated) Additional commands to run before installing cdk-assert Use this to setup proxies or npm mirrors. Default: -
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role: (deprecated) Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the PublishAssetsAction. Default: - No VPC

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4ce6a0c6943083c5761b667a413f2d1a556a0d77aff064d3f43a051c6e144a87)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PublishAssetsActionProps(
            action_name=action_name,
            asset_type=asset_type,
            cloud_assembly_input=cloud_assembly_input,
            build_spec=build_spec,
            cdk_cli_version=cdk_cli_version,
            create_buildspec_file=create_buildspec_file,
            dependable=dependable,
            pre_install_commands=pre_install_commands,
            project_name=project_name,
            role=role,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addPublishCommand")
    def add_publish_command(
        self,
        relative_manifest_path: builtins.str,
        asset_selector: builtins.str,
    ) -> None:
        '''(deprecated) Add a single publishing command.

        Manifest path should be relative to the root Cloud Assembly.

        :param relative_manifest_path: -
        :param asset_selector: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fcf4e5a78f888e9c917cf036235370249526172ed77c04f1b5e1261e85fed01)
            check_type(argname="argument relative_manifest_path", value=relative_manifest_path, expected_type=type_hints["relative_manifest_path"])
            check_type(argname="argument asset_selector", value=asset_selector, expected_type=type_hints["asset_selector"])
        return typing.cast(None, jsii.invoke(self, "addPublishCommand", [relative_manifest_path, asset_selector]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(deprecated) Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a864eb4995a9dde2272a396a55ad920203a466ef5daac0a7fc666fc01e7fad52)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b0c2663267c453297081ba1ccb9429d8cf3d8fc6a3aa746224a1a6e84ceb1af5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''(deprecated) Exists to implement IAction.

        :stability: deprecated
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.PublishAssetsActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "asset_type": "assetType",
        "cloud_assembly_input": "cloudAssemblyInput",
        "build_spec": "buildSpec",
        "cdk_cli_version": "cdkCliVersion",
        "create_buildspec_file": "createBuildspecFile",
        "dependable": "dependable",
        "pre_install_commands": "preInstallCommands",
        "project_name": "projectName",
        "role": "role",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class PublishAssetsActionProps:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        asset_type: AssetType,
        cloud_assembly_input: _Artifact_9905eec2,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        create_buildspec_file: typing.Optional[builtins.bool] = None,
        dependable: typing.Optional[_IDependable_1175c9f7] = None,
        pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(deprecated) Props for a PublishAssetsAction.

        :param action_name: (deprecated) Name of publishing action.
        :param asset_type: (deprecated) AssetType we're publishing.
        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param build_spec: (deprecated) Custom BuildSpec that is merged with generated one. Default: - none
        :param cdk_cli_version: (deprecated) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param create_buildspec_file: (deprecated) Use a file buildspec written to the cloud assembly instead of an inline buildspec. This prevents size limitation errors as inline specs have a max length of 25600 characters Default: false
        :param dependable: (deprecated) Any Dependable construct that the CodeBuild project needs to take a dependency on. Default: - none
        :param pre_install_commands: (deprecated) Additional commands to run before installing cdk-assert Use this to setup proxies or npm mirrors. Default: -
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role: (deprecated) Role to use for CodePipeline and CodeBuild to build and publish the assets. Default: - Automatically generated
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the PublishAssetsAction. Default: - No VPC

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # build_spec: codebuild.BuildSpec
            # dependable: monocdk.IDependable
            # role: iam.Role
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # vpc: ec2.Vpc
            
            publish_assets_action_props = pipelines.PublishAssetsActionProps(
                action_name="actionName",
                asset_type=pipelines.AssetType.FILE,
                cloud_assembly_input=artifact,
            
                # the properties below are optional
                build_spec=build_spec,
                cdk_cli_version="cdkCliVersion",
                create_buildspec_file=False,
                dependable=dependable,
                pre_install_commands=["preInstallCommands"],
                project_name="projectName",
                role=role,
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                vpc=vpc
            )
        '''
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__35d6e68a44f57e99e4812a360f7501bd528f3a9c4891d25d9ee6dcbdb4b40259)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument asset_type", value=asset_type, expected_type=type_hints["asset_type"])
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
            check_type(argname="argument create_buildspec_file", value=create_buildspec_file, expected_type=type_hints["create_buildspec_file"])
            check_type(argname="argument dependable", value=dependable, expected_type=type_hints["dependable"])
            check_type(argname="argument pre_install_commands", value=pre_install_commands, expected_type=type_hints["pre_install_commands"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_name": action_name,
            "asset_type": asset_type,
            "cloud_assembly_input": cloud_assembly_input,
        }
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if create_buildspec_file is not None:
            self._values["create_buildspec_file"] = create_buildspec_file
        if dependable is not None:
            self._values["dependable"] = dependable
        if pre_install_commands is not None:
            self._values["pre_install_commands"] = pre_install_commands
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(deprecated) Name of publishing action.

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> AssetType:
        '''(deprecated) AssetType we're publishing.

        :stability: deprecated
        '''
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast(AssetType, result)

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) Custom BuildSpec that is merged with generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Version of CDK CLI to 'npm install'.

        :default: - Latest version

        :stability: deprecated
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_buildspec_file(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Use a file buildspec written to the cloud assembly instead of an inline buildspec.

        This prevents size limitation errors as inline specs have a max length of 25600 characters

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("create_buildspec_file")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def dependable(self) -> typing.Optional[_IDependable_1175c9f7]:
        '''(deprecated) Any Dependable construct that the CodeBuild project needs to take a dependency on.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("dependable")
        return typing.cast(typing.Optional[_IDependable_1175c9f7], result)

    @builtins.property
    def pre_install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Additional commands to run before installing cdk-assert Use this to setup proxies or npm mirrors.

        :default: -

        :stability: deprecated
        '''
        result = self._values.get("pre_install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(deprecated) Role to use for CodePipeline and CodeBuild to build and publish the assets.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the PublishAssetsAction.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublishAssetsActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.S3SourceOptions",
    jsii_struct_bases=[],
    name_mapping={"action_name": "actionName", "trigger": "trigger"},
)
class S3SourceOptions:
    def __init__(
        self,
        *,
        action_name: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[_S3Trigger_688e3a4a] = None,
    ) -> None:
        '''(experimental) Options for S3 sources.

        :param action_name: (experimental) The action name used for this source in the CodePipeline. Default: - The bucket name
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline_actions as codepipeline_actions
            from monocdk import pipelines
            
            s3_source_options = pipelines.S3SourceOptions(
                action_name="actionName",
                trigger=codepipeline_actions.S3Trigger.NONE
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cd7c4a9eeb00b204d16927bae73a204482dab1b382200197327fe63dd82c597a)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument trigger", value=trigger, expected_type=type_hints["trigger"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if action_name is not None:
            self._values["action_name"] = action_name
        if trigger is not None:
            self._values["trigger"] = trigger

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) The action name used for this source in the CodePipeline.

        :default: - The bucket name

        :stability: experimental
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def trigger(self) -> typing.Optional[_S3Trigger_688e3a4a]:
        '''(experimental) How should CodePipeline detect source changes for this Action.

        Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail,
        as otherwise the CloudWatch Events will not be emitted.

        :default: S3Trigger.POLL

        :see: https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/log-s3-data-events.html
        :stability: experimental
        '''
        result = self._values.get("trigger")
        return typing.cast(typing.Optional[_S3Trigger_688e3a4a], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "S3SourceOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08, _IGrantable_4c5a91d1)
class ShellScriptAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.ShellScriptAction",
):
    '''(deprecated) Validate a revision using shell commands.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codebuild as codebuild
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import aws_ec2 as ec2
        from monocdk import aws_iam as iam
        from monocdk import aws_s3 as s3
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        # bucket: s3.Bucket
        # build_image: codebuild.IBuildImage
        # policy_statement: iam.PolicyStatement
        # security_group: ec2.SecurityGroup
        # stack_output: pipelines.StackOutput
        # subnet: ec2.Subnet
        # subnet_filter: ec2.SubnetFilter
        # value: Any
        # vpc: ec2.Vpc
        
        shell_script_action = pipelines.ShellScriptAction(
            action_name="actionName",
            commands=["commands"],
        
            # the properties below are optional
            additional_artifacts=[artifact],
            bash_options="bashOptions",
            environment=codebuild.BuildEnvironment(
                build_image=build_image,
                certificate=codebuild.BuildEnvironmentCertificate(
                    bucket=bucket,
                    object_key="objectKey"
                ),
                compute_type=codebuild.ComputeType.SMALL,
                environment_variables={
                    "environment_variables_key": codebuild.BuildEnvironmentVariable(
                        value=value,
        
                        # the properties below are optional
                        type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                    )
                },
                privileged=False
            ),
            environment_variables={
                "environment_variables_key": codebuild.BuildEnvironmentVariable(
                    value=value,
        
                    # the properties below are optional
                    type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                )
            },
            role_policy_statements=[policy_statement],
            run_order=123,
            security_groups=[security_group],
            subnet_selection=ec2.SubnetSelection(
                availability_zones=["availabilityZones"],
                one_per_az=False,
                subnet_filters=[subnet_filter],
                subnet_group_name="subnetGroupName",
                subnet_name="subnetName",
                subnets=[subnet],
                subnet_type=ec2.SubnetType.ISOLATED
            ),
            use_outputs={
                "use_outputs_key": stack_output
            },
            vpc=vpc
        )
    '''

    def __init__(
        self,
        *,
        action_name: builtins.str,
        commands: typing.Sequence[builtins.str],
        additional_artifacts: typing.Optional[typing.Sequence[_Artifact_9905eec2]] = None,
        bash_options: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        run_order: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        use_outputs: typing.Optional[typing.Mapping[builtins.str, "StackOutput"]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param action_name: (deprecated) Name of the validation action in the pipeline.
        :param commands: (deprecated) Commands to run.
        :param additional_artifacts: (deprecated) Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: (deprecated) Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param environment: (deprecated) The CodeBuild environment where scripts are executed. Default: LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. Default: - No additional environment variables
        :param role_policy_statements: (deprecated) Additional policy statements to add to the execution role. Default: - No policy statements
        :param run_order: (deprecated) RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param security_groups: (deprecated) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param use_outputs: (deprecated) Stack outputs to make available as environment variables. Default: - No outputs used
        :param vpc: (deprecated) The VPC where to execute the specified script. Default: - No VPC

        :stability: deprecated
        '''
        props = ShellScriptActionProps(
            action_name=action_name,
            commands=commands,
            additional_artifacts=additional_artifacts,
            bash_options=bash_options,
            environment=environment,
            environment_variables=environment_variables,
            role_policy_statements=role_policy_statements,
            run_order=run_order,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            use_outputs=use_outputs,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(deprecated) Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c49fbf4080a2f4f4888eb06a5b34cafe0549fbd0c65f20c6a5c8ed371b1b1ea4)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0cd73e242f3f3cf2647ac421f5545ad3d873b448cf76c447a61d11bb0cb29d2a)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''(deprecated) Exists to implement IAction.

        :stability: deprecated
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(deprecated) The CodeBuild Project's principal.

        :stability: deprecated
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_6da8803e:
        '''(deprecated) Project generated to run the shell script in.

        :stability: deprecated
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.ShellScriptActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "action_name": "actionName",
        "commands": "commands",
        "additional_artifacts": "additionalArtifacts",
        "bash_options": "bashOptions",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "role_policy_statements": "rolePolicyStatements",
        "run_order": "runOrder",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "use_outputs": "useOutputs",
        "vpc": "vpc",
    },
)
class ShellScriptActionProps:
    def __init__(
        self,
        *,
        action_name: builtins.str,
        commands: typing.Sequence[builtins.str],
        additional_artifacts: typing.Optional[typing.Sequence[_Artifact_9905eec2]] = None,
        bash_options: typing.Optional[builtins.str] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        run_order: typing.Optional[jsii.Number] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        use_outputs: typing.Optional[typing.Mapping[builtins.str, "StackOutput"]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(deprecated) Properties for ShellScriptAction.

        :param action_name: (deprecated) Name of the validation action in the pipeline.
        :param commands: (deprecated) Commands to run.
        :param additional_artifacts: (deprecated) Additional artifacts to use as input for the CodeBuild project. You can use these files to load more complex test sets into the shellscript build environment. The files artifact given here will be unpacked into the current working directory, the other ones will be unpacked into directories which are available through the environment variables $CODEBUILD_SRC_DIR_. The CodeBuild job must have at least one input artifact, so you must provide either at least one additional artifact here or one stack output using ``useOutput``. Default: - No additional artifacts
        :param bash_options: (deprecated) Bash options to set at the start of the script. Default: '-eu' (errexit and nounset)
        :param environment: (deprecated) The CodeBuild environment where scripts are executed. Default: LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. Default: - No additional environment variables
        :param role_policy_statements: (deprecated) Additional policy statements to add to the execution role. Default: - No policy statements
        :param run_order: (deprecated) RunOrder for this action. Use this to sequence the shell script after the deployments. The default value is 100 so you don't have to supply the value if you just want to run this after the application stacks have been deployed, and you don't have more than 100 stacks. Default: 100
        :param security_groups: (deprecated) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param use_outputs: (deprecated) Stack outputs to make available as environment variables. Default: - No outputs used
        :param vpc: (deprecated) The VPC where to execute the specified script. Default: - No VPC

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import aws_s3 as s3
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # bucket: s3.Bucket
            # build_image: codebuild.IBuildImage
            # policy_statement: iam.PolicyStatement
            # security_group: ec2.SecurityGroup
            # stack_output: pipelines.StackOutput
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # value: Any
            # vpc: ec2.Vpc
            
            shell_script_action_props = pipelines.ShellScriptActionProps(
                action_name="actionName",
                commands=["commands"],
            
                # the properties below are optional
                additional_artifacts=[artifact],
                bash_options="bashOptions",
                environment=codebuild.BuildEnvironment(
                    build_image=build_image,
                    certificate=codebuild.BuildEnvironmentCertificate(
                        bucket=bucket,
                        object_key="objectKey"
                    ),
                    compute_type=codebuild.ComputeType.SMALL,
                    environment_variables={
                        "environment_variables_key": codebuild.BuildEnvironmentVariable(
                            value=value,
            
                            # the properties below are optional
                            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                        )
                    },
                    privileged=False
                ),
                environment_variables={
                    "environment_variables_key": codebuild.BuildEnvironmentVariable(
                        value=value,
            
                        # the properties below are optional
                        type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                    )
                },
                role_policy_statements=[policy_statement],
                run_order=123,
                security_groups=[security_group],
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                use_outputs={
                    "use_outputs_key": stack_output
                },
                vpc=vpc
            )
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__278fb7bed3d8bfa7d5973cd2fbf83eef62e29da30aed6823da84b820079002eb)
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument bash_options", value=bash_options, expected_type=type_hints["bash_options"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument use_outputs", value=use_outputs, expected_type=type_hints["use_outputs"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action_name": action_name,
            "commands": commands,
        }
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if bash_options is not None:
            self._values["bash_options"] = bash_options
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if run_order is not None:
            self._values["run_order"] = run_order
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if use_outputs is not None:
            self._values["use_outputs"] = use_outputs
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def action_name(self) -> builtins.str:
        '''(deprecated) Name of the validation action in the pipeline.

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        assert result is not None, "Required property 'action_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(deprecated) Commands to run.

        :stability: deprecated
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[_Artifact_9905eec2]]:
        '''(deprecated) Additional artifacts to use as input for the CodeBuild project.

        You can use these files to load more complex test sets into the
        shellscript build environment.

        The files artifact given here will be unpacked into the current
        working directory, the other ones will be unpacked into directories
        which are available through the environment variables
        $CODEBUILD_SRC_DIR_.

        The CodeBuild job must have at least one input artifact, so you
        must provide either at least one additional artifact here or one
        stack output using ``useOutput``.

        :default: - No additional artifacts

        :stability: deprecated
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[_Artifact_9905eec2]], result)

    @builtins.property
    def bash_options(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Bash options to set at the start of the script.

        :default: '-eu' (errexit and nounset)

        :stability: deprecated
        '''
        result = self._values.get("bash_options")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(deprecated) The CodeBuild environment where scripts are executed.

        :default: LinuxBuildImage.STANDARD_5_0

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(deprecated) Environment variables to send into build.

        :default: - No additional environment variables

        :stability: deprecated
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(deprecated) Additional policy statements to add to the execution role.

        :default: - No policy statements

        :stability: deprecated
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) RunOrder for this action.

        Use this to sequence the shell script after the deployments.

        The default value is 100 so you don't have to supply the value if you just
        want to run this after the application stacks have been deployed, and you
        don't have more than 100 stacks.

        :default: 100

        :stability: deprecated
        '''
        result = self._values.get("run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(deprecated) Which security group to associate with the script's project network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        :default: - Security group will be automatically created.

        :stability: deprecated
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def use_outputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, "StackOutput"]]:
        '''(deprecated) Stack outputs to make available as environment variables.

        :default: - No outputs used

        :stability: deprecated
        '''
        result = self._values.get("use_outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, "StackOutput"]], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the specified script.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShellScriptActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.ShellStepProps",
    jsii_struct_bases=[],
    name_mapping={
        "commands": "commands",
        "additional_inputs": "additionalInputs",
        "env": "env",
        "env_from_cfn_outputs": "envFromCfnOutputs",
        "input": "input",
        "install_commands": "installCommands",
        "primary_output_directory": "primaryOutputDirectory",
    },
)
class ShellStepProps:
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
        input: typing.Optional[IFileSetProducer] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_output_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Construction properties for a ``ShellStep``.

        :param commands: (experimental) Commands to run.
        :param additional_inputs: (experimental) Additional FileSets to put in other directories. Specifies a mapping from directory name to FileSets. During the script execution, the FileSets will be available in the directories indicated. The directory names may be relative. For example, you can put the main input and an additional input side-by-side with the following configuration:: const script = new pipelines.ShellStep('MainScript', { commands: ['npm ci','npm run build','npx cdk synth'], input: pipelines.CodePipelineSource.gitHub('org/source1', 'main'), additionalInputs: { '../siblingdir': pipelines.CodePipelineSource.gitHub('org/source2', 'main'), } }); Default: - No additional inputs
        :param env: (experimental) Environment variables to set. Default: - No environment variables
        :param env_from_cfn_outputs: (experimental) Set environment variables based on Stack Outputs. ``ShellStep``s following stack or stage deployments may access the ``CfnOutput``s of those stacks to get access to --for example--automatically generated resource names or endpoint URLs. Default: - No environment variables created from stack outputs
        :param input: (experimental) FileSet to run these scripts on. The files in the FileSet will be placed in the working directory when the script is executed. Use ``additionalInputs`` to download file sets to other directories as well. Default: - No input specified
        :param install_commands: (experimental) Installation commands to run before the regular commands. For deployment engines that support it, install commands will be classified differently in the job history from the regular ``commands``. Default: - No installation commands
        :param primary_output_directory: (experimental) The directory that will contain the primary output fileset. After running the script, the contents of the given directory will be treated as the primary output of this Step. Default: - No primary output

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # Modern API
            modern_pipeline = pipelines.CodePipeline(self, "Pipeline",
                self_mutation=False,
                synth=pipelines.ShellStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["npm ci", "npm run build", "npx cdk synth"
                    ]
                )
            )
            
            # Original API
            cloud_assembly_artifact = codepipeline.Artifact()
            original_pipeline = pipelines.CdkPipeline(self, "Pipeline",
                self_mutating=False,
                cloud_assembly_artifact=cloud_assembly_artifact
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01207d6669efe1d9b2af97bdfba04ff010b360580dea346962f6a202ef3c7f92)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument additional_inputs", value=additional_inputs, expected_type=type_hints["additional_inputs"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument env_from_cfn_outputs", value=env_from_cfn_outputs, expected_type=type_hints["env_from_cfn_outputs"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
            check_type(argname="argument primary_output_directory", value=primary_output_directory, expected_type=type_hints["primary_output_directory"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
        }
        if additional_inputs is not None:
            self._values["additional_inputs"] = additional_inputs
        if env is not None:
            self._values["env"] = env
        if env_from_cfn_outputs is not None:
            self._values["env_from_cfn_outputs"] = env_from_cfn_outputs
        if input is not None:
            self._values["input"] = input
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if primary_output_directory is not None:
            self._values["primary_output_directory"] = primary_output_directory

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Commands to run.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_inputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]]:
        '''(experimental) Additional FileSets to put in other directories.

        Specifies a mapping from directory name to FileSets. During the
        script execution, the FileSets will be available in the directories
        indicated.

        The directory names may be relative. For example, you can put
        the main input and an additional input side-by-side with the
        following configuration::

           script = pipelines.ShellStep("MainScript",
               commands=["npm ci", "npm run build", "npx cdk synth"],
               input=pipelines.CodePipelineSource.git_hub("org/source1", "main"),
               additional_inputs={
                   "../siblingdir": pipelines.CodePipelineSource.git_hub("org/source2", "main")
               }
           )

        :default: - No additional inputs

        :stability: experimental
        '''
        result = self._values.get("additional_inputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to set.

        :default: - No environment variables

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def env_from_cfn_outputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]]:
        '''(experimental) Set environment variables based on Stack Outputs.

        ``ShellStep``s following stack or stage deployments may
        access the ``CfnOutput``s of those stacks to get access to
        --for example--automatically generated resource names or
        endpoint URLs.

        :default: - No environment variables created from stack outputs

        :stability: experimental
        '''
        result = self._values.get("env_from_cfn_outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]], result)

    @builtins.property
    def input(self) -> typing.Optional[IFileSetProducer]:
        '''(experimental) FileSet to run these scripts on.

        The files in the FileSet will be placed in the working directory when
        the script is executed. Use ``additionalInputs`` to download file sets
        to other directories as well.

        :default: - No input specified

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[IFileSetProducer], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Installation commands to run before the regular commands.

        For deployment engines that support it, install commands will be classified
        differently in the job history from the regular ``commands``.

        :default: - No installation commands

        :stability: experimental
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def primary_output_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory that will contain the primary output fileset.

        After running the script, the contents of the given directory
        will be treated as the primary output of this Step.

        :default: - No primary output

        :stability: experimental
        '''
        result = self._values.get("primary_output_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ShellStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_IAction_ecd54a08, _IGrantable_4c5a91d1)
class SimpleSynthAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.SimpleSynthAction",
):
    '''(deprecated) A standard synth with a generated buildspec.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        source_artifact = codepipeline.Artifact()
        cloud_assembly_artifact = codepipeline.Artifact()
        pipeline = pipelines.CdkPipeline(self, "MyPipeline",
            cloud_assembly_artifact=cloud_assembly_artifact,
            synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                source_artifact=source_artifact,
                cloud_assembly_artifact=cloud_assembly_artifact,
                environment=cdk.aws_codebuild.BuildEnvironment(
                    privileged=True
                )
            )
        )
    '''

    def __init__(
        self,
        *,
        synth_command: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_command: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''
        :param synth_command: (deprecated) The synth command.
        :param build_command: (deprecated) The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: (deprecated) The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: (deprecated) The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: (deprecated) Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands
        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: deprecated
        '''
        props = SimpleSynthActionProps(
            synth_command=synth_command,
            build_command=build_command,
            build_commands=build_commands,
            install_command=install_command,
            install_commands=install_commands,
            test_commands=test_commands,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            build_spec=build_spec,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="standardNpmSynth")
    @builtins.classmethod
    def standard_npm_synth(
        cls,
        *,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> "SimpleSynthAction":
        '''(deprecated) Create a standard NPM synth action.

        Uses ``npm ci`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'npm run build'``.

        :param build_command: (deprecated) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (deprecated) The install command. Default: 'npm ci'
        :param synth_command: (deprecated) The synth command. Default: 'npx cdk synth'
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands
        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: deprecated
        '''
        options = StandardNpmSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            test_commands=test_commands,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            build_spec=build_spec,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        return typing.cast("SimpleSynthAction", jsii.sinvoke(cls, "standardNpmSynth", [options]))

    @jsii.member(jsii_name="standardYarnSynth")
    @builtins.classmethod
    def standard_yarn_synth(
        cls,
        *,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> "SimpleSynthAction":
        '''(deprecated) Create a standard Yarn synth action.

        Uses ``yarn install --frozen-lockfile`` to install dependencies and ``npx cdk synth`` to synthesize.

        If you need a build step, add ``buildCommand: 'yarn build'``.

        :param build_command: (deprecated) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (deprecated) The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: (deprecated) The synth command. Default: 'npx cdk synth'
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands
        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: deprecated
        '''
        options = StandardYarnSynthOptions(
            build_command=build_command,
            install_command=install_command,
            synth_command=synth_command,
            test_commands=test_commands,
            cloud_assembly_artifact=cloud_assembly_artifact,
            source_artifact=source_artifact,
            action_name=action_name,
            additional_artifacts=additional_artifacts,
            build_spec=build_spec,
            copy_environment_variables=copy_environment_variables,
            environment=environment,
            environment_variables=environment_variables,
            project_name=project_name,
            role_policy_statements=role_policy_statements,
            subdirectory=subdirectory,
            subnet_selection=subnet_selection,
            vpc=vpc,
        )

        return typing.cast("SimpleSynthAction", jsii.sinvoke(cls, "standardYarnSynth", [options]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(deprecated) Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2018a6d750028088e68d772c1a323e145d2c829739d25b32932b67c3387e5446)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__502bfb765a1714a3716bfeca6efcbf6f7ca285039594f9b11e503d7ca9e3e3db)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''(deprecated) Exists to implement IAction.

        :stability: deprecated
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(deprecated) The CodeBuild Project's principal.

        :stability: deprecated
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_6da8803e:
        '''(deprecated) Project generated to run the synth command.

        :stability: deprecated
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "project"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.SimpleSynthOptions",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "build_spec": "buildSpec",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
    },
)
class SimpleSynthOptions:
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(deprecated) Configuration options for a SimpleSynth.

        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import aws_s3 as s3
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # bucket: s3.Bucket
            # build_image: codebuild.IBuildImage
            # build_spec: codebuild.BuildSpec
            # policy_statement: iam.PolicyStatement
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # value: Any
            # vpc: ec2.Vpc
            
            simple_synth_options = pipelines.SimpleSynthOptions(
                cloud_assembly_artifact=artifact,
                source_artifact=artifact,
            
                # the properties below are optional
                action_name="actionName",
                additional_artifacts=[pipelines.AdditionalArtifact(
                    artifact=artifact,
                    directory="directory"
                )],
                build_spec=build_spec,
                copy_environment_variables=["copyEnvironmentVariables"],
                environment=codebuild.BuildEnvironment(
                    build_image=build_image,
                    certificate=codebuild.BuildEnvironmentCertificate(
                        bucket=bucket,
                        object_key="objectKey"
                    ),
                    compute_type=codebuild.ComputeType.SMALL,
                    environment_variables={
                        "environment_variables_key": codebuild.BuildEnvironmentVariable(
                            value=value,
            
                            # the properties below are optional
                            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                        )
                    },
                    privileged=False
                ),
                environment_variables={
                    "environment_variables_key": codebuild.BuildEnvironmentVariable(
                        value=value,
            
                        # the properties below are optional
                        type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                    )
                },
                project_name="projectName",
                role_policy_statements=[policy_statement],
                subdirectory="subdirectory",
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                vpc=vpc
            )
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a85675b9cfb390898459f6acee701a2bd59eb85e298dbb295c9520bb1d714432)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument source_artifact", value=source_artifact, expected_type=type_hints["source_artifact"])
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument copy_environment_variables", value=copy_environment_variables, expected_type=type_hints["copy_environment_variables"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The artifact where the CloudAssembly should be emitted.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The source artifact of the CodePipeline.

        :stability: deprecated
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the build action.

        :default: 'Synth'

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(deprecated) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: deprecated
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) custom BuildSpec that is merged with the generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: deprecated
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(deprecated) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(deprecated) Environment variables to send into build.

        NOTE: You may run into the 1000-character limit for the Action configuration if you have a large
        number of variables or if their names or values are very long.
        If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead.
        However, you will not be able to use CodePipeline Variables in this case.

        :default: - No additional environment variables

        :stability: deprecated
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(deprecated) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: deprecated
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: deprecated
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.StackAsset",
    jsii_struct_bases=[],
    name_mapping={
        "asset_id": "assetId",
        "asset_manifest_path": "assetManifestPath",
        "asset_selector": "assetSelector",
        "asset_type": "assetType",
        "is_template": "isTemplate",
        "asset_publishing_role_arn": "assetPublishingRoleArn",
    },
)
class StackAsset:
    def __init__(
        self,
        *,
        asset_id: builtins.str,
        asset_manifest_path: builtins.str,
        asset_selector: builtins.str,
        asset_type: AssetType,
        is_template: builtins.bool,
        asset_publishing_role_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) An asset used by a Stack.

        :param asset_id: (experimental) Asset identifier.
        :param asset_manifest_path: (experimental) Absolute asset manifest path. This needs to be made relative at a later point in time, but when this information is parsed we don't know about the root cloud assembly yet.
        :param asset_selector: (experimental) Asset selector to pass to ``cdk-assets``.
        :param asset_type: (experimental) Type of asset to publish.
        :param is_template: (experimental) Does this asset represent the CloudFormation template for the stack. Default: false
        :param asset_publishing_role_arn: (experimental) Role ARN to assume to publish. Default: - No need to assume any role

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            stack_asset = pipelines.StackAsset(
                asset_id="assetId",
                asset_manifest_path="assetManifestPath",
                asset_selector="assetSelector",
                asset_type=pipelines.AssetType.FILE,
                is_template=False,
            
                # the properties below are optional
                asset_publishing_role_arn="assetPublishingRoleArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e73e21a339c0d1134c80e66f961e27a00d0c3d0b49aaba12421f5f49a12cd549)
            check_type(argname="argument asset_id", value=asset_id, expected_type=type_hints["asset_id"])
            check_type(argname="argument asset_manifest_path", value=asset_manifest_path, expected_type=type_hints["asset_manifest_path"])
            check_type(argname="argument asset_selector", value=asset_selector, expected_type=type_hints["asset_selector"])
            check_type(argname="argument asset_type", value=asset_type, expected_type=type_hints["asset_type"])
            check_type(argname="argument is_template", value=is_template, expected_type=type_hints["is_template"])
            check_type(argname="argument asset_publishing_role_arn", value=asset_publishing_role_arn, expected_type=type_hints["asset_publishing_role_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "asset_id": asset_id,
            "asset_manifest_path": asset_manifest_path,
            "asset_selector": asset_selector,
            "asset_type": asset_type,
            "is_template": is_template,
        }
        if asset_publishing_role_arn is not None:
            self._values["asset_publishing_role_arn"] = asset_publishing_role_arn

    @builtins.property
    def asset_id(self) -> builtins.str:
        '''(experimental) Asset identifier.

        :stability: experimental
        '''
        result = self._values.get("asset_id")
        assert result is not None, "Required property 'asset_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_manifest_path(self) -> builtins.str:
        '''(experimental) Absolute asset manifest path.

        This needs to be made relative at a later point in time, but when this
        information is parsed we don't know about the root cloud assembly yet.

        :stability: experimental
        '''
        result = self._values.get("asset_manifest_path")
        assert result is not None, "Required property 'asset_manifest_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_selector(self) -> builtins.str:
        '''(experimental) Asset selector to pass to ``cdk-assets``.

        :stability: experimental
        '''
        result = self._values.get("asset_selector")
        assert result is not None, "Required property 'asset_selector' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def asset_type(self) -> AssetType:
        '''(experimental) Type of asset to publish.

        :stability: experimental
        '''
        result = self._values.get("asset_type")
        assert result is not None, "Required property 'asset_type' is missing"
        return typing.cast(AssetType, result)

    @builtins.property
    def is_template(self) -> builtins.bool:
        '''(experimental) Does this asset represent the CloudFormation template for the stack.

        :default: false

        :stability: experimental
        '''
        result = self._values.get("is_template")
        assert result is not None, "Required property 'is_template' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def asset_publishing_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role ARN to assume to publish.

        :default: - No need to assume any role

        :stability: experimental
        '''
        result = self._values.get("asset_publishing_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackAsset(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackDeployment(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.StackDeployment",
):
    '''(experimental) Deployment of a single Stack.

    You don't need to instantiate this class -- it will
    be automatically instantiated as necessary when you
    add a ``Stage`` to a pipeline.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import cx_api
        from monocdk import pipelines
        
        # cloud_formation_stack_artifact: cx_api.CloudFormationStackArtifact
        
        stack_deployment = pipelines.StackDeployment.from_artifact(cloud_formation_stack_artifact)
    '''

    @jsii.member(jsii_name="fromArtifact")
    @builtins.classmethod
    def from_artifact(
        cls,
        stack_artifact: _CloudFormationStackArtifact_45074b84,
    ) -> "StackDeployment":
        '''(experimental) Build a ``StackDeployment`` from a Stack Artifact in a Cloud Assembly.

        :param stack_artifact: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cac9d369aa01c3b266f6d40155393b16752609a414589ca39f88b1f66c2fb44)
            check_type(argname="argument stack_artifact", value=stack_artifact, expected_type=type_hints["stack_artifact"])
        return typing.cast("StackDeployment", jsii.sinvoke(cls, "fromArtifact", [stack_artifact]))

    @jsii.member(jsii_name="addStackDependency")
    def add_stack_dependency(self, stack_deployment: "StackDeployment") -> None:
        '''(experimental) Add a dependency on another stack.

        :param stack_deployment: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fd804115f5882d087e98f3e5d377331bc1b595d871e1ff444e43a419857d39eb)
            check_type(argname="argument stack_deployment", value=stack_deployment, expected_type=type_hints["stack_deployment"])
        return typing.cast(None, jsii.invoke(self, "addStackDependency", [stack_deployment]))

    @jsii.member(jsii_name="addStackSteps")
    def add_stack_steps(
        self,
        pre: typing.Sequence["Step"],
        change_set: typing.Sequence["Step"],
        post: typing.Sequence["Step"],
    ) -> None:
        '''(experimental) Adds steps to each phase of the stack.

        :param pre: steps executed before stack.prepare.
        :param change_set: steps executed after stack.prepare and before stack.deploy.
        :param post: steps executed after stack.deploy.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1177f7360ee051e7ede8cfc9a5203a52cbc9726d0f4b752b604f5afd1c8392b7)
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
            check_type(argname="argument change_set", value=change_set, expected_type=type_hints["change_set"])
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
        return typing.cast(None, jsii.invoke(self, "addStackSteps", [pre, change_set, post]))

    @builtins.property
    @jsii.member(jsii_name="absoluteTemplatePath")
    def absolute_template_path(self) -> builtins.str:
        '''(experimental) Template path on disk to CloudAssembly.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "absoluteTemplatePath"))

    @builtins.property
    @jsii.member(jsii_name="assets")
    def assets(self) -> typing.List[StackAsset]:
        '''(experimental) Assets referenced by this stack.

        :stability: experimental
        '''
        return typing.cast(typing.List[StackAsset], jsii.get(self, "assets"))

    @builtins.property
    @jsii.member(jsii_name="changeSet")
    def change_set(self) -> typing.List["Step"]:
        '''(experimental) Steps that take place after stack is prepared but before stack deploys.

        Your pipeline engine may not disable ``prepareStep``.

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "changeSet"))

    @builtins.property
    @jsii.member(jsii_name="constructPath")
    def construct_path(self) -> builtins.str:
        '''(experimental) Construct path for this stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "constructPath"))

    @builtins.property
    @jsii.member(jsii_name="post")
    def post(self) -> typing.List["Step"]:
        '''(experimental) Steps to execute after stack deploys.

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "post"))

    @builtins.property
    @jsii.member(jsii_name="pre")
    def pre(self) -> typing.List["Step"]:
        '''(experimental) Steps that take place before stack is prepared.

        If your pipeline engine disables 'prepareStep', then this will happen before stack deploys

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "pre"))

    @builtins.property
    @jsii.member(jsii_name="stackArtifactId")
    def stack_artifact_id(self) -> builtins.str:
        '''(experimental) Artifact ID for this stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackArtifactId"))

    @builtins.property
    @jsii.member(jsii_name="stackDependencies")
    def stack_dependencies(self) -> typing.List["StackDeployment"]:
        '''(experimental) Other stacks this stack depends on.

        :stability: experimental
        '''
        return typing.cast(typing.List["StackDeployment"], jsii.get(self, "stackDependencies"))

    @builtins.property
    @jsii.member(jsii_name="stackName")
    def stack_name(self) -> builtins.str:
        '''(experimental) Name for this stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackName"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Tags to apply to the stack.

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="account")
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account where the stack should be deployed.

        :default: - Pipeline account

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "account"))

    @builtins.property
    @jsii.member(jsii_name="assumeRoleArn")
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role to assume before deploying this stack.

        :default: - Don't assume any role

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "assumeRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="executionRoleArn")
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Execution role to pass to CloudFormation.

        :default: - No execution role

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "executionRoleArn"))

    @builtins.property
    @jsii.member(jsii_name="region")
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region where the stack should be deployed.

        :default: - Pipeline region

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "region"))

    @builtins.property
    @jsii.member(jsii_name="templateAsset")
    def template_asset(self) -> typing.Optional[StackAsset]:
        '''(experimental) The asset that represents the CloudFormation template for this stack.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[StackAsset], jsii.get(self, "templateAsset"))

    @builtins.property
    @jsii.member(jsii_name="templateUrl")
    def template_url(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 URL which points to the template asset location in the publishing bucket.

        This is ``undefined`` if the stack template is not published. Use the
        ``DefaultStackSynthesizer`` to ensure it is.

        Example value: ``https://bucket.s3.amazonaws.com/object/key``

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "templateUrl"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.StackDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "absolute_template_path": "absoluteTemplatePath",
        "construct_path": "constructPath",
        "stack_artifact_id": "stackArtifactId",
        "stack_name": "stackName",
        "account": "account",
        "assets": "assets",
        "assume_role_arn": "assumeRoleArn",
        "execution_role_arn": "executionRoleArn",
        "region": "region",
        "tags": "tags",
        "template_s3_uri": "templateS3Uri",
    },
)
class StackDeploymentProps:
    def __init__(
        self,
        *,
        absolute_template_path: builtins.str,
        construct_path: builtins.str,
        stack_artifact_id: builtins.str,
        stack_name: builtins.str,
        account: typing.Optional[builtins.str] = None,
        assets: typing.Optional[typing.Sequence[typing.Union[StackAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
        assume_role_arn: typing.Optional[builtins.str] = None,
        execution_role_arn: typing.Optional[builtins.str] = None,
        region: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        template_s3_uri: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a ``StackDeployment``.

        :param absolute_template_path: (experimental) Template path on disk to cloud assembly (cdk.out).
        :param construct_path: (experimental) Construct path for this stack.
        :param stack_artifact_id: (experimental) Artifact ID for this stack.
        :param stack_name: (experimental) Name for this stack.
        :param account: (experimental) Account where the stack should be deployed. Default: - Pipeline account
        :param assets: (experimental) Assets referenced by this stack. Default: - No assets
        :param assume_role_arn: (experimental) Role to assume before deploying this stack. Default: - Don't assume any role
        :param execution_role_arn: (experimental) Execution role to pass to CloudFormation. Default: - No execution role
        :param region: (experimental) Region where the stack should be deployed. Default: - Pipeline region
        :param tags: (experimental) Tags to apply to the stack. Default: - No tags
        :param template_s3_uri: (experimental) The S3 URL which points to the template asset location in the publishing bucket. Default: - Stack template is not published

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            stack_deployment_props = pipelines.StackDeploymentProps(
                absolute_template_path="absoluteTemplatePath",
                construct_path="constructPath",
                stack_artifact_id="stackArtifactId",
                stack_name="stackName",
            
                # the properties below are optional
                account="account",
                assets=[pipelines.StackAsset(
                    asset_id="assetId",
                    asset_manifest_path="assetManifestPath",
                    asset_selector="assetSelector",
                    asset_type=pipelines.AssetType.FILE,
                    is_template=False,
            
                    # the properties below are optional
                    asset_publishing_role_arn="assetPublishingRoleArn"
                )],
                assume_role_arn="assumeRoleArn",
                execution_role_arn="executionRoleArn",
                region="region",
                tags={
                    "tags_key": "tags"
                },
                template_s3_uri="templateS3Uri"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d06ceb728c1f4dff3443356ec12d902b0722f8042dc15992def99bd137e517a5)
            check_type(argname="argument absolute_template_path", value=absolute_template_path, expected_type=type_hints["absolute_template_path"])
            check_type(argname="argument construct_path", value=construct_path, expected_type=type_hints["construct_path"])
            check_type(argname="argument stack_artifact_id", value=stack_artifact_id, expected_type=type_hints["stack_artifact_id"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
            check_type(argname="argument account", value=account, expected_type=type_hints["account"])
            check_type(argname="argument assets", value=assets, expected_type=type_hints["assets"])
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
            check_type(argname="argument execution_role_arn", value=execution_role_arn, expected_type=type_hints["execution_role_arn"])
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument template_s3_uri", value=template_s3_uri, expected_type=type_hints["template_s3_uri"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "absolute_template_path": absolute_template_path,
            "construct_path": construct_path,
            "stack_artifact_id": stack_artifact_id,
            "stack_name": stack_name,
        }
        if account is not None:
            self._values["account"] = account
        if assets is not None:
            self._values["assets"] = assets
        if assume_role_arn is not None:
            self._values["assume_role_arn"] = assume_role_arn
        if execution_role_arn is not None:
            self._values["execution_role_arn"] = execution_role_arn
        if region is not None:
            self._values["region"] = region
        if tags is not None:
            self._values["tags"] = tags
        if template_s3_uri is not None:
            self._values["template_s3_uri"] = template_s3_uri

    @builtins.property
    def absolute_template_path(self) -> builtins.str:
        '''(experimental) Template path on disk to cloud assembly (cdk.out).

        :stability: experimental
        '''
        result = self._values.get("absolute_template_path")
        assert result is not None, "Required property 'absolute_template_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def construct_path(self) -> builtins.str:
        '''(experimental) Construct path for this stack.

        :stability: experimental
        '''
        result = self._values.get("construct_path")
        assert result is not None, "Required property 'construct_path' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_artifact_id(self) -> builtins.str:
        '''(experimental) Artifact ID for this stack.

        :stability: experimental
        '''
        result = self._values.get("stack_artifact_id")
        assert result is not None, "Required property 'stack_artifact_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stack_name(self) -> builtins.str:
        '''(experimental) Name for this stack.

        :stability: experimental
        '''
        result = self._values.get("stack_name")
        assert result is not None, "Required property 'stack_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def account(self) -> typing.Optional[builtins.str]:
        '''(experimental) Account where the stack should be deployed.

        :default: - Pipeline account

        :stability: experimental
        '''
        result = self._values.get("account")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def assets(self) -> typing.Optional[typing.List[StackAsset]]:
        '''(experimental) Assets referenced by this stack.

        :default: - No assets

        :stability: experimental
        '''
        result = self._values.get("assets")
        return typing.cast(typing.Optional[typing.List[StackAsset]], result)

    @builtins.property
    def assume_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Role to assume before deploying this stack.

        :default: - Don't assume any role

        :stability: experimental
        '''
        result = self._values.get("assume_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execution_role_arn(self) -> typing.Optional[builtins.str]:
        '''(experimental) Execution role to pass to CloudFormation.

        :default: - No execution role

        :stability: experimental
        '''
        result = self._values.get("execution_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def region(self) -> typing.Optional[builtins.str]:
        '''(experimental) Region where the stack should be deployed.

        :default: - Pipeline region

        :stability: experimental
        '''
        result = self._values.get("region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Tags to apply to the stack.

        :default: - No tags

        :stability: experimental
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def template_s3_uri(self) -> typing.Optional[builtins.str]:
        '''(experimental) The S3 URL which points to the template asset location in the publishing bucket.

        :default: - Stack template is not published

        :stability: experimental
        '''
        result = self._values.get("template_s3_uri")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StackOutput(metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.StackOutput"):
    '''(deprecated) A single output of a Stack.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import pipelines
        
        # artifact_path: codepipeline.ArtifactPath
        
        stack_output = pipelines.StackOutput(artifact_path, "outputName")
    '''

    def __init__(
        self,
        artifact_file: _ArtifactPath_a5b79113,
        output_name: builtins.str,
    ) -> None:
        '''(deprecated) Build a StackOutput from a known artifact and an output name.

        :param artifact_file: -
        :param output_name: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0ff54bc06b9a2bcd06f714ff5c57ee062f376e76dbd290b36b16b193b270f50c)
            check_type(argname="argument artifact_file", value=artifact_file, expected_type=type_hints["artifact_file"])
            check_type(argname="argument output_name", value=output_name, expected_type=type_hints["output_name"])
        jsii.create(self.__class__, self, [artifact_file, output_name])

    @builtins.property
    @jsii.member(jsii_name="artifactFile")
    def artifact_file(self) -> _ArtifactPath_a5b79113:
        '''(deprecated) The artifact and file the output is stored in.

        :stability: deprecated
        '''
        return typing.cast(_ArtifactPath_a5b79113, jsii.get(self, "artifactFile"))

    @builtins.property
    @jsii.member(jsii_name="outputName")
    def output_name(self) -> builtins.str:
        '''(deprecated) The name of the output in the JSON object in the file.

        :stability: deprecated
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputName"))


class StackOutputReference(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.StackOutputReference",
):
    '''(experimental) A Reference to a Stack Output.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import pipelines
        
        # cfn_output: monocdk.CfnOutput
        
        stack_output_reference = pipelines.StackOutputReference.from_cfn_output(cfn_output)
    '''

    @jsii.member(jsii_name="fromCfnOutput")
    @builtins.classmethod
    def from_cfn_output(cls, output: _CfnOutput_a4d857a8) -> "StackOutputReference":
        '''(experimental) Create a StackOutputReference that references the given CfnOutput.

        :param output: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7d8f8949f797521c2554d3d48815420747ab7a11546ac59c15f9466c76e8e51b)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
        return typing.cast("StackOutputReference", jsii.sinvoke(cls, "fromCfnOutput", [output]))

    @jsii.member(jsii_name="isProducedBy")
    def is_produced_by(self, stack: StackDeployment) -> builtins.bool:
        '''(experimental) Whether or not this stack output is being produced by the given Stack deployment.

        :param stack: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__65abb849ba53caed5b5a4ed45e3948847f4efd560ec4c02180bbf59dc3a15abd)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
        return typing.cast(builtins.bool, jsii.invoke(self, "isProducedBy", [stack]))

    @builtins.property
    @jsii.member(jsii_name="outputName")
    def output_name(self) -> builtins.str:
        '''(experimental) Output name of the producing stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "outputName"))

    @builtins.property
    @jsii.member(jsii_name="stackDescription")
    def stack_description(self) -> builtins.str:
        '''(experimental) A human-readable description of the producing stack.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stackDescription"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.StackSteps",
    jsii_struct_bases=[],
    name_mapping={
        "stack": "stack",
        "change_set": "changeSet",
        "post": "post",
        "pre": "pre",
    },
)
class StackSteps:
    def __init__(
        self,
        *,
        stack: _Stack_9f43e4a3,
        change_set: typing.Optional[typing.Sequence["Step"]] = None,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
    ) -> None:
        '''(experimental) Instructions for additional steps that are run at stack level.

        :param stack: (experimental) The stack you want the steps to run in.
        :param change_set: (experimental) Steps that execute after stack is prepared but before stack is deployed. Default: - no additional steps
        :param post: (experimental) Steps that execute after stack is deployed. Default: - no additional steps
        :param pre: (experimental) Steps that execute before stack is prepared. Default: - no additional steps

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import pipelines
            
            # stack: monocdk.Stack
            # step: pipelines.Step
            
            stack_steps = pipelines.StackSteps(
                stack=stack,
            
                # the properties below are optional
                change_set=[step],
                post=[step],
                pre=[step]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d6daea77b45dcb8268287e85ce6401e8eb98630995956c31836eac882f666d7)
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument change_set", value=change_set, expected_type=type_hints["change_set"])
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "stack": stack,
        }
        if change_set is not None:
            self._values["change_set"] = change_set
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre

    @builtins.property
    def stack(self) -> _Stack_9f43e4a3:
        '''(experimental) The stack you want the steps to run in.

        :stability: experimental
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_Stack_9f43e4a3, result)

    @builtins.property
    def change_set(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Steps that execute after stack is prepared but before stack is deployed.

        :default: - no additional steps

        :stability: experimental
        '''
        result = self._values.get("change_set")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def post(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Steps that execute after stack is deployed.

        :default: - no additional steps

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Steps that execute before stack is prepared.

        :default: - no additional steps

        :stability: experimental
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StackSteps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class StageDeployment(
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.StageDeployment",
):
    '''(experimental) Deployment of a single ``Stage``.

    A ``Stage`` consists of one or more ``Stacks``, which will be
    deployed in dependency order.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import monocdk as monocdk
        from monocdk import pipelines
        
        # stack: monocdk.Stack
        # stage: monocdk.Stage
        # step: pipelines.Step
        
        stage_deployment = pipelines.StageDeployment.from_stage(stage,
            post=[step],
            pre=[step],
            stack_steps=[pipelines.StackSteps(
                stack=stack,
        
                # the properties below are optional
                change_set=[step],
                post=[step],
                pre=[step]
            )],
            stage_name="stageName"
        )
    '''

    @jsii.member(jsii_name="fromStage")
    @builtins.classmethod
    def from_stage(
        cls,
        stage: _Stage_9729985a,
        *,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> "StageDeployment":
        '''(experimental) Create a new ``StageDeployment`` from a ``Stage``.

        Synthesizes the target stage, and deployes the stacks found inside
        in dependency order.

        :param stage: -
        :param post: (experimental) Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: (experimental) Instructions for additional steps that are run at the stack level. Default: - No additional instructions
        :param stage_name: (experimental) Stage name to use in the pipeline. Default: - Use Stage's construct ID

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bbae825bd30eec9062ec6592072743027c2511f1400096d05eca75ec51887542)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        props = StageDeploymentProps(
            post=post, pre=pre, stack_steps=stack_steps, stage_name=stage_name
        )

        return typing.cast("StageDeployment", jsii.sinvoke(cls, "fromStage", [stage, props]))

    @jsii.member(jsii_name="addPost")
    def add_post(self, *steps: "Step") -> None:
        '''(experimental) Add an additional step to run after all of the stacks in this stage.

        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c0244aef5fcff04ee6efad7dc0c39f5f9644b965c8227457e72169470b67a0b)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPost", [*steps]))

    @jsii.member(jsii_name="addPre")
    def add_pre(self, *steps: "Step") -> None:
        '''(experimental) Add an additional step to run before any of the stacks in this stage.

        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d44a927346e96ba73dde340cd6e31e6e1adf346dbdb0a91f8d56dea3bc1d316)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPre", [*steps]))

    @builtins.property
    @jsii.member(jsii_name="post")
    def post(self) -> typing.List["Step"]:
        '''(experimental) Additional steps that are run after all of the stacks in the stage.

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "post"))

    @builtins.property
    @jsii.member(jsii_name="pre")
    def pre(self) -> typing.List["Step"]:
        '''(experimental) Additional steps that are run before any of the stacks in the stage.

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "pre"))

    @builtins.property
    @jsii.member(jsii_name="stacks")
    def stacks(self) -> typing.List[StackDeployment]:
        '''(experimental) The stacks deployed in this stage.

        :stability: experimental
        '''
        return typing.cast(typing.List[StackDeployment], jsii.get(self, "stacks"))

    @builtins.property
    @jsii.member(jsii_name="stackSteps")
    def stack_steps(self) -> typing.List[StackSteps]:
        '''(experimental) Instructions for additional steps that are run at stack level.

        :stability: experimental
        '''
        return typing.cast(typing.List[StackSteps], jsii.get(self, "stackSteps"))

    @builtins.property
    @jsii.member(jsii_name="stageName")
    def stage_name(self) -> builtins.str:
        '''(experimental) The display name of this stage.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "stageName"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.StageDeploymentProps",
    jsii_struct_bases=[],
    name_mapping={
        "post": "post",
        "pre": "pre",
        "stack_steps": "stackSteps",
        "stage_name": "stageName",
    },
)
class StageDeploymentProps:
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence["Step"]] = None,
        pre: typing.Optional[typing.Sequence["Step"]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
        stage_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for a ``StageDeployment``.

        :param post: (experimental) Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: (experimental) Instructions for additional steps that are run at the stack level. Default: - No additional instructions
        :param stage_name: (experimental) Stage name to use in the pipeline. Default: - Use Stage's construct ID

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import monocdk as monocdk
            from monocdk import pipelines
            
            # stack: monocdk.Stack
            # step: pipelines.Step
            
            stage_deployment_props = pipelines.StageDeploymentProps(
                post=[step],
                pre=[step],
                stack_steps=[pipelines.StackSteps(
                    stack=stack,
            
                    # the properties below are optional
                    change_set=[step],
                    post=[step],
                    pre=[step]
                )],
                stage_name="stageName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ab88758be77812a028d3398c40feabfc7dacc4ee296d01e58256b4d85937733)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
            check_type(argname="argument stack_steps", value=stack_steps, expected_type=type_hints["stack_steps"])
            check_type(argname="argument stage_name", value=stage_name, expected_type=type_hints["stage_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre
        if stack_steps is not None:
            self._values["stack_steps"] = stack_steps
        if stage_name is not None:
            self._values["stage_name"] = stage_name

    @builtins.property
    def post(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Additional steps to run after all of the stacks in the stage.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List["Step"]]:
        '''(experimental) Additional steps to run before any of the stacks in the stage.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List["Step"]], result)

    @builtins.property
    def stack_steps(self) -> typing.Optional[typing.List[StackSteps]]:
        '''(experimental) Instructions for additional steps that are run at the stack level.

        :default: - No additional instructions

        :stability: experimental
        '''
        result = self._values.get("stack_steps")
        return typing.cast(typing.Optional[typing.List[StackSteps]], result)

    @builtins.property
    def stage_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Stage name to use in the pipeline.

        :default: - Use Stage's construct ID

        :stability: experimental
        '''
        result = self._values.get("stage_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StageDeploymentProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.StandardNpmSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "build_spec": "buildSpec",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
        "test_commands": "testCommands",
    },
)
class StandardNpmSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(deprecated) Options for a convention-based synth using NPM.

        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param build_command: (deprecated) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (deprecated) The install command. Default: 'npm ci'
        :param synth_command: (deprecated) The synth command. Default: 'npx cdk synth'
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            source_artifact = codepipeline.Artifact()
            cloud_assembly_artifact = codepipeline.Artifact()
            pipeline = pipelines.CdkPipeline(self, "MyPipeline",
                cloud_assembly_artifact=cloud_assembly_artifact,
                synth_action=pipelines.SimpleSynthAction.standard_npm_synth(
                    source_artifact=source_artifact,
                    cloud_assembly_artifact=cloud_assembly_artifact,
                    environment=cdk.aws_codebuild.BuildEnvironment(
                        privileged=True
                    )
                )
            )
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__13e06e4060aaafc208237d76240a1f7dd00a48369e1b28ac6002ce075c0998ef)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument source_artifact", value=source_artifact, expected_type=type_hints["source_artifact"])
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument copy_environment_variables", value=copy_environment_variables, expected_type=type_hints["copy_environment_variables"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument install_command", value=install_command, expected_type=type_hints["install_command"])
            check_type(argname="argument synth_command", value=synth_command, expected_type=type_hints["synth_command"])
            check_type(argname="argument test_commands", value=test_commands, expected_type=type_hints["test_commands"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command
        if test_commands is not None:
            self._values["test_commands"] = test_commands

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The artifact where the CloudAssembly should be emitted.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The source artifact of the CodePipeline.

        :stability: deprecated
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the build action.

        :default: 'Synth'

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(deprecated) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: deprecated
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) custom BuildSpec that is merged with the generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: deprecated
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(deprecated) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(deprecated) Environment variables to send into build.

        NOTE: You may run into the 1000-character limit for the Action configuration if you have a large
        number of variables or if their names or values are very long.
        If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead.
        However, you will not be able to use CodePipeline Variables in this case.

        :default: - No additional environment variables

        :stability: deprecated
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(deprecated) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: deprecated
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: deprecated
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        :default: - No build required

        :stability: deprecated
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The install command.

        :default: 'npm ci'

        :stability: deprecated
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synth_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The synth command.

        :default: 'npx cdk synth'

        :stability: deprecated
        '''
        result = self._values.get("synth_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Test commands.

        These commands are run after the build commands but before the
        synth command.

        :default: - No test commands

        :stability: deprecated
        '''
        result = self._values.get("test_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardNpmSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.StandardYarnSynthOptions",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "build_spec": "buildSpec",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "build_command": "buildCommand",
        "install_command": "installCommand",
        "synth_command": "synthCommand",
        "test_commands": "testCommands",
    },
)
class StandardYarnSynthOptions(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        build_command: typing.Optional[builtins.str] = None,
        install_command: typing.Optional[builtins.str] = None,
        synth_command: typing.Optional[builtins.str] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(deprecated) Options for a convention-based synth using Yarn.

        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param build_command: (deprecated) The build command. By default, we assume NPM projects are either written in JavaScript or are using ``ts-node``, so don't need a build command. Otherwise, put the build command here, for example ``npm run build``. Default: - No build required
        :param install_command: (deprecated) The install command. Default: 'yarn install --frozen-lockfile'
        :param synth_command: (deprecated) The synth command. Default: 'npx cdk synth'
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import aws_s3 as s3
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # bucket: s3.Bucket
            # build_image: codebuild.IBuildImage
            # build_spec: codebuild.BuildSpec
            # policy_statement: iam.PolicyStatement
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # value: Any
            # vpc: ec2.Vpc
            
            standard_yarn_synth_options = pipelines.StandardYarnSynthOptions(
                cloud_assembly_artifact=artifact,
                source_artifact=artifact,
            
                # the properties below are optional
                action_name="actionName",
                additional_artifacts=[pipelines.AdditionalArtifact(
                    artifact=artifact,
                    directory="directory"
                )],
                build_command="buildCommand",
                build_spec=build_spec,
                copy_environment_variables=["copyEnvironmentVariables"],
                environment=codebuild.BuildEnvironment(
                    build_image=build_image,
                    certificate=codebuild.BuildEnvironmentCertificate(
                        bucket=bucket,
                        object_key="objectKey"
                    ),
                    compute_type=codebuild.ComputeType.SMALL,
                    environment_variables={
                        "environment_variables_key": codebuild.BuildEnvironmentVariable(
                            value=value,
            
                            # the properties below are optional
                            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                        )
                    },
                    privileged=False
                ),
                environment_variables={
                    "environment_variables_key": codebuild.BuildEnvironmentVariable(
                        value=value,
            
                        # the properties below are optional
                        type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                    )
                },
                install_command="installCommand",
                project_name="projectName",
                role_policy_statements=[policy_statement],
                subdirectory="subdirectory",
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                synth_command="synthCommand",
                test_commands=["testCommands"],
                vpc=vpc
            )
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7bdc6a4e618df7aa27db0344d6980d298db7001a4603e89fb12bc1f5027f4744)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument source_artifact", value=source_artifact, expected_type=type_hints["source_artifact"])
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument copy_environment_variables", value=copy_environment_variables, expected_type=type_hints["copy_environment_variables"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument install_command", value=install_command, expected_type=type_hints["install_command"])
            check_type(argname="argument synth_command", value=synth_command, expected_type=type_hints["synth_command"])
            check_type(argname="argument test_commands", value=test_commands, expected_type=type_hints["test_commands"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if install_command is not None:
            self._values["install_command"] = install_command
        if synth_command is not None:
            self._values["synth_command"] = synth_command
        if test_commands is not None:
            self._values["test_commands"] = test_commands

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The artifact where the CloudAssembly should be emitted.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The source artifact of the CodePipeline.

        :stability: deprecated
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the build action.

        :default: 'Synth'

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(deprecated) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: deprecated
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) custom BuildSpec that is merged with the generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: deprecated
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(deprecated) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(deprecated) Environment variables to send into build.

        NOTE: You may run into the 1000-character limit for the Action configuration if you have a large
        number of variables or if their names or values are very long.
        If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead.
        However, you will not be able to use CodePipeline Variables in this case.

        :default: - No additional environment variables

        :stability: deprecated
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(deprecated) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: deprecated
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: deprecated
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The build command.

        By default, we assume NPM projects are either written in JavaScript or are
        using ``ts-node``, so don't need a build command.

        Otherwise, put the build command here, for example ``npm run build``.

        :default: - No build required

        :stability: deprecated
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The install command.

        :default: 'yarn install --frozen-lockfile'

        :stability: deprecated
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def synth_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The synth command.

        :default: 'npx cdk synth'

        :stability: deprecated
        '''
        result = self._values.get("synth_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def test_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Test commands.

        These commands are run after the build commands but before the
        synth command.

        :default: - No test commands

        :stability: deprecated
        '''
        result = self._values.get("test_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StandardYarnSynthOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(IFileSetProducer)
class Step(metaclass=jsii.JSIIAbstractClass, jsii_type="monocdk.pipelines.Step"):
    '''(experimental) A generic Step which can be added to a Pipeline.

    Steps can be used to add Sources, Build Actions and Validations
    to your pipeline.

    This class is abstract. See specific subclasses of Step for
    useful steps to add to your Pipeline

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Step A will depend on step B and step B will depend on step C
        ordered_steps = pipelines.Step.sequence([
            pipelines.ManualApprovalStep("A"),
            pipelines.ManualApprovalStep("B"),
            pipelines.ManualApprovalStep("C")
        ])
    '''

    def __init__(self, id: builtins.str) -> None:
        '''
        :param id: Identifier for this step.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cc6ac099d78b2aa83433e11000f3f983d367125575066f1f5230f770688c2a6e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="sequence")
    @builtins.classmethod
    def sequence(cls, steps: typing.Sequence["Step"]) -> typing.List["Step"]:
        '''(experimental) Define a sequence of steps to be executed in order.

        If you need more fine-grained step ordering, use the ``addStepDependency()``
        API. For example, if you want ``secondStep`` to occur after ``firstStep``, call
        ``secondStep.addStepDependency(firstStep)``.

        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3745bac2f2fca236c0359fc3123da78a73451c197cb968ccd41b5f1f48de32d7)
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
        return typing.cast(typing.List["Step"], jsii.sinvoke(cls, "sequence", [steps]))

    @jsii.member(jsii_name="addDependencyFileSet")
    def _add_dependency_file_set(self, fs: "FileSet") -> None:
        '''(experimental) Add an additional FileSet to the set of file sets required by this step.

        This will lead to a dependency on the producer of that file set.

        :param fs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ac834aea5414ce95f5062c2a6343e6e9bc5c7f3458e92cdda4bb3a0d2fe4c1fc)
            check_type(argname="argument fs", value=fs, expected_type=type_hints["fs"])
        return typing.cast(None, jsii.invoke(self, "addDependencyFileSet", [fs]))

    @jsii.member(jsii_name="addStepDependency")
    def add_step_dependency(self, step: "Step") -> None:
        '''(experimental) Add a dependency on another step.

        :param step: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__18089ae266c819934cc9906ae5663b1602439f40e20f258beb5698017c052906)
            check_type(argname="argument step", value=step, expected_type=type_hints["step"])
        return typing.cast(None, jsii.invoke(self, "addStepDependency", [step]))

    @jsii.member(jsii_name="configurePrimaryOutput")
    def _configure_primary_output(self, fs: "FileSet") -> None:
        '''(experimental) Configure the given FileSet as the primary output of this step.

        :param fs: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d2aaee5dadd18842e2dfea554fbf1b749e1d9d784b98b6d2bfccdca6f250d7ef)
            check_type(argname="argument fs", value=fs, expected_type=type_hints["fs"])
        return typing.cast(None, jsii.invoke(self, "configurePrimaryOutput", [fs]))

    @jsii.member(jsii_name="discoverReferencedOutputs")
    def _discover_referenced_outputs(self, structure: typing.Any) -> None:
        '''(experimental) Crawl the given structure for references to StepOutputs and add dependencies on all steps found.

        Should be called in the constructor of subclasses based on what the user
        passes in as construction properties. The format of the structure passed in
        here does not have to correspond exactly to what gets rendered into the
        engine, it just needs to contain the same data.

        :param structure: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1156c4db1d2756ee467272e3ce5f6d4e69528cfadab77412b2fc6c86d0714aa6)
            check_type(argname="argument structure", value=structure, expected_type=type_hints["structure"])
        return typing.cast(None, jsii.invoke(self, "discoverReferencedOutputs", [structure]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this Step.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="dependencies")
    def dependencies(self) -> typing.List["Step"]:
        '''(experimental) Return the steps this step depends on, based on the FileSets it requires.

        :stability: experimental
        '''
        return typing.cast(typing.List["Step"], jsii.get(self, "dependencies"))

    @builtins.property
    @jsii.member(jsii_name="dependencyFileSets")
    def dependency_file_sets(self) -> typing.List["FileSet"]:
        '''(experimental) The list of FileSets consumed by this Step.

        :stability: experimental
        '''
        return typing.cast(typing.List["FileSet"], jsii.get(self, "dependencyFileSets"))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Identifier for this step.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="isSource")
    def is_source(self) -> builtins.bool:
        '''(experimental) Whether or not this is a Source step.

        What it means to be a Source step depends on the engine.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isSource"))

    @builtins.property
    @jsii.member(jsii_name="primaryOutput")
    def primary_output(self) -> typing.Optional["FileSet"]:
        '''(experimental) The primary FileSet produced by this Step.

        Not all steps produce an output FileSet--if they do
        you can substitute the ``Step`` object for the ``FileSet`` object.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["FileSet"], jsii.get(self, "primaryOutput"))


class _StepProxy(Step):
    pass

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, Step).__jsii_proxy_class__ = lambda : _StepProxy


@jsii.implements(_IAction_ecd54a08)
class UpdatePipelineAction(
    _Construct_e78e779f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.UpdatePipelineAction",
):
    '''(deprecated) Action to self-mutate the pipeline.

    Creates a CodeBuild project which will use the CDK CLI
    to deploy the pipeline stack.

    You do not need to instantiate this action -- it will automatically
    be added by the pipeline.

    :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

    :stability: deprecated
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codebuild as codebuild
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        # build_spec: codebuild.BuildSpec
        # docker_credential: pipelines.DockerCredential
        
        update_pipeline_action = pipelines.UpdatePipelineAction(self, "MyUpdatePipelineAction",
            cloud_assembly_input=artifact,
            pipeline_stack_hierarchical_id="pipelineStackHierarchicalId",
        
            # the properties below are optional
            build_spec=build_spec,
            cdk_cli_version="cdkCliVersion",
            docker_credentials=[docker_credential],
            pipeline_stack_name="pipelineStackName",
            privileged=False,
            project_name="projectName"
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        pipeline_stack_hierarchical_id: builtins.str,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        pipeline_stack_name: typing.Optional[builtins.str] = None,
        privileged: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_hierarchical_id: (deprecated) Hierarchical id of the pipeline stack.
        :param build_spec: (deprecated) Custom BuildSpec that is merged with generated one. Default: - none
        :param cdk_cli_version: (deprecated) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param docker_credentials: (deprecated) Docker registries and associated credentials necessary during the pipeline self-update stage. Default: []
        :param pipeline_stack_name: (deprecated) Name of the pipeline stack. Default: - none
        :param privileged: (deprecated) Whether the build step should run in privileged mode. Default: - false
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6aa6e12523cb7010899a8ed2b91bf42e1cee599398e114550c05b736665a0da7)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = UpdatePipelineActionProps(
            cloud_assembly_input=cloud_assembly_input,
            pipeline_stack_hierarchical_id=pipeline_stack_hierarchical_id,
            build_spec=build_spec,
            cdk_cli_version=cdk_cli_version,
            docker_credentials=docker_credentials,
            pipeline_stack_name=pipeline_stack_name,
            privileged=privileged,
            project_name=project_name,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _Construct_e78e779f,
        stage: _IStage_5a7e7342,
        *,
        bucket: _IBucket_73486e29,
        role: _IRole_59af6f50,
    ) -> _ActionConfig_0c698b52:
        '''(deprecated) Exists to implement IAction.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cc359fed8424414c70f0a816104c60b835eea14de12980e41cbcbe3a495515d)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _ActionBindOptions_20e0a317(bucket=bucket, role=role)

        return typing.cast(_ActionConfig_0c698b52, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_IRuleTarget_d45ec729] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
        event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_Schedule_297d3fad] = None,
        targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
    ) -> _Rule_6cfff189:
        '''(deprecated) Exists to implement IAction.

        :param name: -
        :param target: -
        :param description: (experimental) A description of the rule's purpose. Default: - No description.
        :param enabled: (experimental) Indicates whether the rule is enabled. Default: true
        :param event_bus: (experimental) The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: (experimental) Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: (experimental) A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: (experimental) The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: (experimental) Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0f06076c81cb6e0d2674dcb8c8226256384e75baea58011bd488c3d7f1ab83e6)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _RuleProps_32051f01(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_Rule_6cfff189, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _ActionProperties_c7760ac6:
        '''(deprecated) Exists to implement IAction.

        :stability: deprecated
        '''
        return typing.cast(_ActionProperties_c7760ac6, jsii.get(self, "actionProperties"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.UpdatePipelineActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "pipeline_stack_hierarchical_id": "pipelineStackHierarchicalId",
        "build_spec": "buildSpec",
        "cdk_cli_version": "cdkCliVersion",
        "docker_credentials": "dockerCredentials",
        "pipeline_stack_name": "pipelineStackName",
        "privileged": "privileged",
        "project_name": "projectName",
    },
)
class UpdatePipelineActionProps:
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        pipeline_stack_hierarchical_id: builtins.str,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        pipeline_stack_name: typing.Optional[builtins.str] = None,
        privileged: typing.Optional[builtins.bool] = None,
        project_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Props for the UpdatePipelineAction.

        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param pipeline_stack_hierarchical_id: (deprecated) Hierarchical id of the pipeline stack.
        :param build_spec: (deprecated) Custom BuildSpec that is merged with generated one. Default: - none
        :param cdk_cli_version: (deprecated) Version of CDK CLI to 'npm install'. Default: - Latest version
        :param docker_credentials: (deprecated) Docker registries and associated credentials necessary during the pipeline self-update stage. Default: []
        :param pipeline_stack_name: (deprecated) Name of the pipeline stack. Default: - none
        :param privileged: (deprecated) Whether the build step should run in privileged mode. Default: - false
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # build_spec: codebuild.BuildSpec
            # docker_credential: pipelines.DockerCredential
            
            update_pipeline_action_props = pipelines.UpdatePipelineActionProps(
                cloud_assembly_input=artifact,
                pipeline_stack_hierarchical_id="pipelineStackHierarchicalId",
            
                # the properties below are optional
                build_spec=build_spec,
                cdk_cli_version="cdkCliVersion",
                docker_credentials=[docker_credential],
                pipeline_stack_name="pipelineStackName",
                privileged=False,
                project_name="projectName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98ea5f4d415127a7ce6e7d4d5d8bf8bafa6b92876d1d3441223a56be3779b671)
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument pipeline_stack_hierarchical_id", value=pipeline_stack_hierarchical_id, expected_type=type_hints["pipeline_stack_hierarchical_id"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument pipeline_stack_name", value=pipeline_stack_name, expected_type=type_hints["pipeline_stack_name"])
            check_type(argname="argument privileged", value=privileged, expected_type=type_hints["privileged"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
            "pipeline_stack_hierarchical_id": pipeline_stack_hierarchical_id,
        }
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if pipeline_stack_name is not None:
            self._values["pipeline_stack_name"] = pipeline_stack_name
        if privileged is not None:
            self._values["privileged"] = privileged
        if project_name is not None:
            self._values["project_name"] = project_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def pipeline_stack_hierarchical_id(self) -> builtins.str:
        '''(deprecated) Hierarchical id of the pipeline stack.

        :stability: deprecated
        '''
        result = self._values.get("pipeline_stack_hierarchical_id")
        assert result is not None, "Required property 'pipeline_stack_hierarchical_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) Custom BuildSpec that is merged with generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Version of CDK CLI to 'npm install'.

        :default: - Latest version

        :stability: deprecated
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_credentials(self) -> typing.Optional[typing.List[DockerCredential]]:
        '''(deprecated) Docker registries and associated credentials necessary during the pipeline self-update stage.

        :default: []

        :stability: deprecated
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[DockerCredential]], result)

    @builtins.property
    def pipeline_stack_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the pipeline stack.

        :default: - none

        :deprecated: - Use ``pipelineStackHierarchicalId`` instead.

        :stability: deprecated
        '''
        result = self._values.get("pipeline_stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def privileged(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Whether the build step should run in privileged mode.

        :default: - false

        :stability: deprecated
        '''
        result = self._values.get("privileged")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "UpdatePipelineActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Wave(metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.Wave"):
    '''(experimental) Multiple stages that are deployed in parallel.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # pipeline: pipelines.CodePipeline
        
        europe_wave = pipeline.add_wave("Europe")
        europe_wave.add_stage(MyApplicationStage(self, "Ireland",
            env=cdk.Environment(region="eu-west-1")
        ))
        europe_wave.add_stage(MyApplicationStage(self, "Germany",
            env=cdk.Environment(region="eu-central-1")
        ))
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        post: typing.Optional[typing.Sequence[Step]] = None,
        pre: typing.Optional[typing.Sequence[Step]] = None,
    ) -> None:
        '''
        :param id: Identifier for this Wave.
        :param post: (experimental) Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4c81c281b340fcfad218742c416caae2ad8edaf8e50a08fafe9b39487b0716a3)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = WaveProps(post=post, pre=pre)

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="addPost")
    def add_post(self, *steps: Step) -> None:
        '''(experimental) Add an additional step to run after all of the stages in this wave.

        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5c3d6e1bb54a453d5e3450ed26e45bac6dc6ec4f8f8d3b7a341ebe01d14a7642)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPost", [*steps]))

    @jsii.member(jsii_name="addPre")
    def add_pre(self, *steps: Step) -> None:
        '''(experimental) Add an additional step to run before any of the stages in this wave.

        :param steps: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8460205a923996e7a85baf47ac9cfe3b025855b5b6f4bdb241f6976065ae5816)
            check_type(argname="argument steps", value=steps, expected_type=typing.Tuple[type_hints["steps"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "addPre", [*steps]))

    @jsii.member(jsii_name="addStage")
    def add_stage(
        self,
        stage: _Stage_9729985a,
        *,
        post: typing.Optional[typing.Sequence[Step]] = None,
        pre: typing.Optional[typing.Sequence[Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> StageDeployment:
        '''(experimental) Add a Stage to this wave.

        It will be deployed in parallel with all other stages in this
        wave.

        :param stage: -
        :param post: (experimental) Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: (experimental) Instructions for stack level steps. Default: - No additional instructions

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cb682cda07b2c2d6dbb6f200aeceb5bee91916059c7592b004a9fe1fe838030e)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = AddStageOpts(post=post, pre=pre, stack_steps=stack_steps)

        return typing.cast(StageDeployment, jsii.invoke(self, "addStage", [stage, options]))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Identifier for this Wave.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="post")
    def post(self) -> typing.List[Step]:
        '''(experimental) Additional steps that are run after all of the stages in the wave.

        :stability: experimental
        '''
        return typing.cast(typing.List[Step], jsii.get(self, "post"))

    @builtins.property
    @jsii.member(jsii_name="pre")
    def pre(self) -> typing.List[Step]:
        '''(experimental) Additional steps that are run before any of the stages in the wave.

        :stability: experimental
        '''
        return typing.cast(typing.List[Step], jsii.get(self, "pre"))

    @builtins.property
    @jsii.member(jsii_name="stages")
    def stages(self) -> typing.List[StageDeployment]:
        '''(experimental) The stages that are deployed in this wave.

        :stability: experimental
        '''
        return typing.cast(typing.List[StageDeployment], jsii.get(self, "stages"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.WaveOptions",
    jsii_struct_bases=[],
    name_mapping={"post": "post", "pre": "pre"},
)
class WaveOptions:
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence[Step]] = None,
        pre: typing.Optional[typing.Sequence[Step]] = None,
    ) -> None:
        '''(experimental) Options to pass to ``addWave``.

        :param post: (experimental) Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        :exampleMetadata: infused

        Example::

            pipeline = pipelines.CodePipeline(self, "Pipeline",
                synth=pipelines.ShellStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["npm ci", "npm run build", "npx cdk synth"]
                ),
            
                # Turn this on because the pipeline uses Docker image assets
                docker_enabled_for_self_mutation=True
            )
            
            pipeline.add_wave("MyWave",
                post=[
                    pipelines.CodeBuildStep("RunApproval",
                        commands=["command-from-image"],
                        build_environment=cdk.aws_codebuild.BuildEnvironment(
                            # The user of a Docker image asset in the pipeline requires turning on
                            # 'dockerEnabledForSelfMutation'.
                            build_image=codebuild.LinuxBuildImage.from_asset(self, "Image",
                                directory="./docker-image"
                            )
                        )
                    )
                ]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3dd0f783298c6421e8b29e19d65812322f309c595caa14b7a9f8fdbefc00fee0)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre

    @builtins.property
    def post(self) -> typing.Optional[typing.List[Step]]:
        '''(experimental) Additional steps to run after all of the stages in the wave.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List[Step]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List[Step]]:
        '''(experimental) Additional steps to run before any of the stages in the wave.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List[Step]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaveOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.WaveProps",
    jsii_struct_bases=[],
    name_mapping={"post": "post", "pre": "pre"},
)
class WaveProps:
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence[Step]] = None,
        pre: typing.Optional[typing.Sequence[Step]] = None,
    ) -> None:
        '''(experimental) Construction properties for a ``Wave``.

        :param post: (experimental) Additional steps to run after all of the stages in the wave. Default: - No additional steps
        :param pre: (experimental) Additional steps to run before any of the stages in the wave. Default: - No additional steps

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import pipelines
            
            # step: pipelines.Step
            
            wave_props = pipelines.WaveProps(
                post=[step],
                pre=[step]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__adc974eafc2eed0817f0733876ffe71c1f108ed7fa2a50d5f4dc1c8e78427838)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre

    @builtins.property
    def post(self) -> typing.Optional[typing.List[Step]]:
        '''(experimental) Additional steps to run after all of the stages in the wave.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List[Step]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List[Step]]:
        '''(experimental) Additional steps to run before any of the stages in the wave.

        :default: - No additional steps

        :stability: experimental
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List[Step]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WaveProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.AddStageOptions",
    jsii_struct_bases=[BaseStageOptions],
    name_mapping={
        "confirm_broadening_permissions": "confirmBroadeningPermissions",
        "security_notification_topic": "securityNotificationTopic",
        "extra_run_order_space": "extraRunOrderSpace",
        "manual_approvals": "manualApprovals",
    },
)
class AddStageOptions(BaseStageOptions):
    def __init__(
        self,
        *,
        confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
        security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
        extra_run_order_space: typing.Optional[jsii.Number] = None,
        manual_approvals: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''(deprecated) Options for adding an application stage to a pipeline.

        :param confirm_broadening_permissions: (deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes. If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this property to override the stage configuration. For example, Pipeline Stage "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three applications will run a security check, but if we want to disable the one for "C", we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline stage behavior. Adds 1 to the run order space. Default: false
        :param security_notification_topic: (deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application. Default: undefined no notification topic for security check manual approval action
        :param extra_run_order_space: (deprecated) Add room for extra actions. You can use this to make extra room in the runOrder sequence between the changeset 'prepare' and 'execute' actions and insert your own actions there. Default: 0
        :param manual_approvals: (deprecated) Add manual approvals before executing change sets. This gives humans the opportunity to confirm the change set looks alright before deploying it. Default: false

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_sns as sns
            from monocdk import pipelines
            
            # topic: sns.Topic
            
            add_stage_options = pipelines.AddStageOptions(
                confirm_broadening_permissions=False,
                extra_run_order_space=123,
                manual_approvals=False,
                security_notification_topic=topic
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e0fa7d0ae0a29b445ff18db93c9ff98dec5c3e00a2edef37dec03ef223dadc8)
            check_type(argname="argument confirm_broadening_permissions", value=confirm_broadening_permissions, expected_type=type_hints["confirm_broadening_permissions"])
            check_type(argname="argument security_notification_topic", value=security_notification_topic, expected_type=type_hints["security_notification_topic"])
            check_type(argname="argument extra_run_order_space", value=extra_run_order_space, expected_type=type_hints["extra_run_order_space"])
            check_type(argname="argument manual_approvals", value=manual_approvals, expected_type=type_hints["manual_approvals"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if confirm_broadening_permissions is not None:
            self._values["confirm_broadening_permissions"] = confirm_broadening_permissions
        if security_notification_topic is not None:
            self._values["security_notification_topic"] = security_notification_topic
        if extra_run_order_space is not None:
            self._values["extra_run_order_space"] = extra_run_order_space
        if manual_approvals is not None:
            self._values["manual_approvals"] = manual_approvals

    @builtins.property
    def confirm_broadening_permissions(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Runs a ``cdk diff --security-only --fail`` to pause the pipeline if there are any security changes.

        If the stage is configured with ``confirmBroadeningPermissions`` enabled, you can use this
        property to override the stage configuration. For example, Pipeline Stage
        "Prod" has confirmBroadeningPermissions enabled, with applications "A", "B", "C". All three
        applications will run a security check, but if we want to disable the one for "C",
        we run ``stage.addApplication(C, { confirmBroadeningPermissions: false })`` to override the pipeline
        stage behavior.

        Adds 1 to the run order space.

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("confirm_broadening_permissions")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def security_notification_topic(self) -> typing.Optional[_ITopic_465e36b9]:
        '''(deprecated) Optional SNS topic to send notifications to when the security check registers changes within the application.

        :default: undefined no notification topic for security check manual approval action

        :stability: deprecated
        '''
        result = self._values.get("security_notification_topic")
        return typing.cast(typing.Optional[_ITopic_465e36b9], result)

    @builtins.property
    def extra_run_order_space(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Add room for extra actions.

        You can use this to make extra room in the runOrder sequence between the
        changeset 'prepare' and 'execute' actions and insert your own actions there.

        :default: 0

        :stability: deprecated
        '''
        result = self._values.get("extra_run_order_space")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def manual_approvals(self) -> typing.Optional[builtins.bool]:
        '''(deprecated) Add manual approvals before executing change sets.

        This gives humans the opportunity to confirm the change set looks alright
        before deploying it.

        :default: false

        :stability: deprecated
        '''
        result = self._values.get("manual_approvals")
        return typing.cast(typing.Optional[builtins.bool], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CdkStackActionFromArtifactOptions",
    jsii_struct_bases=[DeployCdkStackActionOptions],
    name_mapping={
        "cloud_assembly_input": "cloudAssemblyInput",
        "base_action_name": "baseActionName",
        "change_set_name": "changeSetName",
        "execute_run_order": "executeRunOrder",
        "output": "output",
        "output_file_name": "outputFileName",
        "prepare_run_order": "prepareRunOrder",
        "stack_name": "stackName",
    },
)
class CdkStackActionFromArtifactOptions(DeployCdkStackActionOptions):
    def __init__(
        self,
        *,
        cloud_assembly_input: _Artifact_9905eec2,
        base_action_name: typing.Optional[builtins.str] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        execute_run_order: typing.Optional[jsii.Number] = None,
        output: typing.Optional[_Artifact_9905eec2] = None,
        output_file_name: typing.Optional[builtins.str] = None,
        prepare_run_order: typing.Optional[jsii.Number] = None,
        stack_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(deprecated) Options for the 'fromStackArtifact' operation.

        :param cloud_assembly_input: (deprecated) The CodePipeline artifact that holds the Cloud Assembly.
        :param base_action_name: (deprecated) Base name of the action. Default: stackName
        :param change_set_name: (deprecated) Name of the change set to create and deploy. Default: 'PipelineChange'
        :param execute_run_order: (deprecated) Run order for the Execute action. Default: - prepareRunOrder + 1
        :param output: (deprecated) Artifact to write Stack Outputs to. Default: - No outputs
        :param output_file_name: (deprecated) Filename in output to write Stack outputs to. Default: - Required when 'output' is set
        :param prepare_run_order: (deprecated) Run order for the Prepare action. Default: 1
        :param stack_name: (deprecated) The name of the stack that should be created/updated. Default: - Same as stack artifact

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            
            cdk_stack_action_from_artifact_options = pipelines.CdkStackActionFromArtifactOptions(
                cloud_assembly_input=artifact,
            
                # the properties below are optional
                base_action_name="baseActionName",
                change_set_name="changeSetName",
                execute_run_order=123,
                output=artifact,
                output_file_name="outputFileName",
                prepare_run_order=123,
                stack_name="stackName"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c0e0da41d774fadaaee80a06929a0d56b3f96d869344aeed3da0ea5aa63cad8)
            check_type(argname="argument cloud_assembly_input", value=cloud_assembly_input, expected_type=type_hints["cloud_assembly_input"])
            check_type(argname="argument base_action_name", value=base_action_name, expected_type=type_hints["base_action_name"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument execute_run_order", value=execute_run_order, expected_type=type_hints["execute_run_order"])
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument output_file_name", value=output_file_name, expected_type=type_hints["output_file_name"])
            check_type(argname="argument prepare_run_order", value=prepare_run_order, expected_type=type_hints["prepare_run_order"])
            check_type(argname="argument stack_name", value=stack_name, expected_type=type_hints["stack_name"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_input": cloud_assembly_input,
        }
        if base_action_name is not None:
            self._values["base_action_name"] = base_action_name
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if execute_run_order is not None:
            self._values["execute_run_order"] = execute_run_order
        if output is not None:
            self._values["output"] = output
        if output_file_name is not None:
            self._values["output_file_name"] = output_file_name
        if prepare_run_order is not None:
            self._values["prepare_run_order"] = prepare_run_order
        if stack_name is not None:
            self._values["stack_name"] = stack_name

    @builtins.property
    def cloud_assembly_input(self) -> _Artifact_9905eec2:
        '''(deprecated) The CodePipeline artifact that holds the Cloud Assembly.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_input")
        assert result is not None, "Required property 'cloud_assembly_input' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def base_action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Base name of the action.

        :default: stackName

        :stability: deprecated
        '''
        result = self._values.get("base_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the change set to create and deploy.

        :default: 'PipelineChange'

        :stability: deprecated
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Execute action.

        :default: - prepareRunOrder + 1

        :stability: deprecated
        '''
        result = self._values.get("execute_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def output(self) -> typing.Optional[_Artifact_9905eec2]:
        '''(deprecated) Artifact to write Stack Outputs to.

        :default: - No outputs

        :stability: deprecated
        '''
        result = self._values.get("output")
        return typing.cast(typing.Optional[_Artifact_9905eec2], result)

    @builtins.property
    def output_file_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Filename in output to write Stack outputs to.

        :default: - Required when 'output' is set

        :stability: deprecated
        '''
        result = self._values.get("output_file_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def prepare_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) Run order for the Prepare action.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("prepare_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def stack_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the stack that should be created/updated.

        :default: - Same as stack artifact

        :stability: deprecated
        '''
        result = self._values.get("stack_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CdkStackActionFromArtifactOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.pipelines.CodeBuildStepProps",
    jsii_struct_bases=[ShellStepProps],
    name_mapping={
        "commands": "commands",
        "additional_inputs": "additionalInputs",
        "env": "env",
        "env_from_cfn_outputs": "envFromCfnOutputs",
        "input": "input",
        "install_commands": "installCommands",
        "primary_output_directory": "primaryOutputDirectory",
        "action_role": "actionRole",
        "build_environment": "buildEnvironment",
        "partial_build_spec": "partialBuildSpec",
        "project_name": "projectName",
        "role": "role",
        "role_policy_statements": "rolePolicyStatements",
        "security_groups": "securityGroups",
        "subnet_selection": "subnetSelection",
        "timeout": "timeout",
        "vpc": "vpc",
    },
)
class CodeBuildStepProps(ShellStepProps):
    def __init__(
        self,
        *,
        commands: typing.Sequence[builtins.str],
        additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
        input: typing.Optional[IFileSetProducer] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_output_directory: typing.Optional[builtins.str] = None,
        action_role: typing.Optional[_IRole_59af6f50] = None,
        build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    ) -> None:
        '''(experimental) Construction props for a CodeBuildStep.

        :param commands: (experimental) Commands to run.
        :param additional_inputs: (experimental) Additional FileSets to put in other directories. Specifies a mapping from directory name to FileSets. During the script execution, the FileSets will be available in the directories indicated. The directory names may be relative. For example, you can put the main input and an additional input side-by-side with the following configuration:: const script = new pipelines.ShellStep('MainScript', { commands: ['npm ci','npm run build','npx cdk synth'], input: pipelines.CodePipelineSource.gitHub('org/source1', 'main'), additionalInputs: { '../siblingdir': pipelines.CodePipelineSource.gitHub('org/source2', 'main'), } }); Default: - No additional inputs
        :param env: (experimental) Environment variables to set. Default: - No environment variables
        :param env_from_cfn_outputs: (experimental) Set environment variables based on Stack Outputs. ``ShellStep``s following stack or stage deployments may access the ``CfnOutput``s of those stacks to get access to --for example--automatically generated resource names or endpoint URLs. Default: - No environment variables created from stack outputs
        :param input: (experimental) FileSet to run these scripts on. The files in the FileSet will be placed in the working directory when the script is executed. Use ``additionalInputs`` to download file sets to other directories as well. Default: - No input specified
        :param install_commands: (experimental) Installation commands to run before the regular commands. For deployment engines that support it, install commands will be classified differently in the job history from the regular ``commands``. Default: - No installation commands
        :param primary_output_directory: (experimental) The directory that will contain the primary output fileset. After running the script, the contents of the given directory will be treated as the primary output of this Step. Default: - No primary output
        :param action_role: (experimental) Custom execution role to be used for the Code Build Action. Default: - A role is automatically created
        :param build_environment: (experimental) Changes to environment. This environment will be combined with the pipeline's default environment. Default: - Use the pipeline's default build environment
        :param partial_build_spec: (experimental) Additional configuration that can only be configured via BuildSpec. You should not use this to specify output artifacts; those should be supplied via the other properties of this class, otherwise CDK Pipelines won't be able to inspect the artifacts. Set the ``commands`` to an empty array if you want to fully specify the BuildSpec using this field. The BuildSpec must be available inline--it cannot reference a file on disk. Default: - BuildSpec completely derived from other properties
        :param project_name: (experimental) Name for the generated CodeBuild project. Default: - Automatically generated
        :param role: (experimental) Custom execution role to be used for the CodeBuild project. Default: - A role is automatically created
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param security_groups: (experimental) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC

        :stability: experimental
        :exampleMetadata: infused

        Example::

            pipelines.CodePipeline(self, "Pipeline",
                synth=pipelines.CodeBuildStep("Synth",
                    input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                        connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                    ),
                    commands=["...", "npm ci", "npm run build", "npx cdk synth", "..."
                    ],
                    role_policy_statements=[
                        iam.PolicyStatement(
                            actions=["sts:AssumeRole"],
                            resources=["*"],
                            conditions={
                                "StringEquals": {
                                    "iam:ResourceTag/aws-cdk:bootstrap-role": "lookup"
                                }
                            }
                        )
                    ]
                )
            )
        '''
        if isinstance(build_environment, dict):
            build_environment = _BuildEnvironment_77bc5f50(**build_environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__437f9584e204e93834fa598928d0925b482a2ce6f1fdfd0254a819e12f077420)
            check_type(argname="argument commands", value=commands, expected_type=type_hints["commands"])
            check_type(argname="argument additional_inputs", value=additional_inputs, expected_type=type_hints["additional_inputs"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument env_from_cfn_outputs", value=env_from_cfn_outputs, expected_type=type_hints["env_from_cfn_outputs"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
            check_type(argname="argument primary_output_directory", value=primary_output_directory, expected_type=type_hints["primary_output_directory"])
            check_type(argname="argument action_role", value=action_role, expected_type=type_hints["action_role"])
            check_type(argname="argument build_environment", value=build_environment, expected_type=type_hints["build_environment"])
            check_type(argname="argument partial_build_spec", value=partial_build_spec, expected_type=type_hints["partial_build_spec"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument security_groups", value=security_groups, expected_type=type_hints["security_groups"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument timeout", value=timeout, expected_type=type_hints["timeout"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "commands": commands,
        }
        if additional_inputs is not None:
            self._values["additional_inputs"] = additional_inputs
        if env is not None:
            self._values["env"] = env
        if env_from_cfn_outputs is not None:
            self._values["env_from_cfn_outputs"] = env_from_cfn_outputs
        if input is not None:
            self._values["input"] = input
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if primary_output_directory is not None:
            self._values["primary_output_directory"] = primary_output_directory
        if action_role is not None:
            self._values["action_role"] = action_role
        if build_environment is not None:
            self._values["build_environment"] = build_environment
        if partial_build_spec is not None:
            self._values["partial_build_spec"] = partial_build_spec
        if project_name is not None:
            self._values["project_name"] = project_name
        if role is not None:
            self._values["role"] = role
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if security_groups is not None:
            self._values["security_groups"] = security_groups
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if timeout is not None:
            self._values["timeout"] = timeout
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Commands to run.

        :stability: experimental
        '''
        result = self._values.get("commands")
        assert result is not None, "Required property 'commands' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def additional_inputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]]:
        '''(experimental) Additional FileSets to put in other directories.

        Specifies a mapping from directory name to FileSets. During the
        script execution, the FileSets will be available in the directories
        indicated.

        The directory names may be relative. For example, you can put
        the main input and an additional input side-by-side with the
        following configuration::

           script = pipelines.ShellStep("MainScript",
               commands=["npm ci", "npm run build", "npx cdk synth"],
               input=pipelines.CodePipelineSource.git_hub("org/source1", "main"),
               additional_inputs={
                   "../siblingdir": pipelines.CodePipelineSource.git_hub("org/source2", "main")
               }
           )

        :default: - No additional inputs

        :stability: experimental
        '''
        result = self._values.get("additional_inputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''(experimental) Environment variables to set.

        :default: - No environment variables

        :stability: experimental
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def env_from_cfn_outputs(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]]:
        '''(experimental) Set environment variables based on Stack Outputs.

        ``ShellStep``s following stack or stage deployments may
        access the ``CfnOutput``s of those stacks to get access to
        --for example--automatically generated resource names or
        endpoint URLs.

        :default: - No environment variables created from stack outputs

        :stability: experimental
        '''
        result = self._values.get("env_from_cfn_outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]], result)

    @builtins.property
    def input(self) -> typing.Optional[IFileSetProducer]:
        '''(experimental) FileSet to run these scripts on.

        The files in the FileSet will be placed in the working directory when
        the script is executed. Use ``additionalInputs`` to download file sets
        to other directories as well.

        :default: - No input specified

        :stability: experimental
        '''
        result = self._values.get("input")
        return typing.cast(typing.Optional[IFileSetProducer], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(experimental) Installation commands to run before the regular commands.

        For deployment engines that support it, install commands will be classified
        differently in the job history from the regular ``commands``.

        :default: - No installation commands

        :stability: experimental
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def primary_output_directory(self) -> typing.Optional[builtins.str]:
        '''(experimental) The directory that will contain the primary output fileset.

        After running the script, the contents of the given directory
        will be treated as the primary output of this Step.

        :default: - No primary output

        :stability: experimental
        '''
        result = self._values.get("primary_output_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def action_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Custom execution role to be used for the Code Build Action.

        :default: - A role is automatically created

        :stability: experimental
        '''
        result = self._values.get("action_role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def build_environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Changes to environment.

        This environment will be combined with the pipeline's default
        environment.

        :default: - Use the pipeline's default build environment

        :stability: experimental
        '''
        result = self._values.get("build_environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def partial_build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) Additional configuration that can only be configured via BuildSpec.

        You should not use this to specify output artifacts; those
        should be supplied via the other properties of this class, otherwise
        CDK Pipelines won't be able to inspect the artifacts.

        Set the ``commands`` to an empty array if you want to fully specify
        the BuildSpec using this field.

        The BuildSpec must be available inline--it cannot reference a file
        on disk.

        :default: - BuildSpec completely derived from other properties

        :stability: experimental
        '''
        result = self._values.get("partial_build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the generated CodeBuild project.

        :default: - Automatically generated

        :stability: experimental
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Custom execution role to be used for the CodeBuild project.

        :default: - A role is automatically created

        :stability: experimental
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_IRole_59af6f50], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: experimental
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Which security group to associate with the script's project network interfaces.

        If no security group is identified, one will be created automatically.

        Only used if 'vpc' is supplied.

        :default: - Security group will be automatically created.

        :stability: experimental
        '''
        result = self._values.get("security_groups")
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: experimental
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        result = self._values.get("timeout")
        return typing.cast(typing.Optional[_Duration_070aa057], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: experimental
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CodeBuildStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodePipeline(
    PipelineBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CodePipeline",
):
    '''(experimental) A CDK Pipeline that uses CodePipeline to deploy CDK apps.

    This is a ``Pipeline`` with its ``engine`` property set to
    ``CodePipelineEngine``, and exists for nicer ergonomics for
    users that don't need to switch out engines.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Modern API
        modern_pipeline = pipelines.CodePipeline(self, "Pipeline",
            self_mutation=False,
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["npm ci", "npm run build", "npx cdk synth"
                ]
            )
        )
        
        # Original API
        cloud_assembly_artifact = codepipeline.Artifact()
        original_pipeline = pipelines.CdkPipeline(self, "Pipeline",
            self_mutating=False,
            cloud_assembly_artifact=cloud_assembly_artifact
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        synth: IFileSetProducer,
        asset_publishing_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        cli_version: typing.Optional[builtins.str] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
        cross_account_keys: typing.Optional[builtins.bool] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
        docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
        pipeline_name: typing.Optional[builtins.str] = None,
        publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
        reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
        self_mutation: typing.Optional[builtins.bool] = None,
        self_mutation_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        synth_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param synth: (experimental) The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param asset_publishing_code_build_defaults: (experimental) Additional customizations to apply to the asset publishing CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param cli_version: (experimental) CDK CLI version to use in self-mutation and asset publishing steps. If you want to lock the CDK CLI version used in the pipeline, by steps that are automatically generated for you, specify the version here. We recommend you do not specify this value, as not specifying it always uses the latest CLI version which is backwards compatible with old versions. If you do specify it, be aware that this version should always be equal to or higher than the version of the CDK framework used by the CDK app, when the CDK commands are run during your pipeline execution. When you change this version, the *next time* the ``SelfMutate`` step runs it will still be using the CLI of the the *previous* version that was in this property: it will only start using the new version after ``SelfMutate`` completes successfully. That means that if you want to update both framework and CLI version, you should update the CLI version first, commit, push and deploy, and only then update the framework version. Default: - Latest version
        :param code_build_defaults: (experimental) Customize the CodeBuild projects created for this pipeline. Default: - All projects run non-privileged build, SMALL instance, LinuxBuildImage.STANDARD_5_0
        :param code_pipeline: (experimental) An existing Pipeline to be reused and built upon. [disable-awslint:ref-via-interface] Default: - a new underlying pipeline is created.
        :param cross_account_keys: (experimental) Create KMS keys for the artifact buckets, allowing cross-account deployments. The artifact buckets have to be encrypted to support deploying CDK apps to another account, so if you want to do that or want to have your artifact buckets encrypted, be sure to set this value to ``true``. Be aware there is a cost associated with maintaining the KMS keys. Default: false
        :param docker_credentials: (experimental) A list of credentials used to authenticate to Docker registries. Specify any credentials necessary within the pipeline to build, synth, update, or publish assets. Default: []
        :param docker_enabled_for_self_mutation: (experimental) Enable Docker for the self-mutate step. Set this to true if the pipeline itself uses Docker container assets (for example, if you use ``LinuxBuildImage.fromAsset()`` as the build image of a CodeBuild step in the pipeline). You do not need to set it if you build Docker image assets in the application Stages and Stacks that are *deployed* by this pipeline. Configures privileged mode for the self-mutation CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the Docker asset in the pipeline. Default: false
        :param docker_enabled_for_synth: (experimental) Enable Docker for the 'synth' step. Set this to true if you are using file assets that require "bundling" anywhere in your application (meaning an asset compilation step will be run with the tools provided by a Docker image), both for the Pipeline stack as well as the application stacks. A common way to use bundling assets in your application is by using the ``@aws-cdk/aws-lambda-nodejs`` library. Configures privileged mode for the synth CodeBuild action. If you are about to turn this on in an already-deployed Pipeline, set the value to ``true`` first, commit and allow the pipeline to self-update, and only then use the bundled asset. Default: false
        :param pipeline_name: (experimental) The name of the CodePipeline pipeline. Default: - Automatically generated
        :param publish_assets_in_parallel: (experimental) Publish assets in multiple CodeBuild projects. If set to false, use one Project per type to publish all assets. Publishing in parallel improves concurrency and may reduce publishing latency, but may also increase overall provisioning time of the CodeBuild projects. Experiment and see what value works best for you. Default: true
        :param reuse_cross_region_support_stacks: (experimental) Reuse the same cross region support stack for all pipelines in the App. Default: - true (Use the same support stack for all pipelines in App)
        :param self_mutation: (experimental) Whether the pipeline will update itself. This needs to be set to ``true`` to allow the pipeline to reconfigure itself when assets or stages are being added to it, and ``true`` is the recommended setting. You can temporarily set this to ``false`` while you are iterating on the pipeline itself and prefer to deploy changes using ``cdk deploy``. Default: true
        :param self_mutation_code_build_defaults: (experimental) Additional customizations to apply to the self mutation CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied
        :param synth_code_build_defaults: (experimental) Additional customizations to apply to the synthesize CodeBuild projects. Default: - Only ``codeBuildDefaults`` are applied

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d85a5fcace279a9c8a8912c66d2e35bfd3f42fb89f8587472d0092a1d3b16e3)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodePipelineProps(
            synth=synth,
            asset_publishing_code_build_defaults=asset_publishing_code_build_defaults,
            cli_version=cli_version,
            code_build_defaults=code_build_defaults,
            code_pipeline=code_pipeline,
            cross_account_keys=cross_account_keys,
            docker_credentials=docker_credentials,
            docker_enabled_for_self_mutation=docker_enabled_for_self_mutation,
            docker_enabled_for_synth=docker_enabled_for_synth,
            pipeline_name=pipeline_name,
            publish_assets_in_parallel=publish_assets_in_parallel,
            reuse_cross_region_support_stacks=reuse_cross_region_support_stacks,
            self_mutation=self_mutation,
            self_mutation_code_build_defaults=self_mutation_code_build_defaults,
            synth_code_build_defaults=synth_code_build_defaults,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="doBuildPipeline")
    def _do_build_pipeline(self) -> None:
        '''(experimental) Implemented by subclasses to do the actual pipeline construction.

        :stability: experimental
        '''
        return typing.cast(None, jsii.invoke(self, "doBuildPipeline", []))

    @builtins.property
    @jsii.member(jsii_name="pipeline")
    def pipeline(self) -> _Pipeline_7744fe74:
        '''(experimental) The CodePipeline pipeline that deploys the CDK app.

        Only available after the pipeline has been built.

        :stability: experimental
        '''
        return typing.cast(_Pipeline_7744fe74, jsii.get(self, "pipeline"))

    @builtins.property
    @jsii.member(jsii_name="synthProject")
    def synth_project(self) -> _IProject_6da8803e:
        '''(experimental) The CodeBuild project that performs the Synth.

        Only available after the pipeline has been built.

        :stability: experimental
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "synthProject"))


@jsii.implements(ICodePipelineActionFactory)
class CodePipelineSource(
    Step,
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="monocdk.pipelines.CodePipelineSource",
):
    '''(experimental) Factory for CodePipeline source steps.

    This class contains a number of factory methods for the different types
    of sources that CodePipeline supports.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Access the CommitId of a GitHub source in the synth
        source = pipelines.CodePipelineSource.git_hub("owner/repo", "main")
        
        pipeline = pipelines.CodePipeline(scope, "MyPipeline",
            synth=pipelines.ShellStep("Synth",
                input=source,
                commands=[],
                env={
                    "COMMIT_ID": source.source_attribute("CommitId")
                }
            )
        )
    '''

    def __init__(self, id: builtins.str) -> None:
        '''
        :param id: Identifier for this step.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__db56607b1d9203fc1146d005d14fa14fd5016be97decee6bfd1244ddedffa4de)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="codeCommit")
    @builtins.classmethod
    def code_commit(
        cls,
        repository: _IRepository_cdb2a3c0,
        branch: builtins.str,
        *,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        event_role: typing.Optional[_IRole_59af6f50] = None,
        trigger: typing.Optional[_CodeCommitTrigger_3c8c9539] = None,
    ) -> "CodePipelineSource":
        '''(experimental) Returns a CodeCommit source.

        If you need access to symlinks or the repository history, be sure to set
        ``codeBuildCloneOutput``.

        :param repository: The CodeCommit repository.
        :param branch: The branch to use.
        :param code_build_clone_output: (experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files). This provides access to repository history, and retains symlinks (symlinks would otherwise be removed by CodePipeline). **Note**: if this option is true, only CodeBuild jobs can use the output artifact. Default: false
        :param event_role: (experimental) Role to be used by on commit event rule. Used only when trigger value is CodeCommitTrigger.EVENTS. Default: a new role will be created.
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Default: CodeCommitTrigger.EVENTS

        :stability: experimental

        Example::

            # repository: codecommit.IRepository
            
            pipelines.CodePipelineSource.code_commit(repository, "main")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a89a99ee25ed767a94cf1be34a0ad78494cba669639858a340a2c3f16e320517)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        props = CodeCommitSourceOptions(
            code_build_clone_output=code_build_clone_output,
            event_role=event_role,
            trigger=trigger,
        )

        return typing.cast("CodePipelineSource", jsii.sinvoke(cls, "codeCommit", [repository, branch, props]))

    @jsii.member(jsii_name="connection")
    @builtins.classmethod
    def connection(
        cls,
        repo_string: builtins.str,
        branch: builtins.str,
        *,
        connection_arn: builtins.str,
        code_build_clone_output: typing.Optional[builtins.bool] = None,
        trigger_on_push: typing.Optional[builtins.bool] = None,
    ) -> "CodePipelineSource":
        '''(experimental) Returns a CodeStar connection source.

        A CodeStar connection allows AWS CodePipeline to
        access external resources, such as repositories in GitHub, GitHub Enterprise or
        BitBucket.

        To use this method, you first need to create a CodeStar connection
        using the AWS console. In the process, you may have to sign in to the external provider
        -- GitHub, for example -- to authorize AWS to read and modify your repository.
        Once you have done this, copy the connection ARN and use it to create the source.

        Example::

           pipelines.CodePipelineSource.connection("owner/repo", "main",
               connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
           )

        If you need access to symlinks or the repository history, be sure to set
        ``codeBuildCloneOutput``.

        :param repo_string: A string that encodes owner and repository separated by a slash (e.g. 'owner/repo').
        :param branch: The branch to use.
        :param connection_arn: (experimental) The ARN of the CodeStar Connection created in the AWS console that has permissions to access this GitHub or BitBucket repository.
        :param code_build_clone_output: (experimental) If this is set, the next CodeBuild job clones the repository (instead of CodePipeline downloading the files). This provides access to repository history, and retains symlinks (symlinks would otherwise be removed by CodePipeline). **Note**: if this option is true, only CodeBuild jobs can use the output artifact. Default: false
        :param trigger_on_push: (experimental) Controls automatically starting your pipeline when a new commit is made on the configured repository and branch. If unspecified, the default value is true, and the field does not display by default. Default: true

        :see: https://docs.aws.amazon.com/dtconsole/latest/userguide/welcome-connections.html
        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__14a4c9d712ca2f16098d4c50799265e2252314fb8d8d010195939831972ef707)
            check_type(argname="argument repo_string", value=repo_string, expected_type=type_hints["repo_string"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        props = ConnectionSourceOptions(
            connection_arn=connection_arn,
            code_build_clone_output=code_build_clone_output,
            trigger_on_push=trigger_on_push,
        )

        return typing.cast("CodePipelineSource", jsii.sinvoke(cls, "connection", [repo_string, branch, props]))

    @jsii.member(jsii_name="ecr")
    @builtins.classmethod
    def ecr(
        cls,
        repository: _IRepository_8b4d2894,
        *,
        action_name: typing.Optional[builtins.str] = None,
        image_tag: typing.Optional[builtins.str] = None,
    ) -> "CodePipelineSource":
        '''(experimental) Returns an ECR source.

        :param repository: The repository that will be watched for changes.
        :param action_name: (experimental) The action name used for this source in the CodePipeline. Default: - The repository name
        :param image_tag: (experimental) The image tag that will be checked for changes. Default: latest

        :stability: experimental

        Example::

            # repository: ecr.IRepository
            
            pipelines.CodePipelineSource.ecr(repository,
                image_tag="latest"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__70d08c563c0fc15976dd12862f257616bd66af8f7fad5dda0af3679257c21f53)
            check_type(argname="argument repository", value=repository, expected_type=type_hints["repository"])
        props = ECRSourceOptions(action_name=action_name, image_tag=image_tag)

        return typing.cast("CodePipelineSource", jsii.sinvoke(cls, "ecr", [repository, props]))

    @jsii.member(jsii_name="gitHub")
    @builtins.classmethod
    def git_hub(
        cls,
        repo_string: builtins.str,
        branch: builtins.str,
        *,
        authentication: typing.Optional[_SecretValue_c18506ef] = None,
        trigger: typing.Optional[_GitHubTrigger_0a61ded3] = None,
    ) -> "CodePipelineSource":
        '''(experimental) Returns a GitHub source, using OAuth tokens to authenticate with GitHub and a separate webhook to detect changes.

        This is no longer
        the recommended method. Please consider using ``connection()``
        instead.

        Pass in the owner and repository in a single string, like this::

           pipelines.CodePipelineSource.git_hub("owner/repo", "main")

        Authentication will be done by a secret called ``github-token`` in AWS
        Secrets Manager (unless specified otherwise).

        The token should have these permissions:

        - **repo** - to read the repository
        - **admin:repo_hook** - if you plan to use webhooks (true by default)

        If you need access to symlinks or the repository history, use a source of type
        ``connection`` instead.

        :param repo_string: -
        :param branch: -
        :param authentication: (experimental) A GitHub OAuth token to use for authentication. It is recommended to use a Secrets Manager ``Secret`` to obtain the token:: const oauth = cdk.SecretValue.secretsManager('my-github-token'); The GitHub Personal Access Token should have these scopes: - **repo** - to read the repository - **admin:repo_hook** - if you plan to use webhooks (true by default) Default: - SecretValue.secretsManager('github-token')
        :param trigger: (experimental) How AWS CodePipeline should be triggered. With the default value "WEBHOOK", a webhook is created in GitHub that triggers the action. With "POLL", CodePipeline periodically checks the source for changes. With "None", the action is not triggered through changes in the source. To use ``WEBHOOK``, your GitHub Personal Access Token should have **admin:repo_hook** scope (in addition to the regular **repo** scope). Default: GitHubTrigger.WEBHOOK

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef46e9e27c2ca91d4fd872dba3b56caf30e8f4c077f34a7c9b84e9f3b505f648)
            check_type(argname="argument repo_string", value=repo_string, expected_type=type_hints["repo_string"])
            check_type(argname="argument branch", value=branch, expected_type=type_hints["branch"])
        props = GitHubSourceOptions(authentication=authentication, trigger=trigger)

        return typing.cast("CodePipelineSource", jsii.sinvoke(cls, "gitHub", [repo_string, branch, props]))

    @jsii.member(jsii_name="s3")
    @builtins.classmethod
    def s3(
        cls,
        bucket: _IBucket_73486e29,
        object_key: builtins.str,
        *,
        action_name: typing.Optional[builtins.str] = None,
        trigger: typing.Optional[_S3Trigger_688e3a4a] = None,
    ) -> "CodePipelineSource":
        '''(experimental) Returns an S3 source.

        :param bucket: The bucket where the source code is located.
        :param object_key: -
        :param action_name: (experimental) The action name used for this source in the CodePipeline. Default: - The bucket name
        :param trigger: (experimental) How should CodePipeline detect source changes for this Action. Note that if this is S3Trigger.EVENTS, you need to make sure to include the source Bucket in a CloudTrail Trail, as otherwise the CloudWatch Events will not be emitted. Default: S3Trigger.POLL

        :stability: experimental

        Example::

            # bucket: s3.Bucket
            
            pipelines.CodePipelineSource.s3(bucket, "path/to/file.zip")
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df87e01880f520549a13e05a00a4f2b1d253868cf0a9d867a2350a29fcd1a192)
            check_type(argname="argument bucket", value=bucket, expected_type=type_hints["bucket"])
            check_type(argname="argument object_key", value=object_key, expected_type=type_hints["object_key"])
        props = S3SourceOptions(action_name=action_name, trigger=trigger)

        return typing.cast("CodePipelineSource", jsii.sinvoke(cls, "s3", [bucket, object_key, props]))

    @jsii.member(jsii_name="getAction")
    @abc.abstractmethod
    def _get_action(
        self,
        output: _Artifact_9905eec2,
        action_name: builtins.str,
        run_order: jsii.Number,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> _Action_22e6ab5f:
        '''
        :param output: -
        :param action_name: -
        :param run_order: -
        :param variables_namespace: -

        :stability: experimental
        '''
        ...

    @jsii.member(jsii_name="produceAction")
    def produce_action(
        self,
        stage: _IStage_5a7e7342,
        *,
        action_name: builtins.str,
        artifacts: ArtifactMap,
        pipeline: CodePipeline,
        run_order: jsii.Number,
        scope: _constructs_77d1e7e8.Construct,
        before_self_mutation: typing.Optional[builtins.bool] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> CodePipelineActionFactoryResult:
        '''(experimental) Create the desired Action and add it to the pipeline.

        :param stage: -
        :param action_name: (experimental) Name the action should get.
        :param artifacts: (experimental) Helper object to translate FileSets to CodePipeline Artifacts.
        :param pipeline: (experimental) The pipeline the action is being generated for.
        :param run_order: (experimental) RunOrder the action should get.
        :param scope: (experimental) Scope in which to create constructs.
        :param before_self_mutation: (experimental) Whether or not this action is inserted before self mutation. If it is, the action should take care to reflect some part of its own definition in the pipeline action definition, to trigger a restart after self-mutation (if necessary). Default: false
        :param code_build_defaults: (experimental) If this action factory creates a CodeBuild step, default options to inherit. Default: - No CodeBuild project defaults
        :param fallback_artifact: (experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use. CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If the Project doesn't actually care about its input (it can be anything), it can use the Artifact passed here. Default: - A fallback artifact does not exist
        :param variables_namespace: (experimental) If this step is producing outputs, the variables namespace assigned to it. Pass this on to the Action you are creating. Default: - Step doesn't produce any outputs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__651affe1806145cfe56c37f0b9a64b9eb3d011260c3cfc470408624e9e4ae9f5)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = ProduceActionOptions(
            action_name=action_name,
            artifacts=artifacts,
            pipeline=pipeline,
            run_order=run_order,
            scope=scope,
            before_self_mutation=before_self_mutation,
            code_build_defaults=code_build_defaults,
            fallback_artifact=fallback_artifact,
            variables_namespace=variables_namespace,
        )

        return typing.cast(CodePipelineActionFactoryResult, jsii.invoke(self, "produceAction", [stage, options]))

    @jsii.member(jsii_name="sourceAttribute")
    def source_attribute(self, name: builtins.str) -> builtins.str:
        '''(experimental) Return an attribute of the current source revision.

        These values can be passed into the environment variables of pipeline steps,
        so your steps can access information about the source revision.

        Pipeline synth step has some source attributes predefined in the environment.
        If these suffice, you don't need to use this method for the synth step.

        :param name: -

        :see: https://docs.aws.amazon.com/codepipeline/latest/userguide/reference-variables.html#reference-variables-list
        :stability: experimental

        Example::

            # Access the CommitId of a GitHub source in the synth
            source = pipelines.CodePipelineSource.git_hub("owner/repo", "main")
            
            pipeline = pipelines.CodePipeline(scope, "MyPipeline",
                synth=pipelines.ShellStep("Synth",
                    input=source,
                    commands=[],
                    env={
                        "COMMIT_ID": source.source_attribute("CommitId")
                    }
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__39faa66828209f8fccf949c101f0dc72be33edb6963b16e7cd551f1fe6f18ed5)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
        return typing.cast(builtins.str, jsii.invoke(self, "sourceAttribute", [name]))

    @builtins.property
    @jsii.member(jsii_name="isSource")
    def is_source(self) -> builtins.bool:
        '''(experimental) Whether or not this is a Source step.

        What it means to be a Source step depends on the engine.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isSource"))


class _CodePipelineSourceProxy(
    CodePipelineSource,
    jsii.proxy_for(Step), # type: ignore[misc]
):
    @jsii.member(jsii_name="getAction")
    def _get_action(
        self,
        output: _Artifact_9905eec2,
        action_name: builtins.str,
        run_order: jsii.Number,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> _Action_22e6ab5f:
        '''
        :param output: -
        :param action_name: -
        :param run_order: -
        :param variables_namespace: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f8b439002b6c7c05168263ed1e165629611868c388ac1315d69e0671e041301d)
            check_type(argname="argument output", value=output, expected_type=type_hints["output"])
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument run_order", value=run_order, expected_type=type_hints["run_order"])
            check_type(argname="argument variables_namespace", value=variables_namespace, expected_type=type_hints["variables_namespace"])
        return typing.cast(_Action_22e6ab5f, jsii.invoke(self, "getAction", [output, action_name, run_order, variables_namespace]))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, CodePipelineSource).__jsii_proxy_class__ = lambda : _CodePipelineSourceProxy


@jsii.implements(ICodePipelineActionFactory)
class ConfirmPermissionsBroadening(
    Step,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.ConfirmPermissionsBroadening",
):
    '''(experimental) Pause the pipeline if a deployment would add IAM permissions or Security Group rules.

    This step is only supported in CodePipeline pipelines.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # pipeline: pipelines.CodePipeline
        
        stage = MyApplicationStage(self, "MyApplication")
        pipeline.add_stage(stage,
            pre=[
                pipelines.ConfirmPermissionsBroadening("Check", stage=stage)
            ]
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        stage: _Stage_9729985a,
        notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    ) -> None:
        '''
        :param id: -
        :param stage: (experimental) The CDK Stage object to check the stacks of. This should be the same Stage object you are passing to ``addStage()``.
        :param notification_topic: (experimental) Topic to send notifications when a human needs to give manual confirmation. Default: - no notification

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c4faf61b3c00ca77f596f69c20ef198b6764c9bdc1f66d6390c2289d8e5829a1)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = PermissionsBroadeningCheckProps(
            stage=stage, notification_topic=notification_topic
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="produceAction")
    def produce_action(
        self,
        stage: _IStage_5a7e7342,
        *,
        action_name: builtins.str,
        artifacts: ArtifactMap,
        pipeline: CodePipeline,
        run_order: jsii.Number,
        scope: _constructs_77d1e7e8.Construct,
        before_self_mutation: typing.Optional[builtins.bool] = None,
        code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
        fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
        variables_namespace: typing.Optional[builtins.str] = None,
    ) -> CodePipelineActionFactoryResult:
        '''(experimental) Create the desired Action and add it to the pipeline.

        :param stage: -
        :param action_name: (experimental) Name the action should get.
        :param artifacts: (experimental) Helper object to translate FileSets to CodePipeline Artifacts.
        :param pipeline: (experimental) The pipeline the action is being generated for.
        :param run_order: (experimental) RunOrder the action should get.
        :param scope: (experimental) Scope in which to create constructs.
        :param before_self_mutation: (experimental) Whether or not this action is inserted before self mutation. If it is, the action should take care to reflect some part of its own definition in the pipeline action definition, to trigger a restart after self-mutation (if necessary). Default: false
        :param code_build_defaults: (experimental) If this action factory creates a CodeBuild step, default options to inherit. Default: - No CodeBuild project defaults
        :param fallback_artifact: (experimental) An input artifact that CodeBuild projects that don't actually need an input artifact can use. CodeBuild Projects MUST have an input artifact in order to be added to the Pipeline. If the Project doesn't actually care about its input (it can be anything), it can use the Artifact passed here. Default: - A fallback artifact does not exist
        :param variables_namespace: (experimental) If this step is producing outputs, the variables namespace assigned to it. Pass this on to the Action you are creating. Default: - Step doesn't produce any outputs

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1dd2d0e65a526f013f09e9d57ecc320078999c93e08adbf297c4a644b99eacd2)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = ProduceActionOptions(
            action_name=action_name,
            artifacts=artifacts,
            pipeline=pipeline,
            run_order=run_order,
            scope=scope,
            before_self_mutation=before_self_mutation,
            code_build_defaults=code_build_defaults,
            fallback_artifact=fallback_artifact,
            variables_namespace=variables_namespace,
        )

        return typing.cast(CodePipelineActionFactoryResult, jsii.invoke(self, "produceAction", [stage, options]))


@jsii.implements(IFileSetProducer)
class FileSet(metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.FileSet"):
    '''(experimental) A set of files traveling through the deployment pipeline.

    Individual steps in the pipeline produce or consume
    ``FileSet``s.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class MyJenkinsStep(pipelines.Steppipelines.ICodePipelineActionFactory):
            def __init__(self, provider, input):
                super().__init__("MyJenkinsStep")
        
                # This is necessary if your step accepts parametres, like environment variables,
                # that may contain outputs from other steps. It doesn't matter what the
                # structure is, as long as it contains the values that may contain outputs.
                self.discover_referenced_outputs({
                    "env": {}
                })
        
            def produce_action(self, stage, *, scope, actionName, runOrder, variablesNamespace=None, artifacts, fallbackArtifact=None, pipeline, codeBuildDefaults=None, beforeSelfMutation=None):
        
                # This is where you control what type of Action gets added to the
                # CodePipeline
                stage.add_action(cpactions.JenkinsAction(
                    # Copy 'actionName' and 'runOrder' from the options
                    action_name=action_name,
                    run_order=run_order,
        
                    # Jenkins-specific configuration
                    type=cpactions.JenkinsActionType.TEST,
                    jenkins_provider=self.provider,
                    project_name="MyJenkinsProject",
        
                    # Translate the FileSet into a codepipeline.Artifact
                    inputs=[artifacts.to_code_pipeline(self.input)]
                ))
        
                return cdk.pipelines.CodePipelineActionFactoryResult(run_orders_consumed=1)
    '''

    def __init__(
        self,
        id: builtins.str,
        producer: typing.Optional[Step] = None,
    ) -> None:
        '''
        :param id: Human-readable descriptor for this file set (does not need to be unique).
        :param producer: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9b50efdffc61a4f9cece5390be0e7e41023d4075f25439c34ffe3851976d15c5)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        jsii.create(self.__class__, self, [id, producer])

    @jsii.member(jsii_name="producedBy")
    def produced_by(self, producer: typing.Optional[Step] = None) -> None:
        '''(experimental) Mark the given Step as the producer for this FileSet.

        This method can only be called once.

        :param producer: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7356adad32add6e22c90cc2f4aa896446bd3616ba262edea0995e27bc807c717)
            check_type(argname="argument producer", value=producer, expected_type=type_hints["producer"])
        return typing.cast(None, jsii.invoke(self, "producedBy", [producer]))

    @jsii.member(jsii_name="toString")
    def to_string(self) -> builtins.str:
        '''(experimental) Return a string representation of this FileSet.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.invoke(self, "toString", []))

    @builtins.property
    @jsii.member(jsii_name="id")
    def id(self) -> builtins.str:
        '''(experimental) Human-readable descriptor for this file set (does not need to be unique).

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "id"))

    @builtins.property
    @jsii.member(jsii_name="producer")
    def producer(self) -> Step:
        '''(experimental) The Step that produces this FileSet.

        :stability: experimental
        '''
        return typing.cast(Step, jsii.get(self, "producer"))

    @builtins.property
    @jsii.member(jsii_name="primaryOutput")
    def primary_output(self) -> typing.Optional["FileSet"]:
        '''(experimental) The primary output of a file set producer.

        The primary output of a FileSet is itself.

        :stability: experimental
        '''
        return typing.cast(typing.Optional["FileSet"], jsii.get(self, "primaryOutput"))


class ManualApprovalStep(
    Step,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.ManualApprovalStep",
):
    '''(experimental) A manual approval step.

    If this step is added to a Pipeline, the Pipeline will
    be paused waiting for a human to resume it

    Only engines that support pausing the deployment will
    support this step type.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # pipeline: pipelines.CodePipeline
        
        preprod = MyApplicationStage(self, "PreProd")
        prod = MyApplicationStage(self, "Prod")
        
        pipeline.add_stage(preprod,
            post=[
                pipelines.ShellStep("Validate Endpoint",
                    commands=["curl -Ssf https://my.webservice.com/"]
                )
            ]
        )
        pipeline.add_stage(prod,
            pre=[
                pipelines.ManualApprovalStep("PromoteToProd")
            ]
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        comment: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param comment: (experimental) The comment to display with this manual approval. Default: - No comment

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b369e1d78a8136d31211bc358d3c5cacdbcc8518faf31deac05239ca29270f81)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ManualApprovalStepProps(comment=comment)

        jsii.create(self.__class__, self, [id, props])

    @builtins.property
    @jsii.member(jsii_name="comment")
    def comment(self) -> typing.Optional[builtins.str]:
        '''(experimental) The comment associated with this manual approval.

        :default: - No comment

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "comment"))


class ShellStep(Step, metaclass=jsii.JSIIMeta, jsii_type="monocdk.pipelines.ShellStep"):
    '''(experimental) Run shell script commands in the pipeline.

    This is a generic step designed
    to be deployment engine agnostic.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # Modern API
        modern_pipeline = pipelines.CodePipeline(self, "Pipeline",
            self_mutation=False,
            synth=pipelines.ShellStep("Synth",
                input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["npm ci", "npm run build", "npx cdk synth"
                ]
            )
        )
        
        # Original API
        cloud_assembly_artifact = codepipeline.Artifact()
        original_pipeline = pipelines.CdkPipeline(self, "Pipeline",
            self_mutating=False,
            cloud_assembly_artifact=cloud_assembly_artifact
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        commands: typing.Sequence[builtins.str],
        additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
        input: typing.Optional[IFileSetProducer] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_output_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param commands: (experimental) Commands to run.
        :param additional_inputs: (experimental) Additional FileSets to put in other directories. Specifies a mapping from directory name to FileSets. During the script execution, the FileSets will be available in the directories indicated. The directory names may be relative. For example, you can put the main input and an additional input side-by-side with the following configuration:: const script = new pipelines.ShellStep('MainScript', { commands: ['npm ci','npm run build','npx cdk synth'], input: pipelines.CodePipelineSource.gitHub('org/source1', 'main'), additionalInputs: { '../siblingdir': pipelines.CodePipelineSource.gitHub('org/source2', 'main'), } }); Default: - No additional inputs
        :param env: (experimental) Environment variables to set. Default: - No environment variables
        :param env_from_cfn_outputs: (experimental) Set environment variables based on Stack Outputs. ``ShellStep``s following stack or stage deployments may access the ``CfnOutput``s of those stacks to get access to --for example--automatically generated resource names or endpoint URLs. Default: - No environment variables created from stack outputs
        :param input: (experimental) FileSet to run these scripts on. The files in the FileSet will be placed in the working directory when the script is executed. Use ``additionalInputs`` to download file sets to other directories as well. Default: - No input specified
        :param install_commands: (experimental) Installation commands to run before the regular commands. For deployment engines that support it, install commands will be classified differently in the job history from the regular ``commands``. Default: - No installation commands
        :param primary_output_directory: (experimental) The directory that will contain the primary output fileset. After running the script, the contents of the given directory will be treated as the primary output of this Step. Default: - No primary output

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d3ad11656e74961349db39d7e4f6031f5000393e2aa101114d3400f7ee5feba0)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = ShellStepProps(
            commands=commands,
            additional_inputs=additional_inputs,
            env=env,
            env_from_cfn_outputs=env_from_cfn_outputs,
            input=input,
            install_commands=install_commands,
            primary_output_directory=primary_output_directory,
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="addOutputDirectory")
    def add_output_directory(self, directory: builtins.str) -> FileSet:
        '''(experimental) Add an additional output FileSet based on a directory.

        After running the script, the contents of the given directory
        will be exported as a ``FileSet``. Use the ``FileSet`` as the
        input to another step.

        Multiple calls with the exact same directory name string (not normalized)
        will return the same FileSet.

        :param directory: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ef1d9cf7e496ac4f1abb47e79cbaaad11b487568f4669d49f4b6c6c868352dbd)
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
        return typing.cast(FileSet, jsii.invoke(self, "addOutputDirectory", [directory]))

    @jsii.member(jsii_name="primaryOutputDirectory")
    def primary_output_directory(self, directory: builtins.str) -> FileSet:
        '''(experimental) Configure the given output directory as primary output.

        If no primary output has been configured yet, this directory
        will become the primary output of this ShellStep, otherwise this
        method will throw if the given directory is different than the
        currently configured primary output directory.

        :param directory: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16418d7295b78b107b8b9cf7e28adc671ec842a35352a39912ca835cd9853fc4)
            check_type(argname="argument directory", value=directory, expected_type=type_hints["directory"])
        return typing.cast(FileSet, jsii.invoke(self, "primaryOutputDirectory", [directory]))

    @builtins.property
    @jsii.member(jsii_name="commands")
    def commands(self) -> typing.List[builtins.str]:
        '''(experimental) Commands to run.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "commands"))

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''(experimental) Environment variables to set.

        :default: - No environment variables

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="envFromCfnOutputs")
    def env_from_cfn_outputs(
        self,
    ) -> typing.Mapping[builtins.str, StackOutputReference]:
        '''(experimental) Set environment variables based on Stack Outputs.

        :default: - No environment variables created from stack outputs

        :stability: experimental
        '''
        return typing.cast(typing.Mapping[builtins.str, StackOutputReference], jsii.get(self, "envFromCfnOutputs"))

    @builtins.property
    @jsii.member(jsii_name="inputs")
    def inputs(self) -> typing.List[FileSetLocation]:
        '''(experimental) Input FileSets.

        A list of ``(FileSet, directory)`` pairs, which are a copy of the
        input properties. This list should not be modified directly.

        :stability: experimental
        '''
        return typing.cast(typing.List[FileSetLocation], jsii.get(self, "inputs"))

    @builtins.property
    @jsii.member(jsii_name="installCommands")
    def install_commands(self) -> typing.List[builtins.str]:
        '''(experimental) Installation commands to run before the regular commands.

        For deployment engines that support it, install commands will be classified
        differently in the job history from the regular ``commands``.

        :default: - No installation commands

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "installCommands"))

    @builtins.property
    @jsii.member(jsii_name="outputs")
    def outputs(self) -> typing.List[FileSetLocation]:
        '''(experimental) Output FileSets.

        A list of ``(FileSet, directory)`` pairs, which are a copy of the
        input properties. This list should not be modified directly.

        :stability: experimental
        '''
        return typing.cast(typing.List[FileSetLocation], jsii.get(self, "outputs"))


@jsii.data_type(
    jsii_type="monocdk.pipelines.SimpleSynthActionProps",
    jsii_struct_bases=[SimpleSynthOptions],
    name_mapping={
        "cloud_assembly_artifact": "cloudAssemblyArtifact",
        "source_artifact": "sourceArtifact",
        "action_name": "actionName",
        "additional_artifacts": "additionalArtifacts",
        "build_spec": "buildSpec",
        "copy_environment_variables": "copyEnvironmentVariables",
        "environment": "environment",
        "environment_variables": "environmentVariables",
        "project_name": "projectName",
        "role_policy_statements": "rolePolicyStatements",
        "subdirectory": "subdirectory",
        "subnet_selection": "subnetSelection",
        "vpc": "vpc",
        "synth_command": "synthCommand",
        "build_command": "buildCommand",
        "build_commands": "buildCommands",
        "install_command": "installCommand",
        "install_commands": "installCommands",
        "test_commands": "testCommands",
    },
)
class SimpleSynthActionProps(SimpleSynthOptions):
    def __init__(
        self,
        *,
        cloud_assembly_artifact: _Artifact_9905eec2,
        source_artifact: _Artifact_9905eec2,
        action_name: typing.Optional[builtins.str] = None,
        additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
        build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
        environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
        project_name: typing.Optional[builtins.str] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        subdirectory: typing.Optional[builtins.str] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        synth_command: builtins.str,
        build_command: typing.Optional[builtins.str] = None,
        build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        install_command: typing.Optional[builtins.str] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''(deprecated) Construction props for SimpleSynthAction.

        :param cloud_assembly_artifact: (deprecated) The artifact where the CloudAssembly should be emitted.
        :param source_artifact: (deprecated) The source artifact of the CodePipeline.
        :param action_name: (deprecated) Name of the build action. Default: 'Synth'
        :param additional_artifacts: (deprecated) Produce additional output artifacts after the build based on the given directories. Can be used to produce additional artifacts during the build step, separate from the cloud assembly, which can be used further on in the pipeline. Directories are evaluated with respect to ``subdirectory``. Default: - No additional artifacts generated
        :param build_spec: (deprecated) custom BuildSpec that is merged with the generated one. Default: - none
        :param copy_environment_variables: (deprecated) Environment variables to copy over from parent env. These are environment variables that are being used by the build. Default: - No environment variables copied
        :param environment: (deprecated) Build environment to use for CodeBuild job. Default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0
        :param environment_variables: (deprecated) Environment variables to send into build. NOTE: You may run into the 1000-character limit for the Action configuration if you have a large number of variables or if their names or values are very long. If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead. However, you will not be able to use CodePipeline Variables in this case. Default: - No additional environment variables
        :param project_name: (deprecated) Name of the CodeBuild project. Default: - Automatically generated
        :param role_policy_statements: (deprecated) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param subdirectory: (deprecated) Directory inside the source where package.json and cdk.json are located. Default: - Repository root
        :param subnet_selection: (deprecated) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param vpc: (deprecated) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param synth_command: (deprecated) The synth command.
        :param build_command: (deprecated) The build command. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param build_commands: (deprecated) The build commands. If your programming language requires a compilation step, put the compilation command here. Default: - No build required
        :param install_command: (deprecated) The install command. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param install_commands: (deprecated) Install commands. If not provided by the build image or another dependency management tool, at least install the CDK CLI here using ``npm install -g aws-cdk``. Default: - No install required
        :param test_commands: (deprecated) Test commands. These commands are run after the build commands but before the synth command. Default: - No test commands

        :deprecated: This class is part of the old API. Use the API based on the ``CodePipeline`` class instead

        :stability: deprecated
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_codebuild as codebuild
            from monocdk import aws_codepipeline as codepipeline
            from monocdk import aws_ec2 as ec2
            from monocdk import aws_iam as iam
            from monocdk import aws_s3 as s3
            from monocdk import pipelines
            
            # artifact: codepipeline.Artifact
            # bucket: s3.Bucket
            # build_image: codebuild.IBuildImage
            # build_spec: codebuild.BuildSpec
            # policy_statement: iam.PolicyStatement
            # subnet: ec2.Subnet
            # subnet_filter: ec2.SubnetFilter
            # value: Any
            # vpc: ec2.Vpc
            
            simple_synth_action_props = pipelines.SimpleSynthActionProps(
                cloud_assembly_artifact=artifact,
                source_artifact=artifact,
                synth_command="synthCommand",
            
                # the properties below are optional
                action_name="actionName",
                additional_artifacts=[pipelines.AdditionalArtifact(
                    artifact=artifact,
                    directory="directory"
                )],
                build_command="buildCommand",
                build_commands=["buildCommands"],
                build_spec=build_spec,
                copy_environment_variables=["copyEnvironmentVariables"],
                environment=codebuild.BuildEnvironment(
                    build_image=build_image,
                    certificate=codebuild.BuildEnvironmentCertificate(
                        bucket=bucket,
                        object_key="objectKey"
                    ),
                    compute_type=codebuild.ComputeType.SMALL,
                    environment_variables={
                        "environment_variables_key": codebuild.BuildEnvironmentVariable(
                            value=value,
            
                            # the properties below are optional
                            type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                        )
                    },
                    privileged=False
                ),
                environment_variables={
                    "environment_variables_key": codebuild.BuildEnvironmentVariable(
                        value=value,
            
                        # the properties below are optional
                        type=codebuild.BuildEnvironmentVariableType.PLAINTEXT
                    )
                },
                install_command="installCommand",
                install_commands=["installCommands"],
                project_name="projectName",
                role_policy_statements=[policy_statement],
                subdirectory="subdirectory",
                subnet_selection=ec2.SubnetSelection(
                    availability_zones=["availabilityZones"],
                    one_per_az=False,
                    subnet_filters=[subnet_filter],
                    subnet_group_name="subnetGroupName",
                    subnet_name="subnetName",
                    subnets=[subnet],
                    subnet_type=ec2.SubnetType.ISOLATED
                ),
                test_commands=["testCommands"],
                vpc=vpc
            )
        '''
        if isinstance(environment, dict):
            environment = _BuildEnvironment_77bc5f50(**environment)
        if isinstance(subnet_selection, dict):
            subnet_selection = _SubnetSelection_1284e62c(**subnet_selection)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__df96ff352741339be53857b1c07478b90eb0dd2dc13338c066d6252436366af9)
            check_type(argname="argument cloud_assembly_artifact", value=cloud_assembly_artifact, expected_type=type_hints["cloud_assembly_artifact"])
            check_type(argname="argument source_artifact", value=source_artifact, expected_type=type_hints["source_artifact"])
            check_type(argname="argument action_name", value=action_name, expected_type=type_hints["action_name"])
            check_type(argname="argument additional_artifacts", value=additional_artifacts, expected_type=type_hints["additional_artifacts"])
            check_type(argname="argument build_spec", value=build_spec, expected_type=type_hints["build_spec"])
            check_type(argname="argument copy_environment_variables", value=copy_environment_variables, expected_type=type_hints["copy_environment_variables"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument environment_variables", value=environment_variables, expected_type=type_hints["environment_variables"])
            check_type(argname="argument project_name", value=project_name, expected_type=type_hints["project_name"])
            check_type(argname="argument role_policy_statements", value=role_policy_statements, expected_type=type_hints["role_policy_statements"])
            check_type(argname="argument subdirectory", value=subdirectory, expected_type=type_hints["subdirectory"])
            check_type(argname="argument subnet_selection", value=subnet_selection, expected_type=type_hints["subnet_selection"])
            check_type(argname="argument vpc", value=vpc, expected_type=type_hints["vpc"])
            check_type(argname="argument synth_command", value=synth_command, expected_type=type_hints["synth_command"])
            check_type(argname="argument build_command", value=build_command, expected_type=type_hints["build_command"])
            check_type(argname="argument build_commands", value=build_commands, expected_type=type_hints["build_commands"])
            check_type(argname="argument install_command", value=install_command, expected_type=type_hints["install_command"])
            check_type(argname="argument install_commands", value=install_commands, expected_type=type_hints["install_commands"])
            check_type(argname="argument test_commands", value=test_commands, expected_type=type_hints["test_commands"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "cloud_assembly_artifact": cloud_assembly_artifact,
            "source_artifact": source_artifact,
            "synth_command": synth_command,
        }
        if action_name is not None:
            self._values["action_name"] = action_name
        if additional_artifacts is not None:
            self._values["additional_artifacts"] = additional_artifacts
        if build_spec is not None:
            self._values["build_spec"] = build_spec
        if copy_environment_variables is not None:
            self._values["copy_environment_variables"] = copy_environment_variables
        if environment is not None:
            self._values["environment"] = environment
        if environment_variables is not None:
            self._values["environment_variables"] = environment_variables
        if project_name is not None:
            self._values["project_name"] = project_name
        if role_policy_statements is not None:
            self._values["role_policy_statements"] = role_policy_statements
        if subdirectory is not None:
            self._values["subdirectory"] = subdirectory
        if subnet_selection is not None:
            self._values["subnet_selection"] = subnet_selection
        if vpc is not None:
            self._values["vpc"] = vpc
        if build_command is not None:
            self._values["build_command"] = build_command
        if build_commands is not None:
            self._values["build_commands"] = build_commands
        if install_command is not None:
            self._values["install_command"] = install_command
        if install_commands is not None:
            self._values["install_commands"] = install_commands
        if test_commands is not None:
            self._values["test_commands"] = test_commands

    @builtins.property
    def cloud_assembly_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The artifact where the CloudAssembly should be emitted.

        :stability: deprecated
        '''
        result = self._values.get("cloud_assembly_artifact")
        assert result is not None, "Required property 'cloud_assembly_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def source_artifact(self) -> _Artifact_9905eec2:
        '''(deprecated) The source artifact of the CodePipeline.

        :stability: deprecated
        '''
        result = self._values.get("source_artifact")
        assert result is not None, "Required property 'source_artifact' is missing"
        return typing.cast(_Artifact_9905eec2, result)

    @builtins.property
    def action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the build action.

        :default: 'Synth'

        :stability: deprecated
        '''
        result = self._values.get("action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def additional_artifacts(self) -> typing.Optional[typing.List[AdditionalArtifact]]:
        '''(deprecated) Produce additional output artifacts after the build based on the given directories.

        Can be used to produce additional artifacts during the build step,
        separate from the cloud assembly, which can be used further on in the
        pipeline.

        Directories are evaluated with respect to ``subdirectory``.

        :default: - No additional artifacts generated

        :stability: deprecated
        '''
        result = self._values.get("additional_artifacts")
        return typing.cast(typing.Optional[typing.List[AdditionalArtifact]], result)

    @builtins.property
    def build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(deprecated) custom BuildSpec that is merged with the generated one.

        :default: - none

        :stability: deprecated
        '''
        result = self._values.get("build_spec")
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], result)

    @builtins.property
    def copy_environment_variables(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Environment variables to copy over from parent env.

        These are environment variables that are being used by the build.

        :default: - No environment variables copied

        :stability: deprecated
        '''
        result = self._values.get("copy_environment_variables")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(deprecated) Build environment to use for CodeBuild job.

        :default: BuildEnvironment.LinuxBuildImage.STANDARD_5_0

        :stability: deprecated
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], result)

    @builtins.property
    def environment_variables(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]]:
        '''(deprecated) Environment variables to send into build.

        NOTE: You may run into the 1000-character limit for the Action configuration if you have a large
        number of variables or if their names or values are very long.
        If you do, pass them to the underlying CodeBuild project directly in ``environment`` instead.
        However, you will not be able to use CodePipeline Variables in this case.

        :default: - No additional environment variables

        :stability: deprecated
        '''
        result = self._values.get("environment_variables")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, _BuildEnvironmentVariable_00095c97]], result)

    @builtins.property
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Name of the CodeBuild project.

        :default: - Automatically generated

        :stability: deprecated
        '''
        result = self._values.get("project_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(deprecated) Policy statements to add to role used during the synth.

        Can be used to add acces to a CodeArtifact repository etc.

        :default: - No policy statements added to CodeBuild Project Role

        :stability: deprecated
        '''
        result = self._values.get("role_policy_statements")
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], result)

    @builtins.property
    def subdirectory(self) -> typing.Optional[builtins.str]:
        '''(deprecated) Directory inside the source where package.json and cdk.json are located.

        :default: - Repository root

        :stability: deprecated
        '''
        result = self._values.get("subdirectory")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(deprecated) Which subnets to use.

        Only used if 'vpc' is supplied.

        :default: - All private subnets.

        :stability: deprecated
        '''
        result = self._values.get("subnet_selection")
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], result)

    @builtins.property
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(deprecated) The VPC where to execute the SimpleSynth.

        :default: - No VPC

        :stability: deprecated
        '''
        result = self._values.get("vpc")
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], result)

    @builtins.property
    def synth_command(self) -> builtins.str:
        '''(deprecated) The synth command.

        :stability: deprecated
        '''
        result = self._values.get("synth_command")
        assert result is not None, "Required property 'synth_command' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def build_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The build command.

        If your programming language requires a compilation step, put the
        compilation command here.

        :default: - No build required

        :deprecated: Use ``buildCommands`` instead

        :stability: deprecated
        '''
        result = self._values.get("build_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def build_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) The build commands.

        If your programming language requires a compilation step, put the
        compilation command here.

        :default: - No build required

        :stability: deprecated
        '''
        result = self._values.get("build_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def install_command(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The install command.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        :default: - No install required

        :deprecated: Use ``installCommands`` instead

        :stability: deprecated
        '''
        result = self._values.get("install_command")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def install_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Install commands.

        If not provided by the build image or another dependency
        management tool, at least install the CDK CLI here using
        ``npm install -g aws-cdk``.

        :default: - No install required

        :stability: deprecated
        '''
        result = self._values.get("install_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def test_commands(self) -> typing.Optional[typing.List[builtins.str]]:
        '''(deprecated) Test commands.

        These commands are run after the build commands but before the
        synth command.

        :default: - No test commands

        :stability: deprecated
        '''
        result = self._values.get("test_commands")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SimpleSynthActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class CodeBuildStep(
    ShellStep,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CodeBuildStep",
):
    '''(experimental) Run a script as a CodeBuild Project.

    The BuildSpec must be available inline--it cannot reference a file
    on disk. If your current build instructions are in a file like
    ``buildspec.yml`` in your repository, extract them to a script
    (say, ``build.sh``) and invoke that script as part of the build::

       pipelines.CodeBuildStep("Synth",
           commands=["./build.sh"]
       )

    :stability: experimental
    :exampleMetadata: infused

    Example::

        pipelines.CodePipeline(self, "Pipeline",
            synth=pipelines.CodeBuildStep("Synth",
                input=pipelines.CodePipelineSource.connection("my-org/my-app", "main",
                    connection_arn="arn:aws:codestar-connections:us-east-1:222222222222:connection/7d2469ff-514a-4e4f-9003-5ca4a43cdc41"
                ),
                commands=["...", "npm ci", "npm run build", "npx cdk synth", "..."
                ],
                role_policy_statements=[
                    iam.PolicyStatement(
                        actions=["sts:AssumeRole"],
                        resources=["*"],
                        conditions={
                            "StringEquals": {
                                "iam:ResourceTag/aws-cdk:bootstrap-role": "lookup"
                            }
                        }
                    )
                ]
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        *,
        action_role: typing.Optional[_IRole_59af6f50] = None,
        build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
        partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
        project_name: typing.Optional[builtins.str] = None,
        role: typing.Optional[_IRole_59af6f50] = None,
        role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
        security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
        subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
        timeout: typing.Optional[_Duration_070aa057] = None,
        vpc: typing.Optional[_IVpc_6d1f76c4] = None,
        commands: typing.Sequence[builtins.str],
        additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
        input: typing.Optional[IFileSetProducer] = None,
        install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
        primary_output_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param id: -
        :param action_role: (experimental) Custom execution role to be used for the Code Build Action. Default: - A role is automatically created
        :param build_environment: (experimental) Changes to environment. This environment will be combined with the pipeline's default environment. Default: - Use the pipeline's default build environment
        :param partial_build_spec: (experimental) Additional configuration that can only be configured via BuildSpec. You should not use this to specify output artifacts; those should be supplied via the other properties of this class, otherwise CDK Pipelines won't be able to inspect the artifacts. Set the ``commands`` to an empty array if you want to fully specify the BuildSpec using this field. The BuildSpec must be available inline--it cannot reference a file on disk. Default: - BuildSpec completely derived from other properties
        :param project_name: (experimental) Name for the generated CodeBuild project. Default: - Automatically generated
        :param role: (experimental) Custom execution role to be used for the CodeBuild project. Default: - A role is automatically created
        :param role_policy_statements: (experimental) Policy statements to add to role used during the synth. Can be used to add acces to a CodeArtifact repository etc. Default: - No policy statements added to CodeBuild Project Role
        :param security_groups: (experimental) Which security group to associate with the script's project network interfaces. If no security group is identified, one will be created automatically. Only used if 'vpc' is supplied. Default: - Security group will be automatically created.
        :param subnet_selection: (experimental) Which subnets to use. Only used if 'vpc' is supplied. Default: - All private subnets.
        :param timeout: (experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete. For valid values, see the timeoutInMinutes field in the AWS CodeBuild User Guide. Default: Duration.hours(1)
        :param vpc: (experimental) The VPC where to execute the SimpleSynth. Default: - No VPC
        :param commands: (experimental) Commands to run.
        :param additional_inputs: (experimental) Additional FileSets to put in other directories. Specifies a mapping from directory name to FileSets. During the script execution, the FileSets will be available in the directories indicated. The directory names may be relative. For example, you can put the main input and an additional input side-by-side with the following configuration:: const script = new pipelines.ShellStep('MainScript', { commands: ['npm ci','npm run build','npx cdk synth'], input: pipelines.CodePipelineSource.gitHub('org/source1', 'main'), additionalInputs: { '../siblingdir': pipelines.CodePipelineSource.gitHub('org/source2', 'main'), } }); Default: - No additional inputs
        :param env: (experimental) Environment variables to set. Default: - No environment variables
        :param env_from_cfn_outputs: (experimental) Set environment variables based on Stack Outputs. ``ShellStep``s following stack or stage deployments may access the ``CfnOutput``s of those stacks to get access to --for example--automatically generated resource names or endpoint URLs. Default: - No environment variables created from stack outputs
        :param input: (experimental) FileSet to run these scripts on. The files in the FileSet will be placed in the working directory when the script is executed. Use ``additionalInputs`` to download file sets to other directories as well. Default: - No input specified
        :param install_commands: (experimental) Installation commands to run before the regular commands. For deployment engines that support it, install commands will be classified differently in the job history from the regular ``commands``. Default: - No installation commands
        :param primary_output_directory: (experimental) The directory that will contain the primary output fileset. After running the script, the contents of the given directory will be treated as the primary output of this Step. Default: - No primary output

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d26449ed6ece76731213baa7e3228da7b38ab538a9d821ccd180b7ec79add123)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CodeBuildStepProps(
            action_role=action_role,
            build_environment=build_environment,
            partial_build_spec=partial_build_spec,
            project_name=project_name,
            role=role,
            role_policy_statements=role_policy_statements,
            security_groups=security_groups,
            subnet_selection=subnet_selection,
            timeout=timeout,
            vpc=vpc,
            commands=commands,
            additional_inputs=additional_inputs,
            env=env,
            env_from_cfn_outputs=env_from_cfn_outputs,
            input=input,
            install_commands=install_commands,
            primary_output_directory=primary_output_directory,
        )

        jsii.create(self.__class__, self, [id, props])

    @jsii.member(jsii_name="exportedVariable")
    def exported_variable(self, variable_name: builtins.str) -> builtins.str:
        '''(experimental) Reference a CodePipeline variable defined by the CodeBuildStep.

        The variable must be set in the shell of the CodeBuild step when
        it finishes its ``post_build`` phase.

        :param variable_name: the name of the variable for reference.

        :stability: experimental

        Example::

            # Access the output of one CodeBuildStep in another CodeBuildStep
            # pipeline: pipelines.CodePipeline
            
            
            step1 = pipelines.CodeBuildStep("Step1",
                commands=["export MY_VAR=hello"]
            )
            
            step2 = pipelines.CodeBuildStep("Step2",
                env={
                    "IMPORTED_VAR": step1.exported_variable("MY_VAR")
                },
                commands=["echo $IMPORTED_VAR"]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__841756ad0c29682b3a9b312ca1c310b0b27f7aeca08a53fd3aa399399aa29024)
            check_type(argname="argument variable_name", value=variable_name, expected_type=type_hints["variable_name"])
        return typing.cast(builtins.str, jsii.invoke(self, "exportedVariable", [variable_name]))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The CodeBuild Project's principal.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="project")
    def project(self) -> _IProject_6da8803e:
        '''(experimental) CodeBuild Project generated for the pipeline.

        Will only be available after the pipeline has been built.

        :stability: experimental
        '''
        return typing.cast(_IProject_6da8803e, jsii.get(self, "project"))

    @builtins.property
    @jsii.member(jsii_name="actionRole")
    def action_role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Custom execution role to be used for the Code Build Action.

        :default: - A role is automatically created

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "actionRole"))

    @builtins.property
    @jsii.member(jsii_name="buildEnvironment")
    def build_environment(self) -> typing.Optional[_BuildEnvironment_77bc5f50]:
        '''(experimental) Build environment.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_BuildEnvironment_77bc5f50], jsii.get(self, "buildEnvironment"))

    @builtins.property
    @jsii.member(jsii_name="partialBuildSpec")
    def partial_build_spec(self) -> typing.Optional[_BuildSpec_1d70c5a1]:
        '''(experimental) Additional configuration that can only be configured via BuildSpec.

        Contains exported variables

        :default: - Contains the exported variables

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_BuildSpec_1d70c5a1], jsii.get(self, "partialBuildSpec"))

    @builtins.property
    @jsii.member(jsii_name="projectName")
    def project_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Name for the generated CodeBuild project.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "projectName"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) Custom execution role to be used for the CodeBuild project.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))

    @builtins.property
    @jsii.member(jsii_name="rolePolicyStatements")
    def role_policy_statements(
        self,
    ) -> typing.Optional[typing.List[_PolicyStatement_296fe8a3]]:
        '''(experimental) Policy statements to add to role used during the synth.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_PolicyStatement_296fe8a3]], jsii.get(self, "rolePolicyStatements"))

    @builtins.property
    @jsii.member(jsii_name="securityGroups")
    def security_groups(self) -> typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]]:
        '''(experimental) Which security group to associate with the script's project network interfaces.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[typing.List[_ISecurityGroup_cdbba9d3]], jsii.get(self, "securityGroups"))

    @builtins.property
    @jsii.member(jsii_name="subnetSelection")
    def subnet_selection(self) -> typing.Optional[_SubnetSelection_1284e62c]:
        '''(experimental) Which subnets to use.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_SubnetSelection_1284e62c], jsii.get(self, "subnetSelection"))

    @builtins.property
    @jsii.member(jsii_name="timeout")
    def timeout(self) -> typing.Optional[_Duration_070aa057]:
        '''(experimental) The number of minutes after which AWS CodeBuild stops the build if it's not complete.

        For valid values, see the timeoutInMinutes field in the AWS
        CodeBuild User Guide.

        :default: Duration.hours(1)

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_Duration_070aa057], jsii.get(self, "timeout"))

    @builtins.property
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> typing.Optional[_IVpc_6d1f76c4]:
        '''(experimental) The VPC where to execute the SimpleSynth.

        :default: - No value specified at construction time, use defaults

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IVpc_6d1f76c4], jsii.get(self, "vpc"))


class CodePipelineFileSet(
    FileSet,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.pipelines.CodePipelineFileSet",
):
    '''(experimental) A FileSet created from a CodePipeline artifact.

    You only need to use this if you want to add CDK Pipeline stages
    add the end of an existing CodePipeline, which should be very rare.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_codepipeline as codepipeline
        from monocdk import pipelines
        
        # artifact: codepipeline.Artifact
        
        code_pipeline_file_set = pipelines.CodePipelineFileSet.from_artifact(artifact)
    '''

    @jsii.member(jsii_name="fromArtifact")
    @builtins.classmethod
    def from_artifact(cls, artifact: _Artifact_9905eec2) -> "CodePipelineFileSet":
        '''(experimental) Turn a CodePipeline Artifact into a FileSet.

        :param artifact: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__05e74cfd4b72679ac7d410b48e116f9ca181b4eb2329a7f7684fb4b555b1cca0)
            check_type(argname="argument artifact", value=artifact, expected_type=type_hints["artifact"])
        return typing.cast("CodePipelineFileSet", jsii.sinvoke(cls, "fromArtifact", [artifact]))


__all__ = [
    "AddManualApprovalOptions",
    "AddStackOptions",
    "AddStageOptions",
    "AddStageOpts",
    "AdditionalArtifact",
    "ArtifactMap",
    "AssetPublishingCommand",
    "AssetType",
    "BaseStageOptions",
    "CdkPipeline",
    "CdkPipelineProps",
    "CdkStackActionFromArtifactOptions",
    "CdkStage",
    "CdkStageProps",
    "CodeBuildOptions",
    "CodeBuildStep",
    "CodeBuildStepProps",
    "CodeCommitSourceOptions",
    "CodePipeline",
    "CodePipelineActionFactoryResult",
    "CodePipelineFileSet",
    "CodePipelineProps",
    "CodePipelineSource",
    "ConfirmPermissionsBroadening",
    "ConnectionSourceOptions",
    "DeployCdkStackAction",
    "DeployCdkStackActionOptions",
    "DeployCdkStackActionProps",
    "DockerCredential",
    "DockerCredentialUsage",
    "ECRSourceOptions",
    "EcrDockerCredentialOptions",
    "ExternalDockerCredentialOptions",
    "FileSet",
    "FileSetLocation",
    "FromStackArtifactOptions",
    "GitHubSourceOptions",
    "ICodePipelineActionFactory",
    "IFileSetProducer",
    "IStageHost",
    "ManualApprovalStep",
    "ManualApprovalStepProps",
    "PermissionsBroadeningCheckProps",
    "PipelineBase",
    "PipelineBaseProps",
    "ProduceActionOptions",
    "PublishAssetsAction",
    "PublishAssetsActionProps",
    "S3SourceOptions",
    "ShellScriptAction",
    "ShellScriptActionProps",
    "ShellStep",
    "ShellStepProps",
    "SimpleSynthAction",
    "SimpleSynthActionProps",
    "SimpleSynthOptions",
    "StackAsset",
    "StackDeployment",
    "StackDeploymentProps",
    "StackOutput",
    "StackOutputReference",
    "StackSteps",
    "StageDeployment",
    "StageDeploymentProps",
    "StandardNpmSynthOptions",
    "StandardYarnSynthOptions",
    "Step",
    "UpdatePipelineAction",
    "UpdatePipelineActionProps",
    "Wave",
    "WaveOptions",
    "WaveProps",
]

publication.publish()

def _typecheckingstub__e53258e8e55f1f48f8e89ec099df484ebf0e21b0f5287fa8c58754651696e903(
    *,
    action_name: typing.Optional[builtins.str] = None,
    run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c6b0ec1eac8734e21ef987fc6ad8cd13dc3b2ea57aa69cc15b2d89b66087add0(
    *,
    execute_run_order: typing.Optional[jsii.Number] = None,
    run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cbdd7c9c07f484b32b780bd09df59fb5411ba050e54c7a4a85fa9a4c706823a(
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01648844dea0ebea986c7ef74a4e0d14916f34667388b56d215d458193819851(
    *,
    artifact: _Artifact_9905eec2,
    directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7ee5722d41e6ff9c6d9dbb16ce0b07bb64b60cd2d275f2a83cc3dbf32c72a2bd(
    x: FileSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__794e1417e465e0dcfa5211235a8cd8fc29a100be525e796247e4cb0049908cbb(
    *,
    asset_id: builtins.str,
    asset_manifest_path: builtins.str,
    asset_publishing_role_arn: builtins.str,
    asset_selector: builtins.str,
    asset_type: AssetType,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c7ba3195a09ef48eb12384d783971206b5781b004c60fb1f9675a59382afd7bf(
    *,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__989087d830a094fcb5bc56d06a252db98005b5de8dc8ca23ffdd1558bb9a9266(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    asset_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    asset_pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    self_mutating: typing.Optional[builtins.bool] = None,
    self_mutation_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    single_publisher_per_type: typing.Optional[builtins.bool] = None,
    source_action: typing.Optional[_IAction_ecd54a08] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    support_docker_assets: typing.Optional[builtins.bool] = None,
    synth_action: typing.Optional[_IAction_ecd54a08] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__60667ecd41c7688b8d136a9e85f911265251d9c4c127095a6200a987090a7901(
    app_stage: _Stage_9729985a,
    *,
    extra_run_order_space: typing.Optional[jsii.Number] = None,
    manual_approvals: typing.Optional[builtins.bool] = None,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a21b566b5d6896234548128a0ba7342473aaf41024030bc7822b69f1bfbe75fa(
    stage_name: builtins.str,
    *,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4d10f3ea6630fe455a878f375963488e94d9692a28b3664284f1004a5d7a0aa1(
    cfn_output: _CfnOutput_a4d857a8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40acafbdef3fb1f200a0d9756a6be77e36ee43b979374cbba5b27e24b8215a79(
    stage_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__37f58057546cb907ffff99db5e3d900e2c1fb8278c6f2389f9943aaca1e45637(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    asset_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    asset_pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    enable_key_rotation: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    self_mutating: typing.Optional[builtins.bool] = None,
    self_mutation_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    single_publisher_per_type: typing.Optional[builtins.bool] = None,
    source_action: typing.Optional[_IAction_ecd54a08] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    support_docker_assets: typing.Optional[builtins.bool] = None,
    synth_action: typing.Optional[_IAction_ecd54a08] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dcc892f6f4314c93abf00b34101b146bb57a9578dc757b57de68eec784cf5bfd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    host: IStageHost,
    pipeline_stage: _IStage_5a7e7342,
    stage_name: builtins.str,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e44c877680f4153b7c1f9881e76412aa3418d316db52e4a18c6258423edc07bc(
    *actions: _IAction_ecd54a08,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d902744d394475fde2e3845a01b0e70231c5d650614aa06522a6e4f568f5f419(
    app_stage: _Stage_9729985a,
    *,
    extra_run_order_space: typing.Optional[jsii.Number] = None,
    manual_approvals: typing.Optional[builtins.bool] = None,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2c65e3001ed993d169c1125c20e8842cd226b968a6b4bba2d69b909ef07ac5cb(
    stack_artifact: _CloudFormationStackArtifact_45074b84,
    *,
    execute_run_order: typing.Optional[jsii.Number] = None,
    run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e24ca59156e0d56a199b747248a2332a03baeaeb0221db9542ff539d983505d6(
    artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd1fc645e90737eb0946de226128e7dbda3b2ec36fdf212763ef0ccabfd07be1(
    count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01a24e3cc881e3e895d7faa2336a1becf55bb39e624e37e5408ad218deeb3eaa(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    host: IStageHost,
    pipeline_stage: _IStage_5a7e7342,
    stage_name: builtins.str,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0e6d8f505c71a5a7594d231c58fd8d71a3d2dde1f874d16412b8113303bb5cee(
    *,
    build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    role_policy: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42daba2cc573cb139cb9afedb97b9407dc8e2947e5ea960ba7630d9dc96ea10d(
    *,
    code_build_clone_output: typing.Optional[builtins.bool] = None,
    event_role: typing.Optional[_IRole_59af6f50] = None,
    trigger: typing.Optional[_CodeCommitTrigger_3c8c9539] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0432247cd51e19450ab87dda01d3544325a396496478d68484f7a7ca057d368c(
    *,
    run_orders_consumed: jsii.Number,
    project: typing.Optional[_IProject_6da8803e] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5919f25f6a406bdbb4545664160a07a5eb12f43540c7fea542192d0c92d5f06c(
    *,
    synth: IFileSetProducer,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d503e56d92e6cc70b17815bbb0d8c54b6ba19e381750270bf4cbdc4bf141792e(
    *,
    connection_arn: builtins.str,
    code_build_clone_output: typing.Optional[builtins.bool] = None,
    trigger_on_push: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e289929d9836be1457a5c52f5c987a6ec8b2b32323befa43844034df9df66c73(
    scope: _constructs_77d1e7e8.Construct,
    artifact: _CloudFormationStackArtifact_45074b84,
    *,
    stack_name: typing.Optional[builtins.str] = None,
    cloud_assembly_input: _Artifact_9905eec2,
    base_action_name: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    execute_run_order: typing.Optional[jsii.Number] = None,
    output: typing.Optional[_Artifact_9905eec2] = None,
    output_file_name: typing.Optional[builtins.str] = None,
    prepare_run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c7f13cc7af69642e823b9ae4596283bafc1919d6494c3f27e352c811092eb51(
    scope: _Construct_e78e779f,
    stage: _IStage_5a7e7342,
    *,
    bucket: _IBucket_73486e29,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8d1d5b94df4243d1bf6f32e938a2cd4c01b1368e0d38ef428d55d65870b477b(
    name: builtins.str,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_Schedule_297d3fad] = None,
    targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__580643b9e49a8d6b994bcc1390d4e1cc15d22bd68ccf64a036deee5b4c2eef2e(
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    base_action_name: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    execute_run_order: typing.Optional[jsii.Number] = None,
    output: typing.Optional[_Artifact_9905eec2] = None,
    output_file_name: typing.Optional[builtins.str] = None,
    prepare_run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798f30cdb14e8e151292faf76d49af4b82a70ce48063d5e71e1e05e701577e55(
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    base_action_name: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    execute_run_order: typing.Optional[jsii.Number] = None,
    output: typing.Optional[_Artifact_9905eec2] = None,
    output_file_name: typing.Optional[builtins.str] = None,
    prepare_run_order: typing.Optional[jsii.Number] = None,
    action_role: _IRole_59af6f50,
    stack_name: builtins.str,
    template_path: builtins.str,
    cloud_formation_execution_role: typing.Optional[_IRole_59af6f50] = None,
    dependency_stack_artifact_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    region: typing.Optional[builtins.str] = None,
    stack_artifact_id: typing.Optional[builtins.str] = None,
    template_configuration_path: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5e76ae688baeaaddaa7fa9734504f555938deb1a93526f10f3f13dfaee2b8b6c(
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__500861ffeb59a40b6a53b015db083a8adeb677084ce60b91789661aa8cbdffaa(
    registry_domain: builtins.str,
    secret: _ISecret_22fb8757,
    *,
    assume_role: typing.Optional[_IRole_59af6f50] = None,
    secret_password_field: typing.Optional[builtins.str] = None,
    secret_username_field: typing.Optional[builtins.str] = None,
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8acf161909cdbe772a62d7e23bb291d0e182ef3b916887f5ec841bd3d6b03e5(
    secret: _ISecret_22fb8757,
    *,
    assume_role: typing.Optional[_IRole_59af6f50] = None,
    secret_password_field: typing.Optional[builtins.str] = None,
    secret_username_field: typing.Optional[builtins.str] = None,
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7889ac91b601338be20c192d3dc6673fd9f2b011a31f5d49177c721aea12776d(
    repositories: typing.Sequence[_IRepository_8b4d2894],
    *,
    assume_role: typing.Optional[_IRole_59af6f50] = None,
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__77881d6b41b1c44c8d52604541b28a60f92ad1cc2c96066592145107244f5d3d(
    grantee: _IGrantable_4c5a91d1,
    usage: DockerCredentialUsage,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f3ff22db6310dd4291743f33e7f7cbd2963aaff8816b0f0795c0f67f4aa9a4f7(
    *,
    action_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8645702d045218b4bdadcf05a41b11f8b20878e58f88c246168c0b9bd54bc15(
    *,
    assume_role: typing.Optional[_IRole_59af6f50] = None,
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__67479b6a052b7d47efe89a76048dac1dbe326d8bc870d70421741e1d137f2d0f(
    *,
    assume_role: typing.Optional[_IRole_59af6f50] = None,
    secret_password_field: typing.Optional[builtins.str] = None,
    secret_username_field: typing.Optional[builtins.str] = None,
    usages: typing.Optional[typing.Sequence[DockerCredentialUsage]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__44274088f5e1908d0356a1eeb98202c75e3be05060c87ac54d8c93a0242fc874(
    *,
    directory: builtins.str,
    file_set: FileSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59e72826ad96fd840e207fca89ae680da762de7b812dcd831ee6be2535727c9d(
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    execute_run_order: typing.Optional[jsii.Number] = None,
    output: typing.Optional[_Artifact_9905eec2] = None,
    output_file_name: typing.Optional[builtins.str] = None,
    prepare_run_order: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1307a9d666c3054703688c68914c5dbffb3aa27bad41a54e05a5484eebc6eaff(
    *,
    authentication: typing.Optional[_SecretValue_c18506ef] = None,
    trigger: typing.Optional[_GitHubTrigger_0a61ded3] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65adb69ac9d1c05d47c8eb8994f4f7a62111b5272eb0de742efece996c3ff43b(
    stage: _IStage_5a7e7342,
    *,
    action_name: builtins.str,
    artifacts: ArtifactMap,
    pipeline: CodePipeline,
    run_order: jsii.Number,
    scope: _constructs_77d1e7e8.Construct,
    before_self_mutation: typing.Optional[builtins.bool] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
    variables_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72651e1cd8c36fc3f2b7264c158060cf2a92d6b76466ad147679d7865920bfcd(
    stack_artifact_id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4407d3d9237c8acef0cb985742f530d6193ef57265c488c3f4951bf1e53e4b67(
    *,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__de137c3eea148a4e5a972cbfe48d1491c82ed2763990b7a357ec2e199734ca5c(
    *,
    stage: _Stage_9729985a,
    notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ebd565b4d620f66756c14cd03cfdd7fbabf44f60b27e556dcbc563303c2abb50(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    synth: IFileSetProducer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92803ad9223ee20ab44b2af82f86d4f006db21e2a4a55f09ac87c15b6afd5552(
    stage: _Stage_9729985a,
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8a671d62de7f5749fc258e0d502e0fda4dc9f8064a58775dd00014db204c0ee3(
    id: builtins.str,
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__973e6d2cd25db9dfd4ffb41b9e86771ebbddd86d44abded80db56708394849d5(
    *,
    synth: IFileSetProducer,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1ab2583853973cef62592c9fa850b1f25bcfd02e0286dab2b0c75948d35d5d93(
    *,
    action_name: builtins.str,
    artifacts: ArtifactMap,
    pipeline: CodePipeline,
    run_order: jsii.Number,
    scope: _constructs_77d1e7e8.Construct,
    before_self_mutation: typing.Optional[builtins.bool] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
    variables_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4ce6a0c6943083c5761b667a413f2d1a556a0d77aff064d3f43a051c6e144a87(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    action_name: builtins.str,
    asset_type: AssetType,
    cloud_assembly_input: _Artifact_9905eec2,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    create_buildspec_file: typing.Optional[builtins.bool] = None,
    dependable: typing.Optional[_IDependable_1175c9f7] = None,
    pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fcf4e5a78f888e9c917cf036235370249526172ed77c04f1b5e1261e85fed01(
    relative_manifest_path: builtins.str,
    asset_selector: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a864eb4995a9dde2272a396a55ad920203a466ef5daac0a7fc666fc01e7fad52(
    scope: _Construct_e78e779f,
    stage: _IStage_5a7e7342,
    *,
    bucket: _IBucket_73486e29,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b0c2663267c453297081ba1ccb9429d8cf3d8fc6a3aa746224a1a6e84ceb1af5(
    name: builtins.str,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_Schedule_297d3fad] = None,
    targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__35d6e68a44f57e99e4812a360f7501bd528f3a9c4891d25d9ee6dcbdb4b40259(
    *,
    action_name: builtins.str,
    asset_type: AssetType,
    cloud_assembly_input: _Artifact_9905eec2,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    create_buildspec_file: typing.Optional[builtins.bool] = None,
    dependable: typing.Optional[_IDependable_1175c9f7] = None,
    pre_install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cd7c4a9eeb00b204d16927bae73a204482dab1b382200197327fe63dd82c597a(
    *,
    action_name: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[_S3Trigger_688e3a4a] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c49fbf4080a2f4f4888eb06a5b34cafe0549fbd0c65f20c6a5c8ed371b1b1ea4(
    scope: _Construct_e78e779f,
    stage: _IStage_5a7e7342,
    *,
    bucket: _IBucket_73486e29,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0cd73e242f3f3cf2647ac421f5545ad3d873b448cf76c447a61d11bb0cb29d2a(
    name: builtins.str,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_Schedule_297d3fad] = None,
    targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__278fb7bed3d8bfa7d5973cd2fbf83eef62e29da30aed6823da84b820079002eb(
    *,
    action_name: builtins.str,
    commands: typing.Sequence[builtins.str],
    additional_artifacts: typing.Optional[typing.Sequence[_Artifact_9905eec2]] = None,
    bash_options: typing.Optional[builtins.str] = None,
    environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    run_order: typing.Optional[jsii.Number] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    use_outputs: typing.Optional[typing.Mapping[builtins.str, StackOutput]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01207d6669efe1d9b2af97bdfba04ff010b360580dea346962f6a202ef3c7f92(
    *,
    commands: typing.Sequence[builtins.str],
    additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
    input: typing.Optional[IFileSetProducer] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_output_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2018a6d750028088e68d772c1a323e145d2c829739d25b32932b67c3387e5446(
    scope: _Construct_e78e779f,
    stage: _IStage_5a7e7342,
    *,
    bucket: _IBucket_73486e29,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__502bfb765a1714a3716bfeca6efcbf6f7ca285039594f9b11e503d7ca9e3e3db(
    name: builtins.str,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_Schedule_297d3fad] = None,
    targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a85675b9cfb390898459f6acee701a2bd59eb85e298dbb295c9520bb1d714432(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    source_artifact: _Artifact_9905eec2,
    action_name: typing.Optional[builtins.str] = None,
    additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e73e21a339c0d1134c80e66f961e27a00d0c3d0b49aaba12421f5f49a12cd549(
    *,
    asset_id: builtins.str,
    asset_manifest_path: builtins.str,
    asset_selector: builtins.str,
    asset_type: AssetType,
    is_template: builtins.bool,
    asset_publishing_role_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cac9d369aa01c3b266f6d40155393b16752609a414589ca39f88b1f66c2fb44(
    stack_artifact: _CloudFormationStackArtifact_45074b84,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fd804115f5882d087e98f3e5d377331bc1b595d871e1ff444e43a419857d39eb(
    stack_deployment: StackDeployment,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1177f7360ee051e7ede8cfc9a5203a52cbc9726d0f4b752b604f5afd1c8392b7(
    pre: typing.Sequence[Step],
    change_set: typing.Sequence[Step],
    post: typing.Sequence[Step],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d06ceb728c1f4dff3443356ec12d902b0722f8042dc15992def99bd137e517a5(
    *,
    absolute_template_path: builtins.str,
    construct_path: builtins.str,
    stack_artifact_id: builtins.str,
    stack_name: builtins.str,
    account: typing.Optional[builtins.str] = None,
    assets: typing.Optional[typing.Sequence[typing.Union[StackAsset, typing.Dict[builtins.str, typing.Any]]]] = None,
    assume_role_arn: typing.Optional[builtins.str] = None,
    execution_role_arn: typing.Optional[builtins.str] = None,
    region: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    template_s3_uri: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0ff54bc06b9a2bcd06f714ff5c57ee062f376e76dbd290b36b16b193b270f50c(
    artifact_file: _ArtifactPath_a5b79113,
    output_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7d8f8949f797521c2554d3d48815420747ab7a11546ac59c15f9466c76e8e51b(
    output: _CfnOutput_a4d857a8,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__65abb849ba53caed5b5a4ed45e3948847f4efd560ec4c02180bbf59dc3a15abd(
    stack: StackDeployment,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d6daea77b45dcb8268287e85ce6401e8eb98630995956c31836eac882f666d7(
    *,
    stack: _Stack_9f43e4a3,
    change_set: typing.Optional[typing.Sequence[Step]] = None,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bbae825bd30eec9062ec6592072743027c2511f1400096d05eca75ec51887542(
    stage: _Stage_9729985a,
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c0244aef5fcff04ee6efad7dc0c39f5f9644b965c8227457e72169470b67a0b(
    *steps: Step,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d44a927346e96ba73dde340cd6e31e6e1adf346dbdb0a91f8d56dea3bc1d316(
    *steps: Step,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ab88758be77812a028d3398c40feabfc7dacc4ee296d01e58256b4d85937733(
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
    stage_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__13e06e4060aaafc208237d76240a1f7dd00a48369e1b28ac6002ce075c0998ef(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    source_artifact: _Artifact_9905eec2,
    action_name: typing.Optional[builtins.str] = None,
    additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    build_command: typing.Optional[builtins.str] = None,
    install_command: typing.Optional[builtins.str] = None,
    synth_command: typing.Optional[builtins.str] = None,
    test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7bdc6a4e618df7aa27db0344d6980d298db7001a4603e89fb12bc1f5027f4744(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    source_artifact: _Artifact_9905eec2,
    action_name: typing.Optional[builtins.str] = None,
    additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    build_command: typing.Optional[builtins.str] = None,
    install_command: typing.Optional[builtins.str] = None,
    synth_command: typing.Optional[builtins.str] = None,
    test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cc6ac099d78b2aa83433e11000f3f983d367125575066f1f5230f770688c2a6e(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3745bac2f2fca236c0359fc3123da78a73451c197cb968ccd41b5f1f48de32d7(
    steps: typing.Sequence[Step],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ac834aea5414ce95f5062c2a6343e6e9bc5c7f3458e92cdda4bb3a0d2fe4c1fc(
    fs: FileSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__18089ae266c819934cc9906ae5663b1602439f40e20f258beb5698017c052906(
    step: Step,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d2aaee5dadd18842e2dfea554fbf1b749e1d9d784b98b6d2bfccdca6f250d7ef(
    fs: FileSet,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1156c4db1d2756ee467272e3ce5f6d4e69528cfadab77412b2fc6c86d0714aa6(
    structure: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6aa6e12523cb7010899a8ed2b91bf42e1cee599398e114550c05b736665a0da7(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    pipeline_stack_hierarchical_id: builtins.str,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    pipeline_stack_name: typing.Optional[builtins.str] = None,
    privileged: typing.Optional[builtins.bool] = None,
    project_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cc359fed8424414c70f0a816104c60b835eea14de12980e41cbcbe3a495515d(
    scope: _Construct_e78e779f,
    stage: _IStage_5a7e7342,
    *,
    bucket: _IBucket_73486e29,
    role: _IRole_59af6f50,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0f06076c81cb6e0d2674dcb8c8226256384e75baea58011bd488c3d7f1ab83e6(
    name: builtins.str,
    target: typing.Optional[_IRuleTarget_d45ec729] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_IEventBus_2ca38c95] = None,
    event_pattern: typing.Optional[typing.Union[_EventPattern_a23fbf37, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_Schedule_297d3fad] = None,
    targets: typing.Optional[typing.Sequence[_IRuleTarget_d45ec729]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98ea5f4d415127a7ce6e7d4d5d8bf8bafa6b92876d1d3441223a56be3779b671(
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    pipeline_stack_hierarchical_id: builtins.str,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    cdk_cli_version: typing.Optional[builtins.str] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    pipeline_stack_name: typing.Optional[builtins.str] = None,
    privileged: typing.Optional[builtins.bool] = None,
    project_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4c81c281b340fcfad218742c416caae2ad8edaf8e50a08fafe9b39487b0716a3(
    id: builtins.str,
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5c3d6e1bb54a453d5e3450ed26e45bac6dc6ec4f8f8d3b7a341ebe01d14a7642(
    *steps: Step,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8460205a923996e7a85baf47ac9cfe3b025855b5b6f4bdb241f6976065ae5816(
    *steps: Step,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cb682cda07b2c2d6dbb6f200aeceb5bee91916059c7592b004a9fe1fe838030e(
    stage: _Stage_9729985a,
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
    stack_steps: typing.Optional[typing.Sequence[typing.Union[StackSteps, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3dd0f783298c6421e8b29e19d65812322f309c595caa14b7a9f8fdbefc00fee0(
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__adc974eafc2eed0817f0733876ffe71c1f108ed7fa2a50d5f4dc1c8e78427838(
    *,
    post: typing.Optional[typing.Sequence[Step]] = None,
    pre: typing.Optional[typing.Sequence[Step]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e0fa7d0ae0a29b445ff18db93c9ff98dec5c3e00a2edef37dec03ef223dadc8(
    *,
    confirm_broadening_permissions: typing.Optional[builtins.bool] = None,
    security_notification_topic: typing.Optional[_ITopic_465e36b9] = None,
    extra_run_order_space: typing.Optional[jsii.Number] = None,
    manual_approvals: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c0e0da41d774fadaaee80a06929a0d56b3f96d869344aeed3da0ea5aa63cad8(
    *,
    cloud_assembly_input: _Artifact_9905eec2,
    base_action_name: typing.Optional[builtins.str] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    execute_run_order: typing.Optional[jsii.Number] = None,
    output: typing.Optional[_Artifact_9905eec2] = None,
    output_file_name: typing.Optional[builtins.str] = None,
    prepare_run_order: typing.Optional[jsii.Number] = None,
    stack_name: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__437f9584e204e93834fa598928d0925b482a2ce6f1fdfd0254a819e12f077420(
    *,
    commands: typing.Sequence[builtins.str],
    additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
    input: typing.Optional[IFileSetProducer] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_output_directory: typing.Optional[builtins.str] = None,
    action_role: typing.Optional[_IRole_59af6f50] = None,
    build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    project_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3d85a5fcace279a9c8a8912c66d2e35bfd3f42fb89f8587472d0092a1d3b16e3(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    synth: IFileSetProducer,
    asset_publishing_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    cli_version: typing.Optional[builtins.str] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    code_pipeline: typing.Optional[_Pipeline_7744fe74] = None,
    cross_account_keys: typing.Optional[builtins.bool] = None,
    docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
    docker_enabled_for_self_mutation: typing.Optional[builtins.bool] = None,
    docker_enabled_for_synth: typing.Optional[builtins.bool] = None,
    pipeline_name: typing.Optional[builtins.str] = None,
    publish_assets_in_parallel: typing.Optional[builtins.bool] = None,
    reuse_cross_region_support_stacks: typing.Optional[builtins.bool] = None,
    self_mutation: typing.Optional[builtins.bool] = None,
    self_mutation_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    synth_code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__db56607b1d9203fc1146d005d14fa14fd5016be97decee6bfd1244ddedffa4de(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a89a99ee25ed767a94cf1be34a0ad78494cba669639858a340a2c3f16e320517(
    repository: _IRepository_cdb2a3c0,
    branch: builtins.str,
    *,
    code_build_clone_output: typing.Optional[builtins.bool] = None,
    event_role: typing.Optional[_IRole_59af6f50] = None,
    trigger: typing.Optional[_CodeCommitTrigger_3c8c9539] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__14a4c9d712ca2f16098d4c50799265e2252314fb8d8d010195939831972ef707(
    repo_string: builtins.str,
    branch: builtins.str,
    *,
    connection_arn: builtins.str,
    code_build_clone_output: typing.Optional[builtins.bool] = None,
    trigger_on_push: typing.Optional[builtins.bool] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__70d08c563c0fc15976dd12862f257616bd66af8f7fad5dda0af3679257c21f53(
    repository: _IRepository_8b4d2894,
    *,
    action_name: typing.Optional[builtins.str] = None,
    image_tag: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef46e9e27c2ca91d4fd872dba3b56caf30e8f4c077f34a7c9b84e9f3b505f648(
    repo_string: builtins.str,
    branch: builtins.str,
    *,
    authentication: typing.Optional[_SecretValue_c18506ef] = None,
    trigger: typing.Optional[_GitHubTrigger_0a61ded3] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df87e01880f520549a13e05a00a4f2b1d253868cf0a9d867a2350a29fcd1a192(
    bucket: _IBucket_73486e29,
    object_key: builtins.str,
    *,
    action_name: typing.Optional[builtins.str] = None,
    trigger: typing.Optional[_S3Trigger_688e3a4a] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__651affe1806145cfe56c37f0b9a64b9eb3d011260c3cfc470408624e9e4ae9f5(
    stage: _IStage_5a7e7342,
    *,
    action_name: builtins.str,
    artifacts: ArtifactMap,
    pipeline: CodePipeline,
    run_order: jsii.Number,
    scope: _constructs_77d1e7e8.Construct,
    before_self_mutation: typing.Optional[builtins.bool] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
    variables_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__39faa66828209f8fccf949c101f0dc72be33edb6963b16e7cd551f1fe6f18ed5(
    name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8b439002b6c7c05168263ed1e165629611868c388ac1315d69e0671e041301d(
    output: _Artifact_9905eec2,
    action_name: builtins.str,
    run_order: jsii.Number,
    variables_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c4faf61b3c00ca77f596f69c20ef198b6764c9bdc1f66d6390c2289d8e5829a1(
    id: builtins.str,
    *,
    stage: _Stage_9729985a,
    notification_topic: typing.Optional[_ITopic_465e36b9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1dd2d0e65a526f013f09e9d57ecc320078999c93e08adbf297c4a644b99eacd2(
    stage: _IStage_5a7e7342,
    *,
    action_name: builtins.str,
    artifacts: ArtifactMap,
    pipeline: CodePipeline,
    run_order: jsii.Number,
    scope: _constructs_77d1e7e8.Construct,
    before_self_mutation: typing.Optional[builtins.bool] = None,
    code_build_defaults: typing.Optional[typing.Union[CodeBuildOptions, typing.Dict[builtins.str, typing.Any]]] = None,
    fallback_artifact: typing.Optional[_Artifact_9905eec2] = None,
    variables_namespace: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9b50efdffc61a4f9cece5390be0e7e41023d4075f25439c34ffe3851976d15c5(
    id: builtins.str,
    producer: typing.Optional[Step] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7356adad32add6e22c90cc2f4aa896446bd3616ba262edea0995e27bc807c717(
    producer: typing.Optional[Step] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b369e1d78a8136d31211bc358d3c5cacdbcc8518faf31deac05239ca29270f81(
    id: builtins.str,
    *,
    comment: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d3ad11656e74961349db39d7e4f6031f5000393e2aa101114d3400f7ee5feba0(
    id: builtins.str,
    *,
    commands: typing.Sequence[builtins.str],
    additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
    input: typing.Optional[IFileSetProducer] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_output_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ef1d9cf7e496ac4f1abb47e79cbaaad11b487568f4669d49f4b6c6c868352dbd(
    directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16418d7295b78b107b8b9cf7e28adc671ec842a35352a39912ca835cd9853fc4(
    directory: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__df96ff352741339be53857b1c07478b90eb0dd2dc13338c066d6252436366af9(
    *,
    cloud_assembly_artifact: _Artifact_9905eec2,
    source_artifact: _Artifact_9905eec2,
    action_name: typing.Optional[builtins.str] = None,
    additional_artifacts: typing.Optional[typing.Sequence[typing.Union[AdditionalArtifact, typing.Dict[builtins.str, typing.Any]]]] = None,
    build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    copy_environment_variables: typing.Optional[typing.Sequence[builtins.str]] = None,
    environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    environment_variables: typing.Optional[typing.Mapping[builtins.str, typing.Union[_BuildEnvironmentVariable_00095c97, typing.Dict[builtins.str, typing.Any]]]] = None,
    project_name: typing.Optional[builtins.str] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    subdirectory: typing.Optional[builtins.str] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    synth_command: builtins.str,
    build_command: typing.Optional[builtins.str] = None,
    build_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    install_command: typing.Optional[builtins.str] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    test_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d26449ed6ece76731213baa7e3228da7b38ab538a9d821ccd180b7ec79add123(
    id: builtins.str,
    *,
    action_role: typing.Optional[_IRole_59af6f50] = None,
    build_environment: typing.Optional[typing.Union[_BuildEnvironment_77bc5f50, typing.Dict[builtins.str, typing.Any]]] = None,
    partial_build_spec: typing.Optional[_BuildSpec_1d70c5a1] = None,
    project_name: typing.Optional[builtins.str] = None,
    role: typing.Optional[_IRole_59af6f50] = None,
    role_policy_statements: typing.Optional[typing.Sequence[_PolicyStatement_296fe8a3]] = None,
    security_groups: typing.Optional[typing.Sequence[_ISecurityGroup_cdbba9d3]] = None,
    subnet_selection: typing.Optional[typing.Union[_SubnetSelection_1284e62c, typing.Dict[builtins.str, typing.Any]]] = None,
    timeout: typing.Optional[_Duration_070aa057] = None,
    vpc: typing.Optional[_IVpc_6d1f76c4] = None,
    commands: typing.Sequence[builtins.str],
    additional_inputs: typing.Optional[typing.Mapping[builtins.str, IFileSetProducer]] = None,
    env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    env_from_cfn_outputs: typing.Optional[typing.Mapping[builtins.str, _CfnOutput_a4d857a8]] = None,
    input: typing.Optional[IFileSetProducer] = None,
    install_commands: typing.Optional[typing.Sequence[builtins.str]] = None,
    primary_output_directory: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__841756ad0c29682b3a9b312ca1c310b0b27f7aeca08a53fd3aa399399aa29024(
    variable_name: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__05e74cfd4b72679ac7d410b48e116f9ca181b4eb2329a7f7684fb4b555b1cca0(
    artifact: _Artifact_9905eec2,
) -> None:
    """Type checking stubs"""
    pass
