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
    'GetPromptResult',
    'AwaitableGetPromptResult',
    'get_prompt',
    'get_prompt_output',
]

@pulumi.output_type
class GetPromptResult:
    """
    A collection of values returned by getPrompt.
    """
    def __init__(__self__, arn=None, id=None, instance_id=None, name=None, prompt_id=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if instance_id and not isinstance(instance_id, str):
            raise TypeError("Expected argument 'instance_id' to be a str")
        pulumi.set(__self__, "instance_id", instance_id)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if prompt_id and not isinstance(prompt_id, str):
            raise TypeError("Expected argument 'prompt_id' to be a str")
        pulumi.set(__self__, "prompt_id", prompt_id)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the Prompt.
        """
        return pulumi.get(self, "arn")

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
        return pulumi.get(self, "instance_id")

    @property
    @pulumi.getter
    def name(self) -> str:
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="promptId")
    def prompt_id(self) -> str:
        """
        Identifier for the prompt.
        """
        return pulumi.get(self, "prompt_id")


class AwaitableGetPromptResult(GetPromptResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetPromptResult(
            arn=self.arn,
            id=self.id,
            instance_id=self.instance_id,
            name=self.name,
            prompt_id=self.prompt_id)


def get_prompt(instance_id: Optional[str] = None,
               name: Optional[str] = None,
               opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetPromptResult:
    """
    Provides details about a specific Amazon Connect Prompt.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_prompt(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Beep.wav")
    ```


    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Prompt by name
    """
    __args__ = dict()
    __args__['instanceId'] = instance_id
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:connect/getPrompt:getPrompt', __args__, opts=opts, typ=GetPromptResult).value

    return AwaitableGetPromptResult(
        arn=__ret__.arn,
        id=__ret__.id,
        instance_id=__ret__.instance_id,
        name=__ret__.name,
        prompt_id=__ret__.prompt_id)


@_utilities.lift_output_func(get_prompt)
def get_prompt_output(instance_id: Optional[pulumi.Input[str]] = None,
                      name: Optional[pulumi.Input[str]] = None,
                      opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetPromptResult]:
    """
    Provides details about a specific Amazon Connect Prompt.

    ## Example Usage

    By `name`

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.connect.get_prompt(instance_id="aaaaaaaa-bbbb-cccc-dddd-111111111111",
        name="Beep.wav")
    ```


    :param str instance_id: Reference to the hosting Amazon Connect Instance
    :param str name: Returns information on a specific Prompt by name
    """
    ...
