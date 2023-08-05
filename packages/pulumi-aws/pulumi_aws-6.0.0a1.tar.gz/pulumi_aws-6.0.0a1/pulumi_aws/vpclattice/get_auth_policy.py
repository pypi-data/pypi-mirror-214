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
    'GetAuthPolicyResult',
    'AwaitableGetAuthPolicyResult',
    'get_auth_policy',
    'get_auth_policy_output',
]

@pulumi.output_type
class GetAuthPolicyResult:
    """
    A collection of values returned by getAuthPolicy.
    """
    def __init__(__self__, id=None, policy=None, resource_identifier=None, state=None):
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if policy and not isinstance(policy, str):
            raise TypeError("Expected argument 'policy' to be a str")
        pulumi.set(__self__, "policy", policy)
        if resource_identifier and not isinstance(resource_identifier, str):
            raise TypeError("Expected argument 'resource_identifier' to be a str")
        pulumi.set(__self__, "resource_identifier", resource_identifier)
        if state and not isinstance(state, str):
            raise TypeError("Expected argument 'state' to be a str")
        pulumi.set(__self__, "state", state)

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter
    def policy(self) -> Optional[str]:
        """
        The auth policy. The policy string in JSON must not contain newlines or blank lines.
        """
        return pulumi.get(self, "policy")

    @property
    @pulumi.getter(name="resourceIdentifier")
    def resource_identifier(self) -> str:
        return pulumi.get(self, "resource_identifier")

    @property
    @pulumi.getter
    def state(self) -> Optional[str]:
        """
        The state of the auth policy. The auth policy is only active when the auth type is set to AWS_IAM. If you provide a policy, then authentication and authorization decisions are made based on this policy and the client's IAM policy. If the Auth type is NONE, then, any auth policy you provide will remain inactive.
        """
        return pulumi.get(self, "state")


class AwaitableGetAuthPolicyResult(GetAuthPolicyResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetAuthPolicyResult(
            id=self.id,
            policy=self.policy,
            resource_identifier=self.resource_identifier,
            state=self.state)


def get_auth_policy(policy: Optional[str] = None,
                    resource_identifier: Optional[str] = None,
                    state: Optional[str] = None,
                    opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetAuthPolicyResult:
    """
    Data source for managing an AWS VPC Lattice Auth Policy.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.vpclattice.get_auth_policy(resource_identifier=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str policy: The auth policy. The policy string in JSON must not contain newlines or blank lines.
    :param str resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.
    :param str state: The state of the auth policy. The auth policy is only active when the auth type is set to AWS_IAM. If you provide a policy, then authentication and authorization decisions are made based on this policy and the client's IAM policy. If the Auth type is NONE, then, any auth policy you provide will remain inactive.
    """
    __args__ = dict()
    __args__['policy'] = policy
    __args__['resourceIdentifier'] = resource_identifier
    __args__['state'] = state
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:vpclattice/getAuthPolicy:getAuthPolicy', __args__, opts=opts, typ=GetAuthPolicyResult).value

    return AwaitableGetAuthPolicyResult(
        id=__ret__.id,
        policy=__ret__.policy,
        resource_identifier=__ret__.resource_identifier,
        state=__ret__.state)


@_utilities.lift_output_func(get_auth_policy)
def get_auth_policy_output(policy: Optional[pulumi.Input[Optional[str]]] = None,
                           resource_identifier: Optional[pulumi.Input[str]] = None,
                           state: Optional[pulumi.Input[Optional[str]]] = None,
                           opts: Optional[pulumi.InvokeOptions] = None) -> pulumi.Output[GetAuthPolicyResult]:
    """
    Data source for managing an AWS VPC Lattice Auth Policy.

    ## Example Usage
    ### Basic Usage

    ```python
    import pulumi
    import pulumi_aws as aws

    test = aws.vpclattice.get_auth_policy(resource_identifier=%!v(PANIC=Format method: runtime error: invalid memory address or nil pointer dereference))
    ```


    :param str policy: The auth policy. The policy string in JSON must not contain newlines or blank lines.
    :param str resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.
    :param str state: The state of the auth policy. The auth policy is only active when the auth type is set to AWS_IAM. If you provide a policy, then authentication and authorization decisions are made based on this policy and the client's IAM policy. If the Auth type is NONE, then, any auth policy you provide will remain inactive.
    """
    ...
