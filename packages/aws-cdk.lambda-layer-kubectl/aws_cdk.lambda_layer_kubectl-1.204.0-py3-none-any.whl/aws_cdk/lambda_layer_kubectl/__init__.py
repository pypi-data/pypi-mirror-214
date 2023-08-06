'''
# AWS Lambda Layer with kubectl (and helm)

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module exports a single class called `KubectlLayer` which is a `lambda.Layer` that bundles the [`kubectl`](https://kubernetes.io/docs/reference/kubectl/kubectl/) and the [`helm`](https://helm.sh/) command line.

> * Helm Version: 3.5.4
> * Kubectl Version: 1.20.0

Usage:

```python
# KubectlLayer bundles the 'kubectl' and 'helm' command lines
from aws_cdk.lambda_layer_kubectl import KubectlLayer

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

from ._jsii import *

import aws_cdk.aws_lambda as _aws_cdk_aws_lambda_5443dbc3
import constructs as _constructs_77d1e7e8


class KubectlLayer(
    _aws_cdk_aws_lambda_5443dbc3.LayerVersion,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/lambda-layer-kubectl.KubectlLayer",
):
    '''An AWS Lambda layer that includes ``kubectl`` and ``helm``.

    :exampleMetadata: infused

    Example::

        # KubectlLayer bundles the 'kubectl' and 'helm' command lines
        from aws_cdk.lambda_layer_kubectl import KubectlLayer
        
        # fn: lambda.Function
        
        fn.add_layers(KubectlLayer(self, "KubectlLayer"))
    '''

    def __init__(self, scope: _constructs_77d1e7e8.Construct, id: builtins.str) -> None:
        '''
        :param scope: -
        :param id: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3d29e04d890187ad55d8cc0954ff1b96a1fea49f83759e8b912bac3e69a99457)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        jsii.create(self.__class__, self, [scope, id])


__all__ = [
    "KubectlLayer",
]

publication.publish()

def _typecheckingstub__3d29e04d890187ad55d8cc0954ff1b96a1fea49f83759e8b912bac3e69a99457(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
) -> None:
    """Type checking stubs"""
    pass
