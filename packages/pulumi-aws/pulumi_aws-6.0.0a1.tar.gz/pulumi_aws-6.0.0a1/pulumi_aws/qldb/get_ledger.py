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
    'GetLedgerResult',
    'AwaitableGetLedgerResult',
    'get_ledger',
    'get_ledger_output',
]

@pulumi.output_type
class GetLedgerResult:
    """
    A collection of values returned by getLedger.
    """
    def __init__(__self__, arn=None, deletion_protection=None, id=None, kms_key=None, name=None, permissions_mode=None, tags=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if deletion_protection and not isinstance(deletion_protection, bool):
            raise TypeError("Expected argument 'deletion_protection' to be a bool")
        pulumi.set(__self__, "deletion_protection", deletion_protection)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if kms_key and not isinstance(kms_key, str):
            raise TypeError("Expected argument 'kms_key' to be a str")
        pulumi.set(__self__, "kms_key", kms_key)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if permissions_mode and not isinstance(permissions_mode, str):
            raise TypeError("Expected argument 'permissions_mode' to be a str")
        pulumi.set(__self__, "permissions_mode", permissions_mode)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def arn(self) -> str:
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="deletionProtection")
    def deletion_protection(self) -> bool:
        return pulumi.get(self, "deletion_protection")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="kmsKey")
    def kms_key(self) -> str:
        return pulumi.get(self, "kms_key")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="permissionsMode")
    def permissions_mode(self) -> str:
        return pulumi.get(self, "permissions_mode")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        return pulumi.get(self, "tags")


class AwaitableGetLedgerResult(GetLedgerResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLedgerResult(
            arn=self.arn,
            deletion_protection=self.deletion_protection,
            id=self.id,
            kms_key=self.kms_key,
            name=self.name,
            permissions_mode=self.permissions_mode,
            tags=self.tags)


def get_ledger(name: Optional[str] = None,
               tags: Optional[Mapping[str, str]] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLedgerResult:
    """
    Use this data source to fetch information about a Quantum Ledger Database.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.qldb.get_ledger(name="an_example_ledger")
    ```


    :param str name: Friendly name of the ledger to match.
    """
    __args__ = dict()
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:qldb/getLedger:getLedger', __args__, opts=opts, typ=GetLedgerResult).value

    return AwaitableGetLedgerResult(
        arn=__ret__.arn,
        deletion_protection=__ret__.deletion_protection,
        id=__ret__.id,
        kms_key=__ret__.kms_key,
        name=__ret__.name,
        permissions_mode=__ret__.permissions_mode,
        tags=__ret__.tags)


@_utilities.lift_output_func(get_ledger)
def get_ledger_output(name: Optional[pulumi.Input[str]] = None,
                      tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLedgerResult]:
    """
    Use this data source to fetch information about a Quantum Ledger Database.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.qldb.get_ledger(name="an_example_ledger")
    ```


    :param str name: Friendly name of the ledger to match.
    """
    ...
