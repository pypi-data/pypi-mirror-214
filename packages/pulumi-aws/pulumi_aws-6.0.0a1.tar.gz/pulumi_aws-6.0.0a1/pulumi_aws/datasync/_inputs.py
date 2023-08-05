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
    'EfsLocationEc2ConfigArgs',
    'FsxOpenZfsFileSystemProtocolArgs',
    'FsxOpenZfsFileSystemProtocolNfsArgs',
    'FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs',
    'LocationHdfsNameNodeArgs',
    'LocationHdfsQopConfigurationArgs',
    'LocationSmbMountOptionsArgs',
    'NfsLocationMountOptionsArgs',
    'NfsLocationOnPremConfigArgs',
    'S3LocationS3ConfigArgs',
    'TaskExcludesArgs',
    'TaskIncludesArgs',
    'TaskOptionsArgs',
    'TaskScheduleArgs',
]

@pulumi.input_type
class EfsLocationEc2ConfigArgs:
    def __init__(__self__, *,
                 security_group_arns: pulumi.Input[Sequence[pulumi.Input[str]]],
                 subnet_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] security_group_arns: List of Amazon Resource Names (ARNs) of the EC2 Security Groups that are associated with the EFS Mount Target.
        :param pulumi.Input[str] subnet_arn: Amazon Resource Name (ARN) of the EC2 Subnet that is associated with the EFS Mount Target.
        """
        pulumi.set(__self__, "security_group_arns", security_group_arns)
        pulumi.set(__self__, "subnet_arn", subnet_arn)

    @property
    @pulumi.getter(name="securityGroupArns")
    def security_group_arns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of Amazon Resource Names (ARNs) of the EC2 Security Groups that are associated with the EFS Mount Target.
        """
        return pulumi.get(self, "security_group_arns")

    @security_group_arns.setter
    def security_group_arns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "security_group_arns", value)

    @property
    @pulumi.getter(name="subnetArn")
    def subnet_arn(self) -> pulumi.Input[str]:
        """
        Amazon Resource Name (ARN) of the EC2 Subnet that is associated with the EFS Mount Target.
        """
        return pulumi.get(self, "subnet_arn")

    @subnet_arn.setter
    def subnet_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "subnet_arn", value)


@pulumi.input_type
class FsxOpenZfsFileSystemProtocolArgs:
    def __init__(__self__, *,
                 nfs: pulumi.Input['FsxOpenZfsFileSystemProtocolNfsArgs']):
        """
        :param pulumi.Input['FsxOpenZfsFileSystemProtocolNfsArgs'] nfs: Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system. See below.
        """
        pulumi.set(__self__, "nfs", nfs)

    @property
    @pulumi.getter
    def nfs(self) -> pulumi.Input['FsxOpenZfsFileSystemProtocolNfsArgs']:
        """
        Represents the Network File System (NFS) protocol that DataSync uses to access your FSx for OpenZFS file system. See below.
        """
        return pulumi.get(self, "nfs")

    @nfs.setter
    def nfs(self, value: pulumi.Input['FsxOpenZfsFileSystemProtocolNfsArgs']):
        pulumi.set(self, "nfs", value)


@pulumi.input_type
class FsxOpenZfsFileSystemProtocolNfsArgs:
    def __init__(__self__, *,
                 mount_options: pulumi.Input['FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs']):
        """
        :param pulumi.Input['FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs'] mount_options: Represents the mount options that are available for DataSync to access an NFS location. See below.
        """
        pulumi.set(__self__, "mount_options", mount_options)

    @property
    @pulumi.getter(name="mountOptions")
    def mount_options(self) -> pulumi.Input['FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs']:
        """
        Represents the mount options that are available for DataSync to access an NFS location. See below.
        """
        return pulumi.get(self, "mount_options")

    @mount_options.setter
    def mount_options(self, value: pulumi.Input['FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs']):
        pulumi.set(self, "mount_options", value)


@pulumi.input_type
class FsxOpenZfsFileSystemProtocolNfsMountOptionsArgs:
    def __init__(__self__, *,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] version: The specific NFS version that you want DataSync to use for mounting your NFS share. Valid values: `AUTOMATIC`, `NFS3`, `NFS4_0` and `NFS4_1`. Default: `AUTOMATIC`
        """
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The specific NFS version that you want DataSync to use for mounting your NFS share. Valid values: `AUTOMATIC`, `NFS3`, `NFS4_0` and `NFS4_1`. Default: `AUTOMATIC`
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class LocationHdfsNameNodeArgs:
    def __init__(__self__, *,
                 hostname: pulumi.Input[str],
                 port: pulumi.Input[int]):
        """
        :param pulumi.Input[str] hostname: The hostname of the NameNode in the HDFS cluster. This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.
        :param pulumi.Input[int] port: The port that the NameNode uses to listen to client requests.
        """
        pulumi.set(__self__, "hostname", hostname)
        pulumi.set(__self__, "port", port)

    @property
    @pulumi.getter
    def hostname(self) -> pulumi.Input[str]:
        """
        The hostname of the NameNode in the HDFS cluster. This value is the IP address or Domain Name Service (DNS) name of the NameNode. An agent that's installed on-premises uses this hostname to communicate with the NameNode in the network.
        """
        return pulumi.get(self, "hostname")

    @hostname.setter
    def hostname(self, value: pulumi.Input[str]):
        pulumi.set(self, "hostname", value)

    @property
    @pulumi.getter
    def port(self) -> pulumi.Input[int]:
        """
        The port that the NameNode uses to listen to client requests.
        """
        return pulumi.get(self, "port")

    @port.setter
    def port(self, value: pulumi.Input[int]):
        pulumi.set(self, "port", value)


@pulumi.input_type
class LocationHdfsQopConfigurationArgs:
    def __init__(__self__, *,
                 data_transfer_protection: Optional[pulumi.Input[str]] = None,
                 rpc_protection: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] data_transfer_protection: The data transfer protection setting configured on the HDFS cluster. This setting corresponds to your dfs.data.transfer.protection setting in the hdfs-site.xml file on your Hadoop cluster. Valid values are `DISABLED`, `AUTHENTICATION`, `INTEGRITY` and `PRIVACY`.
        :param pulumi.Input[str] rpc_protection: The RPC protection setting configured on the HDFS cluster. This setting corresponds to your hadoop.rpc.protection setting in your core-site.xml file on your Hadoop cluster. Valid values are `DISABLED`, `AUTHENTICATION`, `INTEGRITY` and `PRIVACY`.
        """
        if data_transfer_protection is not None:
            pulumi.set(__self__, "data_transfer_protection", data_transfer_protection)
        if rpc_protection is not None:
            pulumi.set(__self__, "rpc_protection", rpc_protection)

    @property
    @pulumi.getter(name="dataTransferProtection")
    def data_transfer_protection(self) -> Optional[pulumi.Input[str]]:
        """
        The data transfer protection setting configured on the HDFS cluster. This setting corresponds to your dfs.data.transfer.protection setting in the hdfs-site.xml file on your Hadoop cluster. Valid values are `DISABLED`, `AUTHENTICATION`, `INTEGRITY` and `PRIVACY`.
        """
        return pulumi.get(self, "data_transfer_protection")

    @data_transfer_protection.setter
    def data_transfer_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "data_transfer_protection", value)

    @property
    @pulumi.getter(name="rpcProtection")
    def rpc_protection(self) -> Optional[pulumi.Input[str]]:
        """
        The RPC protection setting configured on the HDFS cluster. This setting corresponds to your hadoop.rpc.protection setting in your core-site.xml file on your Hadoop cluster. Valid values are `DISABLED`, `AUTHENTICATION`, `INTEGRITY` and `PRIVACY`.
        """
        return pulumi.get(self, "rpc_protection")

    @rpc_protection.setter
    def rpc_protection(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "rpc_protection", value)


@pulumi.input_type
class LocationSmbMountOptionsArgs:
    def __init__(__self__, *,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] version: The specific SMB version that you want DataSync to use for mounting your SMB share. Valid values: `AUTOMATIC`, `SMB2`, and `SMB3`. Default: `AUTOMATIC`
        """
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The specific SMB version that you want DataSync to use for mounting your SMB share. Valid values: `AUTOMATIC`, `SMB2`, and `SMB3`. Default: `AUTOMATIC`
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class NfsLocationMountOptionsArgs:
    def __init__(__self__, *,
                 version: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] version: The specific NFS version that you want DataSync to use for mounting your NFS share. Valid values: `AUTOMATIC`, `NFS3`, `NFS4_0` and `NFS4_1`. Default: `AUTOMATIC`
        """
        if version is not None:
            pulumi.set(__self__, "version", version)

    @property
    @pulumi.getter
    def version(self) -> Optional[pulumi.Input[str]]:
        """
        The specific NFS version that you want DataSync to use for mounting your NFS share. Valid values: `AUTOMATIC`, `NFS3`, `NFS4_0` and `NFS4_1`. Default: `AUTOMATIC`
        """
        return pulumi.get(self, "version")

    @version.setter
    def version(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "version", value)


@pulumi.input_type
class NfsLocationOnPremConfigArgs:
    def __init__(__self__, *,
                 agent_arns: pulumi.Input[Sequence[pulumi.Input[str]]]):
        """
        :param pulumi.Input[Sequence[pulumi.Input[str]]] agent_arns: List of Amazon Resource Names (ARNs) of the DataSync Agents used to connect to the NFS server.
        """
        pulumi.set(__self__, "agent_arns", agent_arns)

    @property
    @pulumi.getter(name="agentArns")
    def agent_arns(self) -> pulumi.Input[Sequence[pulumi.Input[str]]]:
        """
        List of Amazon Resource Names (ARNs) of the DataSync Agents used to connect to the NFS server.
        """
        return pulumi.get(self, "agent_arns")

    @agent_arns.setter
    def agent_arns(self, value: pulumi.Input[Sequence[pulumi.Input[str]]]):
        pulumi.set(self, "agent_arns", value)


@pulumi.input_type
class S3LocationS3ConfigArgs:
    def __init__(__self__, *,
                 bucket_access_role_arn: pulumi.Input[str]):
        """
        :param pulumi.Input[str] bucket_access_role_arn: ARN of the IAM Role used to connect to the S3 Bucket.
        """
        pulumi.set(__self__, "bucket_access_role_arn", bucket_access_role_arn)

    @property
    @pulumi.getter(name="bucketAccessRoleArn")
    def bucket_access_role_arn(self) -> pulumi.Input[str]:
        """
        ARN of the IAM Role used to connect to the S3 Bucket.
        """
        return pulumi.get(self, "bucket_access_role_arn")

    @bucket_access_role_arn.setter
    def bucket_access_role_arn(self, value: pulumi.Input[str]):
        pulumi.set(self, "bucket_access_role_arn", value)


@pulumi.input_type
class TaskExcludesArgs:
    def __init__(__self__, *,
                 filter_type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] filter_type: The type of filter rule to apply. Valid values: `SIMPLE_PATTERN`.
        :param pulumi.Input[str] value: A single filter string that consists of the patterns to exclude. The patterns are delimited by "|" (that is, a pipe), for example: `/folder1|/folder2`
        """
        if filter_type is not None:
            pulumi.set(__self__, "filter_type", filter_type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of filter rule to apply. Valid values: `SIMPLE_PATTERN`.
        """
        return pulumi.get(self, "filter_type")

    @filter_type.setter
    def filter_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        A single filter string that consists of the patterns to exclude. The patterns are delimited by "|" (that is, a pipe), for example: `/folder1|/folder2`
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class TaskIncludesArgs:
    def __init__(__self__, *,
                 filter_type: Optional[pulumi.Input[str]] = None,
                 value: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] filter_type: The type of filter rule to apply. Valid values: `SIMPLE_PATTERN`.
        :param pulumi.Input[str] value: A single filter string that consists of the patterns to include. The patterns are delimited by "|" (that is, a pipe), for example: `/folder1|/folder2`
        """
        if filter_type is not None:
            pulumi.set(__self__, "filter_type", filter_type)
        if value is not None:
            pulumi.set(__self__, "value", value)

    @property
    @pulumi.getter(name="filterType")
    def filter_type(self) -> Optional[pulumi.Input[str]]:
        """
        The type of filter rule to apply. Valid values: `SIMPLE_PATTERN`.
        """
        return pulumi.get(self, "filter_type")

    @filter_type.setter
    def filter_type(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "filter_type", value)

    @property
    @pulumi.getter
    def value(self) -> Optional[pulumi.Input[str]]:
        """
        A single filter string that consists of the patterns to include. The patterns are delimited by "|" (that is, a pipe), for example: `/folder1|/folder2`
        """
        return pulumi.get(self, "value")

    @value.setter
    def value(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "value", value)


@pulumi.input_type
class TaskOptionsArgs:
    def __init__(__self__, *,
                 atime: Optional[pulumi.Input[str]] = None,
                 bytes_per_second: Optional[pulumi.Input[int]] = None,
                 gid: Optional[pulumi.Input[str]] = None,
                 log_level: Optional[pulumi.Input[str]] = None,
                 mtime: Optional[pulumi.Input[str]] = None,
                 overwrite_mode: Optional[pulumi.Input[str]] = None,
                 posix_permissions: Optional[pulumi.Input[str]] = None,
                 preserve_deleted_files: Optional[pulumi.Input[str]] = None,
                 preserve_devices: Optional[pulumi.Input[str]] = None,
                 security_descriptor_copy_flags: Optional[pulumi.Input[str]] = None,
                 task_queueing: Optional[pulumi.Input[str]] = None,
                 transfer_mode: Optional[pulumi.Input[str]] = None,
                 uid: Optional[pulumi.Input[str]] = None,
                 verify_mode: Optional[pulumi.Input[str]] = None):
        """
        :param pulumi.Input[str] atime: A file metadata that shows the last time a file was accessed (that is when the file was read or written to). If set to `BEST_EFFORT`, the DataSync Task attempts to preserve the original (that is, the version before sync `PREPARING` phase) `atime` attribute on all source files. Valid values: `BEST_EFFORT`, `NONE`. Default: `BEST_EFFORT`.
        :param pulumi.Input[int] bytes_per_second: Limits the bandwidth utilized. For example, to set a maximum of 1 MB, set this value to `1048576`. Value values: `-1` or greater. Default: `-1` (unlimited).
        :param pulumi.Input[str] gid: Group identifier of the file's owners. Valid values: `BOTH`, `INT_VALUE`, `NAME`, `NONE`. Default: `INT_VALUE` (preserve integer value of the ID).
        :param pulumi.Input[str] log_level: Determines the type of logs that DataSync publishes to a log stream in the Amazon CloudWatch log group that you provide. Valid values: `OFF`, `BASIC`, `TRANSFER`. Default: `OFF`.
        :param pulumi.Input[str] mtime: A file metadata that indicates the last time a file was modified (written to) before the sync `PREPARING` phase. Value values: `NONE`, `PRESERVE`. Default: `PRESERVE`.
        :param pulumi.Input[str] overwrite_mode: Determines whether files at the destination should be overwritten or preserved when copying files. Valid values: `ALWAYS`, `NEVER`. Default: `ALWAYS`.
        :param pulumi.Input[str] posix_permissions: Determines which users or groups can access a file for a specific purpose such as reading, writing, or execution of the file. Valid values: `NONE`, `PRESERVE`. Default: `PRESERVE`.
        :param pulumi.Input[str] preserve_deleted_files: Whether files deleted in the source should be removed or preserved in the destination file system. Valid values: `PRESERVE`, `REMOVE`. Default: `PRESERVE`.
        :param pulumi.Input[str] preserve_devices: Whether the DataSync Task should preserve the metadata of block and character devices in the source files system, and recreate the files with that device name and metadata on the destination. The DataSync Task can’t sync the actual contents of such devices, because many of the devices are non-terminal and don’t return an end of file (EOF) marker. Valid values: `NONE`, `PRESERVE`. Default: `NONE` (ignore special devices).
        :param pulumi.Input[str] security_descriptor_copy_flags: Determines which components of the SMB security descriptor are copied from source to destination objects. This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. Valid values: `NONE`, `OWNER_DACL`, `OWNER_DACL_SACL`.
        :param pulumi.Input[str] task_queueing: Determines whether tasks should be queued before executing the tasks. Valid values: `ENABLED`, `DISABLED`. Default `ENABLED`.
        :param pulumi.Input[str] transfer_mode: Determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing to the destination location. Valid values: `CHANGED`, `ALL`. Default: `CHANGED`
        :param pulumi.Input[str] uid: User identifier of the file's owners. Valid values: `BOTH`, `INT_VALUE`, `NAME`, `NONE`. Default: `INT_VALUE` (preserve integer value of the ID).
        :param pulumi.Input[str] verify_mode: Whether a data integrity verification should be performed at the end of a task execution after all data and metadata have been transferred. Valid values: `NONE`, `POINT_IN_TIME_CONSISTENT`, `ONLY_FILES_TRANSFERRED`. Default: `POINT_IN_TIME_CONSISTENT`.
        """
        if atime is not None:
            pulumi.set(__self__, "atime", atime)
        if bytes_per_second is not None:
            pulumi.set(__self__, "bytes_per_second", bytes_per_second)
        if gid is not None:
            pulumi.set(__self__, "gid", gid)
        if log_level is not None:
            pulumi.set(__self__, "log_level", log_level)
        if mtime is not None:
            pulumi.set(__self__, "mtime", mtime)
        if overwrite_mode is not None:
            pulumi.set(__self__, "overwrite_mode", overwrite_mode)
        if posix_permissions is not None:
            pulumi.set(__self__, "posix_permissions", posix_permissions)
        if preserve_deleted_files is not None:
            pulumi.set(__self__, "preserve_deleted_files", preserve_deleted_files)
        if preserve_devices is not None:
            pulumi.set(__self__, "preserve_devices", preserve_devices)
        if security_descriptor_copy_flags is not None:
            pulumi.set(__self__, "security_descriptor_copy_flags", security_descriptor_copy_flags)
        if task_queueing is not None:
            pulumi.set(__self__, "task_queueing", task_queueing)
        if transfer_mode is not None:
            pulumi.set(__self__, "transfer_mode", transfer_mode)
        if uid is not None:
            pulumi.set(__self__, "uid", uid)
        if verify_mode is not None:
            pulumi.set(__self__, "verify_mode", verify_mode)

    @property
    @pulumi.getter
    def atime(self) -> Optional[pulumi.Input[str]]:
        """
        A file metadata that shows the last time a file was accessed (that is when the file was read or written to). If set to `BEST_EFFORT`, the DataSync Task attempts to preserve the original (that is, the version before sync `PREPARING` phase) `atime` attribute on all source files. Valid values: `BEST_EFFORT`, `NONE`. Default: `BEST_EFFORT`.
        """
        return pulumi.get(self, "atime")

    @atime.setter
    def atime(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "atime", value)

    @property
    @pulumi.getter(name="bytesPerSecond")
    def bytes_per_second(self) -> Optional[pulumi.Input[int]]:
        """
        Limits the bandwidth utilized. For example, to set a maximum of 1 MB, set this value to `1048576`. Value values: `-1` or greater. Default: `-1` (unlimited).
        """
        return pulumi.get(self, "bytes_per_second")

    @bytes_per_second.setter
    def bytes_per_second(self, value: Optional[pulumi.Input[int]]):
        pulumi.set(self, "bytes_per_second", value)

    @property
    @pulumi.getter
    def gid(self) -> Optional[pulumi.Input[str]]:
        """
        Group identifier of the file's owners. Valid values: `BOTH`, `INT_VALUE`, `NAME`, `NONE`. Default: `INT_VALUE` (preserve integer value of the ID).
        """
        return pulumi.get(self, "gid")

    @gid.setter
    def gid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "gid", value)

    @property
    @pulumi.getter(name="logLevel")
    def log_level(self) -> Optional[pulumi.Input[str]]:
        """
        Determines the type of logs that DataSync publishes to a log stream in the Amazon CloudWatch log group that you provide. Valid values: `OFF`, `BASIC`, `TRANSFER`. Default: `OFF`.
        """
        return pulumi.get(self, "log_level")

    @log_level.setter
    def log_level(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "log_level", value)

    @property
    @pulumi.getter
    def mtime(self) -> Optional[pulumi.Input[str]]:
        """
        A file metadata that indicates the last time a file was modified (written to) before the sync `PREPARING` phase. Value values: `NONE`, `PRESERVE`. Default: `PRESERVE`.
        """
        return pulumi.get(self, "mtime")

    @mtime.setter
    def mtime(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "mtime", value)

    @property
    @pulumi.getter(name="overwriteMode")
    def overwrite_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Determines whether files at the destination should be overwritten or preserved when copying files. Valid values: `ALWAYS`, `NEVER`. Default: `ALWAYS`.
        """
        return pulumi.get(self, "overwrite_mode")

    @overwrite_mode.setter
    def overwrite_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "overwrite_mode", value)

    @property
    @pulumi.getter(name="posixPermissions")
    def posix_permissions(self) -> Optional[pulumi.Input[str]]:
        """
        Determines which users or groups can access a file for a specific purpose such as reading, writing, or execution of the file. Valid values: `NONE`, `PRESERVE`. Default: `PRESERVE`.
        """
        return pulumi.get(self, "posix_permissions")

    @posix_permissions.setter
    def posix_permissions(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "posix_permissions", value)

    @property
    @pulumi.getter(name="preserveDeletedFiles")
    def preserve_deleted_files(self) -> Optional[pulumi.Input[str]]:
        """
        Whether files deleted in the source should be removed or preserved in the destination file system. Valid values: `PRESERVE`, `REMOVE`. Default: `PRESERVE`.
        """
        return pulumi.get(self, "preserve_deleted_files")

    @preserve_deleted_files.setter
    def preserve_deleted_files(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preserve_deleted_files", value)

    @property
    @pulumi.getter(name="preserveDevices")
    def preserve_devices(self) -> Optional[pulumi.Input[str]]:
        """
        Whether the DataSync Task should preserve the metadata of block and character devices in the source files system, and recreate the files with that device name and metadata on the destination. The DataSync Task can’t sync the actual contents of such devices, because many of the devices are non-terminal and don’t return an end of file (EOF) marker. Valid values: `NONE`, `PRESERVE`. Default: `NONE` (ignore special devices).
        """
        return pulumi.get(self, "preserve_devices")

    @preserve_devices.setter
    def preserve_devices(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "preserve_devices", value)

    @property
    @pulumi.getter(name="securityDescriptorCopyFlags")
    def security_descriptor_copy_flags(self) -> Optional[pulumi.Input[str]]:
        """
        Determines which components of the SMB security descriptor are copied from source to destination objects. This value is only used for transfers between SMB and Amazon FSx for Windows File Server locations, or between two Amazon FSx for Windows File Server locations. Valid values: `NONE`, `OWNER_DACL`, `OWNER_DACL_SACL`.
        """
        return pulumi.get(self, "security_descriptor_copy_flags")

    @security_descriptor_copy_flags.setter
    def security_descriptor_copy_flags(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "security_descriptor_copy_flags", value)

    @property
    @pulumi.getter(name="taskQueueing")
    def task_queueing(self) -> Optional[pulumi.Input[str]]:
        """
        Determines whether tasks should be queued before executing the tasks. Valid values: `ENABLED`, `DISABLED`. Default `ENABLED`.
        """
        return pulumi.get(self, "task_queueing")

    @task_queueing.setter
    def task_queueing(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "task_queueing", value)

    @property
    @pulumi.getter(name="transferMode")
    def transfer_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Determines whether DataSync transfers only the data and metadata that differ between the source and the destination location, or whether DataSync transfers all the content from the source, without comparing to the destination location. Valid values: `CHANGED`, `ALL`. Default: `CHANGED`
        """
        return pulumi.get(self, "transfer_mode")

    @transfer_mode.setter
    def transfer_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "transfer_mode", value)

    @property
    @pulumi.getter
    def uid(self) -> Optional[pulumi.Input[str]]:
        """
        User identifier of the file's owners. Valid values: `BOTH`, `INT_VALUE`, `NAME`, `NONE`. Default: `INT_VALUE` (preserve integer value of the ID).
        """
        return pulumi.get(self, "uid")

    @uid.setter
    def uid(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "uid", value)

    @property
    @pulumi.getter(name="verifyMode")
    def verify_mode(self) -> Optional[pulumi.Input[str]]:
        """
        Whether a data integrity verification should be performed at the end of a task execution after all data and metadata have been transferred. Valid values: `NONE`, `POINT_IN_TIME_CONSISTENT`, `ONLY_FILES_TRANSFERRED`. Default: `POINT_IN_TIME_CONSISTENT`.
        """
        return pulumi.get(self, "verify_mode")

    @verify_mode.setter
    def verify_mode(self, value: Optional[pulumi.Input[str]]):
        pulumi.set(self, "verify_mode", value)


@pulumi.input_type
class TaskScheduleArgs:
    def __init__(__self__, *,
                 schedule_expression: pulumi.Input[str]):
        """
        :param pulumi.Input[str] schedule_expression: Specifies the schedule you want your task to use for repeated executions. For more information, see [Schedule Expressions for Rules](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).
        """
        pulumi.set(__self__, "schedule_expression", schedule_expression)

    @property
    @pulumi.getter(name="scheduleExpression")
    def schedule_expression(self) -> pulumi.Input[str]:
        """
        Specifies the schedule you want your task to use for repeated executions. For more information, see [Schedule Expressions for Rules](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html).
        """
        return pulumi.get(self, "schedule_expression")

    @schedule_expression.setter
    def schedule_expression(self, value: pulumi.Input[str]):
        pulumi.set(self, "schedule_expression", value)


