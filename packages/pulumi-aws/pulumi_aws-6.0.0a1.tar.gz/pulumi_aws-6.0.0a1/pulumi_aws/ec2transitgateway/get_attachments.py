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
    'GetAttachmentsResult',
    'AwaitableGetAttachmentsResult',
    'get_attachments',
    'get_attachments_output',
]

@pulumi.output_type
class GetAttachmentsResult:
    """
    A collection of values returned by getAttachments.
    """
    def __init__(__self__, filters=None, id=None, ids=None, tags=None):
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAttachmentsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def ids(self) -> Sequence[str]:
        """
        A list of all attachments ids matching the filter. You can retrieve more information about the attachment using the [ec2transitgateway_get_attachment][2] data source, searching by identifier.
        """
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetAttachmentsResult(GetAttachmentsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAttachmentsResult(
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            tags=self.tags)


def get_attachments(filters: Optional[Sequence[pulumi.InputType['GetAttachmentsFilterArgs']]] = None,
                    tags: Optional[Mapping[str, str]] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAttachmentsResult:
    """
    Get information on EC2 Transit Gateway Attachments.

    ## Example Usage


    :param Sequence[pulumi.InputType['GetAttachmentsFilterArgs']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    """
    __args__ = dict()
    __args__['filters'] = filters
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2transitgateway/getAttachments:getAttachments', __args__, opts=opts, typ=GetAttachmentsResult).value

    return AwaitableGetAttachmentsResult(
        filters=__ret__.filters,
        id=__ret__.id,
        ids=__ret__.ids,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_attachments)
def get_attachments_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAttachmentsFilterArgs']]]]] = None,
                           tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAttachmentsResult]:
    """
    Get information on EC2 Transit Gateway Attachments.

    ## Example Usage


    :param Sequence[pulumi.InputType['GetAttachmentsFilterArgs']] filters: One or more configuration blocks containing name-values filters. Detailed below.
    """
    ...
