import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ..._jsii import *

import constructs as _constructs_77d1e7e8
from ... import (
    Construct as _Construct_e78e779f,
    ConstructNode as _ConstructNode_33e3628c,
    Duration as _Duration_070aa057,
    Resource as _Resource_abff4495,
    Size as _Size_7fbd4337,
)
from ...aws_cloudwatch import (
    Metric as _Metric_5b2b8e58,
    MetricOptions as _MetricOptions_1c185ae8,
    Unit as _Unit_113c79f9,
)
from ...aws_codeguruprofiler import IProfilingGroup as _IProfilingGroup_418eb20c
from ...aws_ec2 import (
    Connections as _Connections_57ccbda9,
    ISecurityGroup as _ISecurityGroup_cdbba9d3,
    IVpc as _IVpc_6d1f76c4,
    SubnetSelection as _SubnetSelection_1284e62c,
)
from ...aws_iam import (
    Grant as _Grant_bcb5eae7,
    IGrantable as _IGrantable_4c5a91d1,
    IPrincipal as _IPrincipal_93b48231,
    IRole as _IRole_59af6f50,
    PolicyStatement as _PolicyStatement_296fe8a3,
)
from ...aws_kms import IKey as _IKey_36930160
from ...aws_lambda import (
    Alias as _Alias_9e39972c,
    AliasOptions as _AliasOptions_c9b06466,
    Architecture as _Architecture_24056b62,
    Code as _Code_e8adcb06,
    EventInvokeConfigOptions as _EventInvokeConfigOptions_5cec26e1,
    EventSourceMapping as _EventSourceMapping_64d554a4,
    EventSourceMappingOptions as _EventSourceMappingOptions_36519f99,
    FileSystem as _FileSystem_17be1f4c,
    FunctionProps as _FunctionProps_5561697c,
    FunctionUrl as _FunctionUrl_0f64d446,
    FunctionUrlAuthType as _FunctionUrlAuthType_4cfe7120,
    FunctionUrlCorsOptions as _FunctionUrlCorsOptions_3bbf24b0,
    FunctionUrlOptions as _FunctionUrlOptions_dae61a5b,
    ICodeSigningConfig as _ICodeSigningConfig_5d77bccf,
    IDestination as _IDestination_7f253ff1,
    IEventSource as _IEventSource_7914870e,
    IEventSourceDlq as _IEventSourceDlq_f5ae73e7,
    IFunction as _IFunction_6e14f09e,
    ILayerVersion as _ILayerVersion_b2b86380,
    IVersion as _IVersion_316c9051,
    LambdaInsightsVersion as _LambdaInsightsVersion_2966e73b,
    LogRetentionRetryOptions as _LogRetentionRetryOptions_7acc40ab,
    Permission as _Permission_0b3dcf94,
    Runtime as _Runtime_932d369a,
    SourceAccessConfiguration as _SourceAccessConfiguration_afc347bf,
    StartingPosition as _StartingPosition_9192859a,
    Tracing as _Tracing_b7f4a8b6,
    VersionOptions as _VersionOptions_085bb455,
    VersionWeight as _VersionWeight_7bcc86af,
)
from ...aws_logs import RetentionDays as _RetentionDays_6c560d31
from ...aws_sns import ITopic as _ITopic_465e36b9
from ...aws_sqs import IQueue as _IQueue_45a01ab4


@jsii.implements(_IVersion_316c9051)
class EdgeFunction(
    _Resource_abff4495,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_cloudfront.experimental.EdgeFunction",
):
    '''(experimental) A Lambda@Edge function.

    Convenience resource for requesting a Lambda function in the 'us-east-1' region for use with Lambda@Edge.
    Implements several restrictions enforced by Lambda@Edge.

    Note that this construct requires that the 'us-east-1' region has been bootstrapped.
    See https://docs.aws.amazon.com/cdk/latest/guide/bootstrapping.html or 'cdk bootstrap --help' for options.

    :stability: experimental
    :resource: AWS::Lambda::Function
    :exampleMetadata: infused

    Example::

        # my_bucket: s3.Bucket
        # A Lambda@Edge function added to default behavior of a Distribution
        # and triggered on every request
        my_func = cloudfront.experimental.EdgeFunction(self, "MyFunction",
            runtime=lambda_.Runtime.NODEJS_14_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
        )
        cloudfront.Distribution(self, "myDist",
            default_behavior=cloudfront.aws_cloudfront.BehaviorOptions(
                origin=origins.S3Origin(my_bucket),
                edge_lambdas=[cloudfront.aws_cloudfront.EdgeLambda(
                    function_version=my_func.current_version,
                    event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST
                )
                ]
            )
        )
    '''

    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        stack_id: typing.Optional[builtins.str] = None,
        code: _Code_e8adcb06,
        handler: builtins.str,
        runtime: _Runtime_932d369a,
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
        :param stack_id: (experimental) The stack ID of Lambda@Edge function. Default: - ``edge-lambda-stack-${region}``
        :param code: (experimental) The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: (experimental) The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: (experimental) The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide. Use ``Runtime.FROM_IMAGE`` when when defining a function from a Docker image.
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
            type_hints = typing.get_type_hints(_typecheckingstub__9e33863d6a57cfd60df8599c199479f6571585f2ece433bd10ccebb7d1179bd6)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = EdgeFunctionProps(
            stack_id=stack_id,
            code=code,
            handler=handler,
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

    @jsii.member(jsii_name="addAlias")
    def add_alias(
        self,
        alias_name: builtins.str,
        *,
        additional_versions: typing.Optional[typing.Sequence[typing.Union[_VersionWeight_7bcc86af, typing.Dict[builtins.str, typing.Any]]]] = None,
        description: typing.Optional[builtins.str] = None,
        provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> _Alias_9e39972c:
        '''(experimental) Defines an alias for this version.

        :param alias_name: -
        :param additional_versions: (experimental) Additional versions with individual weights this alias points to. Individual additional version weights specified here should add up to (less than) one. All remaining weight is routed to the default version. For example, the config is Example:: version: "1" additionalVersions: [{ version: "2", weight: 0.05 }] Then 5% of traffic will be routed to function version 2, while the remaining 95% of traffic will be routed to function version 1. Default: No additional versions
        :param description: (experimental) Description for the alias. Default: No description
        :param provisioned_concurrent_executions: (experimental) Specifies a provisioned concurrency configuration for a function's alias. Default: No provisioned concurrency
        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c6362ac57f434dd0b690ff82bde9f499565307fd5acf6dd6d1c5938106f60aeb)
            check_type(argname="argument alias_name", value=alias_name, expected_type=type_hints["alias_name"])
        options = _AliasOptions_c9b06466(
            additional_versions=additional_versions,
            description=description,
            provisioned_concurrent_executions=provisioned_concurrent_executions,
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        return typing.cast(_Alias_9e39972c, jsii.invoke(self, "addAlias", [alias_name, options]))

    @jsii.member(jsii_name="addEventSource")
    def add_event_source(self, source: _IEventSource_7914870e) -> None:
        '''(experimental) Adds an event source to this function.

        :param source: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3e708d1c15730a6c2fcd255240c77016451cdfd8e9e395f1e39b529dacd36d1c)
            check_type(argname="argument source", value=source, expected_type=type_hints["source"])
        return typing.cast(None, jsii.invoke(self, "addEventSource", [source]))

    @jsii.member(jsii_name="addEventSourceMapping")
    def add_event_source_mapping(
        self,
        id: builtins.str,
        *,
        batch_size: typing.Optional[jsii.Number] = None,
        bisect_batch_on_error: typing.Optional[builtins.bool] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_source_arn: typing.Optional[builtins.str] = None,
        kafka_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
        kafka_topic: typing.Optional[builtins.str] = None,
        max_batching_window: typing.Optional[_Duration_070aa057] = None,
        max_record_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
        parallelization_factor: typing.Optional[jsii.Number] = None,
        report_batch_item_failures: typing.Optional[builtins.bool] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
        source_access_configurations: typing.Optional[typing.Sequence[typing.Union[_SourceAccessConfiguration_afc347bf, typing.Dict[builtins.str, typing.Any]]]] = None,
        starting_position: typing.Optional[_StartingPosition_9192859a] = None,
        tumbling_window: typing.Optional[_Duration_070aa057] = None,
    ) -> _EventSourceMapping_64d554a4:
        '''(experimental) Adds an event source that maps to this AWS Lambda function.

        :param id: -
        :param batch_size: (experimental) The largest number of records that AWS Lambda will retrieve from your event source at the time of invoking your function. Your function receives an event with all the retrieved records. Valid Range: Minimum value of 1. Maximum value of 10000. Default: - Amazon Kinesis, Amazon DynamoDB, and Amazon MSK is 100 records. The default for Amazon SQS is 10 messages. For standard SQS queues, the maximum is 10,000. For FIFO SQS queues, the maximum is 10.
        :param bisect_batch_on_error: (experimental) If the function returns an error, split the batch in two and retry. Default: false
        :param enabled: (experimental) Set to false to disable the event source upon creation. Default: true
        :param event_source_arn: (experimental) The Amazon Resource Name (ARN) of the event source. Any record added to this stream can invoke the Lambda function. Default: - not set if using a self managed Kafka cluster, throws an error otherwise
        :param kafka_bootstrap_servers: (experimental) A list of host and port pairs that are the addresses of the Kafka brokers in a self managed "bootstrap" Kafka cluster that a Kafka client connects to initially to bootstrap itself. They are in the format ``abc.example.com:9096``. Default: - none
        :param kafka_topic: (experimental) The name of the Kafka topic. Default: - no topic
        :param max_batching_window: (experimental) The maximum amount of time to gather records before invoking the function. Maximum of Duration.minutes(5) Default: Duration.seconds(0)
        :param max_record_age: (experimental) The maximum age of a record that Lambda sends to a function for processing. Valid Range: - Minimum value of 60 seconds - Maximum value of 7 days Default: - infinite or until the record expires.
        :param on_failure: (experimental) An Amazon SQS queue or Amazon SNS topic destination for discarded records. Default: discarded records are ignored
        :param parallelization_factor: (experimental) The number of batches to process from each shard concurrently. Valid Range: - Minimum value of 1 - Maximum value of 10 Default: 1
        :param report_batch_item_failures: (experimental) Allow functions to return partially successful responses for a batch of records. Default: false
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Set to ``undefined`` if you want lambda to keep retrying infinitely or until the record expires. Valid Range: - Minimum value of 0 - Maximum value of 10000 Default: - infinite or until the record expires.
        :param source_access_configurations: (experimental) Specific settings like the authentication protocol or the VPC components to secure access to your event source. Default: - none
        :param starting_position: (experimental) The position in the DynamoDB, Kinesis or MSK stream where AWS Lambda should start reading. Default: - Required for Amazon Kinesis, Amazon DynamoDB, and Amazon MSK Streams sources.
        :param tumbling_window: (experimental) The size of the tumbling windows to group records sent to DynamoDB or Kinesis. Default: - None

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3feca7ff6d834b38364d8712841b4f39cbb8cae0a5115d0ef68f8d8bb476e29f)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        options = _EventSourceMappingOptions_36519f99(
            batch_size=batch_size,
            bisect_batch_on_error=bisect_batch_on_error,
            enabled=enabled,
            event_source_arn=event_source_arn,
            kafka_bootstrap_servers=kafka_bootstrap_servers,
            kafka_topic=kafka_topic,
            max_batching_window=max_batching_window,
            max_record_age=max_record_age,
            on_failure=on_failure,
            parallelization_factor=parallelization_factor,
            report_batch_item_failures=report_batch_item_failures,
            retry_attempts=retry_attempts,
            source_access_configurations=source_access_configurations,
            starting_position=starting_position,
            tumbling_window=tumbling_window,
        )

        return typing.cast(_EventSourceMapping_64d554a4, jsii.invoke(self, "addEventSourceMapping", [id, options]))

    @jsii.member(jsii_name="addFunctionUrl")
    def add_function_url(
        self,
        *,
        auth_type: typing.Optional[_FunctionUrlAuthType_4cfe7120] = None,
        cors: typing.Optional[typing.Union[_FunctionUrlCorsOptions_3bbf24b0, typing.Dict[builtins.str, typing.Any]]] = None,
    ) -> _FunctionUrl_0f64d446:
        '''(experimental) Adds a url to this lambda function.

        :param auth_type: (experimental) The type of authentication that your function URL uses. Default: FunctionUrlAuthType.AWS_IAM
        :param cors: (experimental) The cross-origin resource sharing (CORS) settings for your function URL. Default: - No CORS configuration.

        :stability: experimental
        '''
        options = _FunctionUrlOptions_dae61a5b(auth_type=auth_type, cors=cors)

        return typing.cast(_FunctionUrl_0f64d446, jsii.invoke(self, "addFunctionUrl", [options]))

    @jsii.member(jsii_name="addPermission")
    def add_permission(
        self,
        id: builtins.str,
        *,
        principal: _IPrincipal_93b48231,
        action: typing.Optional[builtins.str] = None,
        event_source_token: typing.Optional[builtins.str] = None,
        function_url_auth_type: typing.Optional[_FunctionUrlAuthType_4cfe7120] = None,
        scope: typing.Optional[_Construct_e78e779f] = None,
        source_account: typing.Optional[builtins.str] = None,
        source_arn: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Adds a permission to the Lambda resource policy.

        :param id: -
        :param principal: (experimental) The entity for which you are granting permission to invoke the Lambda function. This entity can be any valid AWS service principal, such as s3.amazonaws.com or sns.amazonaws.com, or, if you are granting cross-account permission, an AWS account ID. For example, you might want to allow a custom application in another AWS account to push events to Lambda by invoking your function. The principal can be either an AccountPrincipal or a ServicePrincipal.
        :param action: (experimental) The Lambda actions that you want to allow in this statement. For example, you can specify lambda:CreateFunction to specify a certain action, or use a wildcard (``lambda:*``) to grant permission to all Lambda actions. For a list of actions, see Actions and Condition Context Keys for AWS Lambda in the IAM User Guide. Default: 'lambda:InvokeFunction'
        :param event_source_token: (experimental) A unique token that must be supplied by the principal invoking the function. Default: The caller would not need to present a token.
        :param function_url_auth_type: (experimental) The authType for the function URL that you are granting permissions for. Default: - No functionUrlAuthType
        :param scope: (experimental) The scope to which the permission constructs be attached. The default is the Lambda function construct itself, but this would need to be different in cases such as cross-stack references where the Permissions would need to sit closer to the consumer of this permission (i.e., the caller). Default: - The instance of lambda.IFunction
        :param source_account: (experimental) The AWS account ID (without hyphens) of the source owner. For example, if you specify an S3 bucket in the SourceArn property, this value is the bucket owner's account ID. You can use this property to ensure that all source principals are owned by a specific account.
        :param source_arn: (experimental) The ARN of a resource that is invoking your function. When granting Amazon Simple Storage Service (Amazon S3) permission to invoke your function, specify this property with the bucket ARN as its value. This ensures that events generated only from the specified bucket, not just any bucket from any AWS account that creates a mapping to your function, can invoke the function.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a1aa72530561b6b0097d08918d784e0b8bc4da3fd24bba9088007692c140be6c)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        permission = _Permission_0b3dcf94(
            principal=principal,
            action=action,
            event_source_token=event_source_token,
            function_url_auth_type=function_url_auth_type,
            scope=scope,
            source_account=source_account,
            source_arn=source_arn,
        )

        return typing.cast(None, jsii.invoke(self, "addPermission", [id, permission]))

    @jsii.member(jsii_name="addToRolePolicy")
    def add_to_role_policy(self, statement: _PolicyStatement_296fe8a3) -> None:
        '''(experimental) Adds a statement to the IAM role assumed by the instance.

        :param statement: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9107e126cded390da28f1e13def042bcd2eff13fe828755050439488c02bf480)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToRolePolicy", [statement]))

    @jsii.member(jsii_name="configureAsyncInvoke")
    def configure_async_invoke(
        self,
        *,
        max_event_age: typing.Optional[_Duration_070aa057] = None,
        on_failure: typing.Optional[_IDestination_7f253ff1] = None,
        on_success: typing.Optional[_IDestination_7f253ff1] = None,
        retry_attempts: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''(experimental) Configures options for asynchronous invocation.

        :param max_event_age: (experimental) The maximum age of a request that Lambda sends to a function for processing. Minimum: 60 seconds Maximum: 6 hours Default: Duration.hours(6)
        :param on_failure: (experimental) The destination for failed invocations. Default: - no destination
        :param on_success: (experimental) The destination for successful invocations. Default: - no destination
        :param retry_attempts: (experimental) The maximum number of times to retry when the function returns an error. Minimum: 0 Maximum: 2 Default: 2

        :stability: experimental
        '''
        options = _EventInvokeConfigOptions_5cec26e1(
            max_event_age=max_event_age,
            on_failure=on_failure,
            on_success=on_success,
            retry_attempts=retry_attempts,
        )

        return typing.cast(None, jsii.invoke(self, "configureAsyncInvoke", [options]))

    @jsii.member(jsii_name="grantInvoke")
    def grant_invoke(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to invoke this Lambda.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b214face5a47c4a7e262ee10a0f63c5f7d7f0e130e155481b40b945c21bb3b74)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantInvoke", [identity]))

    @jsii.member(jsii_name="grantInvokeUrl")
    def grant_invoke_url(self, identity: _IGrantable_4c5a91d1) -> _Grant_bcb5eae7:
        '''(experimental) Grant the given identity permissions to invoke this Lambda Function URL.

        :param identity: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2cfcf3ca8dd99fe9de9534293ef85b5e406fe3e662ffed4c4ea6f1e27f9dd40a)
            check_type(argname="argument identity", value=identity, expected_type=type_hints["identity"])
        return typing.cast(_Grant_bcb5eae7, jsii.invoke(self, "grantInvokeUrl", [identity]))

    @jsii.member(jsii_name="metric")
    def metric(
        self,
        metric_name: builtins.str,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Return the given named metric for this Lambda Return the given named metric for this Function.

        :param metric_name: -
        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__62dd7c18ef9616546f36a04ad59c21844b0d11d28f918f8f65066ec977adcfe6)
            check_type(argname="argument metric_name", value=metric_name, expected_type=type_hints["metric_name"])
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metric", [metric_name, props]))

    @jsii.member(jsii_name="metricDuration")
    def metric_duration(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the Duration of this Lambda How long execution of this Lambda takes.

        Average over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricDuration", [props]))

    @jsii.member(jsii_name="metricErrors")
    def metric_errors(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) How many invocations of this Lambda fail.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricErrors", [props]))

    @jsii.member(jsii_name="metricInvocations")
    def metric_invocations(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of invocations of this Lambda How often this Lambda is invoked.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricInvocations", [props]))

    @jsii.member(jsii_name="metricThrottles")
    def metric_throttles(
        self,
        *,
        account: typing.Optional[builtins.str] = None,
        color: typing.Optional[builtins.str] = None,
        dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
        dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        label: typing.Optional[builtins.str] = None,
        period: typing.Optional[_Duration_070aa057] = None,
        region: typing.Optional[builtins.str] = None,
        statistic: typing.Optional[builtins.str] = None,
        unit: typing.Optional[_Unit_113c79f9] = None,
    ) -> _Metric_5b2b8e58:
        '''(experimental) Metric for the number of throttled invocations of this Lambda How often this Lambda is throttled.

        Sum over 5 minutes

        :param account: (experimental) Account which this metric comes from. Default: - Deployment account.
        :param color: (experimental) The hex color code, prefixed with '#' (e.g. '#00ff00'), to use when this metric is rendered on a graph. The ``Color`` class has a set of standard colors that can be used here. Default: - Automatic color
        :param dimensions: (deprecated) Dimensions of the metric. Default: - No dimensions.
        :param dimensions_map: (experimental) Dimensions of the metric. Default: - No dimensions.
        :param label: (experimental) Label for this metric when added to a Graph in a Dashboard. You can use `dynamic labels <https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/graph-dynamic-labels.html>`_ to show summary information about the entire displayed time series in the legend. For example, if you use:: [max: ${MAX}] MyMetric As the metric label, the maximum value in the visible range will be shown next to the time series name in the graph's legend. Default: - No label
        :param period: (experimental) The period over which the specified statistic is applied. Default: Duration.minutes(5)
        :param region: (experimental) Region which this metric comes from. Default: - Deployment region.
        :param statistic: (experimental) What function to use for aggregating. Can be one of the following: - "Minimum" | "min" - "Maximum" | "max" - "Average" | "avg" - "Sum" | "sum" - "SampleCount | "n" - "pNN.NN" Default: Average
        :param unit: (experimental) Unit used to filter the metric stream. Only refer to datums emitted to the metric stream with the given unit and ignore all others. Only useful when datums are being emitted to the same metric stream under different units. The default is to use all matric datums in the stream, regardless of unit, which is recommended in nearly all cases. CloudWatch does not honor this property for graphs. Default: - All metric datums in the given metric stream

        :stability: experimental
        '''
        props = _MetricOptions_1c185ae8(
            account=account,
            color=color,
            dimensions=dimensions,
            dimensions_map=dimensions_map,
            label=label,
            period=period,
            region=region,
            statistic=statistic,
            unit=unit,
        )

        return typing.cast(_Metric_5b2b8e58, jsii.invoke(self, "metricThrottles", [props]))

    @builtins.property
    @jsii.member(jsii_name="architecture")
    def architecture(self) -> _Architecture_24056b62:
        '''(experimental) The system architectures compatible with this lambda function.

        :stability: experimental
        '''
        return typing.cast(_Architecture_24056b62, jsii.get(self, "architecture"))

    @builtins.property
    @jsii.member(jsii_name="connections")
    def connections(self) -> _Connections_57ccbda9:
        '''(experimental) Not supported.

        Connections are only applicable to VPC-enabled functions.

        :stability: experimental
        '''
        return typing.cast(_Connections_57ccbda9, jsii.get(self, "connections"))

    @builtins.property
    @jsii.member(jsii_name="currentVersion")
    def current_version(self) -> _IVersion_316c9051:
        '''(experimental) Convenience method to make ``EdgeFunction`` conform to the same interface as ``Function``.

        :stability: experimental
        '''
        return typing.cast(_IVersion_316c9051, jsii.get(self, "currentVersion"))

    @builtins.property
    @jsii.member(jsii_name="edgeArn")
    def edge_arn(self) -> builtins.str:
        '''(experimental) The ARN of the version for Lambda@Edge.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "edgeArn"))

    @builtins.property
    @jsii.member(jsii_name="functionArn")
    def function_arn(self) -> builtins.str:
        '''(experimental) The ARN of the function.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionArn"))

    @builtins.property
    @jsii.member(jsii_name="functionName")
    def function_name(self) -> builtins.str:
        '''(experimental) The name of the function.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "functionName"))

    @builtins.property
    @jsii.member(jsii_name="grantPrincipal")
    def grant_principal(self) -> _IPrincipal_93b48231:
        '''(experimental) The principal to grant permissions to.

        :stability: experimental
        '''
        return typing.cast(_IPrincipal_93b48231, jsii.get(self, "grantPrincipal"))

    @builtins.property
    @jsii.member(jsii_name="isBoundToVpc")
    def is_bound_to_vpc(self) -> builtins.bool:
        '''(experimental) Whether or not this Lambda function was bound to a VPC.

        If this is is ``false``, trying to access the ``connections`` object will fail.

        :stability: experimental
        '''
        return typing.cast(builtins.bool, jsii.get(self, "isBoundToVpc"))

    @builtins.property
    @jsii.member(jsii_name="lambda")
    def lambda_(self) -> _IFunction_6e14f09e:
        '''(experimental) The underlying AWS Lambda function.

        :stability: experimental
        '''
        return typing.cast(_IFunction_6e14f09e, jsii.get(self, "lambda"))

    @builtins.property
    @jsii.member(jsii_name="latestVersion")
    def latest_version(self) -> _IVersion_316c9051:
        '''(experimental) The ``$LATEST`` version of this function.

        Note that this is reference to a non-specific AWS Lambda version, which
        means the function this version refers to can return different results in
        different invocations.

        To obtain a reference to an explicit version which references the current
        function configuration, use ``lambdaFunction.currentVersion`` instead.

        :stability: experimental
        '''
        return typing.cast(_IVersion_316c9051, jsii.get(self, "latestVersion"))

    @builtins.property
    @jsii.member(jsii_name="permissionsNode")
    def permissions_node(self) -> _ConstructNode_33e3628c:
        '''(experimental) The construct node where permissions are attached.

        :stability: experimental
        '''
        return typing.cast(_ConstructNode_33e3628c, jsii.get(self, "permissionsNode"))

    @builtins.property
    @jsii.member(jsii_name="resourceArnsForGrantInvoke")
    def resource_arns_for_grant_invoke(self) -> typing.List[builtins.str]:
        '''(experimental) The ARN(s) to put into the resource field of the generated IAM policy for grantInvoke().

        This property is for cdk modules to consume only. You should not need to use this property.
        Instead, use grantInvoke() directly.

        :stability: experimental
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceArnsForGrantInvoke"))

    @builtins.property
    @jsii.member(jsii_name="version")
    def version(self) -> builtins.str:
        '''(experimental) The most recently deployed version of this function.

        :stability: experimental
        '''
        return typing.cast(builtins.str, jsii.get(self, "version"))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> typing.Optional[_IRole_59af6f50]:
        '''(experimental) The IAM role associated with this function.

        :stability: experimental
        '''
        return typing.cast(typing.Optional[_IRole_59af6f50], jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="monocdk.aws_cloudfront.experimental.EdgeFunctionProps",
    jsii_struct_bases=[_FunctionProps_5561697c],
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
        "code": "code",
        "handler": "handler",
        "runtime": "runtime",
        "stack_id": "stackId",
    },
)
class EdgeFunctionProps(_FunctionProps_5561697c):
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
        code: _Code_e8adcb06,
        handler: builtins.str,
        runtime: _Runtime_932d369a,
        stack_id: typing.Optional[builtins.str] = None,
    ) -> None:
        '''(experimental) Properties for creating a Lambda@Edge function.

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
        :param code: (experimental) The source code of your Lambda function. You can point to a file in an Amazon Simple Storage Service (Amazon S3) bucket or specify your source code as inline text.
        :param handler: (experimental) The name of the method within your code that Lambda calls to execute your function. The format includes the file name. It can also include namespaces and other qualifiers, depending on the runtime. For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel. Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image. NOTE: If you specify your source code as inline text by specifying the ZipFile property within the Code property, specify index.function_name as the handler.
        :param runtime: (experimental) The runtime environment for the Lambda function that you are uploading. For valid values, see the Runtime property in the AWS Lambda Developer Guide. Use ``Runtime.FROM_IMAGE`` when when defining a function from a Docker image.
        :param stack_id: (experimental) The stack ID of Lambda@Edge function. Default: - ``edge-lambda-stack-${region}``

        :stability: experimental
        :exampleMetadata: infused

        Example::

            # my_bucket: s3.Bucket
            # A Lambda@Edge function added to default behavior of a Distribution
            # and triggered on every request
            my_func = cloudfront.experimental.EdgeFunction(self, "MyFunction",
                runtime=lambda_.Runtime.NODEJS_14_X,
                handler="index.handler",
                code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler"))
            )
            cloudfront.Distribution(self, "myDist",
                default_behavior=cloudfront.aws_cloudfront.BehaviorOptions(
                    origin=origins.S3Origin(my_bucket),
                    edge_lambdas=[cloudfront.aws_cloudfront.EdgeLambda(
                        function_version=my_func.current_version,
                        event_type=cloudfront.LambdaEdgeEventType.VIEWER_REQUEST
                    )
                    ]
                )
            )
        '''
        if isinstance(current_version_options, dict):
            current_version_options = _VersionOptions_085bb455(**current_version_options)
        if isinstance(log_retention_retry_options, dict):
            log_retention_retry_options = _LogRetentionRetryOptions_7acc40ab(**log_retention_retry_options)
        if isinstance(vpc_subnets, dict):
            vpc_subnets = _SubnetSelection_1284e62c(**vpc_subnets)
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3d927824b42876df5094d27c5f9f48347a33c4f3a00c054ca6fc04e976b45bc)
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
            check_type(argname="argument code", value=code, expected_type=type_hints["code"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
            check_type(argname="argument runtime", value=runtime, expected_type=type_hints["runtime"])
            check_type(argname="argument stack_id", value=stack_id, expected_type=type_hints["stack_id"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "code": code,
            "handler": handler,
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
        if stack_id is not None:
            self._values["stack_id"] = stack_id

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
    def code(self) -> _Code_e8adcb06:
        '''(experimental) The source code of your Lambda function.

        You can point to a file in an
        Amazon Simple Storage Service (Amazon S3) bucket or specify your source
        code as inline text.

        :stability: experimental
        '''
        result = self._values.get("code")
        assert result is not None, "Required property 'code' is missing"
        return typing.cast(_Code_e8adcb06, result)

    @builtins.property
    def handler(self) -> builtins.str:
        '''(experimental) The name of the method within your code that Lambda calls to execute your function.

        The format includes the file name. It can also include
        namespaces and other qualifiers, depending on the runtime.
        For more information, see https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-features.html#gettingstarted-features-programmingmodel.

        Use ``Handler.FROM_IMAGE`` when defining a function from a Docker image.

        NOTE: If you specify your source code as inline text by specifying the
        ZipFile property within the Code property, specify index.function_name as
        the handler.

        :stability: experimental
        '''
        result = self._values.get("handler")
        assert result is not None, "Required property 'handler' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def runtime(self) -> _Runtime_932d369a:
        '''(experimental) The runtime environment for the Lambda function that you are uploading.

        For valid values, see the Runtime property in the AWS Lambda Developer
        Guide.

        Use ``Runtime.FROM_IMAGE`` when when defining a function from a Docker image.

        :stability: experimental
        '''
        result = self._values.get("runtime")
        assert result is not None, "Required property 'runtime' is missing"
        return typing.cast(_Runtime_932d369a, result)

    @builtins.property
    def stack_id(self) -> typing.Optional[builtins.str]:
        '''(experimental) The stack ID of Lambda@Edge function.

        :default: - ``edge-lambda-stack-${region}``

        :stability: experimental
        '''
        result = self._values.get("stack_id")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "EdgeFunctionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "EdgeFunction",
    "EdgeFunctionProps",
]

publication.publish()

def _typecheckingstub__9e33863d6a57cfd60df8599c199479f6571585f2ece433bd10ccebb7d1179bd6(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    stack_id: typing.Optional[builtins.str] = None,
    code: _Code_e8adcb06,
    handler: builtins.str,
    runtime: _Runtime_932d369a,
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

def _typecheckingstub__c6362ac57f434dd0b690ff82bde9f499565307fd5acf6dd6d1c5938106f60aeb(
    alias_name: builtins.str,
    *,
    additional_versions: typing.Optional[typing.Sequence[typing.Union[_VersionWeight_7bcc86af, typing.Dict[builtins.str, typing.Any]]]] = None,
    description: typing.Optional[builtins.str] = None,
    provisioned_concurrent_executions: typing.Optional[jsii.Number] = None,
    max_event_age: typing.Optional[_Duration_070aa057] = None,
    on_failure: typing.Optional[_IDestination_7f253ff1] = None,
    on_success: typing.Optional[_IDestination_7f253ff1] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3e708d1c15730a6c2fcd255240c77016451cdfd8e9e395f1e39b529dacd36d1c(
    source: _IEventSource_7914870e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3feca7ff6d834b38364d8712841b4f39cbb8cae0a5115d0ef68f8d8bb476e29f(
    id: builtins.str,
    *,
    batch_size: typing.Optional[jsii.Number] = None,
    bisect_batch_on_error: typing.Optional[builtins.bool] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_source_arn: typing.Optional[builtins.str] = None,
    kafka_bootstrap_servers: typing.Optional[typing.Sequence[builtins.str]] = None,
    kafka_topic: typing.Optional[builtins.str] = None,
    max_batching_window: typing.Optional[_Duration_070aa057] = None,
    max_record_age: typing.Optional[_Duration_070aa057] = None,
    on_failure: typing.Optional[_IEventSourceDlq_f5ae73e7] = None,
    parallelization_factor: typing.Optional[jsii.Number] = None,
    report_batch_item_failures: typing.Optional[builtins.bool] = None,
    retry_attempts: typing.Optional[jsii.Number] = None,
    source_access_configurations: typing.Optional[typing.Sequence[typing.Union[_SourceAccessConfiguration_afc347bf, typing.Dict[builtins.str, typing.Any]]]] = None,
    starting_position: typing.Optional[_StartingPosition_9192859a] = None,
    tumbling_window: typing.Optional[_Duration_070aa057] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a1aa72530561b6b0097d08918d784e0b8bc4da3fd24bba9088007692c140be6c(
    id: builtins.str,
    *,
    principal: _IPrincipal_93b48231,
    action: typing.Optional[builtins.str] = None,
    event_source_token: typing.Optional[builtins.str] = None,
    function_url_auth_type: typing.Optional[_FunctionUrlAuthType_4cfe7120] = None,
    scope: typing.Optional[_Construct_e78e779f] = None,
    source_account: typing.Optional[builtins.str] = None,
    source_arn: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9107e126cded390da28f1e13def042bcd2eff13fe828755050439488c02bf480(
    statement: _PolicyStatement_296fe8a3,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b214face5a47c4a7e262ee10a0f63c5f7d7f0e130e155481b40b945c21bb3b74(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2cfcf3ca8dd99fe9de9534293ef85b5e406fe3e662ffed4c4ea6f1e27f9dd40a(
    identity: _IGrantable_4c5a91d1,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__62dd7c18ef9616546f36a04ad59c21844b0d11d28f918f8f65066ec977adcfe6(
    metric_name: builtins.str,
    *,
    account: typing.Optional[builtins.str] = None,
    color: typing.Optional[builtins.str] = None,
    dimensions: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    dimensions_map: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    label: typing.Optional[builtins.str] = None,
    period: typing.Optional[_Duration_070aa057] = None,
    region: typing.Optional[builtins.str] = None,
    statistic: typing.Optional[builtins.str] = None,
    unit: typing.Optional[_Unit_113c79f9] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3d927824b42876df5094d27c5f9f48347a33c4f3a00c054ca6fc04e976b45bc(
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
    code: _Code_e8adcb06,
    handler: builtins.str,
    runtime: _Runtime_932d369a,
    stack_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
