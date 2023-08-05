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
    'GetLaunchConfigurationResult',
    'AwaitableGetLaunchConfigurationResult',
    'get_launch_configuration',
    'get_launch_configuration_output',
]

@pulumi.output_type
class GetLaunchConfigurationResult:
    """
    A collection of values returned by getLaunchConfiguration.
    """
    def __init__(__self__, arn=None, associate_public_ip_address=None, ebs_block_devices=None, ebs_optimized=None, enable_monitoring=None, ephemeral_block_devices=None, iam_instance_profile=None, id=None, image_id=None, instance_type=None, key_name=None, metadata_options=None, name=None, placement_tenancy=None, root_block_devices=None, security_groups=None, spot_price=None, user_data=None):
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if associate_public_ip_address and not isinstance(associate_public_ip_address, bool):
            raise TypeError("Expected argument 'associate_public_ip_address' to be a bool")
        pulumi.set(__self__, "associate_public_ip_address", associate_public_ip_address)
        if ebs_block_devices and not isinstance(ebs_block_devices, list):
            raise TypeError("Expected argument 'ebs_block_devices' to be a list")
        pulumi.set(__self__, "ebs_block_devices", ebs_block_devices)
        if ebs_optimized and not isinstance(ebs_optimized, bool):
            raise TypeError("Expected argument 'ebs_optimized' to be a bool")
        pulumi.set(__self__, "ebs_optimized", ebs_optimized)
        if enable_monitoring and not isinstance(enable_monitoring, bool):
            raise TypeError("Expected argument 'enable_monitoring' to be a bool")
        pulumi.set(__self__, "enable_monitoring", enable_monitoring)
        if ephemeral_block_devices and not isinstance(ephemeral_block_devices, list):
            raise TypeError("Expected argument 'ephemeral_block_devices' to be a list")
        pulumi.set(__self__, "ephemeral_block_devices", ephemeral_block_devices)
        if iam_instance_profile and not isinstance(iam_instance_profile, str):
            raise TypeError("Expected argument 'iam_instance_profile' to be a str")
        pulumi.set(__self__, "iam_instance_profile", iam_instance_profile)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if image_id and not isinstance(image_id, str):
            raise TypeError("Expected argument 'image_id' to be a str")
        pulumi.set(__self__, "image_id", image_id)
        if instance_type and not isinstance(instance_type, str):
            raise TypeError("Expected argument 'instance_type' to be a str")
        pulumi.set(__self__, "instance_type", instance_type)
        if key_name and not isinstance(key_name, str):
            raise TypeError("Expected argument 'key_name' to be a str")
        pulumi.set(__self__, "key_name", key_name)
        if metadata_options and not isinstance(metadata_options, list):
            raise TypeError("Expected argument 'metadata_options' to be a list")
        pulumi.set(__self__, "metadata_options", metadata_options)
        if name and not isinstance(name, str):
            raise TypeError("Expected argument 'name' to be a str")
        pulumi.set(__self__, "name", name)
        if placement_tenancy and not isinstance(placement_tenancy, str):
            raise TypeError("Expected argument 'placement_tenancy' to be a str")
        pulumi.set(__self__, "placement_tenancy", placement_tenancy)
        if root_block_devices and not isinstance(root_block_devices, list):
            raise TypeError("Expected argument 'root_block_devices' to be a list")
        pulumi.set(__self__, "root_block_devices", root_block_devices)
        if security_groups and not isinstance(security_groups, list):
            raise TypeError("Expected argument 'security_groups' to be a list")
        pulumi.set(__self__, "security_groups", security_groups)
        if spot_price and not isinstance(spot_price, str):
            raise TypeError("Expected argument 'spot_price' to be a str")
        pulumi.set(__self__, "spot_price", spot_price)
        if user_data and not isinstance(user_data, str):
            raise TypeError("Expected argument 'user_data' to be a str")
        pulumi.set(__self__, "user_data", user_data)

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        Amazon Resource Name of the launch configuration.
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="associatePublicIpAddress")
    def associate_public_ip_address(self) -> bool:
        """
        Whether a Public IP address is associated with the instance.
        """
        return pulumi.get(self, "associate_public_ip_address")

    @property
    @pulumi.getter(name="ebsBlockDevices")
    def ebs_block_devices(self) -> Sequence['outputs.GetLaunchConfigurationEbsBlockDeviceResult']:
        """
        EBS Block Devices attached to the instance.
        """
        return pulumi.get(self, "ebs_block_devices")

    @property
    @pulumi.getter(name="ebsOptimized")
    def ebs_optimized(self) -> bool:
        """
        Whether the launched EC2 instance will be EBS-optimized.
        """
        return pulumi.get(self, "ebs_optimized")

    @property
    @pulumi.getter(name="enableMonitoring")
    def enable_monitoring(self) -> bool:
        """
        Whether Detailed Monitoring is Enabled.
        """
        return pulumi.get(self, "enable_monitoring")

    @property
    @pulumi.getter(name="ephemeralBlockDevices")
    def ephemeral_block_devices(self) -> Sequence['outputs.GetLaunchConfigurationEphemeralBlockDeviceResult']:
        """
        The Ephemeral volumes on the instance.
        """
        return pulumi.get(self, "ephemeral_block_devices")

    @property
    @pulumi.getter(name="iamInstanceProfile")
    def iam_instance_profile(self) -> str:
        """
        The IAM Instance Profile to associate with launched instances.
        """
        return pulumi.get(self, "iam_instance_profile")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="imageId")
    def image_id(self) -> str:
        """
        EC2 Image ID of the instance.
        """
        return pulumi.get(self, "image_id")

    @property
    @pulumi.getter(name="instanceType")
    def instance_type(self) -> str:
        """
        Instance Type of the instance to launch.
        """
        return pulumi.get(self, "instance_type")

    @property
    @pulumi.getter(name="keyName")
    def key_name(self) -> str:
        """
        Key Name that should be used for the instance.
        """
        return pulumi.get(self, "key_name")

    @property
    @pulumi.getter(name="metadataOptions")
    def metadata_options(self) -> Sequence['outputs.GetLaunchConfigurationMetadataOptionResult']:
        """
        Metadata options for the instance.
        """
        return pulumi.get(self, "metadata_options")

    @property
    @pulumi.getter
    def name(self) -> str:
        """
        Name of the launch configuration.
        """
        return pulumi.get(self, "name")

    @property
    @pulumi.getter(name="placementTenancy")
    def placement_tenancy(self) -> str:
        """
        Tenancy of the instance.
        """
        return pulumi.get(self, "placement_tenancy")

    @property
    @pulumi.getter(name="rootBlockDevices")
    def root_block_devices(self) -> Sequence['outputs.GetLaunchConfigurationRootBlockDeviceResult']:
        """
        Root Block Device of the instance.
        """
        return pulumi.get(self, "root_block_devices")

    @property
    @pulumi.getter(name="securityGroups")
    def security_groups(self) -> Sequence[str]:
        """
        List of associated Security Group IDS.
        """
        return pulumi.get(self, "security_groups")

    @property
    @pulumi.getter(name="spotPrice")
    def spot_price(self) -> str:
        """
        Price to use for reserving Spot instances.
        """
        return pulumi.get(self, "spot_price")

    @property
    @pulumi.getter(name="userData")
    def user_data(self) -> str:
        """
        User Data of the instance.
        """
        return pulumi.get(self, "user_data")


class AwaitableGetLaunchConfigurationResult(GetLaunchConfigurationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetLaunchConfigurationResult(
            arn=self.arn,
            associate_public_ip_address=self.associate_public_ip_address,
            ebs_block_devices=self.ebs_block_devices,
            ebs_optimized=self.ebs_optimized,
            enable_monitoring=self.enable_monitoring,
            ephemeral_block_devices=self.ephemeral_block_devices,
            iam_instance_profile=self.iam_instance_profile,
            id=self.id,
            image_id=self.image_id,
            instance_type=self.instance_type,
            key_name=self.key_name,
            metadata_options=self.metadata_options,
            name=self.name,
            placement_tenancy=self.placement_tenancy,
            root_block_devices=self.root_block_devices,
            security_groups=self.security_groups,
            spot_price=self.spot_price,
            user_data=self.user_data)


def get_launch_configuration(name: Optional[str] = None,
                             opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetLaunchConfigurationResult:
    """
    Provides information about a Launch Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ubuntu = aws.ec2.get_launch_configuration(name="test-launch-config")
    ```


    :param str name: Name of the launch configuration.
    """
    __args__ = dict()
    __args__['name'] = name
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:ec2/getLaunchConfiguration:getLaunchConfiguration', __args__, opts=opts, typ=GetLaunchConfigurationResult).value

    return AwaitableGetLaunchConfigurationResult(
        arn=__ret__.arn,
        associate_public_ip_address=__ret__.associate_public_ip_address,
        ebs_block_devices=__ret__.ebs_block_devices,
        ebs_optimized=__ret__.ebs_optimized,
        enable_monitoring=__ret__.enable_monitoring,
        ephemeral_block_devices=__ret__.ephemeral_block_devices,
        iam_instance_profile=__ret__.iam_instance_profile,
        id=__ret__.id,
        image_id=__ret__.image_id,
        instance_type=__ret__.instance_type,
        key_name=__ret__.key_name,
        metadata_options=__ret__.metadata_options,
        name=__ret__.name,
        placement_tenancy=__ret__.placement_tenancy,
        root_block_devices=__ret__.root_block_devices,
        security_groups=__ret__.security_groups,
        spot_price=__ret__.spot_price,
        user_data=__ret__.user_data)


@_utilities.lift_output_func(get_launch_configuration)
def get_launch_configuration_output(name: Optional[pulumi.Input[str]] = None,
                                    opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetLaunchConfigurationResult]:
    """
    Provides information about a Launch Configuration.

    ## Example Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    ubuntu = aws.ec2.get_launch_configuration(name="test-launch-config")
    ```


    :param str name: Name of the launch configuration.
    """
    ...
