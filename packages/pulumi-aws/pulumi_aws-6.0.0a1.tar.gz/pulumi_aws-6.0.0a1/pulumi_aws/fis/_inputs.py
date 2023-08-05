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
    'ExperimentTemplateActionArgs',
    'ExperimentTemplateActionParameterArgs',
    'ExperimentTemplateActionTargetArgs',
    'ExperimentTemplateStopConditionArgs',
    'ExperimentTemplateTargetArgs',
    'ExperimentTemplateTargetFilterArgs',
    'ExperimentTemplateTargetResourceTagArgs',
]

@pulumi.input_type
class ExperimentTemplateActionArgs:
    def __init__(__self__, *,
                 action_id: pulumi.Input[str],
                 name: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 parameters: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateActionParameterArgs']]]] = None,
                 start_afters: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 target: Optional[pulumi.Input['ExperimentTemplateActionTargetArgs']] = None):
        """
        :param pulumi.Input[str] action_id: ID of the action. To find out what actions are supported see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        :param pulumi.Input[str] name: Friendly name of the action.
        :param pulumi.Input[str] description: Description of the action.
        :param pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateActionParameterArgs']]] parameters: Parameter(s) for the action, if applicable. See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] start_afters: Set of action names that must complete before this action can be executed.
        :param pulumi.Input['ExperimentTemplateActionTargetArgs'] target: Action's target, if applicable. See below.
        """
        pulumi.set(__self__, "action_id", action_id)
        pulumi.set(__self__, "name", name)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if parameters is not None:
            pulumi.set(__self__, "parameters", parameters)
        if start_afters is not None:
            pulumi.set(__self__, "start_afters", start_afters)
        if target is not None:
            pulumi.set(__self__, "target", target)

    @property
    @pulumi.getter(name="actionId")
    def action_id(self) -> pulumi.Input[str]:
        """
        ID of the action. To find out what actions are supported see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        """
        return pulumi.get(self, "action_id")

    @action_id.setter
    def action_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "action_id", value)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Friendly name of the action.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Description of the action.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def parameters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateActionParameterArgs']]]]:
        """
        Parameter(s) for the action, if applicable. See below.
        """
        return pulumi.get(self, "parameters")

    @parameters.setter
    def parameters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateActionParameterArgs']]]]):
        pulumi.set(self, "parameters", value)

    @property
    @pulumi.getter(name="startAfters")
    def start_afters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of action names that must complete before this action can be executed.
        """
        return pulumi.get(self, "start_afters")

    @start_afters.setter
    def start_afters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "start_afters", value)

    @property
    @pulumi.getter
    def target(self) -> Optional[pulumi.Input['ExperimentTemplateActionTargetArgs']]:
        """
        Action's target, if applicable. See below.
        """
        return pulumi.get(self, "target")

    @target.setter
    def target(self, value: Optional[pulumi.Input['ExperimentTemplateActionTargetArgs']]):
        pulumi.set(self, "target", value)


@pulumi.input_type
class ExperimentTemplateActionParameterArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: Parameter name.
        :param pulumi.Input[str] value: Parameter value.
               
               For a list of parameters supported by each action, see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Parameter name.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Parameter value.

        For a list of parameters supported by each action, see [AWS FIS actions reference](https://docs.aws.amazon.com/fis/latest/userguide/fis-actions-reference.html).
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ExperimentTemplateActionTargetArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: Target type. Valid values are `Cluster` (EKS Cluster), `Clusters` (ECS Clusters), `DBInstances` (RDS DB Instances), `Instances` (EC2 Instances), `Nodegroups` (EKS Node groups), `Roles` (IAM Roles), `SpotInstances` (EC2 Spot Instances), `Subnets` (VPC Subnets).
        :param pulumi.Input[str] value: Target name, referencing a corresponding target.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Target type. Valid values are `Cluster` (EKS Cluster), `Clusters` (ECS Clusters), `DBInstances` (RDS DB Instances), `Instances` (EC2 Instances), `Nodegroups` (EKS Node groups), `Roles` (IAM Roles), `SpotInstances` (EC2 Spot Instances), `Subnets` (VPC Subnets).
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Target name, referencing a corresponding target.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ExperimentTemplateStopConditionArgs:
    def __init__(__self__, *,
                 source: pulumi.Input[str],
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] source: Source of the condition. One of `none`, `aws:cloudwatch:alarm`.
        :param pulumi.Input[str] value: ARN of the CloudWatch alarm. Required if the source is a CloudWatch alarm.
        """
        pulumi.set(__self__, "source", source)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def source(self) -> pulumi.Input[str]:
        """
        Source of the condition. One of `none`, `aws:cloudwatch:alarm`.
        """
        return pulumi.get(self, "source")

    @source.setter
    def source(self, value: pulumi.Input[str]):
        pulumi.set(self, "source", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        ARN of the CloudWatch alarm. Required if the source is a CloudWatch alarm.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class ExperimentTemplateTargetArgs:
    def __init__(__self__, *,
                 name: pulumi.Input[str],
                 resource_type: pulumi.Input[str],
                 selection_mode: pulumi.Input[str],
                 filters: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetFilterArgs']]]] = None,
                 resource_arns: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]] = None,
                 resource_tags: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetResourceTagArgs']]]] = None):
        """
        :param pulumi.Input[str] name: Friendly name given to the target.
        :param pulumi.Input[str] resource_type: AWS resource type. The resource type must be supported for the specified action. To find out what resource types are supported, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#resource-types).
        :param pulumi.Input[str] selection_mode: Scopes the identified resources. Valid values are `ALL` (all identified resources), `COUNT(n)` (randomly select `n` of the identified resources), `PERCENT(n)` (randomly select `n` percent of the identified resources).
        :param pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetFilterArgs']]] filters: Filter(s) for the target. Filters can be used to select resources based on specific attributes returned by the respective describe action of the resource type. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters). See below.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] resource_arns: Set of ARNs of the resources to target with an action. Conflicts with `resource_tag`.
        :param pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetResourceTagArgs']]] resource_tags: Tag(s) the resources need to have to be considered a valid target for an action. Conflicts with `resource_arns`. See below.
               
               > **NOTE:** The `target` configuration block requires either `resource_arns` or `resource_tag`.
        """
        pulumi.set(__self__, "name", name)
        pulumi.set(__self__, "resource_type", resource_type)
        pulumi.set(__self__, "selection_mode", selection_mode)
        if filters is not None:
            pulumi.set(__self__, "filters", filters)
        if resource_arns is not None:
            pulumi.set(__self__, "resource_arns", resource_arns)
        if resource_tags is not None:
            pulumi.set(__self__, "resource_tags", resource_tags)

    @property
    @pulumi.getter
    def name(self) -> pulumi.Input[str]:
        """
        Friendly name given to the target.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: pulumi.Input[str]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="resourceType")
    def resource_type(self) -> pulumi.Input[str]:
        """
        AWS resource type. The resource type must be supported for the specified action. To find out what resource types are supported, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#resource-types).
        """
        return pulumi.get(self, "resource_type")

    @resource_type.setter
    def resource_type(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_type", value)

    @property
    @pulumi.getter(name="selectionMode")
    def selection_mode(self) -> pulumi.Input[str]:
        """
        Scopes the identified resources. Valid values are `ALL` (all identified resources), `COUNT(n)` (randomly select `n` of the identified resources), `PERCENT(n)` (randomly select `n` percent of the identified resources).
        """
        return pulumi.get(self, "selection_mode")

    @selection_mode.setter
    def selection_mode(self, value: pulumi.Input[str]):
        pulumi.set(self, "selection_mode", value)

    @property
    @pulumi.getter
    def filters(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetFilterArgs']]]]:
        """
        Filter(s) for the target. Filters can be used to select resources based on specific attributes returned by the respective describe action of the resource type. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters). See below.
        """
        return pulumi.get(self, "filters")

    @filters.setter
    def filters(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetFilterArgs']]]]):
        pulumi.set(self, "filters", value)

    @property
    @pulumi.getter(name="resourceArns")
    def resource_arns(self) -> Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]:
        """
        Set of ARNs of the resources to target with an action. Conflicts with `resource_tag`.
        """
        return pulumi.get(self, "resource_arns")

    @resource_arns.setter
    def resource_arns(self, value: Optional[pulumi.Input[Sequence[pulumi.Input[str]]]]):
        pulumi.set(self, "resource_arns", value)

    @property
    @pulumi.getter(name="resourceTags")
    def resource_tags(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetResourceTagArgs']]]]:
        """
        Tag(s) the resources need to have to be considered a valid target for an action. Conflicts with `resource_arns`. See below.

        > **NOTE:** The `target` configuration block requires either `resource_arns` or `resource_tag`.
        """
        return pulumi.get(self, "resource_tags")

    @resource_tags.setter
    def resource_tags(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['ExperimentTemplateTargetResourceTagArgs']]]]):
        pulumi.set(self, "resource_tags", value)


@pulumi.input_type
class ExperimentTemplateTargetFilterArgs:
    def __init__(__self__, *,
                 path: pulumi.Input[str],
                 values: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[str] path: Attribute path for the filter.
        :param pulumi.Input[Sequence[pulumi.Input[str]]] values: Set of attribute values for the filter.
               
               > **NOTE:** Values specified in a `filter` are joined with an `OR` clause, while values across multiple `filter` blocks are joined with an `AND` clause. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters).
        """
        pulumi.set(__self__, "path", path)
        pulumi.set(__self__, "values", values)

    @property
    @pulumi.getter
    def path(self) -> pulumi.Input[str]:
        """
        Attribute path for the filter.
        """
        return pulumi.get(self, "path")

    @path.setter
    def path(self, value: pulumi.Input[str]):
        pulumi.set(self, "path", value)

    @property
    @pulumi.getter
    def values(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        Set of attribute values for the filter.

        > **NOTE:** Values specified in a `filter` are joined with an `OR` clause, while values across multiple `filter` blocks are joined with an `AND` clause. For more information, see [Targets for AWS FIS](https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters).
        """
        return pulumi.get(self, "values")

    @values.setter
    def values(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "values", value)


@pulumi.input_type
class ExperimentTemplateTargetResourceTagArgs:
    def __init__(__self__, *,
                 key: pulumi.Input[str],
                 value: pulumi.Input[str]):
        """
        :param pulumi.Input[str] key: Tag key.
        :param pulumi.Input[str] value: Tag value.
        """
        pulumi.set(__self__, "key", key)
        pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter
    def key(self) -> pulumi.Input[str]:
        """
        Tag key.
        """
        return pulumi.get(self, "key")

    @key.setter
    def key(self, value: pulumi.Input[str]):
        pulumi.set(self, "key", value)

    @property
    @pulumi.getter
    def value(self) -> pulumi.Input[str]:
        """
        Tag value.
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: pulumi.Input[str]):
        pulumi.set(self, "value", value)


