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
    'GetAmiIdsResult',
    'AwaitableGetAmiIdsResult',
    'get_ami_ids',
    'get_ami_ids_output',
]

@pulumi.output_type
class GetAmiIdsResult:
    """
    A collection of values returned by getAmiIds.
    """
    def __init__(__self__, executable_users=None, filters=None, id=None, ids=None, include_deprecated=None, name_regex=None, owners=None, sort_ascending=None):
        if executable_users and not isinstance(executable_users, list):
            raise TypeError("Expected argument 'executable_users' to be a list")
        pulumi.set(__self__, "executable_users", executable_users)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if ids and not isinstance(ids, list):
            raise TypeError("Expected argument 'ids' to be a list")
        pulumi.set(__self__, "ids", ids)
        if include_deprecated and not isinstance(include_deprecated, bool):
            raise TypeError("Expected argument 'include_deprecated' to be a bool")
        pulumi.set(__self__, "include_deprecated", include_deprecated)
        if name_regex and not isinstance(name_regex, str):
            raise TypeError("Expected argument 'name_regex' to be a str")
        pulumi.set(__self__, "name_regex", name_regex)
        if owners and not isinstance(owners, list):
            raise TypeError("Expected argument 'owners' to be a list")
        pulumi.set(__self__, "owners", owners)
        if sort_ascending and not isinstance(sort_ascending, bool):
            raise TypeError("Expected argument 'sort_ascending' to be a bool")
        pulumi.set(__self__, "sort_ascending", sort_ascending)

    @property
    @pulumi.getter(name="executableUsers")
    def executable_users(self) -> Optional[Sequence[str]]:
        return pulumi.get(self, "executable_users")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetAmiIdsFilterResult']]:
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
        return pulumi.get(self, "ids")

    @property
    @pulumi.getter(name="includeDeprecated")
    def include_deprecated(self) -> Optional[bool]:
        return pulumi.get(self, "include_deprecated")

    @property
    @pulumi.getter(name="nameRegex")
    def name_regex(self) -> Optional[str]:
        return pulumi.get(self, "name_regex")

    @property
    @pulumi.getter
    def owners(self) -> Sequence[str]:
        return pulumi.get(self, "owners")

    @property
    @pulumi.getter(name="sortAscending")
    def sort_ascending(self) -> Optional[bool]:
        return pulumi.get(self, "sort_ascending")


class AwaitableGetAmiIdsResult(GetAmiIdsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAmiIdsResult(
            executable_users=self.executable_users,
            filters=self.filters,
            id=self.id,
            ids=self.ids,
            include_deprecated=self.include_deprecated,
            name_regex=self.name_regex,
            owners=self.owners,
            sort_ascending=self.sort_ascending)


def get_ami_ids(executable_users: Optional[Sequence[str]] = None,
                filters: Optional[Sequence[pulumi.InputType['GetAmiIdsFilterArgs']]] = None,
                include_deprecated: Optional[bool] = None,
                name_regex: Optional[str] = None,
                owners: Optional[Sequence[str]] = None,
                sort_ascending: Optional[bool] = None,
                opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAmiIdsResult:
    """
    Use this data source to get a list of AMI IDs matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ubuntu = aws.ec2.get_ami_ids(filters=[aws.ec2.GetAmiIdsFilterArgs(
            name="name",
            values=["ubuntu/images/ubuntu-*-*-amd64-server-*"],
        )],
        owners=["099720109477"])
    ```


    :param Sequence[str] executable_users: Limit search to users with *explicit* launch
           permission on  the image. Valid items are the numeric account ID or `self`.
    :param Sequence[pulumi.InputType['GetAmiIdsFilterArgs']] filters: One or more name/value pairs to filter off of. There
           are several valid keys, for a full reference, check out
           [describe-images in the AWS CLI reference][1].
    :param bool include_deprecated: If true, all deprecated AMIs are included in the response.
           If false, no deprecated AMIs are included in the response. If no value is specified, the default value is `false`.
    :param str name_regex: Regex string to apply to the AMI list returned
           by AWS. This allows more advanced filtering not supported from the AWS API.
           This filtering is done locally on what AWS returns, and could have a performance
           impact if the result is large. Combine this with other
           options to narrow down the list AWS returns.
    :param Sequence[str] owners: List of AMI owners to limit search. At least 1 value must be specified. Valid values: an AWS account ID, `self` (the current account), or an AWS owner alias (e.g., `amazon`, `aws-marketplace`, `microsoft`).
    :param bool sort_ascending: Used to sort AMIs by creation time.
           If no value is specified, the default value is `false`.
    """
    __args__ = dict()
    __args__['executableUsers'] = executable_users
    __args__['filters'] = filters
    __args__['includeDeprecated'] = include_deprecated
    __args__['nameRegex'] = name_regex
    __args__['owners'] = owners
    __args__['sortAscending'] = sort_ascending
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getAmiIds:getAmiIds', __args__, opts=opts, typ=GetAmiIdsResult).value

    return AwaitableGetAmiIdsResult(
        executable_users=__ret__.executable_users,
        filters=__ret__.filters,
        id=__ret__.id,
        ids=__ret__.ids,
        include_deprecated=__ret__.include_deprecated,
        name_regex=__ret__.name_regex,
        owners=__ret__.owners,
        sort_ascending=__ret__.sort_ascending)


@_utilities.lift_output_func(get_ami_ids)
def get_ami_ids_output(executable_users: Optional[pulumi.Input[Optional[Sequence[str]]]] = None,
                       filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetAmiIdsFilterArgs']]]]] = None,
                       include_deprecated: Optional[pulumi.Input[Optional[bool]]] = None,
                       name_regex: Optional[pulumi.Input[Optional[str]]] = None,
                       owners: Optional[pulumi.Input[Sequence[str]]] = None,
                       sort_ascending: Optional[pulumi.Input[Optional[bool]]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAmiIdsResult]:
    """
    Use this data source to get a list of AMI IDs matching the specified criteria.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ubuntu = aws.ec2.get_ami_ids(filters=[aws.ec2.GetAmiIdsFilterArgs(
            name="name",
            values=["ubuntu/images/ubuntu-*-*-amd64-server-*"],
        )],
        owners=["099720109477"])
    ```


    :param Sequence[str] executable_users: Limit search to users with *explicit* launch
           permission on  the image. Valid items are the numeric account ID or `self`.
    :param Sequence[pulumi.InputType['GetAmiIdsFilterArgs']] filters: One or more name/value pairs to filter off of. There
           are several valid keys, for a full reference, check out
           [describe-images in the AWS CLI reference][1].
    :param bool include_deprecated: If true, all deprecated AMIs are included in the response.
           If false, no deprecated AMIs are included in the response. If no value is specified, the default value is `false`.
    :param str name_regex: Regex string to apply to the AMI list returned
           by AWS. This allows more advanced filtering not supported from the AWS API.
           This filtering is done locally on what AWS returns, and could have a performance
           impact if the result is large. Combine this with other
           options to narrow down the list AWS returns.
    :param Sequence[str] owners: List of AMI owners to limit search. At least 1 value must be specified. Valid values: an AWS account ID, `self` (the current account), or an AWS owner alias (e.g., `amazon`, `aws-marketplace`, `microsoft`).
    :param bool sort_ascending: Used to sort AMIs by creation time.
           If no value is specified, the default value is `false`.
    """
    ...
