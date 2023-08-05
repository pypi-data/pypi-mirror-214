# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['BudgetResourceAssociationArgs', 'BudgetResourceAssociation']

@pulumi.input_type
class BudgetResourceAssociationArgs:
    def __init__(__self__, *,
                 budget_name: pulumi.Input[str],
                 resource_id: pulumi.Input[str]):
        """
        The set of arguments for constructing a BudgetResourceAssociation resource.
        :param pulumi.Input[str] budget_name: Budget name.
        :param pulumi.Input[str] resource_id: Resource identifier.
        """
        pulumi.set(__self__, "budget_name", budget_name)
        pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="budgetName")
    def budget_name(self) -> pulumi.Input[str]:
        """
        Budget name.
        """
        return pulumi.get(self, "budget_name")

    @budget_name.setter
    def budget_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "budget_name", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Input[str]:
        """
        Resource identifier.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "resource_id", value)


@pulumi.input_type
class _BudgetResourceAssociationState:
    def __init__(__self__, *,
                 budget_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering BudgetResourceAssociation resources.
        :param pulumi.Input[str] budget_name: Budget name.
        :param pulumi.Input[str] resource_id: Resource identifier.
        """
        if budget_name is not None:
            pulumi.set(__self__, "budget_name", budget_name)
        if resource_id is not None:
            pulumi.set(__self__, "resource_id", resource_id)

    @property
    @pulumi.getter(name="budgetName")
    def budget_name(self) -> Optional[pulumi.Input[str]]:
        """
        Budget name.
        """
        return pulumi.get(self, "budget_name")

    @budget_name.setter
    def budget_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "budget_name", value)

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> Optional[pulumi.Input[str]]:
        """
        Resource identifier.
        """
        return pulumi.get(self, "resource_id")

    @resource_id.setter
    def resource_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "resource_id", value)


class BudgetResourceAssociation(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 budget_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages a Service Catalog Budget Resource Association.

        > **Tip:** A "resource" is either a Service Catalog portfolio or product.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.BudgetResourceAssociation("example",
            budget_name="budget-pjtvyakdlyo3m",
            resource_id="prod-dnigbtea24ste")
        ```

        ## Import

        `aws_servicecatalog_budget_resource_association` can be imported using the budget name and resource ID, e.g.,

        ```sh
         $ pulumi import aws:servicecatalog/budgetResourceAssociation:BudgetResourceAssociation example budget-pjtvyakdlyo3m:prod-dnigbtea24ste
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] budget_name: Budget name.
        :param pulumi.Input[str] resource_id: Resource identifier.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: BudgetResourceAssociationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages a Service Catalog Budget Resource Association.

        > **Tip:** A "resource" is either a Service Catalog portfolio or product.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.servicecatalog.BudgetResourceAssociation("example",
            budget_name="budget-pjtvyakdlyo3m",
            resource_id="prod-dnigbtea24ste")
        ```

        ## Import

        `aws_servicecatalog_budget_resource_association` can be imported using the budget name and resource ID, e.g.,

        ```sh
         $ pulumi import aws:servicecatalog/budgetResourceAssociation:BudgetResourceAssociation example budget-pjtvyakdlyo3m:prod-dnigbtea24ste
        ```

        :param str resource_name: The name of the resource.
        :param BudgetResourceAssociationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(BudgetResourceAssociationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 budget_name: Optional[pulumi.Input[str]] = None,
                 resource_id: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = BudgetResourceAssociationArgs.__new__(BudgetResourceAssociationArgs)

            if budget_name is None and not opts.urn:
                raise TypeError("Missing required property 'budget_name'")
            __props__.__dict__["budget_name"] = budget_name
            if resource_id is None and not opts.urn:
                raise TypeError("Missing required property 'resource_id'")
            __props__.__dict__["resource_id"] = resource_id
        super(BudgetResourceAssociation, __self__).__init__(
            'aws:servicecatalog/budgetResourceAssociation:BudgetResourceAssociation',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            budget_name: Optional[pulumi.Input[str]] = None,
            resource_id: Optional[pulumi.Input[str]] = None) -> 'BudgetResourceAssociation':
        """
        Get an existing BudgetResourceAssociation resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] budget_name: Budget name.
        :param pulumi.Input[str] resource_id: Resource identifier.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _BudgetResourceAssociationState.__new__(_BudgetResourceAssociationState)

        __props__.__dict__["budget_name"] = budget_name
        __props__.__dict__["resource_id"] = resource_id
        return BudgetResourceAssociation(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="budgetName")
    def budget_name(self) -> pulumi.Output[str]:
        """
        Budget name.
        """
        return pulumi.get(self, "budget_name")

    @property
    @pulumi.getter(name="resourceId")
    def resource_id(self) -> pulumi.Output[str]:
        """
        Resource identifier.
        """
        return pulumi.get(self, "resource_id")

