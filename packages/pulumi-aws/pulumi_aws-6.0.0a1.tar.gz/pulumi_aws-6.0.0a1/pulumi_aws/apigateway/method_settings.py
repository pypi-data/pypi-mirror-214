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

__all__ = ['MethodSettingsArgs', 'MethodSettings']

@pulumi.input_type
class MethodSettingsArgs:
    def __init__(__self__, *,
                 method_path: pulumi.Input[str],
                 rest_api: pulumi.Input[str],
                 settings: pulumi.Input['MethodSettingsSettingsArgs'],
                 stage_name: pulumi.Input[str]):
        """
        The set of arguments for constructing a MethodSettings resource.
        :param pulumi.Input[str] method_path: Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        :param pulumi.Input[str] rest_api: ID of the REST API
        :param pulumi.Input['MethodSettingsSettingsArgs'] settings: Settings block, see below.
        :param pulumi.Input[str] stage_name: Name of the stage
        """
        pulumi.set(__self__, "method_path", method_path)
        pulumi.set(__self__, "rest_api", rest_api)
        pulumi.set(__self__, "settings", settings)
        pulumi.set(__self__, "stage_name", stage_name)

    @property
    @pulumi.getter(name="methodPath")
    def method_path(self) -> pulumi.Input[str]:
        """
        Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        """
        return pulumi.get(self, "method_path")

    @method_path.setter
    def method_path(self, value: pulumi.Input[str]):
        pulumi.set(self, "method_path", value)

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Input[str]:
        """
        ID of the REST API
        """
        return pulumi.get(self, "rest_api")

    @rest_api.setter
    def rest_api(self, value: pulumi.Input[str]):
        pulumi.set(self, "rest_api", value)

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Input['MethodSettingsSettingsArgs']:
        """
        Settings block, see below.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: pulumi.Input['MethodSettingsSettingsArgs']):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> pulumi.Input[str]:
        """
        Name of the stage
        """
        return pulumi.get(self, "stage_name")

    @stage_name.setter
    def stage_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "stage_name", value)


@pulumi.input_type
class _MethodSettingsState:
    def __init__(__self__, *,
                 method_path: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input['MethodSettingsSettingsArgs']] = None,
                 stage_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering MethodSettings resources.
        :param pulumi.Input[str] method_path: Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        :param pulumi.Input[str] rest_api: ID of the REST API
        :param pulumi.Input['MethodSettingsSettingsArgs'] settings: Settings block, see below.
        :param pulumi.Input[str] stage_name: Name of the stage
        """
        if method_path is not None:
            pulumi.set(__self__, "method_path", method_path)
        if rest_api is not None:
            pulumi.set(__self__, "rest_api", rest_api)
        if settings is not None:
            pulumi.set(__self__, "settings", settings)
        if stage_name is not None:
            pulumi.set(__self__, "stage_name", stage_name)

    @property
    @pulumi.getter(name="methodPath")
    def method_path(self) -> Optional[pulumi.Input[str]]:
        """
        Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        """
        return pulumi.get(self, "method_path")

    @method_path.setter
    def method_path(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "method_path", value)

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> Optional[pulumi.Input[str]]:
        """
        ID of the REST API
        """
        return pulumi.get(self, "rest_api")

    @rest_api.setter
    def rest_api(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rest_api", value)

    @property
    @pulumi.getter
    def settings(self) -> Optional[pulumi.Input['MethodSettingsSettingsArgs']]:
        """
        Settings block, see below.
        """
        return pulumi.get(self, "settings")

    @settings.setter
    def settings(self, value: Optional[pulumi.Input['MethodSettingsSettingsArgs']]):
        pulumi.set(self, "settings", value)

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> Optional[pulumi.Input[str]]:
        """
        Name of the stage
        """
        return pulumi.get(self, "stage_name")

    @stage_name.setter
    def stage_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "stage_name", value)


class MethodSettings(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 method_path: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[pulumi.InputType['MethodSettingsSettingsArgs']]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Manages API Gateway Stage Method Settings. For example, CloudWatch logging and metrics.

        > **NOTE:** We recommend using this resource in conjunction with the `apigateway.Stage` resource instead of a stage managed by the `apigateway.Deployment` resource optional `stage_name` argument. Stages managed by the `apigateway.Deployment` resource are recreated on redeployment and this resource will require a second apply to recreate the method settings.

        ## Example Usage

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi", body=json.dumps({
            "openapi": "3.0.1",
            "info": {
                "title": "example",
                "version": "1.0",
            },
            "paths": {
                "/path1": {
                    "get": {
                        "x-amazon-apigateway-integration": {
                            "httpMethod": "GET",
                            "payloadFormatVersion": "1.0",
                            "type": "HTTP_PROXY",
                            "uri": "https://ip-ranges.amazonaws.com/ip-ranges.json",
                        },
                    },
                },
            },
        }))
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": example_rest_api.body.apply(lambda body: json.dumps(body)).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        all = aws.apigateway.MethodSettings("all",
            rest_api=example_rest_api.id,
            stage_name=example_stage.stage_name,
            method_path="*/*",
            settings=aws.apigateway.MethodSettingsSettingsArgs(
                metrics_enabled=True,
                logging_level="ERROR",
            ))
        path_specific = aws.apigateway.MethodSettings("pathSpecific",
            rest_api=example_rest_api.id,
            stage_name=example_stage.stage_name,
            method_path="path1/GET",
            settings=aws.apigateway.MethodSettingsSettingsArgs(
                metrics_enabled=True,
                logging_level="INFO",
            ))
        ```

        ## Import

        `aws_api_gateway_method_settings` can be imported using `REST-API-ID/STAGE-NAME/METHOD-PATH`, e.g.,

        ```sh
         $ pulumi import aws:apigateway/methodSettings:MethodSettings example 12345abcde/example/test/GET
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] method_path: Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        :param pulumi.Input[str] rest_api: ID of the REST API
        :param pulumi.Input[pulumi.InputType['MethodSettingsSettingsArgs']] settings: Settings block, see below.
        :param pulumi.Input[str] stage_name: Name of the stage
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: MethodSettingsArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Manages API Gateway Stage Method Settings. For example, CloudWatch logging and metrics.

        > **NOTE:** We recommend using this resource in conjunction with the `apigateway.Stage` resource instead of a stage managed by the `apigateway.Deployment` resource optional `stage_name` argument. Stages managed by the `apigateway.Deployment` resource are recreated on redeployment and this resource will require a second apply to recreate the method settings.

        ## Example Usage

        ```python
        import pulumi
        import hashlib
        import json
        import pulumi_aws as aws

        example_rest_api = aws.apigateway.RestApi("exampleRestApi", body=json.dumps({
            "openapi": "3.0.1",
            "info": {
                "title": "example",
                "version": "1.0",
            },
            "paths": {
                "/path1": {
                    "get": {
                        "x-amazon-apigateway-integration": {
                            "httpMethod": "GET",
                            "payloadFormatVersion": "1.0",
                            "type": "HTTP_PROXY",
                            "uri": "https://ip-ranges.amazonaws.com/ip-ranges.json",
                        },
                    },
                },
            },
        }))
        example_deployment = aws.apigateway.Deployment("exampleDeployment",
            rest_api=example_rest_api.id,
            triggers={
                "redeployment": example_rest_api.body.apply(lambda body: json.dumps(body)).apply(lambda to_json: hashlib.sha1(to_json.encode()).hexdigest()),
            })
        example_stage = aws.apigateway.Stage("exampleStage",
            deployment=example_deployment.id,
            rest_api=example_rest_api.id,
            stage_name="example")
        all = aws.apigateway.MethodSettings("all",
            rest_api=example_rest_api.id,
            stage_name=example_stage.stage_name,
            method_path="*/*",
            settings=aws.apigateway.MethodSettingsSettingsArgs(
                metrics_enabled=True,
                logging_level="ERROR",
            ))
        path_specific = aws.apigateway.MethodSettings("pathSpecific",
            rest_api=example_rest_api.id,
            stage_name=example_stage.stage_name,
            method_path="path1/GET",
            settings=aws.apigateway.MethodSettingsSettingsArgs(
                metrics_enabled=True,
                logging_level="INFO",
            ))
        ```

        ## Import

        `aws_api_gateway_method_settings` can be imported using `REST-API-ID/STAGE-NAME/METHOD-PATH`, e.g.,

        ```sh
         $ pulumi import aws:apigateway/methodSettings:MethodSettings example 12345abcde/example/test/GET
        ```

        :param str resource_name: The name of the resource.
        :param MethodSettingsArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(MethodSettingsArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 method_path: Optional[pulumi.Input[str]] = None,
                 rest_api: Optional[pulumi.Input[str]] = None,
                 settings: Optional[pulumi.Input[pulumi.InputType['MethodSettingsSettingsArgs']]] = None,
                 stage_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = MethodSettingsArgs.__new__(MethodSettingsArgs)

            if method_path is None and not opts.urn:
                raise TypeError("Missing required property 'method_path'")
            __props__.__dict__["method_path"] = method_path
            if rest_api is None and not opts.urn:
                raise TypeError("Missing required property 'rest_api'")
            __props__.__dict__["rest_api"] = rest_api
            if settings is None and not opts.urn:
                raise TypeError("Missing required property 'settings'")
            __props__.__dict__["settings"] = settings
            if stage_name is None and not opts.urn:
                raise TypeError("Missing required property 'stage_name'")
            __props__.__dict__["stage_name"] = stage_name
        super(MethodSettings, __self__).__init__(
            'aws:apigateway/methodSettings:MethodSettings',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            method_path: Optional[pulumi.Input[str]] = None,
            rest_api: Optional[pulumi.Input[str]] = None,
            settings: Optional[pulumi.Input[pulumi.InputType['MethodSettingsSettingsArgs']]] = None,
            stage_name: Optional[pulumi.Input[str]] = None) -> 'MethodSettings':
        """
        Get an existing MethodSettings resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] method_path: Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        :param pulumi.Input[str] rest_api: ID of the REST API
        :param pulumi.Input[pulumi.InputType['MethodSettingsSettingsArgs']] settings: Settings block, see below.
        :param pulumi.Input[str] stage_name: Name of the stage
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _MethodSettingsState.__new__(_MethodSettingsState)

        __props__.__dict__["method_path"] = method_path
        __props__.__dict__["rest_api"] = rest_api
        __props__.__dict__["settings"] = settings
        __props__.__dict__["stage_name"] = stage_name
        return MethodSettings(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter(name="methodPath")
    def method_path(self) -> pulumi.Output[str]:
        """
        Method path defined as `{resource_path}/{http_method}` for an individual method override, or `*/*` for overriding all methods in the stage. Ensure to trim any leading forward slashes in the path (e.g., `trimprefix(aws_api_gateway_resource.example.path, "/")`).
        """
        return pulumi.get(self, "method_path")

    @property
    @pulumi.getter(name="restApi")
    def rest_api(self) -> pulumi.Output[str]:
        """
        ID of the REST API
        """
        return pulumi.get(self, "rest_api")

    @property
    @pulumi.getter
    def settings(self) -> pulumi.Output['outputs.MethodSettingsSettings']:
        """
        Settings block, see below.
        """
        return pulumi.get(self, "settings")

    @property
    @pulumi.getter(name="stageName")
    def stage_name(self) -> pulumi.Output[str]:
        """
        Name of the stage
        """
        return pulumi.get(self, "stage_name")

