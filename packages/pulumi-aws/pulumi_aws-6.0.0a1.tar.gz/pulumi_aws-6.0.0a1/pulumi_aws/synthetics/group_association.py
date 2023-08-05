# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['GroupAssociationArgs', 'GroupAssociation']

@pulumi.input_type
class GroupAssociationArgs:
    def __init__(__self__, *,
                 canary_arn: pulumi.Input[str],
                 group_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a GroupAssociation resource.
        :param pulumi.Input[str] canary_arn: ARN of the canary.
        :param pulumi.Input[str] group_name: Name of the group that the canary will be associated with.
        """
        pulumi.set(__self__, "canary_arn", canary_arn)
        pulumi.set(__self__, "group_name", group_name)

    @property
    @pulumi.getter(name="canaryArn")
    def canary_arn(self) -> pulumi.Input[str]:
        """
        ARN of the canary.
        """
        return pulumi.get(self, "canary_arn")

    @canary_arn.setter
    def canary_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "canary_arn", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Input[str]:
        """
        Name of the group that the canary will be associated with.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_name", value)


@pulumi.input_type
class _GroupAssociationState:
    def __init__(__self__, *,
                 canary_arn: Optional[pulumi.Input[str]] = None,
                 group_arn: Optional[pulumi.Input[str]] = None,
                 group_id: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering GroupAssociation resources.
        :param pulumi.Input[str] canary_arn: ARN of the canary.
        :param pulumi.Input[str] group_id: ID of the Group.
        :param pulumi.Input[str] group_name: Name of the group that the canary will be associated with.
        """
        if canary_arn is not None:
            pulumi.set(__self__, "canary_arn", canary_arn)
        if group_arn is not None:
            pulumi.set(__self__, "group_arn", group_arn)
        if group_id is not None:
            pulumi.set(__self__, "group_id", group_id)
        if group_name is not None:
            pulumi.set(__self__, "group_name", group_name)

    @property
    @pulumi.getter(name="canaryArn")
    def canary_arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the canary.
        """
        return pulumi.get(self, "canary_arn")

    @canary_arn.setter
    def canary_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "canary_arn", value)

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> Optional[pulumi.Input[str]]:
        return pulumi.get(self, "group_arn")

    @group_arn.setter
    def group_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_arn", value)

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the Group.
        """
        return pulumi.get(self, "group_id")

    @group_id.setter
    def group_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_id", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the group that the canary will be associated with.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_name", value)


class GroupAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 canary_arn: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a Synthetics Group Association resource.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.synthetics.GroupAssociation("example",
            group_name=aws_synthetics_group["example"]["name"],
            canary_arn=aws_synthetics_canary["example"]["arn"])
        ```

        ## Import

        CloudWatch Synthetics Group Association can be imported in the form `canary_arn,group_name`, e.g.,

        ```sh
         $ pulumi import aws:synthetics/groupAssociation:GroupAssociation example arn:aws:synthetics:us-west-2:123456789012:canary:tf-acc-test-abcd1234,examplename
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] canary_arn: ARN of the canary.
        :param pulumi.Input[str] group_name: Name of the group that the canary will be associated with.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GroupAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a Synthetics Group Association resource.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.synthetics.GroupAssociation("example",
            group_name=aws_synthetics_group["example"]["name"],
            canary_arn=aws_synthetics_canary["example"]["arn"])
        ```

        ## Import

        CloudWatch Synthetics Group Association can be imported in the form `canary_arn,group_name`, e.g.,

        ```sh
         $ pulumi import aws:synthetics/groupAssociation:GroupAssociation example arn:aws:synthetics:us-west-2:123456789012:canary:tf-acc-test-abcd1234,examplename
        ```

        :param str resource_name: The name of the resource.
        :param GroupAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 canary_arn: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupAssociationArgs.__new__(GroupAssociationArgs)

            if canary_arn is None and not opts.urn:
                raise TypeError("Missing required property 'canary_arn'")
            __props__.__dict__["canary_arn"] = canary_arn
            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__.__dict__["group_name"] = group_name
            __props__.__dict__["group_arn"] = None
            __props__.__dict__["group_id"] = None
        super(GroupAssociation, __self__).__init__(
            'aws:synthetics/groupAssociation:GroupAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            canary_arn: Optional[pulumi.Input[str]] = None,
            group_arn: Optional[pulumi.Input[str]] = None,
            group_id: Optional[pulumi.Input[str]] = None,
            group_name: Optional[pulumi.Input[str]] = None) -> 'GroupAssociation':
        """
        Get an existing GroupAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] canary_arn: ARN of the canary.
        :param pulumi.Input[str] group_id: ID of the Group.
        :param pulumi.Input[str] group_name: Name of the group that the canary will be associated with.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupAssociationState.__new__(_GroupAssociationState)

        __props__.__dict__["canary_arn"] = canary_arn
        __props__.__dict__["group_arn"] = group_arn
        __props__.__dict__["group_id"] = group_id
        __props__.__dict__["group_name"] = group_name
        return GroupAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="canaryArn")
    def canary_arn(self) -> pulumi.Output[str]:
        """
        ARN of the canary.
        """
        return pulumi.get(self, "canary_arn")

    @property
    @pulumi.getter(name="groupArn")
    def group_arn(self) -> pulumi.Output[str]:
        return pulumi.get(self, "group_arn")

    @property
    @pulumi.getter(name="groupId")
    def group_id(self) -> pulumi.Output[str]:
        """
        ID of the Group.
        """
        return pulumi.get(self, "group_id")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Output[str]:
        """
        Name of the group that the canary will be associated with.
        """
        return pulumi.get(self, "group_name")

