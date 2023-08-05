# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['ApplicationArgs', 'Application']

@pulumi.input_type
class ApplicationArgs:
    def __init__(__self__, *,
                 resource_group_name: pulumi.Input[str],
                 auto_config_enabled: Optional[pulumi.Input[bool]] = None,
                 auto_create: Optional[pulumi.Input[bool]] = None,
                 cwe_monitor_enabled: Optional[pulumi.Input[bool]] = None,
                 grouping_type: Optional[pulumi.Input[str]] = None,
                 ops_center_enabled: Optional[pulumi.Input[bool]] = None,
                 ops_item_sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a Application resource.
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
               
               The following arguments are optional:
        :param pulumi.Input[bool] auto_config_enabled: Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        :param pulumi.Input[bool] auto_create: Configures all of the resources in the resource group by applying the recommended configurations.
        :param pulumi.Input[bool] cwe_monitor_enabled: Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        :param pulumi.Input[str] grouping_type: Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        :param pulumi.Input[bool] ops_center_enabled: When set to `true`, creates opsItems for any problems detected on an application.
        :param pulumi.Input[str] ops_item_sns_topic_arn: SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "resource_group_name", resource_group_name)
        if auto_config_enabled is not None:
            pulumi.set(__self__, "auto_config_enabled", auto_config_enabled)
        if auto_create is not None:
            pulumi.set(__self__, "auto_create", auto_create)
        if cwe_monitor_enabled is not None:
            pulumi.set(__self__, "cwe_monitor_enabled", cwe_monitor_enabled)
        if grouping_type is not None:
            pulumi.set(__self__, "grouping_type", grouping_type)
        if ops_center_enabled is not None:
            pulumi.set(__self__, "ops_center_enabled", ops_center_enabled)
        if ops_item_sns_topic_arn is not None:
            pulumi.set(__self__, "ops_item_sns_topic_arn", ops_item_sns_topic_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Input[str]:
        """
        Name of the resource group.

        The following arguments are optional:
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter(name="autoConfigEnabled")
    def auto_config_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        """
        return pulumi.get(self, "auto_config_enabled")

    @auto_config_enabled.setter
    def auto_config_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_config_enabled", value)

    @property
    @pulumi.getter(name="autoCreate")
    def auto_create(self) -> Optional[pulumi.Input[bool]]:
        """
        Configures all of the resources in the resource group by applying the recommended configurations.
        """
        return pulumi.get(self, "auto_create")

    @auto_create.setter
    def auto_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_create", value)

    @property
    @pulumi.getter(name="cweMonitorEnabled")
    def cwe_monitor_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        """
        return pulumi.get(self, "cwe_monitor_enabled")

    @cwe_monitor_enabled.setter
    def cwe_monitor_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cwe_monitor_enabled", value)

    @property
    @pulumi.getter(name="groupingType")
    def grouping_type(self) -> Optional[pulumi.Input[str]]:
        """
        Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        """
        return pulumi.get(self, "grouping_type")

    @grouping_type.setter
    def grouping_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "grouping_type", value)

    @property
    @pulumi.getter(name="opsCenterEnabled")
    def ops_center_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set to `true`, creates opsItems for any problems detected on an application.
        """
        return pulumi.get(self, "ops_center_enabled")

    @ops_center_enabled.setter
    def ops_center_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ops_center_enabled", value)

    @property
    @pulumi.getter(name="opsItemSnsTopicArn")
    def ops_item_sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        """
        return pulumi.get(self, "ops_item_sns_topic_arn")

    @ops_item_sns_topic_arn.setter
    def ops_item_sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ops_item_sns_topic_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _ApplicationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 auto_config_enabled: Optional[pulumi.Input[bool]] = None,
                 auto_create: Optional[pulumi.Input[bool]] = None,
                 cwe_monitor_enabled: Optional[pulumi.Input[bool]] = None,
                 grouping_type: Optional[pulumi.Input[str]] = None,
                 ops_center_enabled: Optional[pulumi.Input[bool]] = None,
                 ops_item_sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering Application resources.
        :param pulumi.Input[str] arn: ARN of the Application.
        :param pulumi.Input[bool] auto_config_enabled: Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        :param pulumi.Input[bool] auto_create: Configures all of the resources in the resource group by applying the recommended configurations.
        :param pulumi.Input[bool] cwe_monitor_enabled: Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        :param pulumi.Input[str] grouping_type: Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        :param pulumi.Input[bool] ops_center_enabled: When set to `true`, creates opsItems for any problems detected on an application.
        :param pulumi.Input[str] ops_item_sns_topic_arn: SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if auto_config_enabled is not None:
            pulumi.set(__self__, "auto_config_enabled", auto_config_enabled)
        if auto_create is not None:
            pulumi.set(__self__, "auto_create", auto_create)
        if cwe_monitor_enabled is not None:
            pulumi.set(__self__, "cwe_monitor_enabled", cwe_monitor_enabled)
        if grouping_type is not None:
            pulumi.set(__self__, "grouping_type", grouping_type)
        if ops_center_enabled is not None:
            pulumi.set(__self__, "ops_center_enabled", ops_center_enabled)
        if ops_item_sns_topic_arn is not None:
            pulumi.set(__self__, "ops_item_sns_topic_arn", ops_item_sns_topic_arn)
        if resource_group_name is not None:
            pulumi.set(__self__, "resource_group_name", resource_group_name)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the Application.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="autoConfigEnabled")
    def auto_config_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        """
        return pulumi.get(self, "auto_config_enabled")

    @auto_config_enabled.setter
    def auto_config_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_config_enabled", value)

    @property
    @pulumi.getter(name="autoCreate")
    def auto_create(self) -> Optional[pulumi.Input[bool]]:
        """
        Configures all of the resources in the resource group by applying the recommended configurations.
        """
        return pulumi.get(self, "auto_create")

    @auto_create.setter
    def auto_create(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "auto_create", value)

    @property
    @pulumi.getter(name="cweMonitorEnabled")
    def cwe_monitor_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        """
        return pulumi.get(self, "cwe_monitor_enabled")

    @cwe_monitor_enabled.setter
    def cwe_monitor_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "cwe_monitor_enabled", value)

    @property
    @pulumi.getter(name="groupingType")
    def grouping_type(self) -> Optional[pulumi.Input[str]]:
        """
        Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        """
        return pulumi.get(self, "grouping_type")

    @grouping_type.setter
    def grouping_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "grouping_type", value)

    @property
    @pulumi.getter(name="opsCenterEnabled")
    def ops_center_enabled(self) -> Optional[pulumi.Input[bool]]:
        """
        When set to `true`, creates opsItems for any problems detected on an application.
        """
        return pulumi.get(self, "ops_center_enabled")

    @ops_center_enabled.setter
    def ops_center_enabled(self, value: Optional[pulumi.Input[bool]]):
        pulumi.set(self, "ops_center_enabled", value)

    @property
    @pulumi.getter(name="opsItemSnsTopicArn")
    def ops_item_sns_topic_arn(self) -> Optional[pulumi.Input[str]]:
        """
        SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        """
        return pulumi.get(self, "ops_item_sns_topic_arn")

    @ops_item_sns_topic_arn.setter
    def ops_item_sns_topic_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "ops_item_sns_topic_arn", value)

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the resource group.

        The following arguments are optional:
        """
        return pulumi.get(self, "resource_group_name")

    @resource_group_name.setter
    def resource_group_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_group_name", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @tags_all.setter
    def tags_all(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags_all", value)


class Application(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_config_enabled: Optional[pulumi.Input[bool]] = None,
                 auto_create: Optional[pulumi.Input[bool]] = None,
                 cwe_monitor_enabled: Optional[pulumi.Input[bool]] = None,
                 grouping_type: Optional[pulumi.Input[str]] = None,
                 ops_center_enabled: Optional[pulumi.Input[bool]] = None,
                 ops_item_sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a ApplicationInsights Application resource.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example_group = aws.resourcegroups.Group("exampleGroup", resource_query=aws.resourcegroups.GroupResourceQueryArgs(
            query=json.dumps({
                "ResourceTypeFilters": ["AWS::EC2::Instance"],
                "TagFilters": [{
                    "Key": "Stage",
                    "Values": ["Test"],
                }],
            }),
        ))
        example_application = aws.applicationinsights.Application("exampleApplication", resource_group_name=example_group.name)
        ```

        ## Import

        ApplicationInsights Applications can be imported using the `resource_group_name`, e.g.,

        ```sh
         $ pulumi import aws:applicationinsights/application:Application some some-application
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[bool] auto_config_enabled: Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        :param pulumi.Input[bool] auto_create: Configures all of the resources in the resource group by applying the recommended configurations.
        :param pulumi.Input[bool] cwe_monitor_enabled: Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        :param pulumi.Input[str] grouping_type: Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        :param pulumi.Input[bool] ops_center_enabled: When set to `true`, creates opsItems for any problems detected on an application.
        :param pulumi.Input[str] ops_item_sns_topic_arn: SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: ApplicationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a ApplicationInsights Application resource.

        ## Example Usage

        ```python
        import pulumi
        import json
        import pulumi_aws as aws

        example_group = aws.resourcegroups.Group("exampleGroup", resource_query=aws.resourcegroups.GroupResourceQueryArgs(
            query=json.dumps({
                "ResourceTypeFilters": ["AWS::EC2::Instance"],
                "TagFilters": [{
                    "Key": "Stage",
                    "Values": ["Test"],
                }],
            }),
        ))
        example_application = aws.applicationinsights.Application("exampleApplication", resource_group_name=example_group.name)
        ```

        ## Import

        ApplicationInsights Applications can be imported using the `resource_group_name`, e.g.,

        ```sh
         $ pulumi import aws:applicationinsights/application:Application some some-application
        ```

        :param str resource_name: The name of the resource.
        :param ApplicationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(ApplicationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 auto_config_enabled: Optional[pulumi.Input[bool]] = None,
                 auto_create: Optional[pulumi.Input[bool]] = None,
                 cwe_monitor_enabled: Optional[pulumi.Input[bool]] = None,
                 grouping_type: Optional[pulumi.Input[str]] = None,
                 ops_center_enabled: Optional[pulumi.Input[bool]] = None,
                 ops_item_sns_topic_arn: Optional[pulumi.Input[str]] = None,
                 resource_group_name: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = ApplicationArgs.__new__(ApplicationArgs)

            __props__.__dict__["auto_config_enabled"] = auto_config_enabled
            __props__.__dict__["auto_create"] = auto_create
            __props__.__dict__["cwe_monitor_enabled"] = cwe_monitor_enabled
            __props__.__dict__["grouping_type"] = grouping_type
            __props__.__dict__["ops_center_enabled"] = ops_center_enabled
            __props__.__dict__["ops_item_sns_topic_arn"] = ops_item_sns_topic_arn
            if resource_group_name is None and not opts.urn:
                raise TypeError("Missing required property 'resource_group_name'")
            __props__.__dict__["resource_group_name"] = resource_group_name
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(Application, __self__).__init__(
            'aws:applicationinsights/application:Application',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            auto_config_enabled: Optional[pulumi.Input[bool]] = None,
            auto_create: Optional[pulumi.Input[bool]] = None,
            cwe_monitor_enabled: Optional[pulumi.Input[bool]] = None,
            grouping_type: Optional[pulumi.Input[str]] = None,
            ops_center_enabled: Optional[pulumi.Input[bool]] = None,
            ops_item_sns_topic_arn: Optional[pulumi.Input[str]] = None,
            resource_group_name: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'Application':
        """
        Get an existing Application resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: ARN of the Application.
        :param pulumi.Input[bool] auto_config_enabled: Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        :param pulumi.Input[bool] auto_create: Configures all of the resources in the resource group by applying the recommended configurations.
        :param pulumi.Input[bool] cwe_monitor_enabled: Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        :param pulumi.Input[str] grouping_type: Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        :param pulumi.Input[bool] ops_center_enabled: When set to `true`, creates opsItems for any problems detected on an application.
        :param pulumi.Input[str] ops_item_sns_topic_arn: SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        :param pulumi.Input[str] resource_group_name: Name of the resource group.
               
               The following arguments are optional:
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _ApplicationState.__new__(_ApplicationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["auto_config_enabled"] = auto_config_enabled
        __props__.__dict__["auto_create"] = auto_create
        __props__.__dict__["cwe_monitor_enabled"] = cwe_monitor_enabled
        __props__.__dict__["grouping_type"] = grouping_type
        __props__.__dict__["ops_center_enabled"] = ops_center_enabled
        __props__.__dict__["ops_item_sns_topic_arn"] = ops_item_sns_topic_arn
        __props__.__dict__["resource_group_name"] = resource_group_name
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return Application(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        ARN of the Application.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="autoConfigEnabled")
    def auto_config_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether Application Insights automatically configures unmonitored resources in the resource group.
        """
        return pulumi.get(self, "auto_config_enabled")

    @property
    @pulumi.getter(name="autoCreate")
    def auto_create(self) -> pulumi.Output[Optional[bool]]:
        """
        Configures all of the resources in the resource group by applying the recommended configurations.
        """
        return pulumi.get(self, "auto_create")

    @property
    @pulumi.getter(name="cweMonitorEnabled")
    def cwe_monitor_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        Indicates whether Application Insights can listen to CloudWatch events for the application resources, such as instance terminated, failed deployment, and others.
        """
        return pulumi.get(self, "cwe_monitor_enabled")

    @property
    @pulumi.getter(name="groupingType")
    def grouping_type(self) -> pulumi.Output[Optional[str]]:
        """
        Application Insights can create applications based on a resource group or on an account. To create an account-based application using all of the resources in the account, set this parameter to `ACCOUNT_BASED`.
        """
        return pulumi.get(self, "grouping_type")

    @property
    @pulumi.getter(name="opsCenterEnabled")
    def ops_center_enabled(self) -> pulumi.Output[Optional[bool]]:
        """
        When set to `true`, creates opsItems for any problems detected on an application.
        """
        return pulumi.get(self, "ops_center_enabled")

    @property
    @pulumi.getter(name="opsItemSnsTopicArn")
    def ops_item_sns_topic_arn(self) -> pulumi.Output[Optional[str]]:
        """
        SNS topic provided to Application Insights that is associated to the created opsItem. Allows you to receive notifications for updates to the opsItem.
        """
        return pulumi.get(self, "ops_item_sns_topic_arn")

    @property
    @pulumi.getter(name="resourceGroupName")
    def resource_group_name(self) -> pulumi.Output[str]:
        """
        Name of the resource group.

        The following arguments are optional:
        """
        return pulumi.get(self, "resource_group_name")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        Map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        Map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

