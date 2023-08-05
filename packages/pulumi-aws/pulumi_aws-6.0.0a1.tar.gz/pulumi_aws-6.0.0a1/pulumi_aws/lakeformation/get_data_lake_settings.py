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

__all__ = [
    'GetDataLakeSettingsResult',
    'AwaitableGetDataLakeSettingsResult',
    'get_data_lake_settings',
    'get_data_lake_settings_output',
]

@pulumi.output_type
class GetDataLakeSettingsResult:
    """
    A collection of values returned by getDataLakeSettings.
    """
    def __init__(__self__, admins=None, allow_external_data_filtering=None, authorized_session_tag_value_lists=None, catalog_id=None, create_database_default_permissions=None, create_table_default_permissions=None, external_data_filtering_allow_lists=None, id=None, trusted_resource_owners=None):
        if admins and not isinstance(admins, list):
            raise TypeError("Expected argument 'admins' to be a list")
        pulumi.set(__self__, "admins", admins)
        if allow_external_data_filtering and not isinstance(allow_external_data_filtering, bool):
            raise TypeError("Expected argument 'allow_external_data_filtering' to be a bool")
        pulumi.set(__self__, "allow_external_data_filtering", allow_external_data_filtering)
        if authorized_session_tag_value_lists and not isinstance(authorized_session_tag_value_lists, list):
            raise TypeError("Expected argument 'authorized_session_tag_value_lists' to be a list")
        pulumi.set(__self__, "authorized_session_tag_value_lists", authorized_session_tag_value_lists)
        if catalog_id and not isinstance(catalog_id, str):
            raise TypeError("Expected argument 'catalog_id' to be a str")
        pulumi.set(__self__, "catalog_id", catalog_id)
        if create_database_default_permissions and not isinstance(create_database_default_permissions, list):
            raise TypeError("Expected argument 'create_database_default_permissions' to be a list")
        pulumi.set(__self__, "create_database_default_permissions", create_database_default_permissions)
        if create_table_default_permissions and not isinstance(create_table_default_permissions, list):
            raise TypeError("Expected argument 'create_table_default_permissions' to be a list")
        pulumi.set(__self__, "create_table_default_permissions", create_table_default_permissions)
        if external_data_filtering_allow_lists and not isinstance(external_data_filtering_allow_lists, list):
            raise TypeError("Expected argument 'external_data_filtering_allow_lists' to be a list")
        pulumi.set(__self__, "external_data_filtering_allow_lists", external_data_filtering_allow_lists)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if trusted_resource_owners and not isinstance(trusted_resource_owners, list):
            raise TypeError("Expected argument 'trusted_resource_owners' to be a list")
        pulumi.set(__self__, "trusted_resource_owners", trusted_resource_owners)

    @property
    @pulumi.getter
    def admins(self) -> Sequence[str]:
        """
        List of ARNs of AWS Lake Formation principals (IAM users or roles).
        """
        return pulumi.get(self, "admins")

    @property
    @pulumi.getter(name="allowExternalDataFiltering")
    def allow_external_data_filtering(self) -> bool:
        """
        Whether to allow Amazon EMR clusters to access data managed by Lake Formation.
        """
        return pulumi.get(self, "allow_external_data_filtering")

    @property
    @pulumi.getter(name="authorizedSessionTagValueLists")
    def authorized_session_tag_value_lists(self) -> Sequence[str]:
        """
        Lake Formation relies on a privileged process secured by Amazon EMR or the third party integrator to tag the user's role while assuming it.
        """
        return pulumi.get(self, "authorized_session_tag_value_lists")

    @property
    @pulumi.getter(name="catalogId")
    def catalog_id(self) -> Optional[str]:
        return pulumi.get(self, "catalog_id")

    @property
    @pulumi.getter(name="createDatabaseDefaultPermissions")
    def create_database_default_permissions(self) -> Sequence['outputs.GetDataLakeSettingsCreateDatabaseDefaultPermissionResult']:
        """
        Up to three configuration blocks of principal permissions for default create database permissions. Detailed below.
        """
        return pulumi.get(self, "create_database_default_permissions")

    @property
    @pulumi.getter(name="createTableDefaultPermissions")
    def create_table_default_permissions(self) -> Sequence['outputs.GetDataLakeSettingsCreateTableDefaultPermissionResult']:
        """
        Up to three configuration blocks of principal permissions for default create table permissions. Detailed below.
        """
        return pulumi.get(self, "create_table_default_permissions")

    @property
    @pulumi.getter(name="externalDataFilteringAllowLists")
    def external_data_filtering_allow_lists(self) -> Sequence[str]:
        """
        A list of the account IDs of Amazon Web Services accounts with Amazon EMR clusters that are to perform data filtering.
        """
        return pulumi.get(self, "external_data_filtering_allow_lists")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="trustedResourceOwners")
    def trusted_resource_owners(self) -> Sequence[str]:
        """
        List of the resource-owning account IDs that the caller's account can use to share their user access details (user ARNs).
        """
        return pulumi.get(self, "trusted_resource_owners")


class AwaitableGetDataLakeSettingsResult(GetDataLakeSettingsResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetDataLakeSettingsResult(
            admins=self.admins,
            allow_external_data_filtering=self.allow_external_data_filtering,
            authorized_session_tag_value_lists=self.authorized_session_tag_value_lists,
            catalog_id=self.catalog_id,
            create_database_default_permissions=self.create_database_default_permissions,
            create_table_default_permissions=self.create_table_default_permissions,
            external_data_filtering_allow_lists=self.external_data_filtering_allow_lists,
            id=self.id,
            trusted_resource_owners=self.trusted_resource_owners)


def get_data_lake_settings(catalog_id: Optional[str] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetDataLakeSettingsResult:
    """
    Get Lake Formation principals designated as data lake administrators and lists of principal permission entries for default create database and default create table permissions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.lakeformation.get_data_lake_settings(catalog_id="14916253649")
    ```


    :param str catalog_id: Identifier for the Data Catalog. By default, the account ID.
    """
    __args__ = dict()
    __args__['catalogId'] = catalog_id
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:lakeformation/getDataLakeSettings:getDataLakeSettings', __args__, opts=opts, typ=GetDataLakeSettingsResult).value

    return AwaitableGetDataLakeSettingsResult(
        admins=__ret__.admins,
        allow_external_data_filtering=__ret__.allow_external_data_filtering,
        authorized_session_tag_value_lists=__ret__.authorized_session_tag_value_lists,
        catalog_id=__ret__.catalog_id,
        create_database_default_permissions=__ret__.create_database_default_permissions,
        create_table_default_permissions=__ret__.create_table_default_permissions,
        external_data_filtering_allow_lists=__ret__.external_data_filtering_allow_lists,
        id=__ret__.id,
        trusted_resource_owners=__ret__.trusted_resource_owners)


@_utilities.lift_output_func(get_data_lake_settings)
def get_data_lake_settings_output(catalog_id: Optional[pulumi.Input[Optional[str]]] = None,
                                  opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetDataLakeSettingsResult]:
    """
    Get Lake Formation principals designated as data lake administrators and lists of principal permission entries for default create database and default create table permissions.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.lakeformation.get_data_lake_settings(catalog_id="14916253649")
    ```


    :param str catalog_id: Identifier for the Data Catalog. By default, the account ID.
    """
    ...
