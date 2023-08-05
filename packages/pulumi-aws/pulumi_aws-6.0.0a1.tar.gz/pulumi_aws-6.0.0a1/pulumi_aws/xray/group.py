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

__all__ = ['GroupArgs', 'Group']

@pulumi.input_type
class GroupArgs:
    def __init__(__self__, *,
                 filter_expression: pulumi.Input[str],
                 group_name: pulumi.Input[str],
                 insights_configuration: Optional[pulumi.Input['GroupInsightsConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Group resource.
        :param pulumi.Input[str] filter_expression: The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        :param pulumi.Input[str] group_name: The name of the group.
        :param pulumi.Input['GroupInsightsConfigurationArgs'] insights_configuration: Configuration options for enabling insights.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        pulumi.set(__self__, "filter_expression", filter_expression)
        pulumi.set(__self__, "group_name", group_name)
        if insights_configuration is not None:
            pulumi.set(__self__, "insights_configuration", insights_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="filterExpression")
    def filter_expression(self) -> pulumi.Input[str]:
        """
        The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        """
        return pulumi.get(self, "filter_expression")

    @filter_expression.setter
    def filter_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "filter_expression", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Input[str]:
        """
        The name of the group.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="insightsConfiguration")
    def insights_configuration(self) -> Optional[pulumi.Input['GroupInsightsConfigurationArgs']]:
        """
        Configuration options for enabling insights.
        """
        return pulumi.get(self, "insights_configuration")

    @insights_configuration.setter
    def insights_configuration(self, value: Optional[pulumi.Input['GroupInsightsConfigurationArgs']]):
        pulumi.set(self, "insights_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _GroupState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 filter_expression: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 insights_configuration: Optional[pulumi.Input['GroupInsightsConfigurationArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Group resources.
        :param pulumi.Input[str] arn: The ARN of the Group.
        :param pulumi.Input[str] filter_expression: The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        :param pulumi.Input[str] group_name: The name of the group.
        :param pulumi.Input['GroupInsightsConfigurationArgs'] insights_configuration: Configuration options for enabling insights.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if filter_expression is not None:
            pulumi.set(__self__, "filter_expression", filter_expression)
        if group_name is not None:
            pulumi.set(__self__, "group_name", group_name)
        if insights_configuration is not None:
            pulumi.set(__self__, "insights_configuration", insights_configuration)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The ARN of the Group.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="filterExpression")
    def filter_expression(self) -> Optional[pulumi.Input[str]]:
        """
        The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        """
        return pulumi.get(self, "filter_expression")

    @filter_expression.setter
    def filter_expression(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_expression", value)

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the group.
        """
        return pulumi.get(self, "group_name")

    @group_name.setter
    def group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "group_name", value)

    @property
    @pulumi.getter(name="insightsConfiguration")
    def insights_configuration(self) -> Optional[pulumi.Input['GroupInsightsConfigurationArgs']]:
        """
        Configuration options for enabling insights.
        """
        return pulumi.get(self, "insights_configuration")

    @insights_configuration.setter
    def insights_configuration(self, value: Optional[pulumi.Input['GroupInsightsConfigurationArgs']]):
        pulumi.set(self, "insights_configuration", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Group(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filter_expression: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 insights_configuration: Optional[pulumi.Input[pulumi.InputType['GroupInsightsConfigurationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Creates and manages an AWS XRay Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.xray.Group("example",
            filter_expression="responsetime > 5",
            group_name="example",
            insights_configuration=aws.xray.GroupInsightsConfigurationArgs(
                insights_enabled=True,
                notifications_enabled=True,
            ))
        ```

        ## Import

        XRay Groups can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:xray/group:Group example arn:aws:xray:us-west-2:1234567890:group/example-group/TNGX7SW5U6QY36T4ZMOUA3HVLBYCZTWDIOOXY3CJAXTHSS3YCWUA
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] filter_expression: The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        :param pulumi.Input[str] group_name: The name of the group.
        :param pulumi.Input[pulumi.InputType['GroupInsightsConfigurationArgs']] insights_configuration: Configuration options for enabling insights.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: GroupArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Creates and manages an AWS XRay Group.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.xray.Group("example",
            filter_expression="responsetime > 5",
            group_name="example",
            insights_configuration=aws.xray.GroupInsightsConfigurationArgs(
                insights_enabled=True,
                notifications_enabled=True,
            ))
        ```

        ## Import

        XRay Groups can be imported using the ARN, e.g.,

        ```sh
         $ pulumi import aws:xray/group:Group example arn:aws:xray:us-west-2:1234567890:group/example-group/TNGX7SW5U6QY36T4ZMOUA3HVLBYCZTWDIOOXY3CJAXTHSS3YCWUA
        ```

        :param str resource_name: The name of the resource.
        :param GroupArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(GroupArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 filter_expression: Optional[pulumi.Input[str]] = None,
                 group_name: Optional[pulumi.Input[str]] = None,
                 insights_configuration: Optional[pulumi.Input[pulumi.InputType['GroupInsightsConfigurationArgs']]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = GroupArgs.__new__(GroupArgs)

            if filter_expression is None and not opts.urn:
                raise TypeError("Missing required property 'filter_expression'")
            __props__.__dict__["filter_expression"] = filter_expression
            if group_name is None and not opts.urn:
                raise TypeError("Missing required property 'group_name'")
            __props__.__dict__["group_name"] = group_name
            __props__.__dict__["insights_configuration"] = insights_configuration
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Group, __self__).__init__(
            'aws:xray/group:Group',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            filter_expression: Optional[pulumi.Input[str]] = None,
            group_name: Optional[pulumi.Input[str]] = None,
            insights_configuration: Optional[pulumi.Input[pulumi.InputType['GroupInsightsConfigurationArgs']]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Group':
        """
        Get an existing Group resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The ARN of the Group.
        :param pulumi.Input[str] filter_expression: The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        :param pulumi.Input[str] group_name: The name of the group.
        :param pulumi.Input[pulumi.InputType['GroupInsightsConfigurationArgs']] insights_configuration: Configuration options for enabling insights.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _GroupState.__new__(_GroupState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["filter_expression"] = filter_expression
        __props__.__dict__["group_name"] = group_name
        __props__.__dict__["insights_configuration"] = insights_configuration
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Group(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The ARN of the Group.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="filterExpression")
    def filter_expression(self) -> pulumi.Output[str]:
        """
        The filter expression defining criteria by which to group traces. more info can be found in official [docs](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-filters.html).
        """
        return pulumi.get(self, "filter_expression")

    @property
    @pulumi.getter(name="groupName")
    def group_name(self) -> pulumi.Output[str]:
        """
        The name of the group.
        """
        return pulumi.get(self, "group_name")

    @property
    @pulumi.getter(name="insightsConfiguration")
    def insights_configuration(self) -> pulumi.Output['outputs.GroupInsightsConfiguration']:
        """
        Configuration options for enabling insights.
        """
        return pulumi.get(self, "insights_configuration")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Key-value mapping of resource tags. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

