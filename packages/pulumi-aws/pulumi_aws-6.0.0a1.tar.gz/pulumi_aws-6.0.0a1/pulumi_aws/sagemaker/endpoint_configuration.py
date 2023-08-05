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

__all__ = ['EndpointConfigurationArgs', 'EndpointConfiguration']

@pulumi.input_type
class EndpointConfigurationArgs:
    def __init__(__self__, *,
                 production_variants: pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]],
                 async_inference_config: Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']] = None,
                 data_capture_config: Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a EndpointConfiguration resource.
        :param pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]] production_variants: An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        :param pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs'] async_inference_config: Specifies configuration for how an endpoint performs asynchronous inference.
        :param pulumi.Input['EndpointConfigurationDataCaptureConfigArgs'] data_capture_config: Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        :param pulumi.Input[str] name_prefix: Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]] shadow_production_variants: Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "production_variants", production_variants)
        if async_inference_config is not None:
            pulumi.set(__self__, "async_inference_config", async_inference_config)
        if data_capture_config is not None:
            pulumi.set(__self__, "data_capture_config", data_capture_config)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if shadow_production_variants is not None:
            pulumi.set(__self__, "shadow_production_variants", shadow_production_variants)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter(name="productionVariants")
    def production_variants(self) -> pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]]:
        """
        An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        """
        return pulumi.get(self, "production_variants")

    @production_variants.setter
    def production_variants(self, value: pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]]):
        pulumi.set(self, "production_variants", value)

    @property
    @pulumi.getter(name="asyncInferenceConfig")
    def async_inference_config(self) -> Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']]:
        """
        Specifies configuration for how an endpoint performs asynchronous inference.
        """
        return pulumi.get(self, "async_inference_config")

    @async_inference_config.setter
    def async_inference_config(self, value: Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']]):
        pulumi.set(self, "async_inference_config", value)

    @property
    @pulumi.getter(name="dataCaptureConfig")
    def data_capture_config(self) -> Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']]:
        """
        Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        """
        return pulumi.get(self, "data_capture_config")

    @data_capture_config.setter
    def data_capture_config(self, value: Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']]):
        pulumi.set(self, "data_capture_config", value)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        """
        return pulumi.get(self, "kms_key_arn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

    @property
    @pulumi.getter(name="shadowProductionVariants")
    def shadow_production_variants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]]:
        """
        Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        """
        return pulumi.get(self, "shadow_production_variants")

    @shadow_production_variants.setter
    def shadow_production_variants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]]):
        pulumi.set(self, "shadow_production_variants", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _EndpointConfigurationState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 async_inference_config: Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']] = None,
                 data_capture_config: Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 production_variants: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        Input properties used for looking up and filtering EndpointConfiguration resources.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
        :param pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs'] async_inference_config: Specifies configuration for how an endpoint performs asynchronous inference.
        :param pulumi.Input['EndpointConfigurationDataCaptureConfigArgs'] data_capture_config: Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        :param pulumi.Input[str] name_prefix: Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]] production_variants: An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        :param pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]] shadow_production_variants: Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if async_inference_config is not None:
            pulumi.set(__self__, "async_inference_config", async_inference_config)
        if data_capture_config is not None:
            pulumi.set(__self__, "data_capture_config", data_capture_config)
        if kms_key_arn is not None:
            pulumi.set(__self__, "kms_key_arn", kms_key_arn)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if name_prefix is not None:
            pulumi.set(__self__, "name_prefix", name_prefix)
        if production_variants is not None:
            pulumi.set(__self__, "production_variants", production_variants)
        if shadow_production_variants is not None:
            pulumi.set(__self__, "shadow_production_variants", shadow_production_variants)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="asyncInferenceConfig")
    def async_inference_config(self) -> Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']]:
        """
        Specifies configuration for how an endpoint performs asynchronous inference.
        """
        return pulumi.get(self, "async_inference_config")

    @async_inference_config.setter
    def async_inference_config(self, value: Optional[pulumi.Input['EndpointConfigurationAsyncInferenceConfigArgs']]):
        pulumi.set(self, "async_inference_config", value)

    @property
    @pulumi.getter(name="dataCaptureConfig")
    def data_capture_config(self) -> Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']]:
        """
        Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        """
        return pulumi.get(self, "data_capture_config")

    @data_capture_config.setter
    def data_capture_config(self, value: Optional[pulumi.Input['EndpointConfigurationDataCaptureConfigArgs']]):
        pulumi.set(self, "data_capture_config", value)

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        """
        return pulumi.get(self, "kms_key_arn")

    @kms_key_arn.setter
    def kms_key_arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "kms_key_arn", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> Optional[pulumi.Input[str]]:
        """
        Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @name_prefix.setter
    def name_prefix(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name_prefix", value)

    @property
    @pulumi.getter(name="productionVariants")
    def production_variants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]]]:
        """
        An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        """
        return pulumi.get(self, "production_variants")

    @production_variants.setter
    def production_variants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationProductionVariantArgs']]]]):
        pulumi.set(self, "production_variants", value)

    @property
    @pulumi.getter(name="shadowProductionVariants")
    def shadow_production_variants(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]]:
        """
        Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        """
        return pulumi.get(self, "shadow_production_variants")

    @shadow_production_variants.setter
    def shadow_production_variants(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['EndpointConfigurationShadowProductionVariantArgs']]]]):
        pulumi.set(self, "shadow_production_variants", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
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


class EndpointConfiguration(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_inference_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationAsyncInferenceConfigArgs']]] = None,
                 data_capture_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationDataCaptureConfigArgs']]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationProductionVariantArgs']]]]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationShadowProductionVariantArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        """
        Provides a SageMaker endpoint configuration resource.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        ec = aws.sagemaker.EndpointConfiguration("ec",
            production_variants=[aws.sagemaker.EndpointConfigurationProductionVariantArgs(
                variant_name="variant-1",
                model_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                initial_instance_count=1,
                instance_type="ml.t2.medium",
            )],
            tags={
                "Name": "foo",
            })
        ```

        ## Import

        Endpoint configurations can be imported using the `name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/endpointConfiguration:EndpointConfiguration test_endpoint_config endpoint-config-foo
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[pulumi.InputType['EndpointConfigurationAsyncInferenceConfigArgs']] async_inference_config: Specifies configuration for how an endpoint performs asynchronous inference.
        :param pulumi.Input[pulumi.InputType['EndpointConfigurationDataCaptureConfigArgs']] data_capture_config: Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        :param pulumi.Input[str] name_prefix: Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationProductionVariantArgs']]]] production_variants: An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationShadowProductionVariantArgs']]]] shadow_production_variants: Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: EndpointConfigurationArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a SageMaker endpoint configuration resource.

        ## Example Usage

        Basic usage:

        ```python
        import pulumi
        import pulumi_aws as aws

        ec = aws.sagemaker.EndpointConfiguration("ec",
            production_variants=[aws.sagemaker.EndpointConfigurationProductionVariantArgs(
                variant_name="variant-1",
                model_name=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference),
                initial_instance_count=1,
                instance_type="ml.t2.medium",
            )],
            tags={
                "Name": "foo",
            })
        ```

        ## Import

        Endpoint configurations can be imported using the `name`, e.g.,

        ```sh
         $ pulumi import aws:sagemaker/endpointConfiguration:EndpointConfiguration test_endpoint_config endpoint-config-foo
        ```

        :param str resource_name: The name of the resource.
        :param EndpointConfigurationArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(EndpointConfigurationArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 async_inference_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationAsyncInferenceConfigArgs']]] = None,
                 data_capture_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationDataCaptureConfigArgs']]] = None,
                 kms_key_arn: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 name_prefix: Optional[pulumi.Input[str]] = None,
                 production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationProductionVariantArgs']]]]] = None,
                 shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationShadowProductionVariantArgs']]]]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = EndpointConfigurationArgs.__new__(EndpointConfigurationArgs)

            __props__.__dict__["async_inference_config"] = async_inference_config
            __props__.__dict__["data_capture_config"] = data_capture_config
            __props__.__dict__["kms_key_arn"] = kms_key_arn
            __props__.__dict__["name"] = name
            __props__.__dict__["name_prefix"] = name_prefix
            if production_variants is None and not opts.urn:
                raise TypeError("Missing required property 'production_variants'")
            __props__.__dict__["production_variants"] = production_variants
            __props__.__dict__["shadow_production_variants"] = shadow_production_variants
            __props__.__dict__["tags"] = tags
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(EndpointConfiguration, __self__).__init__(
            'aws:sagemaker/endpointConfiguration:EndpointConfiguration',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            async_inference_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationAsyncInferenceConfigArgs']]] = None,
            data_capture_config: Optional[pulumi.Input[pulumi.InputType['EndpointConfigurationDataCaptureConfigArgs']]] = None,
            kms_key_arn: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            name_prefix: Optional[pulumi.Input[str]] = None,
            production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationProductionVariantArgs']]]]] = None,
            shadow_production_variants: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationShadowProductionVariantArgs']]]]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None) -> 'EndpointConfiguration':
        """
        Get an existing EndpointConfiguration resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
        :param pulumi.Input[pulumi.InputType['EndpointConfigurationAsyncInferenceConfigArgs']] async_inference_config: Specifies configuration for how an endpoint performs asynchronous inference.
        :param pulumi.Input[pulumi.InputType['EndpointConfigurationDataCaptureConfigArgs']] data_capture_config: Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        :param pulumi.Input[str] kms_key_arn: Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        :param pulumi.Input[str] name: The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        :param pulumi.Input[str] name_prefix: Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationProductionVariantArgs']]]] production_variants: An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['EndpointConfigurationShadowProductionVariantArgs']]]] shadow_production_variants: Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _EndpointConfigurationState.__new__(_EndpointConfigurationState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["async_inference_config"] = async_inference_config
        __props__.__dict__["data_capture_config"] = data_capture_config
        __props__.__dict__["kms_key_arn"] = kms_key_arn
        __props__.__dict__["name"] = name
        __props__.__dict__["name_prefix"] = name_prefix
        __props__.__dict__["production_variants"] = production_variants
        __props__.__dict__["shadow_production_variants"] = shadow_production_variants
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        return EndpointConfiguration(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        The Amazon Resource Name (ARN) assigned by AWS to this endpoint configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="asyncInferenceConfig")
    def async_inference_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigurationAsyncInferenceConfig']]:
        """
        Specifies configuration for how an endpoint performs asynchronous inference.
        """
        return pulumi.get(self, "async_inference_config")

    @property
    @pulumi.getter(name="dataCaptureConfig")
    def data_capture_config(self) -> pulumi.Output[Optional['outputs.EndpointConfigurationDataCaptureConfig']]:
        """
        Specifies the parameters to capture input/output of SageMaker models endpoints. Fields are documented below.
        """
        return pulumi.get(self, "data_capture_config")

    @property
    @pulumi.getter(name="kmsKeyArn")
    def kms_key_arn(self) -> pulumi.Output[Optional[str]]:
        """
        Amazon Resource Name (ARN) of a AWS Key Management Service key that Amazon SageMaker uses to encrypt data on the storage volume attached to the ML compute instance that hosts the endpoint.
        """
        return pulumi.get(self, "kms_key_arn")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        The name of the endpoint configuration. If omitted, this provider will assign a random, unique name. Conflicts with `name_prefix`.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="namePrefix")
    def name_prefix(self) -> pulumi.Output[str]:
        """
        Creates a unique endpoint configuration name beginning with the specified prefix. Conflicts with `name`.
        """
        return pulumi.get(self, "name_prefix")

    @property
    @pulumi.getter(name="productionVariants")
    def production_variants(self) -> pulumi.Output[Sequence['outputs.EndpointConfigurationProductionVariant']]:
        """
        An list of ProductionVariant objects, one for each model that you want to host at this endpoint. Fields are documented below.
        """
        return pulumi.get(self, "production_variants")

    @property
    @pulumi.getter(name="shadowProductionVariants")
    def shadow_production_variants(self) -> pulumi.Output[Optional[Sequence['outputs.EndpointConfigurationShadowProductionVariant']]]:
        """
        Array of ProductionVariant objects. There is one for each model that you want to host at this endpoint in shadow mode with production traffic replicated from the model specified on ProductionVariants.If you use this field, you can only specify one variant for ProductionVariants and one variant for ShadowProductionVariants. Fields are documented below.
        """
        return pulumi.get(self, "shadow_production_variants")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A mapping of tags to assign to the resource. If configured with a provider `default_tags` configuration block present, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

