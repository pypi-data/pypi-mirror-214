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

__all__ = ['FlowDefinitionArgs', 'FlowDefinition']

@pulumi.input_type
class FlowDefinitionArgs:
    def __init__(__self__, *,
                 flow_definition_name: pulumi.Input[str],
                 human_loop_config: pulumi.Input['FlowDefinitionHumanLoopConfigArgs'],
                 output_config: pulumi.Input['FlowDefinitionOutputConfigArgs'],
                 role_arn: pulumi.Input[str],
                 human_loop_activation_config: Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']] = None,
                 human_loop_request_source: Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a FlowDefinition resource.
        :param pulumi.Input[str] flow_definition_name: The name of your flow definition.
        :param pulumi.Input['FlowDefinitionHumanLoopConfigArgs'] human_loop_config: An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        :param pulumi.Input['FlowDefinitionOutputConfigArgs'] output_config: An object containing information about where the human review results will be uploaded. See Output Config details below.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        :param pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs'] human_loop_activation_config: An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        :param pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs'] human_loop_request_source: Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "flow_definition_name", flow_definition_name)
        pulumi.set(__self__, "human_loop_config", human_loop_config)
        pulumi.set(__self__, "output_config", output_config)
        pulumi.set(__self__, "role_arn", role_arn)
        if human_loop_activation_config is not None:
            pulumi.set(__self__, "human_loop_activation_config", human_loop_activation_config)
        if human_loop_request_source is not None:
            pulumi.set(__self__, "human_loop_request_source", human_loop_request_source)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="flowDefinitionName")
    def flow_definition_name(self) -> pulumi.Input[str]:
        """
        The name of your flow definition.
        """
        return pulumi.get(self, "flow_definition_name")

    @flow_definition_name.setter
    def flow_definition_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "flow_definition_name", value)

    @property
    @pulumi.getter(name="humanLoopConfig")
    def human_loop_config(self) -> pulumi.Input['FlowDefinitionHumanLoopConfigArgs']:
        """
        An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        """
        return pulumi.get(self, "human_loop_config")

    @human_loop_config.setter
    def human_loop_config(self, value: pulumi.Input['FlowDefinitionHumanLoopConfigArgs']):
        pulumi.set(self, "human_loop_config", value)

    @property
    @pulumi.getter(name="outputConfig")
    def output_config(self) -> pulumi.Input['FlowDefinitionOutputConfigArgs']:
        """
        An object containing information about where the human review results will be uploaded. See Output Config details below.
        """
        return pulumi.get(self, "output_config")

    @output_config.setter
    def output_config(self, value: pulumi.Input['FlowDefinitionOutputConfigArgs']):
        pulumi.set(self, "output_config", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Input[str]:
        """
        The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter(name="humanLoopActivationConfig")
    def human_loop_activation_config(self) -> Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']]:
        """
        An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        """
        return pulumi.get(self, "human_loop_activation_config")

    @human_loop_activation_config.setter
    def human_loop_activation_config(self, value: Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']]):
        pulumi.set(self, "human_loop_activation_config", value)

    @property
    @pulumi.getter(name="humanLoopRequestSource")
    def human_loop_request_source(self) -> Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']]:
        """
        Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        """
        return pulumi.get(self, "human_loop_request_source")

    @human_loop_request_source.setter
    def human_loop_request_source(self, value: Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']]):
        pulumi.set(self, "human_loop_request_source", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _FlowDefinitionState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 flow_definition_name: Optional[pulumi.Input[str]] = None,
                 human_loop_activation_config: Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']] = None,
                 human_loop_config: Optional[pulumi.Input['FlowDefinitionHumanLoopConfigArgs']] = None,
                 human_loop_request_source: Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']] = None,
                 output_config: Optional[pulumi.Input['FlowDefinitionOutputConfigArgs']] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering FlowDefinition resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Flow Definition.
        :param pulumi.Input[str] flow_definition_name: The name of your flow definition.
        :param pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs'] human_loop_activation_config: An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        :param pulumi.Input['FlowDefinitionHumanLoopConfigArgs'] human_loop_config: An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        :param pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs'] human_loop_request_source: Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        :param pulumi.Input['FlowDefinitionOutputConfigArgs'] output_config: An object containing information about where the human review results will be uploaded. See Output Config details below.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if flow_definition_name is not None:
            pulumi.set(__self__, "flow_definition_name", flow_definition_name)
        if human_loop_activation_config is not None:
            pulumi.set(__self__, "human_loop_activation_config", human_loop_activation_config)
        if human_loop_config is not None:
            pulumi.set(__self__, "human_loop_config", human_loop_config)
        if human_loop_request_source is not None:
            pulumi.set(__self__, "human_loop_request_source", human_loop_request_source)
        if output_config is not None:
            pulumi.set(__self__, "output_config", output_config)
        if role_arn is not None:
            pulumi.set(__self__, "role_arn", role_arn)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Flow Definition.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="flowDefinitionName")
    def flow_definition_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of your flow definition.
        """
        return pulumi.get(self, "flow_definition_name")

    @flow_definition_name.setter
    def flow_definition_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "flow_definition_name", value)

    @property
    @pulumi.getter(name="humanLoopActivationConfig")
    def human_loop_activation_config(self) -> Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']]:
        """
        An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        """
        return pulumi.get(self, "human_loop_activation_config")

    @human_loop_activation_config.setter
    def human_loop_activation_config(self, value: Optional[pulumi.Input['FlowDefinitionHumanLoopActivationConfigArgs']]):
        pulumi.set(self, "human_loop_activation_config", value)

    @property
    @pulumi.getter(name="humanLoopConfig")
    def human_loop_config(self) -> Optional[pulumi.Input['FlowDefinitionHumanLoopConfigArgs']]:
        """
        An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        """
        return pulumi.get(self, "human_loop_config")

    @human_loop_config.setter
    def human_loop_config(self, value: Optional[pulumi.Input['FlowDefinitionHumanLoopConfigArgs']]):
        pulumi.set(self, "human_loop_config", value)

    @property
    @pulumi.getter(name="humanLoopRequestSource")
    def human_loop_request_source(self) -> Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']]:
        """
        Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        """
        return pulumi.get(self, "human_loop_request_source")

    @human_loop_request_source.setter
    def human_loop_request_source(self, value: Optional[pulumi.Input['FlowDefinitionHumanLoopRequestSourceArgs']]):
        pulumi.set(self, "human_loop_request_source", value)

    @property
    @pulumi.getter(name="outputConfig")
    def output_config(self) -> Optional[pulumi.Input['FlowDefinitionOutputConfigArgs']]:
        """
        An object containing information about where the human review results will be uploaded. See Output Config details below.
        """
        return pulumi.get(self, "output_config")

    @output_config.setter
    def output_config(self, value: Optional[pulumi.Input['FlowDefinitionOutputConfigArgs']]):
        pulumi.set(self, "output_config", value)

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @role_arn.setter
    def role_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role_arn", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class FlowDefinition(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 flow_definition_name: Optional[pulumi.Input[str]] = None,
                 human_loop_activation_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopActivationConfigArgs']]] = None,
                 human_loop_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopConfigArgs']]] = None,
                 human_loop_request_source: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopRequestSourceArgs']]] = None,
                 output_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionOutputConfigArgs']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a SageMaker Flow Definition resource.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```
        ### Public Workteam Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=f"arn:aws:sagemaker:{data['aws_region']['current']['name']}:394669845002:workteam/public-crowd/default",
                public_workforce_task_price=aws.sagemaker.FlowDefinitionHumanLoopConfigPublicWorkforceTaskPriceArgs(
                    amount_in_usd=aws.sagemaker.FlowDefinitionHumanLoopConfigPublicWorkforceTaskPriceAmountInUsdArgs(
                        cents=1,
                        tenth_fractions_of_a_cent=2,
                    ),
                ),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```
        ### Human Loop Activation Config Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            human_loop_request_source=aws.sagemaker.FlowDefinitionHumanLoopRequestSourceArgs(
                aws_managed_human_loop_request_source="AWS/Textract/AnalyzeDocument/Forms/V1",
            ),
            human_loop_activation_config=aws.sagemaker.FlowDefinitionHumanLoopActivationConfigArgs(
                human_loop_activation_conditions_config=aws.sagemaker.FlowDefinitionHumanLoopActivationConfigHumanLoopActivationConditionsConfigArgs(
                    human_loop_activation_conditions=\"\"\"        {
        			"Conditions": [
        			  {
        				"ConditionType": "Sampling",
        				"ConditionParameters": {
        				  "RandomSamplingPercentage": 5
        				}
        			  }
        			]
        		}
        \"\"\",
                ),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```

        ## Import

        SageMaker Flow Definitions can be imported using the `flow_definition_name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/flowDefinition:FlowDefinition example example
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] flow_definition_name: The name of your flow definition.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopActivationConfigArgs']] human_loop_activation_config: An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopConfigArgs']] human_loop_config: An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopRequestSourceArgs']] human_loop_request_source: Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionOutputConfigArgs']] output_config: An object containing information about where the human review results will be uploaded. See Output Config details below.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: FlowDefinitionArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker Flow Definition resource.

        ## Example Usage
        ### Basic Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```
        ### Public Workteam Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=f"arn:aws:sagemaker:{data['aws_region']['current']['name']}:394669845002:workteam/public-crowd/default",
                public_workforce_task_price=aws.sagemaker.FlowDefinitionHumanLoopConfigPublicWorkforceTaskPriceArgs(
                    amount_in_usd=aws.sagemaker.FlowDefinitionHumanLoopConfigPublicWorkforceTaskPriceAmountInUsdArgs(
                        cents=1,
                        tenth_fractions_of_a_cent=2,
                    ),
                ),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```
        ### Human Loop Activation Config Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        example = aws.sagemaker.FlowDefinition("example",
            flow_definition_name="example",
            role_arn=aws_iam_role["example"]["arn"],
            human_loop_config=aws.sagemaker.FlowDefinitionHumanLoopConfigArgs(
                human_task_ui_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                task_availability_lifetime_in_seconds=1,
                task_count=1,
                task_description="example",
                task_title="example",
                workteam_arn=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
            ),
            human_loop_request_source=aws.sagemaker.FlowDefinitionHumanLoopRequestSourceArgs(
                aws_managed_human_loop_request_source="AWS/Textract/AnalyzeDocument/Forms/V1",
            ),
            human_loop_activation_config=aws.sagemaker.FlowDefinitionHumanLoopActivationConfigArgs(
                human_loop_activation_conditions_config=aws.sagemaker.FlowDefinitionHumanLoopActivationConfigHumanLoopActivationConditionsConfigArgs(
                    human_loop_activation_conditions=\"\"\"        {
        			"Conditions": [
        			  {
        				"ConditionType": "Sampling",
        				"ConditionParameters": {
        				  "RandomSamplingPercentage": 5
        				}
        			  }
        			]
        		}
        \"\"\",
                ),
            ),
            output_config=aws.sagemaker.FlowDefinitionOutputConfigArgs(
                s3_output_path=f"s3://{aws_s3_bucket['example']['bucket']}/",
            ))
        ```

        ## Import

        SageMaker Flow Definitions can be imported using the `flow_definition_name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/flowDefinition:FlowDefinition example example
        ```

        :param str resource_name: The name of the resource.
        :param FlowDefinitionArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(FlowDefinitionArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 flow_definition_name: Optional[pulumi.Input[str]] = None,
                 human_loop_activation_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopActivationConfigArgs']]] = None,
                 human_loop_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopConfigArgs']]] = None,
                 human_loop_request_source: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopRequestSourceArgs']]] = None,
                 output_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionOutputConfigArgs']]] = None,
                 role_arn: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = FlowDefinitionArgs.__new__(FlowDefinitionArgs)

            if flow_definition_name is None and not opts.urn:
                raise TypeError("Missing required property 'flow_definition_name'")
            __props__.__dict__["flow_definition_name"] = flow_definition_name
            __props__.__dict__["human_loop_activation_config"] = human_loop_activation_config
            if human_loop_config is None and not opts.urn:
                raise TypeError("Missing required property 'human_loop_config'")
            __props__.__dict__["human_loop_config"] = human_loop_config
            __props__.__dict__["human_loop_request_source"] = human_loop_request_source
            if output_config is None and not opts.urn:
                raise TypeError("Missing required property 'output_config'")
            __props__.__dict__["output_config"] = output_config
            if role_arn is None and not opts.urn:
                raise TypeError("Missing required property 'role_arn'")
            __props__.__dict__["role_arn"] = role_arn
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(FlowDefinition, __self__).__init__(
            'aws:sagemaker/flowDefinition:FlowDefinition',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            flow_definition_name: Optional[pulumi.Input[str]] = None,
            human_loop_activation_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopActivationConfigArgs']]] = None,
            human_loop_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopConfigArgs']]] = None,
            human_loop_request_source: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopRequestSourceArgs']]] = None,
            output_config: Optional[pulumi.Input[pulumi.InputType['FlowDefinitionOutputConfigArgs']]] = None,
            role_arn: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'FlowDefinition':
        """
        Get an existing FlowDefinition resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this Flow Definition.
        :param pulumi.Input[str] flow_definition_name: The name of your flow definition.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopActivationConfigArgs']] human_loop_activation_config: An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopConfigArgs']] human_loop_config: An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionHumanLoopRequestSourceArgs']] human_loop_request_source: Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        :param pulumi.Input[pulumi.InputType['FlowDefinitionOutputConfigArgs']] output_config: An object containing information about where the human review results will be uploaded. See Output Config details below.
        :param pulumi.Input[str] role_arn: The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _FlowDefinitionState.__new__(_FlowDefinitionState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["flow_definition_name"] = flow_definition_name
        __props__.__dict__["human_loop_activation_config"] = human_loop_activation_config
        __props__.__dict__["human_loop_config"] = human_loop_config
        __props__.__dict__["human_loop_request_source"] = human_loop_request_source
        __props__.__dict__["output_config"] = output_config
        __props__.__dict__["role_arn"] = role_arn
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return FlowDefinition(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this Flow Definition.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="flowDefinitionName")
    def flow_definition_name(self) -> pulumi.Output[str]:
        """
        The name of your flow definition.
        """
        return pulumi.get(self, "flow_definition_name")

    @property
    @pulumi.getter(name="humanLoopActivationConfig")
    def human_loop_activation_config(self) -> pulumi.Output[Optional['outputs.FlowDefinitionHumanLoopActivationConfig']]:
        """
        An object containing information about the events that trigger a human workflow. See Human Loop Activation Config details below.
        """
        return pulumi.get(self, "human_loop_activation_config")

    @property
    @pulumi.getter(name="humanLoopConfig")
    def human_loop_config(self) -> pulumi.Output['outputs.FlowDefinitionHumanLoopConfig']:
        """
        An object containing information about the tasks the human reviewers will perform. See Human Loop Config details below.
        """
        return pulumi.get(self, "human_loop_config")

    @property
    @pulumi.getter(name="humanLoopRequestSource")
    def human_loop_request_source(self) -> pulumi.Output[Optional['outputs.FlowDefinitionHumanLoopRequestSource']]:
        """
        Container for configuring the source of human task requests. Use to specify if Amazon Rekognition or Amazon Textract is used as an integration source. See Human Loop Request Source details below.
        """
        return pulumi.get(self, "human_loop_request_source")

    @property
    @pulumi.getter(name="outputConfig")
    def output_config(self) -> pulumi.Output['outputs.FlowDefinitionOutputConfig']:
        """
        An object containing information about where the human review results will be uploaded. See Output Config details below.
        """
        return pulumi.get(self, "output_config")

    @property
    @pulumi.getter(name="roleArn")
    def role_arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) of the role needed to call other services on your behalf.
        """
        return pulumi.get(self, "role_arn")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

