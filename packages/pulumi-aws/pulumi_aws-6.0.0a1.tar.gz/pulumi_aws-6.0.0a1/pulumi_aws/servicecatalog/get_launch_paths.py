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
    'GetLaunchPathsResult',
    'AwaitableGetLaunchPathsResult',
    'get_launch_paths',
    'get_launch_paths_output',
]

@pulumi.output_type
class GetLaunchPathsResult:
    """
    A collection of values returned by getLaunchPaths.
    """
    def __init__(__self__, accept_language=None, id=None, product_id=None, summaries=None):
        if accept_language and not isinstance(accept_language, str):
            raise TypeError("Expected argument 'accept_language' to be a str")
        pulumi.set(__self__, "accept_language", accept_language)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if product_id and not isinstance(product_id, str):
            raise TypeError("Expected argument 'product_id' to be a str")
        pulumi.set(__self__, "product_id", product_id)
        if summaries and not isinstance(summaries, list):
            raise TypeError("Expected argument 'summaries' to be a list")
        pulumi.set(__self__, "summaries", summaries)

    @property
    @pulumi.getter(name="acceptLanguage")
    def accept_language(self) -> Optional[str]:
        return pulumi.get(self, "accept_language")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="productId")
    def product_id(self) -> str:
        return pulumi.get(self, "product_id")

    @property
    @pulumi.getter
    def summaries(self) -> Sequence['outputs.GetLaunchPathsSummaryResult']:
        """
        Block with information about the launch path. See details below.
        """
        return pulumi.get(self, "summaries")


class AwaitableGetLaunchPathsResult(GetLaunchPathsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLaunchPathsResult(
            accept_language=self.accept_language,
            id=self.id,
            product_id=self.product_id,
            summaries=self.summaries)


def get_launch_paths(accept_language: Optional[str] = None,
                     product_id: Optional[str] = None,
                     opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLaunchPathsResult:
    """
    Lists the paths to the specified product. A path is how the user has access to a specified product, and is necessary when provisioning a product. A path also determines the constraints put on the product.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_launch_paths(product_id="prod-yakog5pdriver")
    ```


    :param str accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
    :param str product_id: Product identifier.
           
           The following arguments are optional:
    """
    __args__ = dict()
    __args__['acceptLanguage'] = accept_language
    __args__['productId'] = product_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:servicecatalog/getLaunchPaths:getLaunchPaths', __args__, opts=opts, typ=GetLaunchPathsResult).value

    return AwaitableGetLaunchPathsResult(
        accept_language=__ret__.accept_language,
        id=__ret__.id,
        product_id=__ret__.product_id,
        summaries=__ret__.summaries)


@_utilities.lift_output_func(get_launch_paths)
def get_launch_paths_output(accept_language: Optional[pulumi.Input[Optional[str]]] = None,
                            product_id: Optional[pulumi.Input[str]] = None,
                            opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLaunchPathsResult]:
    """
    Lists the paths to the specified product. A path is how the user has access to a specified product, and is necessary when provisioning a product. A path also determines the constraints put on the product.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.servicecatalog.get_launch_paths(product_id="prod-yakog5pdriver")
    ```


    :param str accept_language: Language code. Valid values: `en` (English), `jp` (Japanese), `zh` (Chinese). Default value is `en`.
    :param str product_id: Product identifier.
           
           The following arguments are optional:
    """
    ...
