'''
# AWS APIGatewayv2 Integrations

## Table of Contents

* [HTTP APIs](#http-apis)

  * [Lambda Integration](#lambda)
  * [HTTP Proxy Integration](#http-proxy)
  * [Private Integration](#private-integration)
  * [Request Parameters](#request-parameters)
* [WebSocket APIs](#websocket-apis)

  * [Lambda WebSocket Integration](#lambda-websocket-integration)

## HTTP APIs

Integrations connect a route to backend resources. HTTP APIs support Lambda proxy, AWS service, and HTTP proxy integrations. HTTP proxy integrations are also known as private integrations.

### Lambda

Lambda integrations enable integrating an HTTP API route with a Lambda function. When a client invokes the route, the
API Gateway service forwards the request to the Lambda function and returns the function's response to the client.

The API Gateway service will invoke the lambda function with an event payload of a specific format. The service expects
the function to respond in a specific format. The details on this format is available at [Working with AWS Lambda
proxy integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html).

The following code configures a route `GET /books` with a Lambda proxy integration.

```python
from monocdk.aws_apigatewayv2_integrations import HttpLambdaIntegration

# books_default_fn: lambda.Function

books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### HTTP Proxy

HTTP Proxy integrations enables connecting an HTTP API route to a publicly routable HTTP endpoint. When a client
invokes the route, the API Gateway service forwards the entire request and response between the API Gateway endpoint
and the integrating HTTP endpoint. More information can be found at [Working with HTTP proxy
integrations](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-http.html).

The following code configures a route `GET /books` with an HTTP proxy integration to an HTTP endpoint
`get-books-proxy.myproxy.internal`.

```python
from monocdk.aws_apigatewayv2_integrations import HttpUrlIntegration


books_integration = HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal")

http_api = apigwv2.HttpApi(self, "HttpApi")

http_api.add_routes(
    path="/books",
    methods=[apigwv2.HttpMethod.GET],
    integration=books_integration
)
```

### Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

The following integrations are supported for private resources in a VPC.

#### Application Load Balancer

The following code is a basic application load balancer private integration of HTTP API:

```python
from monocdk.aws_apigatewayv2_integrations import HttpAlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.ApplicationLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpAlbIntegration`.

#### Network Load Balancer

The following code is a basic network load balancer private integration of HTTP API:

```python
from monocdk.aws_apigatewayv2_integrations import HttpNlbIntegration


vpc = ec2.Vpc(self, "VPC")
lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpNlbIntegration("DefaultIntegration", listener)
)
```

When an imported load balancer is used, the `vpc` option must be specified for `HttpNlbIntegration`.

#### Cloud Map Service Discovery

The following code is a basic discovery service private integration of HTTP API:

```python
import monocdk as servicediscovery
from monocdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration


vpc = ec2.Vpc(self, "VPC")
vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
    name="boobar.com",
    vpc=vpc
)
service = namespace.create_service("Service")

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
        vpc_link=vpc_link
    )
)
```

### Request Parameters

Request parameter mapping allows API requests from clients to be modified before they reach backend integrations.
Parameter mapping can be used to specify modifications to request parameters. See [Transforming API requests and
responses](https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html).

The following example creates a new header - `header2` - as a copy of `header1` and removes `header1`.

```python
from monocdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
    )
)
```

To add mapping keys and values not yet supported by the CDK, use the `custom()` method:

```python
from monocdk.aws_apigatewayv2_integrations import HttpAlbIntegration

# lb: elbv2.ApplicationLoadBalancer

listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegration("DefaultIntegration", listener,
        parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
    )
)
```

## WebSocket APIs

WebSocket integrations connect a route to backend resources. The following integrations are supported in the CDK.

### Lambda WebSocket Integration

Lambda integrations enable integrating a WebSocket API route with a Lambda function. When a client connects/disconnects
or sends message specific to a route, the API Gateway service forwards the request to the Lambda function

The API Gateway service will invoke the lambda function with an event payload of a specific format.

The following code configures a `sendmessage` route with a Lambda integration

```python
from monocdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration

# message_handler: lambda.Function


web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
apigwv2.WebSocketStage(self, "mystage",
    web_socket_api=web_socket_api,
    stage_name="dev",
    auto_deploy=True
)
web_socket_api.add_route("sendmessage",
    integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
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

from .. import Construct as _Construct_e78e779f
from ..aws_apigatewayv2 import (
    HttpConnectionType as _HttpConnectionType_4cd688f4,
    HttpIntegrationType as _HttpIntegrationType_9cef8778,
    HttpMethod as _HttpMethod_53075460,
    HttpRouteIntegration as _HttpRouteIntegration_9615aa8e,
    HttpRouteIntegrationBindOptions as _HttpRouteIntegrationBindOptions_71d720e7,
    HttpRouteIntegrationConfig as _HttpRouteIntegrationConfig_ad0a4b4c,
    IHttpRoute as _IHttpRoute_bfbdc841,
    IVpcLink as _IVpcLink_f701d5cb,
    IWebSocketRoute as _IWebSocketRoute_bcd0851a,
    ParameterMapping as _ParameterMapping_31358964,
    PayloadFormatVersion as _PayloadFormatVersion_63c22993,
    WebSocketRouteIntegration as _WebSocketRouteIntegration_7d6df2bb,
    WebSocketRouteIntegrationBindOptions as _WebSocketRouteIntegrationBindOptions_5b8af65c,
    WebSocketRouteIntegrationConfig as _WebSocketRouteIntegrationConfig_9594a91c,
)
from ..aws_elasticloadbalancingv2 import (
    IApplicationListener as _IApplicationListener_90dffa22,
    INetworkListener as _INetworkListener_d2e2b5dc,
)
from ..aws_lambda import IFunction as _IFunction_6e14f09e
from ..aws_servicediscovery import IService as _IService_66c1fbd2


class HttpAlbIntegration(
    _HttpRouteIntegration_9615aa8e,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpAlbIntegration",
):
    '''(experimental) The Application Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_apigatewayv2_integrations import HttpAlbIntegration
        
        # lb: elbv2.ApplicationLoadBalancer
        
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                parameter_mapping=apigwv2.ParameterMapping().custom("myKey", "myValue")
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: _IApplicationListener_90dffa22,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB application listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bd99b00bd78999091cf4fc9c81ad6880431384783b4a5ef63729c6a1e4b57dfb)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpAlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> _HttpRouteIntegrationConfig_ad0a4b4c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_ad0a4b4c, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_4cd688f4:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_4cd688f4, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_4cd688f4) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b90c5236f653dff0e8971810e36800f60a01fd3f83a72268ef0b9583ad452302)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_53075460:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_53075460, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_53075460) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6d4c220ddaecaaa53e62d501e3cc5cdd3b987087cadd28e1fcb9904602d441ef)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_9cef8778:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_9cef8778, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_9cef8778) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4fc05af87f7fbb9808a75f2c374f2ec428f74e12f4f3456f2a912c837ddce12c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_63c22993:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_63c22993, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_63c22993) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d1fd9b356a45266e33a66c05af873817d2239e70459fc94c9abeff8f5ec56c00)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


class HttpLambdaIntegration(
    _HttpRouteIntegration_9615aa8e,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpLambdaIntegration",
):
    '''(experimental) The Lambda Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_apigatewayv2_integrations import HttpLambdaIntegration
        
        # books_default_fn: lambda.Function
        
        books_integration = HttpLambdaIntegration("BooksIntegration", books_default_fn)
        
        http_api = apigwv2.HttpApi(self, "HttpApi")
        
        http_api.add_routes(
            path="/books",
            methods=[apigwv2.HttpMethod.GET],
            integration=books_integration
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        handler: _IFunction_6e14f09e,
        *,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        payload_format_version: typing.Optional[_PayloadFormatVersion_63c22993] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda handler to integrate with.
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4cba1a32314fbe458793b5e5b89b9a46ba23a02731a2ee50dd9b7f843048a818)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        props = HttpLambdaIntegrationProps(
            parameter_mapping=parameter_mapping,
            payload_format_version=payload_format_version,
        )

        jsii.create(self.__class__, self, [id, handler, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> _HttpRouteIntegrationConfig_ad0a4b4c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_ad0a4b4c, jsii.invoke(self, "bind", [_]))

    @jsii.member(jsii_name="completeBind")
    def _complete_bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> None:
        '''(experimental) Complete the binding of the integration to the route.

        In some cases, there is
        some additional work to do, such as adding permissions for the API to access
        the target. This work is necessary whether the integration has just been
        created for this route or it is an existing one, previously created for other
        routes. In most cases, however, concrete implementations do not need to
        override this method.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(None, jsii.invoke(self, "completeBind", [options]))


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpLambdaIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={
        "parameter_mapping": "parameterMapping",
        "payload_format_version": "payloadFormatVersion",
    },
)
class HttpLambdaIntegrationProps:
    def __init__(
        self,
        *,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        payload_format_version: typing.Optional[_PayloadFormatVersion_63c22993] = None,
    ) -> None:
        '''(experimental) Lambda Proxy integration properties.

        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param payload_format_version: (experimental) Version of the payload sent to the lambda handler. Default: PayloadFormatVersion.VERSION_2_0

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_apigatewayv2 as apigatewayv2
            from monocdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # payload_format_version: apigatewayv2.PayloadFormatVersion
            
            http_lambda_integration_props = apigatewayv2_integrations.HttpLambdaIntegrationProps(
                parameter_mapping=parameter_mapping,
                payload_format_version=payload_format_version
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__844e7f2de93931914c5c083190d29cf915039495b61a7d73caa49bda6027960d)
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument payload_format_version", value=payload_format_version, expected_type=type_hints["payload_format_version"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if payload_format_version is not None:
            self._values["payload_format_version"] = payload_format_version

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    @builtins.property
    def payload_format_version(self) -> typing.Optional[_PayloadFormatVersion_63c22993]:
        '''(experimental) Version of the payload sent to the lambda handler.

        :default: PayloadFormatVersion.VERSION_2_0

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-develop-integrations-lambda.html
        :stability: experimental
        '''
        result = self._values.get("payload_format_version")
        return typing.cast(typing.Optional[_PayloadFormatVersion_63c22993], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpLambdaIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpNlbIntegration(
    _HttpRouteIntegration_9615aa8e,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpNlbIntegration",
):
    '''(experimental) The Network Load Balancer integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_apigatewayv2_integrations import HttpNlbIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        lb = elbv2.NetworkLoadBalancer(self, "lb", vpc=vpc)
        listener = lb.add_listener("listener", port=80)
        listener.add_targets("target",
            port=80
        )
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpNlbIntegration("DefaultIntegration", listener)
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        listener: _INetworkListener_d2e2b5dc,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param listener: the ELB network listener.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__15e2c482cb0e90b4151c8575488e433bee7da5d5dbb4f93d4e0a8a088ab5ff9a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument listener", value=listener, expected_type=type_hints["listener"])
        props = HttpNlbIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, listener, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> _HttpRouteIntegrationConfig_ad0a4b4c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_ad0a4b4c, jsii.invoke(self, "bind", [options]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_4cd688f4:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_4cd688f4, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_4cd688f4) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5a761f935897ded9fffa8c83b7069c1b378fa5e06d63c62c5cead2fd7ed53c19)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_53075460:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_53075460, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_53075460) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b8e645fc1abb05dcf27d549bf7f7c5befddc4a3ebc0303fe6a746533e5dce23b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_9cef8778:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_9cef8778, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_9cef8778) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e67738cd4d0ae8c76c5cc5c86d749464a8db936fd0ccffd97b45a5ace6799ac9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_63c22993:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_63c22993, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_63c22993) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__5fc9abca64a2109f9069ac6454d36aa34048feda7c2df5cb2760dad8e7667784)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpPrivateIntegrationOptions",
    jsii_struct_bases=[],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpPrivateIntegrationOptions:
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''(experimental) Base options for private integration.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_apigatewayv2 as apigatewayv2
            from monocdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_private_integration_options = apigatewayv2_integrations.HttpPrivateIntegrationOptions(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc271eedc02a1c1bc0b586ce39e2875a3aa2674d1b905c6902abc1d1345be34c)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_53075460]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_53075460], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_f701d5cb]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_f701d5cb], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpPrivateIntegrationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpServiceDiscoveryIntegration(
    _HttpRouteIntegration_9615aa8e,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpServiceDiscoveryIntegration",
):
    '''(experimental) The Service Discovery integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        import monocdk as servicediscovery
        from monocdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
        
        
        vpc = ec2.Vpc(self, "VPC")
        vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
        namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
            name="boobar.com",
            vpc=vpc
        )
        service = namespace.create_service("Service")
        
        http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
            default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                vpc_link=vpc_link
            )
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        service: _IService_66c1fbd2,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param service: the service discovery resource to integrate with.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b106205b4bfa30611aa5790b07e7da6886e9bfe07aadcc1afff3e0b7a9e7da39)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument service", value=service, expected_type=type_hints["service"])
        props = HttpServiceDiscoveryIntegrationProps(
            method=method,
            parameter_mapping=parameter_mapping,
            secure_server_name=secure_server_name,
            vpc_link=vpc_link,
        )

        jsii.create(self.__class__, self, [id, service, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> _HttpRouteIntegrationConfig_ad0a4b4c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_ad0a4b4c, jsii.invoke(self, "bind", [_]))

    @builtins.property
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> _HttpConnectionType_4cd688f4:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpConnectionType_4cd688f4, jsii.get(self, "connectionType"))

    @_connection_type.setter
    def _connection_type(self, value: _HttpConnectionType_4cd688f4) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1a54c13c06d2eeb9f96ac15694e85f8ebbb07e33e9bb4c1494190f005d230861)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "connectionType", value)

    @builtins.property
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> _HttpMethod_53075460:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpMethod_53075460, jsii.get(self, "httpMethod"))

    @_http_method.setter
    def _http_method(self, value: _HttpMethod_53075460) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__602640242f629725e4d6db71e15fcdf80234113ccbdaf24bba3cc4e781fbbb78)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "httpMethod", value)

    @builtins.property
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> _HttpIntegrationType_9cef8778:
        '''
        :stability: experimental
        '''
        return typing.cast(_HttpIntegrationType_9cef8778, jsii.get(self, "integrationType"))

    @_integration_type.setter
    def _integration_type(self, value: _HttpIntegrationType_9cef8778) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__76d8100067e9ddffabf9d00d7cb2584d91c994991cc11f21154185aee88818dd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "integrationType", value)

    @builtins.property
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> _PayloadFormatVersion_63c22993:
        '''
        :stability: experimental
        '''
        return typing.cast(_PayloadFormatVersion_63c22993, jsii.get(self, "payloadFormatVersion"))

    @_payload_format_version.setter
    def _payload_format_version(self, value: _PayloadFormatVersion_63c22993) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c95313c2acc5ccd1abb232740bf6dac6871a9b228ef566f97f0785943ebb5d76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpServiceDiscoveryIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpServiceDiscoveryIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpServiceDiscoveryIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            import monocdk as servicediscovery
            from monocdk.aws_apigatewayv2_integrations import HttpServiceDiscoveryIntegration
            
            
            vpc = ec2.Vpc(self, "VPC")
            vpc_link = apigwv2.VpcLink(self, "VpcLink", vpc=vpc)
            namespace = servicediscovery.PrivateDnsNamespace(self, "Namespace",
                name="boobar.com",
                vpc=vpc
            )
            service = namespace.create_service("Service")
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpServiceDiscoveryIntegration("DefaultIntegration", service,
                    vpc_link=vpc_link
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__92aca16ea7eca21b1f408638d80f0c62bdb15f920bef05286178b5bfeb067ffe)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_53075460]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_53075460], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_f701d5cb]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_f701d5cb], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpServiceDiscoveryIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class HttpUrlIntegration(
    _HttpRouteIntegration_9615aa8e,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpUrlIntegration",
):
    '''(experimental) The HTTP Proxy integration resource for HTTP API.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_apigatewayv2_authorizers import HttpLambdaAuthorizer, HttpLambdaResponseType
        from monocdk.aws_apigatewayv2_integrations import HttpUrlIntegration
        
        # This function handles your auth logic
        # auth_handler: lambda.Function
        
        
        authorizer = HttpLambdaAuthorizer("BooksAuthorizer", auth_handler,
            response_types=[HttpLambdaResponseType.SIMPLE]
        )
        
        api = apigwv2.HttpApi(self, "HttpApi")
        
        api.add_routes(
            integration=HttpUrlIntegration("BooksIntegration", "https://get-books-proxy.myproxy.internal"),
            path="/books",
            authorizer=authorizer
        )
    '''

    def __init__(
        self,
        id: builtins.str,
        url: builtins.str,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    ) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param url: the URL to proxy to.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e7bda1858ee232e184c24d7aad52405e1f91707e812af4888ea6648aaf786dd)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument url", value=url, expected_type=type_hints["url"])
        props = HttpUrlIntegrationProps(
            method=method, parameter_mapping=parameter_mapping
        )

        jsii.create(self.__class__, self, [id, url, props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IHttpRoute_bfbdc841,
        scope: _Construct_e78e779f,
    ) -> _HttpRouteIntegrationConfig_ad0a4b4c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        _ = _HttpRouteIntegrationBindOptions_71d720e7(route=route, scope=scope)

        return typing.cast(_HttpRouteIntegrationConfig_ad0a4b4c, jsii.invoke(self, "bind", [_]))


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpUrlIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "parameter_mapping": "parameterMapping"},
)
class HttpUrlIntegrationProps:
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    ) -> None:
        '''(experimental) Properties to initialize a new ``HttpProxyIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_apigatewayv2 as apigatewayv2
            from monocdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            
            http_url_integration_props = apigatewayv2_integrations.HttpUrlIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4db37e19c60c0f1b74f569efa2844135cc815cd3a495ecfb843ae92f8b819413)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_53075460]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_53075460], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpUrlIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class WebSocketLambdaIntegration(
    _WebSocketRouteIntegration_7d6df2bb,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.WebSocketLambdaIntegration",
):
    '''(experimental) Lambda WebSocket Integration.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        from monocdk.aws_apigatewayv2_integrations import WebSocketLambdaIntegration
        
        # message_handler: lambda.Function
        
        
        web_socket_api = apigwv2.WebSocketApi(self, "mywsapi")
        apigwv2.WebSocketStage(self, "mystage",
            web_socket_api=web_socket_api,
            stage_name="dev",
            auto_deploy=True
        )
        web_socket_api.add_route("sendmessage",
            integration=WebSocketLambdaIntegration("SendMessageIntegration", message_handler)
        )
    '''

    def __init__(self, id: builtins.str, handler: _IFunction_6e14f09e) -> None:
        '''
        :param id: id of the underlying integration construct.
        :param handler: the Lambda function handler.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__016e35b48717993d8bfa10c7450a8dd2ad8629e72eecab9d5a737288dfc5433a)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument handler", value=handler, expected_type=type_hints["handler"])
        jsii.create(self.__class__, self, [id, handler])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IWebSocketRoute_bcd0851a,
        scope: _Construct_e78e779f,
    ) -> _WebSocketRouteIntegrationConfig_9594a91c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _WebSocketRouteIntegrationBindOptions_5b8af65c(
            route=route, scope=scope
        )

        return typing.cast(_WebSocketRouteIntegrationConfig_9594a91c, jsii.invoke(self, "bind", [options]))


class WebSocketMockIntegration(
    _WebSocketRouteIntegration_7d6df2bb,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.aws_apigatewayv2_integrations.WebSocketMockIntegration",
):
    '''(experimental) Mock WebSocket Integration.

    :stability: experimental
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        from monocdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
        
        web_socket_mock_integration = apigatewayv2_integrations.WebSocketMockIntegration("id")
    '''

    def __init__(self, id: builtins.str) -> None:
        '''
        :param id: id of the underlying integration construct.

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8ad44d6b41be38e37330d1610a2a4776cd1a4cc6d809b75b23209c16a60e54e)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [id])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: _IWebSocketRoute_bcd0851a,
        scope: _Construct_e78e779f,
    ) -> _WebSocketRouteIntegrationConfig_9594a91c:
        '''(experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``WebSocketRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        '''
        options = _WebSocketRouteIntegrationBindOptions_5b8af65c(
            route=route, scope=scope
        )

        return typing.cast(_WebSocketRouteIntegrationConfig_9594a91c, jsii.invoke(self, "bind", [options]))


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpAlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpAlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpAlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: infused

        Example::

            from monocdk.aws_apigatewayv2_integrations import HttpAlbIntegration
            
            # lb: elbv2.ApplicationLoadBalancer
            
            listener = lb.add_listener("listener", port=80)
            listener.add_targets("target",
                port=80
            )
            
            http_endpoint = apigwv2.HttpApi(self, "HttpProxyPrivateApi",
                default_integration=HttpAlbIntegration("DefaultIntegration", listener,
                    parameter_mapping=apigwv2.ParameterMapping().append_header("header2", apigwv2.MappingValue.request_header("header1")).remove_header("header1")
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b63358382aaa98703448fc92dfd796965db033cdd5173dba5c216e9c2782f8d0)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_53075460]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_53075460], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_f701d5cb]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_f701d5cb], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="monocdk.aws_apigatewayv2_integrations.HttpNlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={
        "method": "method",
        "parameter_mapping": "parameterMapping",
        "secure_server_name": "secureServerName",
        "vpc_link": "vpcLink",
    },
)
class HttpNlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[_HttpMethod_53075460] = None,
        parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
        secure_server_name: typing.Optional[builtins.str] = None,
        vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
    ) -> None:
        '''(experimental) Properties to initialize ``HttpNlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param parameter_mapping: (experimental) Specifies how to transform HTTP requests before sending them to the backend. Default: undefined requests are sent to the backend unmodified
        :param secure_server_name: (experimental) Specifies the server name to verified by HTTPS when calling the backend integration. Default: undefined private integration traffic will use HTTP protocol
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            from monocdk import aws_apigatewayv2 as apigatewayv2
            from monocdk import aws_apigatewayv2_integrations as apigatewayv2_integrations
            
            # parameter_mapping: apigatewayv2.ParameterMapping
            # vpc_link: apigatewayv2.VpcLink
            
            http_nlb_integration_props = apigatewayv2_integrations.HttpNlbIntegrationProps(
                method=apigatewayv2.HttpMethod.ANY,
                parameter_mapping=parameter_mapping,
                secure_server_name="secureServerName",
                vpc_link=vpc_link
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af7c2637628de7cf988be25d117c225a8f7b5bc9dc6367e0e1d1e1b029edf5e2)
            check_type(argname="argument method", value=method, expected_type=type_hints["method"])
            check_type(argname="argument parameter_mapping", value=parameter_mapping, expected_type=type_hints["parameter_mapping"])
            check_type(argname="argument secure_server_name", value=secure_server_name, expected_type=type_hints["secure_server_name"])
            check_type(argname="argument vpc_link", value=vpc_link, expected_type=type_hints["vpc_link"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if parameter_mapping is not None:
            self._values["parameter_mapping"] = parameter_mapping
        if secure_server_name is not None:
            self._values["secure_server_name"] = secure_server_name
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[_HttpMethod_53075460]:
        '''(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        '''
        result = self._values.get("method")
        return typing.cast(typing.Optional[_HttpMethod_53075460], result)

    @builtins.property
    def parameter_mapping(self) -> typing.Optional[_ParameterMapping_31358964]:
        '''(experimental) Specifies how to transform HTTP requests before sending them to the backend.

        :default: undefined requests are sent to the backend unmodified

        :see: https://docs.aws.amazon.com/apigateway/latest/developerguide/http-api-parameter-mapping.html
        :stability: experimental
        '''
        result = self._values.get("parameter_mapping")
        return typing.cast(typing.Optional[_ParameterMapping_31358964], result)

    @builtins.property
    def secure_server_name(self) -> typing.Optional[builtins.str]:
        '''(experimental) Specifies the server name to verified by HTTPS when calling the backend integration.

        :default: undefined private integration traffic will use HTTP protocol

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-apigatewayv2-integration-tlsconfig.html
        :stability: experimental
        '''
        result = self._values.get("secure_server_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def vpc_link(self) -> typing.Optional[_IVpcLink_f701d5cb]:
        '''(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        '''
        result = self._values.get("vpc_link")
        return typing.cast(typing.Optional[_IVpcLink_f701d5cb], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpAlbIntegration",
    "HttpAlbIntegrationProps",
    "HttpLambdaIntegration",
    "HttpLambdaIntegrationProps",
    "HttpNlbIntegration",
    "HttpNlbIntegrationProps",
    "HttpPrivateIntegrationOptions",
    "HttpServiceDiscoveryIntegration",
    "HttpServiceDiscoveryIntegrationProps",
    "HttpUrlIntegration",
    "HttpUrlIntegrationProps",
    "WebSocketLambdaIntegration",
    "WebSocketMockIntegration",
]

publication.publish()

def _typecheckingstub__bd99b00bd78999091cf4fc9c81ad6880431384783b4a5ef63729c6a1e4b57dfb(
    id: builtins.str,
    listener: _IApplicationListener_90dffa22,
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b90c5236f653dff0e8971810e36800f60a01fd3f83a72268ef0b9583ad452302(
    value: _HttpConnectionType_4cd688f4,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6d4c220ddaecaaa53e62d501e3cc5cdd3b987087cadd28e1fcb9904602d441ef(
    value: _HttpMethod_53075460,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4fc05af87f7fbb9808a75f2c374f2ec428f74e12f4f3456f2a912c837ddce12c(
    value: _HttpIntegrationType_9cef8778,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d1fd9b356a45266e33a66c05af873817d2239e70459fc94c9abeff8f5ec56c00(
    value: _PayloadFormatVersion_63c22993,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4cba1a32314fbe458793b5e5b89b9a46ba23a02731a2ee50dd9b7f843048a818(
    id: builtins.str,
    handler: _IFunction_6e14f09e,
    *,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    payload_format_version: typing.Optional[_PayloadFormatVersion_63c22993] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__844e7f2de93931914c5c083190d29cf915039495b61a7d73caa49bda6027960d(
    *,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    payload_format_version: typing.Optional[_PayloadFormatVersion_63c22993] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__15e2c482cb0e90b4151c8575488e433bee7da5d5dbb4f93d4e0a8a088ab5ff9a(
    id: builtins.str,
    listener: _INetworkListener_d2e2b5dc,
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5a761f935897ded9fffa8c83b7069c1b378fa5e06d63c62c5cead2fd7ed53c19(
    value: _HttpConnectionType_4cd688f4,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b8e645fc1abb05dcf27d549bf7f7c5befddc4a3ebc0303fe6a746533e5dce23b(
    value: _HttpMethod_53075460,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e67738cd4d0ae8c76c5cc5c86d749464a8db936fd0ccffd97b45a5ace6799ac9(
    value: _HttpIntegrationType_9cef8778,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5fc9abca64a2109f9069ac6454d36aa34048feda7c2df5cb2760dad8e7667784(
    value: _PayloadFormatVersion_63c22993,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc271eedc02a1c1bc0b586ce39e2875a3aa2674d1b905c6902abc1d1345be34c(
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b106205b4bfa30611aa5790b07e7da6886e9bfe07aadcc1afff3e0b7a9e7da39(
    id: builtins.str,
    service: _IService_66c1fbd2,
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1a54c13c06d2eeb9f96ac15694e85f8ebbb07e33e9bb4c1494190f005d230861(
    value: _HttpConnectionType_4cd688f4,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__602640242f629725e4d6db71e15fcdf80234113ccbdaf24bba3cc4e781fbbb78(
    value: _HttpMethod_53075460,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__76d8100067e9ddffabf9d00d7cb2584d91c994991cc11f21154185aee88818dd(
    value: _HttpIntegrationType_9cef8778,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c95313c2acc5ccd1abb232740bf6dac6871a9b228ef566f97f0785943ebb5d76(
    value: _PayloadFormatVersion_63c22993,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__92aca16ea7eca21b1f408638d80f0c62bdb15f920bef05286178b5bfeb067ffe(
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e7bda1858ee232e184c24d7aad52405e1f91707e812af4888ea6648aaf786dd(
    id: builtins.str,
    url: builtins.str,
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4db37e19c60c0f1b74f569efa2844135cc815cd3a495ecfb843ae92f8b819413(
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__016e35b48717993d8bfa10c7450a8dd2ad8629e72eecab9d5a737288dfc5433a(
    id: builtins.str,
    handler: _IFunction_6e14f09e,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8ad44d6b41be38e37330d1610a2a4776cd1a4cc6d809b75b23209c16a60e54e(
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b63358382aaa98703448fc92dfd796965db033cdd5173dba5c216e9c2782f8d0(
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af7c2637628de7cf988be25d117c225a8f7b5bc9dc6367e0e1d1e1b029edf5e2(
    *,
    method: typing.Optional[_HttpMethod_53075460] = None,
    parameter_mapping: typing.Optional[_ParameterMapping_31358964] = None,
    secure_server_name: typing.Optional[builtins.str] = None,
    vpc_link: typing.Optional[_IVpcLink_f701d5cb] = None,
) -> None:
    """Type checking stubs"""
    pass
