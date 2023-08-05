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
    'GetReceivedLicensesResult',
    'AwaitableGetReceivedLicensesResult',
    'get_received_licenses',
    'get_received_licenses_output',
]

@pulumi.output_type
class GetReceivedLicensesResult:
    """
    A collection of values returned by getReceivedLicenses.
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
        List of all the license ARNs found.
        """
        return pulumi.get(self, "arns")

    @property
    @pulumi.getter
    def filters(self) -> Optional[Sequence['outputs.GetReceivedLicensesFilterResult']]:
        return pulumi.get(self, "filters")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")


class AwaitableGetReceivedLicensesResult(GetReceivedLicensesResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetReceivedLicensesResult(
            arns=self.arns,
            filters=self.filters,
            id=self.id)


def get_received_licenses(filters: Optional[Sequence[pulumi.InputType['GetReceivedLicensesFilterArgs']]] = None,
                          opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetReceivedLicensesResult:
    """
    This resource can be used to get a set of license ARNs matching a filter.

    ## Example Usage

    The following shows getting all license ARNs issued from the AWS marketplace. Providing no filter, would provide all license ARNs for the entire account.

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.licensemanager.get_received_licenses(filters=[aws.licensemanager.GetReceivedLicensesFilterArgs(
        name="IssuerName",
        values=["AWS/Marketplace"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetReceivedLicensesFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    __args__ = dict()
    __args__['filters'] = filters
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:licensemanager/getReceivedLicenses:getReceivedLicenses', __args__, opts=opts, typ=GetReceivedLicensesResult).value

    return AwaitableGetReceivedLicensesResult(
        arns=__ret__.arns,
        filters=__ret__.filters,
        id=__ret__.id)


@_utilities.lift_output_func(get_received_licenses)
def get_received_licenses_output(filters: Optional[pulumi.Input[Optional[Sequence[pulumi.InputType['GetReceivedLicensesFilterArgs']]]]] = None,
                                 opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetReceivedLicensesResult]:
    """
    This resource can be used to get a set of license ARNs matching a filter.

    ## Example Usage

    The following shows getting all license ARNs issued from the AWS marketplace. Providing no filter, would provide all license ARNs for the entire account.

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.licensemanager.get_received_licenses(filters=[aws.licensemanager.GetReceivedLicensesFilterArgs(
        name="IssuerName",
        values=["AWS/Marketplace"],
    )])
    ```


    :param Sequence[pulumi.InputType['GetReceivedLicensesFilterArgs']] filters: Custom filter block as described below.
           
           More complex filters can be expressed using one or more `filter` sub-blocks,
           which take the following arguments:
    """
    ...
