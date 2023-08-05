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
    'GetLicenseGrantsResult',
    'AwaitableGetLicenseGrantsResult',
    'get_license_grants',
    'get_license_grants_output',
]

@pulumi.output_type
class GetLicenseGrantsResult:
    """
    A collection of values returned by getLicenseGrants.
    """
    def __init__(__self__, arns=None, filters=None, id=None):
        if arns and not isinstance(arns, list):
            raise TypeError("Expected argument 'arns' to be a list")
        pulumi.set(__self__, "arns", arns)
        if filters and not isinstance(filters, list):
            raise TypeError("Expected argument 'filters' to be a list")
        pulumi.set(__self__, "filters", filters)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)

    @property
    @pulumi.getter
    def arns(self) -> Sequence[str]:
        """
        List of all the license grant ARNs found.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetLicenseGrantsFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetLicenseGrantsResult(GetLicenseGrantsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLicenseGrantsResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id)


def get_license_grants(filters: Optional[Sequence[pulumi.InputType['GetLicenseGrantsFilterArgs']]] = None,
                       opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLicenseGrantsResult:
    """
    This resource can be used to get a set of license grant ARNs matching a filter.

    ## Example Usage

    The following shows getting all license grant ARNs granted to your account.

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_caller_identity()
    test = aws.licensemanager.get_license_grants(filters=[aws.licensemanager.GetLicenseGrantsFilterArgs(
        name="GranteePrincipalARN",
        values=[f"arn:aws:iam::{current.account_id}:root"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetLicenseGrantsFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:licensemanager/getLicenseGrants:getLicenseGrants', __args__, opts=opts, typ=GetLicenseGrantsResult).value

    return AwaitableGetLicenseGrantsResult(
        arns=__ret__.arns,
        filters=__ret__.filters,
        id=__ret__.id)


@_utilities.lift_output_func(get_license_grants)
def get_license_grants_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetLicenseGrantsFilterArgs']]]]] = None,
                              opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLicenseGrantsResult]:
    """
    This resource can be used to get a set of license grant ARNs matching a filter.

    ## Example Usage

    The following shows getting all license grant ARNs granted to your account.

    ```python
    import pulumi
    import pulumi_aws as aws

    current = aws.get_caller_identity()
    test = aws.licensemanager.get_license_grants(filters=[aws.licensemanager.GetLicenseGrantsFilterArgs(
        name="GranteePrincipalARN",
        values=[f"arn:aws:iam::{current.account_id}:root"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetLicenseGrantsFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    ...
