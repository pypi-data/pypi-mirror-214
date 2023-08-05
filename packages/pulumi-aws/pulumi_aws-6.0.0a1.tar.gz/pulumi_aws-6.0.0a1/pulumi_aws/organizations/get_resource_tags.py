# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = [
    'GetResourceTagsResult',
    'AwaitableGetResourceTagsResult',
    'get_resource_tags',
    'get_resource_tags_output',
]

@pulumi.output_type
class GetResourceTagsResult:
    """
    A collection of values returned by getResourceTags.
    """
    def __init__(__self__, id=None, resource_id=None, tags=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if resource_id and not isinstance(resource_id, str):
            raise TypeError("Expected argument 'resource_id' to be a str")
        pulumi.set(__self__, "resource_id", resource_id)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> str:
        return pulumi.get(self, "resource_id")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of key=value pairs for each tag set on the resource.
        """
        return pulumi.get(self, "tags")


class AwaitableGetResourceTagsResult(GetResourceTagsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetResourceTagsResult(
            id=self.id,
            resource_id=self.resource_id,
            tags=self.tags)


def get_resource_tags(resource_id: Optional[str] = None,
                      tags: Optional[Mapping[str, str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetResourceTagsResult:
    """
    Get tags attached to the specified AWS Organizations resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    account = aws.organizations.get_resource_tags(resource_id="123456123846")
    ```


    :param str resource_id: ID of the resource with the tags to list. See details below.
    :param Mapping[str, str] tags: Map of key=value pairs for each tag set on the resource.
    """
    __args__ = dict()
    __args__['resourceId'] = resource_id
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:organizations/getResourceTags:getResourceTags', __args__, opts=opts, typ=GetResourceTagsResult).value

    return AwaitableGetResourceTagsResult(
        id=__ret__.id,
        resource_id=__ret__.resource_id,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_resource_tags)
def get_resource_tags_output(resource_id: Optional[pulumi.Input[str]] = None,
                             tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetResourceTagsResult]:
    """
    Get tags attached to the specified AWS Organizations resource.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    account = aws.organizations.get_resource_tags(resource_id="123456123846")
    ```


    :param str resource_id: ID of the resource with the tags to list. See details below.
    :param Mapping[str, str] tags: Map of key=value pairs for each tag set on the resource.
    """
    ...
