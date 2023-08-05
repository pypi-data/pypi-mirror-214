# coding=utf-8
# *** WARNING: this file was generated by the Pulumi Terraform Bridge (tfgen) Tool. ***
# *** Do not edit by hand unless you're certain you know what you are doing! ***

import copy
import warnings
import pulumi
import pulumi.runtime
from typing import Any, Mapping, Optional, Sequence, Union, overload
from .. import _utilities

__all__ = ['NamedQueryArgs', 'NamedQuery']

@pulumi.input_type
class NamedQueryArgs:
    def __init__(__self__, *,
                 database: pulumi.Input[str],
                 query: pulumi.Input[str],
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 workgroup: Optional[pulumi.Input[str]] = None):
        """
        The set of arguments for constructing a NamedQuery resource.
        :param pulumi.Input[str] database: Database to which the query belongs.
        :param pulumi.Input[str] query: Text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] description: Brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: Plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] workgroup: Workgroup to which the query belongs. Defaults to `primary`
        """
        pulumi.set(__self__, "database", database)
        pulumi.set(__self__, "query", query)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if workgroup is not None:
            pulumi.set(__self__, "workgroup", workgroup)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Input[str]:
        """
        Database to which the query belongs.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: pulumi.Input[str]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def query(self) -> pulumi.Input[str]:
        """
        Text of the query itself. In other words, all query statements. Maximum length of 262144.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: pulumi.Input[str]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Brief explanation of the query. Maximum length of 1024.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Plain language name for the query. Maximum length of 128.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def workgroup(self) -> Optional[pulumi.Input[str]]:
        """
        Workgroup to which the query belongs. Defaults to `primary`
        """
        return pulumi.get(self, "workgroup")

    @workgroup.setter
    def workgroup(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workgroup", value)


@pulumi.input_type
class _NamedQueryState:
    def __init__(__self__, *,
                 database: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 workgroup: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering NamedQuery resources.
        :param pulumi.Input[str] database: Database to which the query belongs.
        :param pulumi.Input[str] description: Brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: Plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: Text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: Workgroup to which the query belongs. Defaults to `primary`
        """
        if database is not None:
            pulumi.set(__self__, "database", database)
        if description is not None:
            pulumi.set(__self__, "description", description)
        if name is not None:
            pulumi.set(__self__, "name", name)
        if query is not None:
            pulumi.set(__self__, "query", query)
        if workgroup is not None:
            pulumi.set(__self__, "workgroup", workgroup)

    @property
    @pulumi.getter
    def database(self) -> Optional[pulumi.Input[str]]:
        """
        Database to which the query belongs.
        """
        return pulumi.get(self, "database")

    @database.setter
    def database(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "database", value)

    @property
    @pulumi.getter
    def description(self) -> Optional[pulumi.Input[str]]:
        """
        Brief explanation of the query. Maximum length of 1024.
        """
        return pulumi.get(self, "description")

    @description.setter
    def description(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "description", value)

    @property
    @pulumi.getter
    def name(self) -> Optional[pulumi.Input[str]]:
        """
        Plain language name for the query. Maximum length of 128.
        """
        return pulumi.get(self, "name")

    @name.setter
    def name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "name", value)

    @property
    @pulumi.getter
    def query(self) -> Optional[pulumi.Input[str]]:
        """
        Text of the query itself. In other words, all query statements. Maximum length of 262144.
        """
        return pulumi.get(self, "query")

    @query.setter
    def query(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "query", value)

    @property
    @pulumi.getter
    def workgroup(self) -> Optional[pulumi.Input[str]]:
        """
        Workgroup to which the query belongs. Defaults to `primary`
        """
        return pulumi.get(self, "workgroup")

    @workgroup.setter
    def workgroup(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "workgroup", value)


class NamedQuery(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 workgroup: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides an Athena Named Query resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket_v2 = aws.s3.BucketV2("hogeBucketV2")
        test_key = aws.kms.Key("testKey",
            deletion_window_in_days=7,
            description="Athena KMS Key")
        test_workgroup = aws.athena.Workgroup("testWorkgroup", configuration=aws.athena.WorkgroupConfigurationArgs(
            result_configuration=aws.athena.WorkgroupConfigurationResultConfigurationArgs(
                encryption_configuration=aws.athena.WorkgroupConfigurationResultConfigurationEncryptionConfigurationArgs(
                    encryption_option="SSE_KMS",
                    kms_key_arn=test_key.arn,
                ),
            ),
        ))
        hoge_database = aws.athena.Database("hogeDatabase",
            name="users",
            bucket=hoge_bucket_v2.id)
        foo = aws.athena.NamedQuery("foo",
            workgroup=test_workgroup.id,
            database=hoge_database.name,
            query=hoge_database.name.apply(lambda name: f"SELECT * FROM {name} limit 10;"))
        ```

        ## Import

        Athena Named Query can be imported using the query ID, e.g.,

        ```sh
         $ pulumi import aws:athena/namedQuery:NamedQuery example 0123456789
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: Database to which the query belongs.
        :param pulumi.Input[str] description: Brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: Plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: Text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: Workgroup to which the query belongs. Defaults to `primary`
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: NamedQueryArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides an Athena Named Query resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        hoge_bucket_v2 = aws.s3.BucketV2("hogeBucketV2")
        test_key = aws.kms.Key("testKey",
            deletion_window_in_days=7,
            description="Athena KMS Key")
        test_workgroup = aws.athena.Workgroup("testWorkgroup", configuration=aws.athena.WorkgroupConfigurationArgs(
            result_configuration=aws.athena.WorkgroupConfigurationResultConfigurationArgs(
                encryption_configuration=aws.athena.WorkgroupConfigurationResultConfigurationEncryptionConfigurationArgs(
                    encryption_option="SSE_KMS",
                    kms_key_arn=test_key.arn,
                ),
            ),
        ))
        hoge_database = aws.athena.Database("hogeDatabase",
            name="users",
            bucket=hoge_bucket_v2.id)
        foo = aws.athena.NamedQuery("foo",
            workgroup=test_workgroup.id,
            database=hoge_database.name,
            query=hoge_database.name.apply(lambda name: f"SELECT * FROM {name} limit 10;"))
        ```

        ## Import

        Athena Named Query can be imported using the query ID, e.g.,

        ```sh
         $ pulumi import aws:athena/namedQuery:NamedQuery example 0123456789
        ```

        :param str resource_name: The name of the resource.
        :param NamedQueryArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(NamedQueryArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 database: Optional[pulumi.Input[str]] = None,
                 description: Optional[pulumi.Input[str]] = None,
                 name: Optional[pulumi.Input[str]] = None,
                 query: Optional[pulumi.Input[str]] = None,
                 workgroup: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = NamedQueryArgs.__new__(NamedQueryArgs)

            if database is None and not opts.urn:
                raise TypeError("Missing required property 'database'")
            __props__.__dict__["database"] = database
            __props__.__dict__["description"] = description
            __props__.__dict__["name"] = name
            if query is None and not opts.urn:
                raise TypeError("Missing required property 'query'")
            __props__.__dict__["query"] = query
            __props__.__dict__["workgroup"] = workgroup
        super(NamedQuery, __self__).__init__(
            'aws:athena/namedQuery:NamedQuery',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            database: Optional[pulumi.Input[str]] = None,
            description: Optional[pulumi.Input[str]] = None,
            name: Optional[pulumi.Input[str]] = None,
            query: Optional[pulumi.Input[str]] = None,
            workgroup: Optional[pulumi.Input[str]] = None) -> 'NamedQuery':
        """
        Get an existing NamedQuery resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] database: Database to which the query belongs.
        :param pulumi.Input[str] description: Brief explanation of the query. Maximum length of 1024.
        :param pulumi.Input[str] name: Plain language name for the query. Maximum length of 128.
        :param pulumi.Input[str] query: Text of the query itself. In other words, all query statements. Maximum length of 262144.
        :param pulumi.Input[str] workgroup: Workgroup to which the query belongs. Defaults to `primary`
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _NamedQueryState.__new__(_NamedQueryState)

        __props__.__dict__["database"] = database
        __props__.__dict__["description"] = description
        __props__.__dict__["name"] = name
        __props__.__dict__["query"] = query
        __props__.__dict__["workgroup"] = workgroup
        return NamedQuery(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def database(self) -> pulumi.Output[str]:
        """
        Database to which the query belongs.
        """
        return pulumi.get(self, "database")

    @property
    @pulumi.getter
    def description(self) -> pulumi.Output[Optional[str]]:
        """
        Brief explanation of the query. Maximum length of 1024.
        """
        return pulumi.get(self, "description")

    @property
    @pulumi.getter
    def name(self) -> pulumi.Output[str]:
        """
        Plain language name for the query. Maximum length of 128.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter
    def query(self) -> pulumi.Output[str]:
        """
        Text of the query itself. In other words, all query statements. Maximum length of 262144.
        """
        return pulumi.get(self, "query")

    @property
    @pulumi.getter
    def workgroup(self) -> pulumi.Output[Optional[str]]:
        """
        Workgroup to which the query belongs. Defaults to `primary`
        """
        return pulumi.get(self, "workgroup")

