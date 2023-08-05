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
    'GetOrganizationResult',
    'AwaitableGetOrganizationResult',
    'get_organization',
]

@pulumi.output_type
class GetOrganizationResult:
    """
    A collection of values returned by getOrganization.
    """
    def __init__(__self__, accounts=None, arn=None, aws_service_access_principals=None, enabled_policy_types=None, feature_set=None, id=None, master_account_arn=None, master_account_email=None, master_account_id=None, non_master_accounts=None, roots=None):
        if accounts and not isinstance(accounts, list):
            raise TypeError("Expected argument 'accounts' to be a list")
        pulumi.set(__self__, "accounts", accounts)
        if arn and not isinstance(arn, str):
            raise TypeError("Expected argument 'arn' to be a str")
        pulumi.set(__self__, "arn", arn)
        if aws_service_access_principals and not isinstance(aws_service_access_principals, list):
            raise TypeError("Expected argument 'aws_service_access_principals' to be a list")
        pulumi.set(__self__, "aws_service_access_principals", aws_service_access_principals)
        if enabled_policy_types and not isinstance(enabled_policy_types, list):
            raise TypeError("Expected argument 'enabled_policy_types' to be a list")
        pulumi.set(__self__, "enabled_policy_types", enabled_policy_types)
        if feature_set and not isinstance(feature_set, str):
            raise TypeError("Expected argument 'feature_set' to be a str")
        pulumi.set(__self__, "feature_set", feature_set)
        if id and not isinstance(id, str):
            raise TypeError("Expected argument 'id' to be a str")
        pulumi.set(__self__, "id", id)
        if master_account_arn and not isinstance(master_account_arn, str):
            raise TypeError("Expected argument 'master_account_arn' to be a str")
        pulumi.set(__self__, "master_account_arn", master_account_arn)
        if master_account_email and not isinstance(master_account_email, str):
            raise TypeError("Expected argument 'master_account_email' to be a str")
        pulumi.set(__self__, "master_account_email", master_account_email)
        if master_account_id and not isinstance(master_account_id, str):
            raise TypeError("Expected argument 'master_account_id' to be a str")
        pulumi.set(__self__, "master_account_id", master_account_id)
        if non_master_accounts and not isinstance(non_master_accounts, list):
            raise TypeError("Expected argument 'non_master_accounts' to be a list")
        pulumi.set(__self__, "non_master_accounts", non_master_accounts)
        if roots and not isinstance(roots, list):
            raise TypeError("Expected argument 'roots' to be a list")
        pulumi.set(__self__, "roots", roots)

    @property
    @pulumi.getter
    def accounts(self) -> Sequence['outputs.GetOrganizationAccountResult']:
        """
        List of organization accounts including the master account. For a list excluding the master account, see the `non_master_accounts` attribute. All elements have these attributes:
        """
        return pulumi.get(self, "accounts")

    @property
    @pulumi.getter
    def arn(self) -> str:
        """
        ARN of the root
        """
        return pulumi.get(self, "arn")

    @property
    @pulumi.getter(name="awsServiceAccessPrincipals")
    def aws_service_access_principals(self) -> Sequence[str]:
        """
        A list of AWS service principal names that have integration enabled with your organization. Organization must have `feature_set` set to `ALL`. For additional information, see the [AWS Organizations User Guide](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_integrate_services.html).
        """
        return pulumi.get(self, "aws_service_access_principals")

    @property
    @pulumi.getter(name="enabledPolicyTypes")
    def enabled_policy_types(self) -> Sequence[str]:
        """
        A list of Organizations policy types that are enabled in the Organization Root. Organization must have `feature_set` set to `ALL`. For additional information about valid policy types (e.g., `SERVICE_CONTROL_POLICY`), see the [AWS Organizations API Reference](https://docs.aws.amazon.com/organizations/latest/APIReference/API_EnablePolicyType.html).
        """
        return pulumi.get(self, "enabled_policy_types")

    @property
    @pulumi.getter(name="featureSet")
    def feature_set(self) -> str:
        """
        FeatureSet of the organization.
        """
        return pulumi.get(self, "feature_set")

    @property
    @pulumi.getter
    def id(self) -> str:
        """
        The provider-assigned unique ID for this managed resource.
        """
        return pulumi.get(self, "id")

    @property
    @pulumi.getter(name="masterAccountArn")
    def master_account_arn(self) -> str:
        """
        ARN of the account that is designated as the master account for the organization.
        """
        return pulumi.get(self, "master_account_arn")

    @property
    @pulumi.getter(name="masterAccountEmail")
    def master_account_email(self) -> str:
        """
        The email address that is associated with the AWS account that is designated as the master account for the organization.
        """
        return pulumi.get(self, "master_account_email")

    @property
    @pulumi.getter(name="masterAccountId")
    def master_account_id(self) -> str:
        """
        Unique identifier (ID) of the master account of an organization.
        """
        return pulumi.get(self, "master_account_id")

    @property
    @pulumi.getter(name="nonMasterAccounts")
    def non_master_accounts(self) -> Sequence['outputs.GetOrganizationNonMasterAccountResult']:
        """
        List of organization accounts excluding the master account. For a list including the master account, see the `accounts` attribute. All elements have these attributes:
        """
        return pulumi.get(self, "non_master_accounts")

    @property
    @pulumi.getter
    def roots(self) -> Sequence['outputs.GetOrganizationRootResult']:
        """
        List of organization roots. All elements have these attributes:
        """
        return pulumi.get(self, "roots")


class AwaitableGetOrganizationResult(GetOrganizationResult):
    # pylint: disable=using-constant-test
    def __await__(self):
        if False:
            yield self
        return GetOrganizationResult(
            accounts=self.accounts,
            arn=self.arn,
            aws_service_access_principals=self.aws_service_access_principals,
            enabled_policy_types=self.enabled_policy_types,
            feature_set=self.feature_set,
            id=self.id,
            master_account_arn=self.master_account_arn,
            master_account_email=self.master_account_email,
            master_account_id=self.master_account_id,
            non_master_accounts=self.non_master_accounts,
            roots=self.roots)


def get_organization(opts: Optional[pulumi.InvokeOptions] = None) -> AwaitableGetOrganizationResult:
    """
    Get information about the organization that the user's account belongs to

    ## Example Usage
    ### List all account IDs for the organization

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.organizations.get_organization()
    pulumi.export("accountIds", [__item.id for __item in example.accounts])
    ```
    ### SNS topic that can be interacted by the organization only

    ```python
    import pulumi
    import pulumi_aws as aws

    example = aws.organizations.get_organization()
    sns_topic = aws.sns.Topic("snsTopic")
    sns_topic_policy_policy_document = sns_topic.arn.apply(lambda arn: aws.iam.get_policy_document_output(statements=[aws.iam.GetPolicyDocumentStatementArgs(
        effect="Allow",
        actions=[
            "SNS:Subscribe",
            "SNS:Publish",
        ],
        conditions=[aws.iam.GetPolicyDocumentStatementConditionArgs(
            test="StringEquals",
            variable="aws:PrincipalOrgID",
            values=[example.id],
        )],
        principals=[aws.iam.GetPolicyDocumentStatementPrincipalArgs(
            type="AWS",
            identifiers=["*"],
        )],
        resources=[arn],
    )]))
    sns_topic_policy_topic_policy = aws.sns.TopicPolicy("snsTopicPolicyTopicPolicy",
        arn=sns_topic.arn,
        policy=sns_topic_policy_policy_document.json)
    ```
    """
    __args__ = dict()
    opts = pulumi.InvokeOptions.merge(_utilities.get_invoke_opts_defaults(), opts)
    __ret__ = pulumi.runtime.invoke('aws:organizations/getOrganization:getOrganization', __args__, opts=opts, typ=GetOrganizationResult).value

    return AwaitableGetOrganizationResult(
        accounts=__ret__.accounts,
        arn=__ret__.arn,
        aws_service_access_principals=__ret__.aws_service_access_principals,
        enabled_policy_types=__ret__.enabled_policy_types,
        feature_set=__ret__.feature_set,
        id=__ret__.id,
        master_account_arn=__ret__.master_account_arn,
        master_account_email=__ret__.master_account_email,
        master_account_id=__ret__.master_account_id,
        non_master_accounts=__ret__.non_master_accounts,
        roots=__ret__.roots)
