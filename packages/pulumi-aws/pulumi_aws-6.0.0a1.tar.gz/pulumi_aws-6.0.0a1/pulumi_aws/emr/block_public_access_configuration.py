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

__all__ = ['BlockPublicAccessConfigurationArgs', 'BlockPublicAccessConfiguration']

@pulumi.input_type
class BlockPublicAccessConfigurationArgs:
    def __init__(__self__, *,
                 block_public_security_group_rules: pulumi.Input[bool],
                 permitted_public_security_group_rule_ranges: Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]] = None):
        """
        The set of arguments for constructing a BlockPublicAccessConfiguration resource.
        :param pulumi.Input[bool] block_public_security_group_rules: Enable or disable EMR Block Public Access.
               
               The following arguments are optional:
        :param pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]] permitted_public_security_group_rule_ranges: Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        pulumi.set(__self__, "block_public_security_group_rules", block_public_security_group_rules)
        if permitted_public_security_group_rule_ranges is not None:
            pulumi.set(__self__, "permitted_public_security_group_rule_ranges", permitted_public_security_group_rule_ranges)

    @property
    @pulumi.getter(name="blockPublicSecurityGroupRules")
    def block_public_security_group_rules(self) -> pulumi.Input[bool]:
        """
        Enable or disable EMR Block Public Access.

        The following arguments are optional:
        """
        return pulumi.get(self, "block_public_security_group_rules")

    @block_public_security_group_rules.setter
    def block_public_security_group_rules(self, value: pulumi.Input[bool]):
        pulumi.set(self, "block_public_security_group_rules", value)

    @property
    @pulumi.getter(name="permittedPublicSecurityGroupRuleRanges")
    def permitted_public_security_group_rule_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]:
        """
        Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        return pulumi.get(self, "permitted_public_security_group_rule_ranges")

    @permitted_public_security_group_rule_ranges.setter
    def permitted_public_security_group_rule_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]):
        pulumi.set(self, "permitted_public_security_group_rule_ranges", value)


@pulumi.input_type
class _BlockPublicAccessConfigurationState:
    def __init__(__self__, *,
                 block_public_security_group_rules: Optional[pulumi.Input[bool]] = None,
                 permitted_public_security_group_rule_ranges: Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]] = None):
        """
        Input properties used for looking up and filtering BlockPublicAccessConfiguration resources.
        :param pulumi.Input[bool] block_public_security_group_rules: Enable or disable EMR Block Public Access.
               
               The following arguments are optional:
        :param pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]] permitted_public_security_group_rule_ranges: Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        if block_public_security_group_rules is not None:
            pulumi.set(__self__, "block_public_security_group_rules", block_public_security_group_rules)
        if permitted_public_security_group_rule_ranges is not None:
            pulumi.set(__self__, "permitted_public_security_group_rule_ranges", permitted_public_security_group_rule_ranges)

    @property
    @pulumi.getter(name="blockPublicSecurityGroupRules")
    def block_public_security_group_rules(self) -> Optional[pulumi.Input[bool]]:
        """
        Enable or disable EMR Block Public Access.

        The following arguments are optional:
        """
        return pulumi.get(self, "block_public_security_group_rules")

    @block_public_security_group_rules.setter
    def block_public_security_group_rules(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "block_public_security_group_rules", value)

    @property
    @pulumi.getter(name="permittedPublicSecurityGroupRuleRanges")
    def permitted_public_security_group_rule_ranges(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]:
        """
        Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        return pulumi.get(self, "permitted_public_security_group_rule_ranges")

    @permitted_public_security_group_rule_ranges.setter
    def permitted_public_security_group_rule_ranges(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]):
        pulumi.set(self, "permitted_public_security_group_rule_ranges", value)


class BlockPublicAccessConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_public_security_group_rules: Optional[pulumi.Input[bool]] = None,
                 permitted_public_security_group_rule_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]] = None,
                 __props__=None):
        """
        Resource for managing an AWS EMR block public access configuration. This region level security configuration restricts the launch of EMR clusters that have associated security groups permitting public access on unspecified ports. See the [EMR Block Public Access Configuration](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-block-public-access.html) documentation for further information.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example", block_public_security_group_rules=True)
        ```
        ### Default Configuration

        By default, each AWS region is equipped with a block public access configuration that prevents EMR clusters from being launched if they have security group rules permitting public access on any port except for port 22. The default configuration can be managed using this resource.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example",
            block_public_security_group_rules=True,
            permitted_public_security_group_rule_ranges=[aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                max_range=22,
                min_range=22,
            )])
        ```

        > **NOTE:** If an `emr.BlockPublicAccessConfiguration` resource is destroyed, the configuration will reset to this default configuration.
        ### Multiple Permitted Public Security Group Rule Ranges

        The resource permits specification of multiple `permitted_public_security_group_rule_range` blocks.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example",
            block_public_security_group_rules=True,
            permitted_public_security_group_rule_ranges=[
                aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                    max_range=22,
                    min_range=22,
                ),
                aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                    max_range=101,
                    min_range=100,
                ),
            ])
        ```
        ### Disabling Block Public Access

        To permit EMR clusters to be launched in the configured region regardless of associated security group rules, the Block Public Access feature can be disabled using this resource.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example", block_public_security_group_rules=False)
        ```

        ## Import

        The current EMR Block Public Access Configuration can be imported, e.g.,

        ```sh
         $ pulumi import aws:emr/blockPublicAccessConfiguration:BlockPublicAccessConfiguration example current
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] block_public_security_group_rules: Enable or disable EMR Block Public Access.
               
               The following arguments are optional:
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]] permitted_public_security_group_rule_ranges: Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BlockPublicAccessConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Resource for managing an AWS EMR block public access configuration. This region level security configuration restricts the launch of EMR clusters that have associated security groups permitting public access on unspecified ports. See the [EMR Block Public Access Configuration](https://docs.aws.amazon.com/emr/latest/ManagementGuide/emr-block-public-access.html) documentation for further information.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example", block_public_security_group_rules=True)
        ```
        ### Default Configuration

        By default, each AWS region is equipped with a block public access configuration that prevents EMR clusters from being launched if they have security group rules permitting public access on any port except for port 22. The default configuration can be managed using this resource.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example",
            block_public_security_group_rules=True,
            permitted_public_security_group_rule_ranges=[aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                max_range=22,
                min_range=22,
            )])
        ```

        > **NOTE:** If an `emr.BlockPublicAccessConfiguration` resource is destroyed, the configuration will reset to this default configuration.
        ### Multiple Permitted Public Security Group Rule Ranges

        The resource permits specification of multiple `permitted_public_security_group_rule_range` blocks.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example",
            block_public_security_group_rules=True,
            permitted_public_security_group_rule_ranges=[
                aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                    max_range=22,
                    min_range=22,
                ),
                aws.emr.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs(
                    max_range=101,
                    min_range=100,
                ),
            ])
        ```
        ### Disabling Block Public Access

        To permit EMR clusters to be launched in the configured region regardless of associated security group rules, the Block Public Access feature can be disabled using this resource.

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.emr.BlockPublicAccessConfiguration("example", block_public_security_group_rules=False)
        ```

        ## Import

        The current EMR Block Public Access Configuration can be imported, e.g.,

        ```sh
         $ pulumi import aws:emr/blockPublicAccessConfiguration:BlockPublicAccessConfiguration example current
        ```

        :param str resource_name: The name of the resource.
        :param BlockPublicAccessConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BlockPublicAccessConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 block_public_security_group_rules: Optional[pulumi.Input[bool]] = None,
                 permitted_public_security_group_rule_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BlockPublicAccessConfigurationArgs.__new__(BlockPublicAccessConfigurationArgs)

            if block_public_security_group_rules is None and not opts.urn:
                raise TypeError("Missing required property 'block_public_security_group_rules'")
            __props__.__dict__["block_public_security_group_rules"] = block_public_security_group_rules
            __props__.__dict__["permitted_public_security_group_rule_ranges"] = permitted_public_security_group_rule_ranges
        super(BlockPublicAccessConfiguration, __self__).__init__(
            'aws:emr/blockPublicAccessConfiguration:BlockPublicAccessConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            block_public_security_group_rules: Optional[pulumi.Input[bool]] = None,
            permitted_public_security_group_rule_ranges: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]]] = None) -> 'BlockPublicAccessConfiguration':
        """
        Get an existing BlockPublicAccessConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] block_public_security_group_rules: Enable or disable EMR Block Public Access.
               
               The following arguments are optional:
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRangeArgs']]]] permitted_public_security_group_rule_ranges: Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BlockPublicAccessConfigurationState.__new__(_BlockPublicAccessConfigurationState)

        __props__.__dict__["block_public_security_group_rules"] = block_public_security_group_rules
        __props__.__dict__["permitted_public_security_group_rule_ranges"] = permitted_public_security_group_rule_ranges
        return BlockPublicAccessConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="blockPublicSecurityGroupRules")
    def block_public_security_group_rules(self) -> pulumi.Output[bool]:
        """
        Enable or disable EMR Block Public Access.

        The following arguments are optional:
        """
        return pulumi.get(self, "block_public_security_group_rules")

    @property
    @pulumi.getter(name="permittedPublicSecurityGroupRuleRanges")
    def permitted_public_security_group_rule_ranges(self) -> pulumi.Output[Optional[Sequence['outputs.BlockPublicAccessConfigurationPermittedPublicSecurityGroupRuleRange']]]:
        """
        Configuration block for defining permitted public security group rule port ranges. Can be defined multiple times per resource. Only valid if `block_public_security_group_rules` is set to `true`.
        """
        return pulumi.get(self, "permitted_public_security_group_rule_ranges")

