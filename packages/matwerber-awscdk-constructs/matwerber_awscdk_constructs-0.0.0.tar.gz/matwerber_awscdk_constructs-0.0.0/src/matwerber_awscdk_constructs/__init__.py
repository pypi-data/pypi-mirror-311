r'''
# Mat Werber's AWS CDK Construct Library

This project is (or at least, is meant to become) a central repository of the various custom AWS CDK constructs I create in the course of my work.

For now, project goals are:

1. Learn how to publish to the CDK Construct Hub
2. Learn to write better constructs.
3. Improve my existing constructs over time rather than re-creating or copy-pasting them when needed across projects.

## FAQ

### How was this project started?

Rather than piece together the various components and decisions needed to publish to the CDK Construct Hub, I opted to use AWS CDK Construct Library template project provided by [projen](https://projen.io/docs/project-types/aws-cdk-construct-library/)

### How does the project get published to Construct Hub?

Commits trigger a GitHub Action to build and publish this library to **npm**.
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk.aws_logs as _aws_cdk_aws_logs_ceddda9d
import constructs as _constructs_77d1e7e8


class SsoIdentityStore(
    _constructs_77d1e7e8.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="awscdk-constructs.SsoIdentityStore",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        *,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
        sso_home_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Creates a custom CloudFormation resource that retrieves information about an existing AWS Identity Center (SSO) identity store ID.

        A singleton AWS Lambda function is created and acts as the custom resource provider by
        using the AWS SsoAdmin ListInstances API to find and make available your identity store ID
        and instance ARN to other stack resources.

        **Requirements for using this resource**:

        - AWS IAM Identity Center must have been already configured in your AWS Organization.
        - This resource must be deployed in either your AWS Organization's management account or an AWS IAM
          Identity Center delegated administrator account.

        :param scope: - The scope in which to define this construct.
        :param id: - The scoped construct ID.
        :param log_group: Optional CloudWatch Log Group to store the invocation logs of the Lambda function backing the custom resource used to retrieve the identity store ID. If not provided, a new log group will be created and configured with a 7-day retention period.
        :param sso_home_region: The AWS region in which AWS Identity Center (aka AWS SSO) is currently configured for your Organization and which will be used in the AWS API call used to retrieve information about your identity store ID. If AWS SSO is not configured in the same region as the current CDK stack, this parameter is required. If AWS SSO is configured in the same region as the stack, you can omit this parameter.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__961b11b5a9cc63d3e32fb76ae53f850f0cd5f696ccc8662a5028ded4a05a6534)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = SsoIdentityStoreProps(
            log_group=log_group, sso_home_region=sso_home_region
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="identityStoreId")
    def identity_store_id(self) -> builtins.str:
        '''The unique identifier for the identity store that is connected to your IAM Identity Center instance.'''
        return typing.cast(builtins.str, jsii.get(self, "identityStoreId"))

    @builtins.property
    @jsii.member(jsii_name="instanceArn")
    def instance_arn(self) -> builtins.str:
        '''The ARN of the IAM Identity Center instance.

        This is a globally unique identifier for your IAM Identity Center instance.
        '''
        return typing.cast(builtins.str, jsii.get(self, "instanceArn"))

    @builtins.property
    @jsii.member(jsii_name="ownerAccountId")
    def owner_account_id(self) -> builtins.str:
        '''The AWS account ID that owns the IAM Identity Center instance.

        This will always be your AWS Organization's
        management account ID.
        '''
        return typing.cast(builtins.str, jsii.get(self, "ownerAccountId"))


@jsii.data_type(
    jsii_type="awscdk-constructs.SsoIdentityStoreProps",
    jsii_struct_bases=[],
    name_mapping={"log_group": "logGroup", "sso_home_region": "ssoHomeRegion"},
)
class SsoIdentityStoreProps:
    def __init__(
        self,
        *,
        log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
        sso_home_region: typing.Optional[builtins.str] = None,
    ) -> None:
        '''An AWS IAM Identity Center identity store used for AWS Single Sign-on (SSO).

        This construct retrieves information about an existing SSO identity store using the AWS SSO Admin API.

        :param log_group: Optional CloudWatch Log Group to store the invocation logs of the Lambda function backing the custom resource used to retrieve the identity store ID. If not provided, a new log group will be created and configured with a 7-day retention period.
        :param sso_home_region: The AWS region in which AWS Identity Center (aka AWS SSO) is currently configured for your Organization and which will be used in the AWS API call used to retrieve information about your identity store ID. If AWS SSO is not configured in the same region as the current CDK stack, this parameter is required. If AWS SSO is configured in the same region as the stack, you can omit this parameter.

        Example::

            const identityStore = new SsoIdentityStore(this, 'MySsoIdentityStore');
            console.log(identityStore.identityStoreId);
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9803d7d65d106ed7f033176fe1f869ef15550a9bd9aab176e9e4aed52bede1f8)
            check_type(argname="argument log_group", value=log_group, expected_type=type_hints["log_group"])
            check_type(argname="argument sso_home_region", value=sso_home_region, expected_type=type_hints["sso_home_region"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if log_group is not None:
            self._values["log_group"] = log_group
        if sso_home_region is not None:
            self._values["sso_home_region"] = sso_home_region

    @builtins.property
    def log_group(self) -> typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup]:
        '''Optional CloudWatch Log Group to store the invocation logs of the Lambda function backing the custom resource used to retrieve the identity store ID.

        If not provided, a new log group will be created and
        configured with a 7-day retention period.
        '''
        result = self._values.get("log_group")
        return typing.cast(typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup], result)

    @builtins.property
    def sso_home_region(self) -> typing.Optional[builtins.str]:
        '''The AWS region in which AWS Identity Center (aka AWS SSO) is currently configured for your Organization and which will be used in the AWS API call used to retrieve information about your identity store ID.

        If AWS SSO is not configured in the same region as the current CDK stack, this parameter is required.
        If AWS SSO is configured in the same region as the stack, you can omit this parameter.
        '''
        result = self._values.get("sso_home_region")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "SsoIdentityStoreProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "SsoIdentityStore",
    "SsoIdentityStoreProps",
]

publication.publish()

def _typecheckingstub__961b11b5a9cc63d3e32fb76ae53f850f0cd5f696ccc8662a5028ded4a05a6534(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    *,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
    sso_home_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9803d7d65d106ed7f033176fe1f869ef15550a9bd9aab176e9e4aed52bede1f8(
    *,
    log_group: typing.Optional[_aws_cdk_aws_logs_ceddda9d.LogGroup] = None,
    sso_home_region: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass
