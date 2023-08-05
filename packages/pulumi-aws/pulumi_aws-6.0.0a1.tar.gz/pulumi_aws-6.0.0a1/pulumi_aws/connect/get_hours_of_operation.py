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
    'GetHoursOfOperationResult',
    'AwaitableGetHoursOfOperationResult',
    'get_hours_of_operation',
    'get_hours_of_operation_output',
]

@pulumi.output_type
class GetHoursOfOperationResult:
    """
    A collection of values returned by getHoursOfOperation.
    """
    def __init__(__self__, arn=None, configs=None, description=None, hours_of_operation_id=None, id=None, instance_id=None, name=None, tags=None, time_zone=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if configs and not isinstance(configs, list):
            raise TypeError("Expected argument 'configs' to be a list")
        pulumi.set(__self__, "configs", configs)
        if description and not isinstance(description, str):
            raise TypeError("Expected argument 'description' to be a str")
        pulumi.set(__self__, "description", description)
        if hours_of_operation_id and not isinstance(hours_of_operation_id, str):
            raise TypeError("Expected argument 'hours_of_operation_id' to be a str")
        pulumi.set(__self__, "hours_of_operation_id", hours_of_operation_id)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if tags and not isinstance(tags, dict):
            raise TypeError("Expected argument 'tags' to be a dict")
        pulumi.set(__self__, "tags", tags)
        if time_zone and not isinstance(time_zone, str):
            raise TypeError("Expected argument 'time_zone' to be a str")
        pulumi.set(__self__, "time_zone", time_zone)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Hours of Operation.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter
    def configs(self) -> Sequence['outputs.GetHoursOfOperationConfigResult']:
        """
        Configuration information for the hours of operation: day, start time, and end time . Config blocks are documented below. Config blocks are documented below.
        """
        return pulumi.get(self, "configs")

    @property
    @pulumi.getter
    def description(self) -> str:
        """
        Description of the Hours of Operation.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter(name="hoursOfOperationId")
    def hours_of_operation_id(self) -> str:
        """
        The identifier for the hours of operation.
        """
        return pulumi.get(self, "hours_of_operation_id")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="instanceId")
    def instance_id(self) -> str:
        """
        Identifier of the hosting Amazon Connect Instance.
        """
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the Hours of Operation.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def tags(self) -> Mapping[str, str]:
        """
        Map of tags to assign to the Hours of Operation.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="timeZone")
    def time_zone(self) -> str:
        """
        Time zone of the Hours of Operation.
        """
        return pulumi.get(self, "time_zone")


class AwaitableGetHoursOfOperationResult(GetHoursOfOperationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetHoursOfOperationResult(
            arn=self.arn,
            configs=self.configs,
            description=self.description,
            hours_of_operation_id=self.hours_of_operation_id,
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            tags=self.tags,
            time_zone=self.time_zone)


def get_hours_of_operation(hours_of_operation_id: Optional[str] = None,
                           instance_id: Optional[str] = None,
                           name: Optional[str] = None,
                           tags: Optional[Mapping[str, str]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetHoursOfOperationResult:
    """
    Provides details about a specific Amazon Connect Hours of Operation.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.connect.get_hours_of_operation(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Test")
    ```

    By `hours_of_operation_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.connect.get_hours_of_operation(hours_of_operation_id="cccccccc-bbbb-cccc-dddd-111111111111",
        instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111")
    ```


    :param str hours_of_operation_id: Returns information on a specific Hours of Operation by hours of operation id
    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Hours of Operation by name
    :param Mapping[str, str] tags: Map of tags to assign to the Hours of Operation.
    """
    __args__ = dict()
    __args__['hoursOfOperationId'] = hours_of_operation_id
    __args__['instanceId'] = instance_id
    __args__['name'] = name
    __args__['tags'] = tags
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:connect/getHoursOfOperation:getHoursOfOperation', __args__, opts=opts, typ=GetHoursOfOperationResult).value

    return AwaitableGetHoursOfOperationResult(
        arn=__ret__.arn,
        configs=__ret__.configs,
        description=__ret__.description,
        hours_of_operation_id=__ret__.hours_of_operation_id,
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        name=__ret__.name,
        tags=__ret__.tags,
        time_zone=__ret__.time_zone)


@_utilities.lift_output_func(get_hours_of_operation)
def get_hours_of_operation_output(hours_of_operation_id: Optional[pulumi.Input[Optional[str]]] = None,
                                  instance_id: Optional[pulumi.Input[str]] = None,
                                  name: Optional[pulumi.Input[Optional[str]]] = None,
                                  tags: Optional[pulumi.Input[Optional[Mapping[str, str]]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetHoursOfOperationResult]:
    """
    Provides details about a specific Amazon Connect Hours of Operation.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.connect.get_hours_of_operation(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Test")
    ```

    By `hours_of_operation_id`

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.connect.get_hours_of_operation(hours_of_operation_id="cccccccc-bbbb-cccc-dddd-111111111111",
        instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111")
    ```


    :param str hours_of_operation_id: Returns information on a specific Hours of Operation by hours of operation id
    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Hours of Operation by name
    :param Mapping[str, str] tags: Map of tags to assign to the Hours of Operation.
    """
    ...
