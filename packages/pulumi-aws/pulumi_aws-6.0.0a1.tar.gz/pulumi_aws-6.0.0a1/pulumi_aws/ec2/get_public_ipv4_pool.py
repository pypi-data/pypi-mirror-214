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

__all__ = [
    'GetPublicIpv4PoolResult',
    'AwaitableGetPublicIpv4PoolResult',
    'get_public_ipv4_pool',
    'get_public_ipv4_pool_output',
]

@pulumi.output_type
class GetPublicIpv4PoolResult:
    """
    A collection of values returned by getPublicIpv4Pool.
    """
    def __init__(__self__, description=None, id=None, network_border_group=None, pool_address_ranges=None, pool_id=None, tags=None, total_address_count=None, total_available_address_count=None):
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if network_border_group and not isinstance(network_border_group, str):
            raise TypeError("Expected argument 'network_border_group' to be a str")
        pulumi.set(__self__, "network_border_group", network_border_group)
        if pool_address_ranges and not isinstance(pool_address_ranges, list):
            raise TypeError("Expected argument 'pool_address_ranges' to be a list")
        pulumi.set(__self__, "pool_address_ranges", pool_address_ranges)
        if pool_id and not isinstance(pool_id, str):
            raise TypeError("Expected argument 'pool_id' to be a str")
        pulumi.set(__self__, "pool_id", pool_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if total_address_count and not isinstance(total_address_count, int):
            raise TypeError("Expected argument 'total_address_count' to be a int")
        pulumi.set(__self__, "total_address_count", total_address_count)
        if total_available_address_count and not isinstance(total_available_address_count, int):
            raise TypeError("Expected argument 'total_available_address_count' to be a int")
        pulumi.set(__self__, "total_available_address_count", total_available_address_count)

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the pool, if any.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="networkBorderGroup")
    def network_border_group(self) -> str:
        """
        Name of the location from which the address pool is advertised.
        * pool_address_ranges` - List of Address Ranges in the Pool; each address range record contains:
        """
        return pulumi.get(self, "network_border_group")

    @property
    @pulumi.getter(name="poolAddressRanges")
    def pool_address_ranges(self) -> Sequence['outputs.GetPublicIpv4PoolPoolAddressRangeResult']:
        return pulumi.get(self, "pool_address_ranges")

    @property
    @pulumi.getter(name="poolId")
    def pool_id(self) -> str:
        return pulumi.get(self, "pool_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Any tags for the address pool.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="totalAddressCount")
    def total_address_count(self) -> int:
        """
        Total number of addresses in the pool.
        """
        return pulumi.get(self, "total_address_count")

    @property
    @pulumi.getter(name="totalAvailableAddressCount")
    def total_available_address_count(self) -> int:
        """
        Total number of available addresses in the pool.
        """
        return pulumi.get(self, "total_available_address_count")


class AwaitableGetPublicIpv4PoolResult(GetPublicIpv4PoolResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPublicIpv4PoolResult(
            description=self.description,
            id=self.id,
            network_border_group=self.network_border_group,
            pool_address_ranges=self.pool_address_ranges,
            pool_id=self.pool_id,
            tags=self.tags,
            total_address_count=self.total_address_count,
            total_available_address_count=self.total_available_address_count)


def get_public_ipv4_pool(pool_id: Optional[str] = None,
                         tags: Optional[Mapping[str, str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPublicIpv4PoolResult:
    """
    Provides details about a specific AWS EC2 Public IPv4 Pool.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_public_ipv4_pool(pool_id="ipv4pool-ec2-000df99cff0c1ec10")
    ```


    :param str pool_id: AWS resource IDs of a public IPv4 pool (as a string) for which this data source will fetch detailed information.
    :param Mapping[str, str] tags: Any tags for the address pool.
    """
    __args__ = dict()
    __args__['poolId'] = pool_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getPublicIpv4Pool:getPublicIpv4Pool', __args__, opts=opts, typ=GetPublicIpv4PoolResult).value

    return AwaitableGetPublicIpv4PoolResult(
        description=__ret__.description,
        id=__ret__.id,
        network_border_group=__ret__.network_border_group,
        pool_address_ranges=__ret__.pool_address_ranges,
        pool_id=__ret__.pool_id,
        tags=__ret__.tags,
        total_address_count=__ret__.total_address_count,
        total_available_address_count=__ret__.total_available_address_count)


@_utilities.lift_output_func(get_public_ipv4_pool)
def get_public_ipv4_pool_output(pool_id: Optional[pulumi.Input[str]] = None,
                                tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPublicIpv4PoolResult]:
    """
    Provides details about a specific AWS EC2 Public IPv4 Pool.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.ec2.get_public_ipv4_pool(pool_id="ipv4pool-ec2-000df99cff0c1ec10")
    ```


    :param str pool_id: AWS resource IDs of a public IPv4 pool (as a string) for which this data source will fetch detailed information.
    :param Mapping[str, str] tags: Any tags for the address pool.
    """
    ...
