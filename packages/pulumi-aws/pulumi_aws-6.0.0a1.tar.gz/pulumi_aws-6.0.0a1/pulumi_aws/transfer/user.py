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

__all__ = ['UserArgs', 'User']

@pulumi.input_type
class UserArgs:
    def __init__(__self__, *,
                 role: pulumi.Input[str],
                 server_id: pulumi.Input[str],
                 user_name: pulumi.Input[str],
                 home_directory: Optional[pulumi.Input[str]] = None,
                 home_directory_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]] = None,
                 home_directory_type: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 posix_profile: Optional[pulumi.Input['UserPosixProfileArgs']] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None):
        """
        The set of arguments for constructing a User resource.
        :param pulumi.Input[str] role: Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        :param pulumi.Input[str] server_id: The Server ID of the Transfer Server (e.g., `s-12345678`)
        :param pulumi.Input[str] user_name: The name used for log in to your SFTP server.
        :param pulumi.Input[str] home_directory: The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        :param pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]] home_directory_mappings: Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        :param pulumi.Input[str] home_directory_type: The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        :param pulumi.Input[str] policy: An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        :param pulumi.Input['UserPosixProfileArgs'] posix_profile: Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        """
        pulumi.set(__self__, "role", role)
        pulumi.set(__self__, "server_id", server_id)
        pulumi.set(__self__, "user_name", user_name)
        if home_directory is not None:
            pulumi.set(__self__, "home_directory", home_directory)
        if home_directory_mappings is not None:
            pulumi.set(__self__, "home_directory_mappings", home_directory_mappings)
        if home_directory_type is not None:
            pulumi.set(__self__, "home_directory_type", home_directory_type)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if posix_profile is not None:
            pulumi.set(__self__, "posix_profile", posix_profile)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)

    @property
    @pulumi.getter
    def role(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: pulumi.Input[str]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Input[str]:
        """
        The Server ID of the Transfer Server (e.g., `s-12345678`)
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: pulumi.Input[str]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Input[str]:
        """
        The name used for log in to your SFTP server.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: pulumi.Input[str]):
        pulumi.set(self, "user_name", value)

    @property
    @pulumi.getter(name="homeDirectory")
    def home_directory(self) -> Optional[pulumi.Input[str]]:
        """
        The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        """
        return pulumi.get(self, "home_directory")

    @home_directory.setter
    def home_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "home_directory", value)

    @property
    @pulumi.getter(name="homeDirectoryMappings")
    def home_directory_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]]:
        """
        Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        """
        return pulumi.get(self, "home_directory_mappings")

    @home_directory_mappings.setter
    def home_directory_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]]):
        pulumi.set(self, "home_directory_mappings", value)

    @property
    @pulumi.getter(name="homeDirectoryType")
    def home_directory_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        """
        return pulumi.get(self, "home_directory_type")

    @home_directory_type.setter
    def home_directory_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "home_directory_type", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="posixProfile")
    def posix_profile(self) -> Optional[pulumi.Input['UserPosixProfileArgs']]:
        """
        Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        """
        return pulumi.get(self, "posix_profile")

    @posix_profile.setter
    def posix_profile(self, value: Optional[pulumi.Input['UserPosixProfileArgs']]):
        pulumi.set(self, "posix_profile", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @tags.setter
    def tags(self, value: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]):
        pulumi.set(self, "tags", value)


@pulumi.input_type
class _UserState:
    def __init__(__self__, *,
                 arn: Optional[pulumi.Input[str]] = None,
                 home_directory: Optional[pulumi.Input[str]] = None,
                 home_directory_mappings: Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]] = None,
                 home_directory_type: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 posix_profile: Optional[pulumi.Input['UserPosixProfileArgs']] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None):
        """
        Input properties used for looking up and filtering User resources.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of Transfer User
        :param pulumi.Input[str] home_directory: The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        :param pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]] home_directory_mappings: Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        :param pulumi.Input[str] home_directory_type: The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        :param pulumi.Input[str] policy: An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        :param pulumi.Input['UserPosixProfileArgs'] posix_profile: Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        :param pulumi.Input[str] role: Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        :param pulumi.Input[str] server_id: The Server ID of the Transfer Server (e.g., `s-12345678`)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_name: The name used for log in to your SFTP server.
        """
        if arn is not None:
            pulumi.set(__self__, "arn", arn)
        if home_directory is not None:
            pulumi.set(__self__, "home_directory", home_directory)
        if home_directory_mappings is not None:
            pulumi.set(__self__, "home_directory_mappings", home_directory_mappings)
        if home_directory_type is not None:
            pulumi.set(__self__, "home_directory_type", home_directory_type)
        if policy is not None:
            pulumi.set(__self__, "policy", policy)
        if posix_profile is not None:
            pulumi.set(__self__, "posix_profile", posix_profile)
        if role is not None:
            pulumi.set(__self__, "role", role)
        if server_id is not None:
            pulumi.set(__self__, "server_id", server_id)
        if tags is not None:
            pulumi.set(__self__, "tags", tags)
        if tags_all is not None:
            pulumi.set(__self__, "tags_all", tags_all)
        if user_name is not None:
            pulumi.set(__self__, "user_name", user_name)

    @property
    @pulumi.getter
    def arn(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of Transfer User
        """
        return pulumi.get(self, "arn")

    @arn.setter
    def arn(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "arn", value)

    @property
    @pulumi.getter(name="homeDirectory")
    def home_directory(self) -> Optional[pulumi.Input[str]]:
        """
        The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        """
        return pulumi.get(self, "home_directory")

    @home_directory.setter
    def home_directory(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "home_directory", value)

    @property
    @pulumi.getter(name="homeDirectoryMappings")
    def home_directory_mappings(self) -> Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]]:
        """
        Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        """
        return pulumi.get(self, "home_directory_mappings")

    @home_directory_mappings.setter
    def home_directory_mappings(self, value: Optional[pulumi.Input[Sequence[pulumi.Input['UserHomeDirectoryMappingArgs']]]]):
        pulumi.set(self, "home_directory_mappings", value)

    @property
    @pulumi.getter(name="homeDirectoryType")
    def home_directory_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        """
        return pulumi.get(self, "home_directory_type")

    @home_directory_type.setter
    def home_directory_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "home_directory_type", value)

    @property
    @pulumi.getter
    def policy(self) -> Optional[pulumi.Input[str]]:
        """
        An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        """
        return pulumi.get(self, "policy")

    @policy.setter
    def policy(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "policy", value)

    @property
    @pulumi.getter(name="posixProfile")
    def posix_profile(self) -> Optional[pulumi.Input['UserPosixProfileArgs']]:
        """
        Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        """
        return pulumi.get(self, "posix_profile")

    @posix_profile.setter
    def posix_profile(self, value: Optional[pulumi.Input['UserPosixProfileArgs']]):
        pulumi.set(self, "posix_profile", value)

    @property
    @pulumi.getter
    def role(self) -> Optional[pulumi.Input[str]]:
        """
        Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        """
        return pulumi.get(self, "role")

    @role.setter
    def role(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "role", value)

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> Optional[pulumi.Input[str]]:
        """
        The Server ID of the Transfer Server (e.g., `s-12345678`)
        """
        return pulumi.get(self, "server_id")

    @server_id.setter
    def server_id(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "server_id", value)

    @property
    @pulumi.getter
    def tags(self) -> Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
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

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> Optional[pulumi.Input[str]]:
        """
        The name used for log in to your SFTP server.
        """
        return pulumi.get(self, "user_name")

    @user_name.setter
    def user_name(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "user_name", value)


class User(pulumi.CustomResource):
    @overload
    def __init__(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 home_directory: Optional[pulumi.Input[str]] = None,
                 home_directory_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserHomeDirectoryMappingArgs']]]]] = None,
                 home_directory_type: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 posix_profile: Optional[pulumi.Input[pulumi.InputType['UserPosixProfileArgs']]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        """
        Provides a AWS Transfer User resource. Managing SSH keys can be accomplished with the `transfer.SshKey` resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo_server = aws.transfer.Server("fooServer",
            identity_provider_type="SERVICE_MANAGED",
            tags={
                "NAME": "tf-acc-test-transfer-server",
            })
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["transfer.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        foo_role = aws.iam.Role("fooRole", assume_role_policy=assume_role.json)
        foo_policy_document = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            sid="AllowFullAccesstoS3",
            effect="Allow",
            actions=["s3:*"],
            resources=["*"],
        )])
        foo_role_policy = aws.iam.RolePolicy("fooRolePolicy",
            role=foo_role.id,
            policy=foo_policy_document.json)
        foo_user = aws.transfer.User("fooUser",
            server_id=foo_server.id,
            user_name="tftestuser",
            role=foo_role.arn,
            home_directory_type="LOGICAL",
            home_directory_mappings=[aws.transfer.UserHomeDirectoryMappingArgs(
                entry="/test.pdf",
                target="/bucket3/test-path/tftestuser.pdf",
            )])
        ```

        ## Import

        Transfer Users can be imported using the `server_id` and `user_name` separated by `/`.

        ```sh
         $ pulumi import aws:transfer/user:User bar s-12345678/test-username
        ```

        :param str resource_name: The name of the resource.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] home_directory: The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserHomeDirectoryMappingArgs']]]] home_directory_mappings: Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        :param pulumi.Input[str] home_directory_type: The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        :param pulumi.Input[str] policy: An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        :param pulumi.Input[pulumi.InputType['UserPosixProfileArgs']] posix_profile: Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        :param pulumi.Input[str] role: Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        :param pulumi.Input[str] server_id: The Server ID of the Transfer Server (e.g., `s-12345678`)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[str] user_name: The name used for log in to your SFTP server.
        """
        ...
    @overload
    def __init__(__self__,
                 resource_name: str,
                 args: UserArgs,
                 opts: Optional[pulumi.ResourceOptions] = None):
        """
        Provides a AWS Transfer User resource. Managing SSH keys can be accomplished with the `transfer.SshKey` resource.

        ## Example Usage

        ```python
        import pulumi
        import pulumi_aws as aws

        foo_server = aws.transfer.Server("fooServer",
            identity_provider_type="SERVICE_MANAGED",
            tags={
                "NAME": "tf-acc-test-transfer-server",
            })
        assume_role = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                type="Service",
                identifiers=["transfer.amazonaws.com"],
            )],
            actions=["sts:AssumeRole"],
        )])
        foo_role = aws.iam.Role("fooRole", assume_role_policy=assume_role.json)
        foo_policy_document = aws.iam.get_policy_document(statements=[aws.iam.GetPolicyDocumentStatementArgs(
            sid="AllowFullAccesstoS3",
            effect="Allow",
            actions=["s3:*"],
            resources=["*"],
        )])
        foo_role_policy = aws.iam.RolePolicy("fooRolePolicy",
            role=foo_role.id,
            policy=foo_policy_document.json)
        foo_user = aws.transfer.User("fooUser",
            server_id=foo_server.id,
            user_name="tftestuser",
            role=foo_role.arn,
            home_directory_type="LOGICAL",
            home_directory_mappings=[aws.transfer.UserHomeDirectoryMappingArgs(
                entry="/test.pdf",
                target="/bucket3/test-path/tftestuser.pdf",
            )])
        ```

        ## Import

        Transfer Users can be imported using the `server_id` and `user_name` separated by `/`.

        ```sh
         $ pulumi import aws:transfer/user:User bar s-12345678/test-username
        ```

        :param str resource_name: The name of the resource.
        :param UserArgs args: The arguments to use to populate this resource's properties.
        :param pulumi.ResourceOptions opts: Options for the resource.
        """
        ...
    def __init__(__self__, resource_name: str, *args, **kwargs):
        resource_args, opts = _utilities.get_resource_args_opts(UserArgs, pulumi.ResourceOptions, *args, **kwargs)
        if resource_args is not None:
            __self__._internal_init(resource_name, opts, **resource_args.__dict__)
        else:
            __self__._internal_init(resource_name, *args, **kwargs)

    def _internal_init(__self__,
                 resource_name: str,
                 opts: Optional[pulumi.ResourceOptions] = None,
                 home_directory: Optional[pulumi.Input[str]] = None,
                 home_directory_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserHomeDirectoryMappingArgs']]]]] = None,
                 home_directory_type: Optional[pulumi.Input[str]] = None,
                 policy: Optional[pulumi.Input[str]] = None,
                 posix_profile: Optional[pulumi.Input[pulumi.InputType['UserPosixProfileArgs']]] = None,
                 role: Optional[pulumi.Input[str]] = None,
                 server_id: Optional[pulumi.Input[str]] = None,
                 tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
                 user_name: Optional[pulumi.Input[str]] = None,
                 __props__=None):
        opts = pulumi.ResourceOptions.merge(_utilities.get_resource_opts_defaults(), opts)
        if not isinstance(opts, pulumi.ResourceOptions):
            raise TypeError('Expected resource options to be a ResourceOptions instance')
        if opts.id is None:
            if __props__ is not None:
                raise TypeError('__props__ is only valid when passed in combination with a valid opts.id to get an existing resource')
            __props__ = UserArgs.__new__(UserArgs)

            __props__.__dict__["home_directory"] = home_directory
            __props__.__dict__["home_directory_mappings"] = home_directory_mappings
            __props__.__dict__["home_directory_type"] = home_directory_type
            __props__.__dict__["policy"] = policy
            __props__.__dict__["posix_profile"] = posix_profile
            if role is None and not opts.urn:
                raise TypeError("Missing required property 'role'")
            __props__.__dict__["role"] = role
            if server_id is None and not opts.urn:
                raise TypeError("Missing required property 'server_id'")
            __props__.__dict__["server_id"] = server_id
            __props__.__dict__["tags"] = tags
            if user_name is None and not opts.urn:
                raise TypeError("Missing required property 'user_name'")
            __props__.__dict__["user_name"] = user_name
            __props__.__dict__["arn"] = None
            __props__.__dict__["tags_all"] = None
        super(User, __self__).__init__(
            'aws:transfer/user:User',
            resource_name,
            __props__,
            opts)

    @staticmethod
    def get(resource_name: str,
            id: pulumi.Input[str],
            opts: Optional[pulumi.ResourceOptions] = None,
            arn: Optional[pulumi.Input[str]] = None,
            home_directory: Optional[pulumi.Input[str]] = None,
            home_directory_mappings: Optional[pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserHomeDirectoryMappingArgs']]]]] = None,
            home_directory_type: Optional[pulumi.Input[str]] = None,
            policy: Optional[pulumi.Input[str]] = None,
            posix_profile: Optional[pulumi.Input[pulumi.InputType['UserPosixProfileArgs']]] = None,
            role: Optional[pulumi.Input[str]] = None,
            server_id: Optional[pulumi.Input[str]] = None,
            tags: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            tags_all: Optional[pulumi.Input[Mapping[str, pulumi.Input[str]]]] = None,
            user_name: Optional[pulumi.Input[str]] = None) -> 'User':
        """
        Get an existing User resource's state with the given name, id, and optional extra
        properties used to qualify the lookup.

        :param str resource_name: The unique name of the resulting resource.
        :param pulumi.Input[str] id: The unique provider ID of the resource to lookup.
        :param pulumi.ResourceOptions opts: Options for the resource.
        :param pulumi.Input[str] arn: Amazon Resource Name (ARN) of Transfer User
        :param pulumi.Input[str] home_directory: The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        :param pulumi.Input[Sequence[pulumi.Input[pulumi.InputType['UserHomeDirectoryMappingArgs']]]] home_directory_mappings: Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        :param pulumi.Input[str] home_directory_type: The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        :param pulumi.Input[str] policy: An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        :param pulumi.Input[pulumi.InputType['UserPosixProfileArgs']] posix_profile: Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        :param pulumi.Input[str] role: Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        :param pulumi.Input[str] server_id: The Server ID of the Transfer Server (e.g., `s-12345678`)
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags: A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        :param pulumi.Input[Mapping[str, pulumi.Input[str]]] tags_all: A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        :param pulumi.Input[str] user_name: The name used for log in to your SFTP server.
        """
        opts = pulumi.ResourceOptions.merge(opts, pulumi.ResourceOptions(id=id))

        __props__ = _UserState.__new__(_UserState)

        __props__.__dict__["arn"] = arn
        __props__.__dict__["home_directory"] = home_directory
        __props__.__dict__["home_directory_mappings"] = home_directory_mappings
        __props__.__dict__["home_directory_type"] = home_directory_type
        __props__.__dict__["policy"] = policy
        __props__.__dict__["posix_profile"] = posix_profile
        __props__.__dict__["role"] = role
        __props__.__dict__["server_id"] = server_id
        __props__.__dict__["tags"] = tags
        __props__.__dict__["tags_all"] = tags_all
        __props__.__dict__["user_name"] = user_name
        return User(resource_name, opts=opts, __props__=__props__)

    @property
    @pulumi.getter
    def arn(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of Transfer User
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="homeDirectory")
    def home_directory(self) -> pulumi.Output[Optional[str]]:
        """
        The landing directory (folder) for a user when they log in to the server using their SFTP client.  It should begin with a `/`.  The first item in the path is the name of the home bucket (accessible as `${Transfer:HomeBucket}` in the policy) and the rest is the home directory (accessible as `${Transfer:HomeDirectory}` in the policy). For example, `/example-bucket-1234/username` would set the home bucket to `example-bucket-1234` and the home directory to `username`.
        """
        return pulumi.get(self, "home_directory")

    @property
    @pulumi.getter(name="homeDirectoryMappings")
    def home_directory_mappings(self) -> pulumi.Output[Optional[Sequence['outputs.UserHomeDirectoryMapping']]]:
        """
        Logical directory mappings that specify what S3 paths and keys should be visible to your user and how you want to make them visible. See Home Directory Mappings below.
        """
        return pulumi.get(self, "home_directory_mappings")

    @property
    @pulumi.getter(name="homeDirectoryType")
    def home_directory_type(self) -> pulumi.Output[Optional[str]]:
        """
        The type of landing directory (folder) you mapped for your users' home directory. Valid values are `PATH` and `LOGICAL`.
        """
        return pulumi.get(self, "home_directory_type")

    @property
    @pulumi.getter
    def policy(self) -> pulumi.Output[Optional[str]]:
        """
        An IAM JSON policy document that scopes down user access to portions of their Amazon S3 bucket. IAM variables you can use inside this policy include `${Transfer:UserName}`, `${Transfer:HomeDirectory}`, and `${Transfer:HomeBucket}`. These are evaluated on-the-fly when navigating the bucket.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="posixProfile")
    def posix_profile(self) -> pulumi.Output[Optional['outputs.UserPosixProfile']]:
        """
        Specifies the full POSIX identity, including user ID (Uid), group ID (Gid), and any secondary groups IDs (SecondaryGids), that controls your users' access to your Amazon EFS file systems. See Posix Profile below.
        """
        return pulumi.get(self, "posix_profile")

    @property
    @pulumi.getter
    def role(self) -> pulumi.Output[str]:
        """
        Amazon Resource Name (ARN) of an IAM role that allows the service to control your user’s access to your Amazon S3 bucket.
        """
        return pulumi.get(self, "role")

    @property
    @pulumi.getter(name="serverId")
    def server_id(self) -> pulumi.Output[str]:
        """
        The Server ID of the Transfer Server (e.g., `s-12345678`)
        """
        return pulumi.get(self, "server_id")

    @property
    @pulumi.getter
    def tags(self) -> pulumi.Output[Optional[Mapping[str, str]]]:
        """
        A map of tags to assign to the resource. If configured with a provider `default_tags` configuration block, tags with matching keys will overwrite those defined at the provider-level.
        """
        return pulumi.get(self, "tags")

    @property
    @pulumi.getter(name="tagsAll")
    def tags_all(self) -> pulumi.Output[Mapping[str, str]]:
        """
        A map of tags assigned to the resource, including those inherited from the provider `default_tags` configuration block.
        """
        return pulumi.get(self, "tags_all")

    @property
    @pulumi.getter(name="userName")
    def user_name(self) -> pulumi.Output[str]:
        """
        The name used for log in to your SFTP server.
        """
        return pulumi.get(self, "user_name")

