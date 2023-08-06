'''
# AWS Lambda Layer with kubectl (and helm)

This module exports a single class called `KubectlLayer` which is a `lambda.Layer` that bundles the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/kubectl/) and the [`helm`](https://helm.sh/) command line.

> * Helm Version: 3.5.4
> * Kubectl Version: 1.20.0

Usage:

```python
# KubectlLayer bundles the 'kubectl' and 'helm' command lines
from monocdk.lambda_layer_kubectl import KubectlLayer

# fn: lambda.Function

fn.add_layers(KubectlLayer(self, "KubectlLayer"))
```

`kubectl` will be installed under `/opt/kubectl/kubectl`, and `helm` will be installed under `/opt/helm/helm`.
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
from ..aws_lambda import LayerVersion as _LayerVersion_34d6006f


class KubectlLayer(
    _LayerVersion_34d6006f,
    metaclass=jsii.JSIIMeta,
    jsii_type="monocdk.lambda_layer_kubectl.KubectlLayer",
):
    '''(experimental) An AWS Lambda layer that includes ``kubectl`` and ``helm``.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        # KubectlLayer bundles the 'kubectl' and 'helm' command lines
        from monocdk.lambda_layer_kubectl import KubectlLayer
        
        # fn: lambda.Function
        
        fn.add_layers(KubectlLayer(self, "KubectlLayer"))
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -

        :stability: experimental
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d959891a2b5b57fac0f58709df70d8838a760860194b3512568998bdcb7c3fd)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "KubectlLayer",
]

publication.publish()

def _typecheckingstub__1d959891a2b5b57fac0f58709df70d8838a760860194b3512568998bdcb7c3fd(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
