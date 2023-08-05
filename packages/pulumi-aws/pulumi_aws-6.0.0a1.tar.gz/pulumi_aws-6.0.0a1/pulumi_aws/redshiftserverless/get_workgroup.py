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
    'GetWorkgroupResult',
    'AwaitableGetWorkgroupResult',
    'get_workgroup',
    'get_workgroup_output',
]

@pulumi.output_type
class GetWorkgroupResult:
    """
    A collection of values returned by getWorkgroup.
    """
    def __init__(__self__, arn=None, endpoints=None, enhanced_vpc_routing=None, id=None, namespace_name=None, publicly_accessible=None, security_group_ids=None, subnet_ids=None, workgroup_id=None, workgroup_name=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if endpoints and not isinstance(endpoints, list):
            raise TypeError("Expected argument 'endpoints' to be a list")
        pulumi.set(__self__, "endpoints", endpoints)
        if enhanced_vpc_routing and not isinstance(enhanced_vpc_routing, bool):
            raise TypeError("Expected argument 'enhanced_vpc_routing' to be a bool")
        pulumi.set(__self__, "enhanced_vpc_routing", enhanced_vpc_routing)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if namespace_name and not isinstance(namespace_name, str):
            raise TypeError("Expected argument 'namespace_name' to be a str")
        pulumi.set(__self__, "namespace_name", namespace_name)
        if publicly_accessible and not isinstance(publicly_accessible, bool):
            raise TypeError("Expected argument 'publicly_accessible' to be a bool")
        pulumi.set(__self__, "publicly_accessible", publicly_accessible)
        if security_group_ids and not isinstance(security_group_ids, list):
            raise TypeError("Expected argument 'security_group_ids' to be a list")
        pulumi.set(__self__, "security_group_ids", security_group_ids)
        if subnet_ids and not isinstance(subnet_ids, list):
            raise TypeError("Expected argument 'subnet_ids' to be a list")
        pulumi.set(__self__, "subnet_ids", subnet_ids)
        if workgroup_id and not isinstance(workgroup_id, str):
            raise TypeError("Expected argument 'workgroup_id' to be a str")
        pulumi.set(__self__, "workgroup_id", workgroup_id)
        if workgroup_name and not isinstance(workgroup_name, str):
            raise TypeError("Expected argument 'workgroup_name' to be a str")
        pulumi.set(__self__, "workgroup_name", workgroup_name)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name (ARN) of the Redshift Serverless Workgroup.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def endpoints(self) -> Sequence['outputs.GetWorkgroupEndpointResult']:
        """
        The endpoint that is created from the workgroup. See `Endpoint` below.
        """
        return pulumi.get(self, "endpoints")

    @property
    @pulumi.getter(name="enhancedVpcRouting")
    def enhanced_vpc_routing(self) -> bool:
        """
        The value that specifies whether to turn on enhanced virtual private cloud (VPC) routing, which forces Amazon Redshift Serverless to route traffic through your VPC instead of over the internet.
        """
        return pulumi.get(self, "enhanced_vpc_routing")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="namespaceName")
    def namespace_name(self) -> str:
        return pulumi.get(self, "namespace_name")

    @property
    @pulumi.getter(name="publiclyAccessible")
    def publicly_accessible(self) -> bool:
        """
        A value that specifies whether the workgroup can be accessed from a public network.
        """
        return pulumi.get(self, "publicly_accessible")

    @property
    @pulumi.getter(name="securityGroupIds")
    def security_group_ids(self) -> Sequence[str]:
        """
        An array of security group IDs to associate with the workgroup.
        """
        return pulumi.get(self, "security_group_ids")

    @property
    @pulumi.getter(name="subnetIds")
    def subnet_ids(self) -> Sequence[str]:
        """
        An array of VPC subnet IDs to associate with the workgroup. When set, must contain at least three subnets spanning three Availability Zones. A minimum number of IP addresses is required and scales with the Base Capacity. For more information, see the following [AWS document](https://docs.aws.amazon.com/redshift/latest/mgmt/serverless-known-issues.html).
        """
        return pulumi.get(self, "subnet_ids")

    @property
    @pulumi.getter(name="workgroupId")
    def workgroup_id(self) -> str:
        """
        The Redshift Workgroup ID.
        """
        return pulumi.get(self, "workgroup_id")

    @property
    @pulumi.getter(name="workgroupName")
    def workgroup_name(self) -> str:
        return pulumi.get(self, "workgroup_name")


class AwaitableGetWorkgroupResult(GetWorkgroupResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetWorkgroupResult(
            arn=self.arn,
            endpoints=self.endpoints,
            enhanced_vpc_routing=self.enhanced_vpc_routing,
            id=self.id,
            namespace_name=self.namespace_name,
            publicly_accessible=self.publicly_accessible,
            security_group_ids=self.security_group_ids,
            subnet_ids=self.subnet_ids,
            workgroup_id=self.workgroup_id,
            workgroup_name=self.workgroup_name)


def get_workgroup(workgroup_name: Optional[str] = None,
                  opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetWorkgroupResult:
    """
    Data source for managing an AWS Redshift Serverless Workgroup.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.redshiftserverless.get_workgroup(workgroup_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str workgroup_name: The name of the workgroup associated with the database.
    """
    __args__ = dict()
    __args__['workgroupName'] = workgroup_name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:redshiftserverless/getWorkgroup:getWorkgroup', __args__, opts=opts, typ=GetWorkgroupResult).value

    return AwaitableGetWorkgroupResult(
        arn=__ret__.arn,
        endpoints=__ret__.endpoints,
        enhanced_vpc_routing=__ret__.enhanced_vpc_routing,
        id=__ret__.id,
        namespace_name=__ret__.namespace_name,
        publicly_accessible=__ret__.publicly_accessible,
        security_group_ids=__ret__.security_group_ids,
        subnet_ids=__ret__.subnet_ids,
        workgroup_id=__ret__.workgroup_id,
        workgroup_name=__ret__.workgroup_name)


@_utilities.lift_output_func(get_workgroup)
def get_workgroup_output(workgroup_name: Optional[pulumi.Input[str]] = None,
                         opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetWorkgroupResult]:
    """
    Data source for managing an AWS Redshift Serverless Workgroup.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.redshiftserverless.get_workgroup(workgroup_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str workgroup_name: The name of the workgroup associated with the database.
    """
    ...
