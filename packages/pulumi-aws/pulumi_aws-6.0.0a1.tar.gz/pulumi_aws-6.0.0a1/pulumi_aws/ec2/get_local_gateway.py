# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities
from . import outputs
from ._inputs import *

__all__ = [
    'GetLocalGatewayResult',
    'AwaitableGetLocalGatewayResult',
    'get_local_gateway',
    'get_local_gateway_output',
]

@pulumi.output_type
class GetLocalGatewayResult:
    """
    A collection of values returned by getLocalGateway.
    """
    def __init__(__self__, filters=None, id=None, outpost_arn=None, owner_id=None, state=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if outpost_arn and not isinstance(outpost_arn, str):
            raise TypeError("Expected argument 'outpost_arn' to be a str")
        pulumi.set(__self__, "outpost_arn", outpost_arn)
        if owner_id and not isinstance(owner_id, str):
            raise TypeError("Expected argument 'owner_id' to be a str")
        pulumi.set(__self__, "owner_id", owner_id)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetLocalGatewayFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="outpostArn")
    def outpost_arn(self) -> str:
        """
        ARN of Outpost
        """
        return pulumi.get(self, "outpost_arn")

    @property
    @pulumi.getter(name="ownerId")
    def owner_id(self) -> str:
        """
        AWS account identifier that owns the Local Gateway.
        """
        return pulumi.get(self, "owner_id")

    @property
    @pulumi.getter
    def state(self) -> str:
        """
        State of the local gateway.
        """
        return pulumi.get(self, "state")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetLocalGatewayResult(GetLocalGatewayResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLocalGatewayResult(
            filters=self.filters,
            id=self.id,
            outpost_arn=self.outpost_arn,
            owner_id=self.owner_id,
            state=self.state,
            tags=self.tags)


def get_local_gateway(filters: Optional[Sequence[pulumi.InputType['GetLocalGatewayFilterArgs']]] = None,
                      id: Optional[str] = None,
                      state: Optional[str] = None,
                      tags: Optional[Mapping[str, str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLocalGatewayResult:
    """
    Provides details about an EC2 Local Gateway.

    ## Example Usage

    The following example shows how one might accept a local gateway id as a variable.

    ```python
    import pulumi
    import pulumi_aws as aws

    config = pulumi.Config()
    local_gateway_id = config.require_object("localGatewayId")
    selected = aws.ec2.get_local_gateway(id=local_gateway_id)
    ```


    :param Sequence[pulumi.InputType['GetLocalGatewayFilterArgs']] filters: Custom filter block as described below.
    :param str id: Id of the specific Local Gateway to retrieve.
    :param str state: Current state of the desired Local Gateway.
           Can be either `"pending"` or `"available"`.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired Local Gateway.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['id'] = id
    __args__['state'] = state
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getLocalGateway:getLocalGateway', __args__, opts=opts, typ=GetLocalGatewayResult).value

    return AwaitableGetLocalGatewayResult(
        filters=__ret__.filters,
        id=__ret__.id,
        outpost_arn=__ret__.outpost_arn,
        owner_id=__ret__.owner_id,
        state=__ret__.state,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_local_gateway)
def get_local_gateway_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetLocalGatewayFilterArgs']]]]] = None,
                             id: Optional[pulumi.Input[Optional[str]]] = None,
                             state: Optional[pulumi.Input[Optional[str]]] = None,
                             tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLocalGatewayResult]:
    """
    Provides details about an EC2 Local Gateway.

    ## Example Usage

    The following example shows how one might accept a local gateway id as a variable.

    ```python
    import pulumi
    import pulumi_aws as aws

    config = pulumi.Config()
    local_gateway_id = config.require_object("localGatewayId")
    selected = aws.ec2.get_local_gateway(id=local_gateway_id)
    ```


    :param Sequence[pulumi.InputType['GetLocalGatewayFilterArgs']] filters: Custom filter block as described below.
    :param str id: Id of the specific Local Gateway to retrieve.
    :param str state: Current state of the desired Local Gateway.
           Can be either `"pending"` or `"available"`.
    :param Mapping[str, str] tags: Mapping of tags, each pair of which must exactly match
           a pair on the desired Local Gateway.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    ...
