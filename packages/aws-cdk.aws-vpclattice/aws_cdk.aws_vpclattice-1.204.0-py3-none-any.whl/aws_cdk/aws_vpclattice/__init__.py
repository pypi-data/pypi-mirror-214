'''
# AWS::VpcLattice Construct Library

<!--BEGIN STABILITY BANNER-->---


![End-of-Support](https://img.shields.io/badge/End--of--Support-critical.svg?style=for-the-badge)

> AWS CDK v1 has reached End-of-Support on 2023-06-01.
> This package is no longer being updated, and users should migrate to AWS CDK v2.
>
> For more information on how to migrate, see the [*Migrating to AWS CDK v2* guide](https://docs.aws.amazon.com/cdk/v2/guide/migrating-v2.html).

---
<!--END STABILITY BANNER-->

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

```python
import aws_cdk.aws_vpclattice as vpclattice
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for VpcLattice construct libraries](https://constructs.dev/search?q=vpclattice)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::VpcLattice resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VpcLattice.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::VpcLattice](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_VpcLattice.html).

(Read the [CDK Contributing Guide](https://github.com/aws/aws-cdk/blob/master/CONTRIBUTING.md) and submit an RFC if you are interested in contributing to this construct library.)

<!--END CFNONLY DISCLAIMER-->
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAccessLogSubscription(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnAccessLogSubscription",
):
    '''A CloudFormation ``AWS::VpcLattice::AccessLogSubscription``.

    Enables access logs to be sent to Amazon CloudWatch, Amazon S3, and Amazon Kinesis Data Firehose. The service network owner can use the access logs to audit the services in the network. The service network owner will only see access logs from clients and services that are associated with their service network. Access log entries represent traffic originated from VPCs associated with that network. For more information, see `Access logs <https://docs.aws.amazon.com/vpc-lattice/latest/ug/monitoring-access-logs.html>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::AccessLogSubscription
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_access_log_subscription = vpclattice.CfnAccessLogSubscription(self, "MyCfnAccessLogSubscription",
            destination_arn="destinationArn",
        
            # the properties below are optional
            resource_identifier="resourceIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        destination_arn: builtins.str,
        resource_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::AccessLogSubscription``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param destination_arn: The Amazon Resource Name (ARN) of the destination. The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.
        :param resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service.
        :param tags: The tags for the access log subscription.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__820e5beddf8e42bf43fff6a76594a893625daee50727ba238549056bbb8ef8b8)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAccessLogSubscriptionProps(
            destination_arn=destination_arn,
            resource_identifier=resource_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__798775518c10513eb0e4aec15f38faca5af7f050010816cf34ad9466870ddadc)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fdd6e394be12ec3be1410128dcbd4cfa81ad2234a0a8151fb579601b6b9f88e0)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the access log subscription.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the access log subscription.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceArn")
    def attr_resource_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the access log subscription.

        :cloudformationAttribute: ResourceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrResourceId")
    def attr_resource_id(self) -> builtins.str:
        '''The ID of the service network or service.

        :cloudformationAttribute: ResourceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrResourceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the access log subscription.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="destinationArn")
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-destinationarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "destinationArn"))

    @destination_arn.setter
    def destination_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8d662aa3158dde46f8905a1b0e44e6a80aeb005bec161af3b447272ad238f754)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "destinationArn", value)

    @builtins.property
    @jsii.member(jsii_name="resourceIdentifier")
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network or service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-resourceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceIdentifier"))

    @resource_identifier.setter
    def resource_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4422b3b30eca9b93cce8d457b3664a951be8c32f67ed6d703d76860fe91e3d99)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIdentifier", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnAccessLogSubscriptionProps",
    jsii_struct_bases=[],
    name_mapping={
        "destination_arn": "destinationArn",
        "resource_identifier": "resourceIdentifier",
        "tags": "tags",
    },
)
class CfnAccessLogSubscriptionProps:
    def __init__(
        self,
        *,
        destination_arn: builtins.str,
        resource_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnAccessLogSubscription``.

        :param destination_arn: The Amazon Resource Name (ARN) of the destination. The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.
        :param resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service.
        :param tags: The tags for the access log subscription.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_access_log_subscription_props = vpclattice.CfnAccessLogSubscriptionProps(
                destination_arn="destinationArn",
            
                # the properties below are optional
                resource_identifier="resourceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c833b9cbd47a408654254b9b3a6a98e83dc48cd6ef2a2bef9300a23549738f5d)
            check_type(argname="argument destination_arn", value=destination_arn, expected_type=type_hints["destination_arn"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "destination_arn": destination_arn,
        }
        if resource_identifier is not None:
            self._values["resource_identifier"] = resource_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def destination_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the destination.

        The supported destination types are CloudWatch Log groups, Kinesis Data Firehose delivery streams, and Amazon S3 buckets.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-destinationarn
        '''
        result = self._values.get("destination_arn")
        assert result is not None, "Required property 'destination_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network or service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the access log subscription.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-accesslogsubscription.html#cfn-vpclattice-accesslogsubscription-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAccessLogSubscriptionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnAuthPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnAuthPolicy",
):
    '''A CloudFormation ``AWS::VpcLattice::AuthPolicy``.

    Creates or updates the auth policy. The policy string in JSON must not contain newlines or blank lines.

    :cloudformationResource: AWS::VpcLattice::AuthPolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        # policy: Any
        
        cfn_auth_policy = vpclattice.CfnAuthPolicy(self, "MyCfnAuthPolicy",
            policy=policy,
            resource_identifier="resourceIdentifier"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy: typing.Any,
        resource_identifier: builtins.str,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::AuthPolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: The auth policy.
        :param resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97934b5b96195967fd5ac0686c4db1587ec155ac0b310f638a7dc22335dd0598)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnAuthPolicyProps(
            policy=policy, resource_identifier=resource_identifier
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__291be3dc9fd26d96a38bd1521783c31d36466bee645edb11f0c06a449cec4fc0)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2ffb8cc8262523a33d9eb4b5a4348e673b35d311b5175fd275728fd44fb6692c)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrState")
    def attr_state(self) -> builtins.str:
        '''The state of the auth policy.

        The auth policy is only active when the auth type is set to ``AWS _IAM`` . If you provide a policy, then authentication and authorization decisions are made based on this policy and the client's IAM policy. If the auth type is ``NONE`` , then any auth policy you provide will remain inactive.

        :cloudformationAttribute: State
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrState"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''The auth policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1854d1e596ae3e2e0c5089200e45e24a5512c05c13f2cc5e3d0444308afa1745)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="resourceIdentifier")
    def resource_identifier(self) -> builtins.str:
        '''The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-resourceidentifier
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceIdentifier"))

    @resource_identifier.setter
    def resource_identifier(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f287ff1f62e737127a1ce4a62d2f6abf5e4021eba0aa78568bc16cb039fa01d0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceIdentifier", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnAuthPolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_identifier": "resourceIdentifier"},
)
class CfnAuthPolicyProps:
    def __init__(
        self,
        *,
        policy: typing.Any,
        resource_identifier: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnAuthPolicy``.

        :param policy: The auth policy.
        :param resource_identifier: The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            # policy: Any
            
            cfn_auth_policy_props = vpclattice.CfnAuthPolicyProps(
                policy=policy,
                resource_identifier="resourceIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__04c2bc9f2f126d1bd9265c062de7475bbc03c205b57535facfe6e1ea63446d0a)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_identifier", value=resource_identifier, expected_type=type_hints["resource_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "resource_identifier": resource_identifier,
        }

    @builtins.property
    def policy(self) -> typing.Any:
        '''The auth policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_identifier(self) -> builtins.str:
        '''The ID or Amazon Resource Name (ARN) of the service network or service for which the policy is created.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-authpolicy.html#cfn-vpclattice-authpolicy-resourceidentifier
        '''
        result = self._values.get("resource_identifier")
        assert result is not None, "Required property 'resource_identifier' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnAuthPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnListener(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnListener",
):
    '''A CloudFormation ``AWS::VpcLattice::Listener``.

    Creates a listener for a service. Before you start using your Amazon VPC Lattice service, you must add one or more listeners. A listener is a process that checks for connection requests to your services. For more information, see `Listeners <https://docs.aws.amazon.com/vpc-lattice/latest/ug/listeners.html>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::Listener
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_listener = vpclattice.CfnListener(self, "MyCfnListener",
            default_action=vpclattice.CfnListener.DefaultActionProperty(
                fixed_response=vpclattice.CfnListener.FixedResponseProperty(
                    status_code=123
                ),
                forward=vpclattice.CfnListener.ForwardProperty(
                    target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
        
                        # the properties below are optional
                        weight=123
                    )]
                )
            ),
            protocol="protocol",
        
            # the properties below are optional
            name="name",
            port=123,
            service_identifier="serviceIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnListener.DefaultActionProperty", typing.Dict[builtins.str, typing.Any]]],
        protocol: builtins.str,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Listener``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param default_action: The action for the default rule. Each listener has a default rule. Each rule consists of a priority, one or more actions, and one or more conditions. The default rule is the rule that's used if no other rules match. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.
        :param protocol: The listener protocol HTTP or HTTPS.
        :param name: The name of the listener. A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param port: The listener port. You can specify a value from ``1`` to ``65535`` . For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param tags: The tags for the listener.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__73c2e416141e7ef0222f1f1653a309562bea8e8506b9533bdf17330d43a55e5b)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnListenerProps(
            default_action=default_action,
            protocol=protocol,
            name=name,
            port=port,
            service_identifier=service_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__12326ee41041465d2ba4da8b8ad4fde7ebba4ecae33893d007d9ccd35a96e583)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__af0732b404002622f3a0865c1e4c8538905f3b87bc5969b6b8453871072f745d)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the listener.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the listener.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service.

        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceId")
    def attr_service_id(self) -> builtins.str:
        '''The ID of the service.

        :cloudformationAttribute: ServiceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the listener.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="defaultAction")
    def default_action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.DefaultActionProperty"]:
        '''The action for the default rule.

        Each listener has a default rule. Each rule consists of a priority, one or more actions, and one or more conditions. The default rule is the rule that's used if no other rules match. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-defaultaction
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.DefaultActionProperty"], jsii.get(self, "defaultAction"))

    @default_action.setter
    def default_action(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.DefaultActionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__59cf95e2aa67f632d4dab721c41f6508baebb19658e79b89c2e07da445e5f1e1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "defaultAction", value)

    @builtins.property
    @jsii.member(jsii_name="protocol")
    def protocol(self) -> builtins.str:
        '''The listener protocol HTTP or HTTPS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-protocol
        '''
        return typing.cast(builtins.str, jsii.get(self, "protocol"))

    @protocol.setter
    def protocol(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f7c52e549bd6fb6641d37006b522005d505dfe672ab7e545bdd7502ed74c420c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "protocol", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the listener.

        A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4fa463ad8da953297419b70e31b57351de2348e405ace086f192861a997245)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="port")
    def port(self) -> typing.Optional[jsii.Number]:
        '''The listener port.

        You can specify a value from ``1`` to ``65535`` . For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-port
        '''
        return typing.cast(typing.Optional[jsii.Number], jsii.get(self, "port"))

    @port.setter
    def port(self, value: typing.Optional[jsii.Number]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__72ca6d7d647098025bbd81d7a18931f2e671a9e08ad86af511a05c973d05aca9)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "port", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8c147db701f108bf950b4c5a2af16e6ef53e8891f637adb3262fe302a15acc12)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnListener.DefaultActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fixed_response": "fixedResponse", "forward": "forward"},
    )
    class DefaultActionProperty:
        def __init__(
            self,
            *,
            fixed_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnListener.FixedResponseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnListener.ForwardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''The action for the default rule.

            Each listener has a default rule. Each rule consists of a priority, one or more actions, and one or more conditions. The default rule is the rule that's used if no other rules match. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

            :param fixed_response: Information about an action that returns a custom HTTP response.
            :param forward: Describes a forward action. You can use forward actions to route requests to one or more target groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                default_action_property = vpclattice.CfnListener.DefaultActionProperty(
                    fixed_response=vpclattice.CfnListener.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice.CfnListener.ForwardProperty(
                        target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                
                            # the properties below are optional
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0287abc785fecab6ab1087702d4a6cca9b64c71acbd133d0e2bbdc1de81595ff)
                check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fixed_response is not None:
                self._values["fixed_response"] = fixed_response
            if forward is not None:
                self._values["forward"] = forward

        @builtins.property
        def fixed_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.FixedResponseProperty"]]:
            '''Information about an action that returns a custom HTTP response.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html#cfn-vpclattice-listener-defaultaction-fixedresponse
            '''
            result = self._values.get("fixed_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.FixedResponseProperty"]], result)

        @builtins.property
        def forward(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.ForwardProperty"]]:
            '''Describes a forward action.

            You can use forward actions to route requests to one or more target groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-defaultaction.html#cfn-vpclattice-listener-defaultaction-forward
            '''
            result = self._values.get("forward")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.ForwardProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DefaultActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnListener.FixedResponseProperty",
        jsii_struct_bases=[],
        name_mapping={"status_code": "statusCode"},
    )
    class FixedResponseProperty:
        def __init__(self, *, status_code: jsii.Number) -> None:
            '''Information about an action that returns a custom HTTP response.

            :param status_code: The HTTP response code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-fixedresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                fixed_response_property = vpclattice.CfnListener.FixedResponseProperty(
                    status_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__81d112c1d223587396b51fc8f7ea66cf1311467ab28fa8307bc6bf5871bca8fe)
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "status_code": status_code,
            }

        @builtins.property
        def status_code(self) -> jsii.Number:
            '''The HTTP response code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-fixedresponse.html#cfn-vpclattice-listener-fixedresponse-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnListener.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnListener.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :param target_groups: The target groups. Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic. The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of traffic will go to that target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                forward_property = vpclattice.CfnListener.ForwardProperty(
                    target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                
                        # the properties below are optional
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0edc0eac6cf08dfafca941a895b9235e1388afd91b819a1cb4242c95e6969cec)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_groups": target_groups,
            }

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.WeightedTargetGroupProperty"]]]:
            '''The target groups.

            Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic.

            The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of traffic will go to that target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-forward.html#cfn-vpclattice-listener-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            assert result is not None, "Required property 'target_groups' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnListener.WeightedTargetGroupProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnListener.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: builtins.str,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the weight of a target group.

            :param target_group_identifier: The ID of the target group.
            :param weight: Only required if you specify multiple target groups for a forward action. The "weight" determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                weighted_target_group_property = vpclattice.CfnListener.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                
                    # the properties below are optional
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d4065ce9456c818a8231706c6240cf8ec601eb4a697f680c46cf226eb5bd7e09)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_group_identifier": target_group_identifier,
            }
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> builtins.str:
            '''The ID of the target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            assert result is not None, "Required property 'target_group_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Only required if you specify multiple target groups for a forward action.

            The "weight" determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-listener-weightedtargetgroup.html#cfn-vpclattice-listener-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnListenerProps",
    jsii_struct_bases=[],
    name_mapping={
        "default_action": "defaultAction",
        "protocol": "protocol",
        "name": "name",
        "port": "port",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnListenerProps:
    def __init__(
        self,
        *,
        default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]]],
        protocol: builtins.str,
        name: typing.Optional[builtins.str] = None,
        port: typing.Optional[jsii.Number] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnListener``.

        :param default_action: The action for the default rule. Each listener has a default rule. Each rule consists of a priority, one or more actions, and one or more conditions. The default rule is the rule that's used if no other rules match. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.
        :param protocol: The listener protocol HTTP or HTTPS.
        :param name: The name of the listener. A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param port: The listener port. You can specify a value from ``1`` to ``65535`` . For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param tags: The tags for the listener.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_listener_props = vpclattice.CfnListenerProps(
                default_action=vpclattice.CfnListener.DefaultActionProperty(
                    fixed_response=vpclattice.CfnListener.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice.CfnListener.ForwardProperty(
                        target_groups=[vpclattice.CfnListener.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
            
                            # the properties below are optional
                            weight=123
                        )]
                    )
                ),
                protocol="protocol",
            
                # the properties below are optional
                name="name",
                port=123,
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9ff2dd627386327f2b9b79c6458e2d44d1394267c935a5eae9ddfe867f634806)
            check_type(argname="argument default_action", value=default_action, expected_type=type_hints["default_action"])
            check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "default_action": default_action,
            "protocol": protocol,
        }
        if name is not None:
            self._values["name"] = name
        if port is not None:
            self._values["port"] = port
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def default_action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnListener.DefaultActionProperty]:
        '''The action for the default rule.

        Each listener has a default rule. Each rule consists of a priority, one or more actions, and one or more conditions. The default rule is the rule that's used if no other rules match. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-defaultaction
        '''
        result = self._values.get("default_action")
        assert result is not None, "Required property 'default_action' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnListener.DefaultActionProperty], result)

    @builtins.property
    def protocol(self) -> builtins.str:
        '''The listener protocol HTTP or HTTPS.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-protocol
        '''
        result = self._values.get("protocol")
        assert result is not None, "Required property 'protocol' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the listener.

        A listener name must be unique within a service. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def port(self) -> typing.Optional[jsii.Number]:
        '''The listener port.

        You can specify a value from ``1`` to ``65535`` . For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-port
        '''
        result = self._values.get("port")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the listener.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-listener.html#cfn-vpclattice-listener-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnListenerProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourcePolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnResourcePolicy",
):
    '''A CloudFormation ``AWS::VpcLattice::ResourcePolicy``.

    Retrieves information about the resource policy. The resource policy is an IAM policy created on behalf of the resource owner when they share a resource.

    :cloudformationResource: AWS::VpcLattice::ResourcePolicy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        # policy: Any
        
        cfn_resource_policy = vpclattice.CfnResourcePolicy(self, "MyCfnResourcePolicy",
            policy=policy,
            resource_arn="resourceArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        policy: typing.Any,
        resource_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ResourcePolicy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param policy: The Amazon Resource Name (ARN) of the service network or service.
        :param resource_arn: An IAM policy.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6ac4e206f522d10e45ed8695c98aa7d4578801cc302793ab783a4fb01f470996)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourcePolicyProps(policy=policy, resource_arn=resource_arn)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e263ac65b58fc049d4c19474eb5e6ef4cbfe321c0b44a3622ebbdb7a05fa86c1)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__16cf3f0d7c924801d4224e9bc1a5a3de3f58d2630ee09d51de4ffa940c47bcb4)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="policy")
    def policy(self) -> typing.Any:
        '''The Amazon Resource Name (ARN) of the service network or service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-policy
        '''
        return typing.cast(typing.Any, jsii.get(self, "policy"))

    @policy.setter
    def policy(self, value: typing.Any) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d8cd48c4b55dbc12516d3f066876df333b023212852663cce22a4dd67b235628)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policy", value)

    @builtins.property
    @jsii.member(jsii_name="resourceArn")
    def resource_arn(self) -> builtins.str:
        '''An IAM policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-resourcearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "resourceArn"))

    @resource_arn.setter
    def resource_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4559a915c278a3327c146870342a0e253462cec97a88340af321abf9513af9bb)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnResourcePolicyProps",
    jsii_struct_bases=[],
    name_mapping={"policy": "policy", "resource_arn": "resourceArn"},
)
class CfnResourcePolicyProps:
    def __init__(self, *, policy: typing.Any, resource_arn: builtins.str) -> None:
        '''Properties for defining a ``CfnResourcePolicy``.

        :param policy: The Amazon Resource Name (ARN) of the service network or service.
        :param resource_arn: An IAM policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            # policy: Any
            
            cfn_resource_policy_props = vpclattice.CfnResourcePolicyProps(
                policy=policy,
                resource_arn="resourceArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e31bafa278251cc933c6a6803b660f75813c3b162992cff3093896a8cacdcae)
            check_type(argname="argument policy", value=policy, expected_type=type_hints["policy"])
            check_type(argname="argument resource_arn", value=resource_arn, expected_type=type_hints["resource_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "policy": policy,
            "resource_arn": resource_arn,
        }

    @builtins.property
    def policy(self) -> typing.Any:
        '''The Amazon Resource Name (ARN) of the service network or service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-policy
        '''
        result = self._values.get("policy")
        assert result is not None, "Required property 'policy' is missing"
        return typing.cast(typing.Any, result)

    @builtins.property
    def resource_arn(self) -> builtins.str:
        '''An IAM policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-resourcepolicy.html#cfn-vpclattice-resourcepolicy-resourcearn
        '''
        result = self._values.get("resource_arn")
        assert result is not None, "Required property 'resource_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourcePolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnRule(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnRule",
):
    '''A CloudFormation ``AWS::VpcLattice::Rule``.

    Creates a listener rule. Each listener has a default rule for checking connection requests, but you can define additional rules. Each rule consists of a priority, one or more actions, and one or more conditions. For more information, see `Listener rules <https://docs.aws.amazon.com/vpc-lattice/latest/ug/listeners.html#listener-rules>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::Rule
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_rule = vpclattice.CfnRule(self, "MyCfnRule",
            action=vpclattice.CfnRule.ActionProperty(
                fixed_response=vpclattice.CfnRule.FixedResponseProperty(
                    status_code=123
                ),
                forward=vpclattice.CfnRule.ForwardProperty(
                    target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
        
                        # the properties below are optional
                        weight=123
                    )]
                )
            ),
            match=vpclattice.CfnRule.MatchProperty(
                http_match=vpclattice.CfnRule.HttpMatchProperty(
                    header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                        match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name",
        
                        # the properties below are optional
                        case_sensitive=False
                    )],
                    method="method",
                    path_match=vpclattice.CfnRule.PathMatchProperty(
                        match=vpclattice.CfnRule.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        ),
        
                        # the properties below are optional
                        case_sensitive=False
                    )
                )
            ),
            priority=123,
        
            # the properties below are optional
            listener_identifier="listenerIdentifier",
            name="name",
            service_identifier="serviceIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.ActionProperty", typing.Dict[builtins.str, typing.Any]]],
        match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.MatchProperty", typing.Dict[builtins.str, typing.Any]]],
        priority: jsii.Number,
        listener_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Rule``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param action: Describes the action for a rule. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.
        :param match: The rule match.
        :param priority: The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        :param listener_identifier: The ID or Amazon Resource Name (ARN) of the listener.
        :param name: The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param tags: The tags for the rule.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__449a68437024cae294f2a7c8eab201a5ef1ea3160260d7ae9d0157d7eccc4cbf)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnRuleProps(
            action=action,
            match=match,
            priority=priority,
            listener_identifier=listener_identifier,
            name=name,
            service_identifier=service_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f930114bcf2b12fea371498e5b19a32f6acd368dc4154e1e097d7321a3925085)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ea7ae3dc0625947bab64ba7e822719c3e517563f3824f5f9ba85e64041b92e4e)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the rule.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the listener.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="action")
    def action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionProperty"]:
        '''Describes the action for a rule.

        Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-action
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionProperty"], jsii.get(self, "action"))

    @action.setter
    def action(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ActionProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2e32eb6ee9dcb9009c73db8fca2988a7b4aead84cb028572ddd439898ddaa4ca)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "action", value)

    @builtins.property
    @jsii.member(jsii_name="match")
    def match(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.MatchProperty"]:
        '''The rule match.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-match
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.MatchProperty"], jsii.get(self, "match"))

    @match.setter
    def match(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.MatchProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d5fe1d8208e0e1751bef2f95e6b8ebf5d940d6cd1f301fde28983b5677280181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "match", value)

    @builtins.property
    @jsii.member(jsii_name="priority")
    def priority(self) -> jsii.Number:
        '''The priority assigned to the rule.

        Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-priority
        '''
        return typing.cast(jsii.Number, jsii.get(self, "priority"))

    @priority.setter
    def priority(self, value: jsii.Number) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__f73272751ae6cbf92bfb950a6ad165cc0d44d9aadfb471b02d23f4f75bde89c7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "priority", value)

    @builtins.property
    @jsii.member(jsii_name="listenerIdentifier")
    def listener_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the listener.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-listeneridentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "listenerIdentifier"))

    @listener_identifier.setter
    def listener_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bad509bb92805c4fd1cb398cc3f5f0f8aced007a58fe592e5fd563c4b9d091f4)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "listenerIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__466901c7a357c7de931d773fd28b10eee0befec10228407d6273802148a74586)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__dc44908fa7a0058a0f5b82695f7acdcfcba9bd43fe7ca0287d2a031d475e1894)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.ActionProperty",
        jsii_struct_bases=[],
        name_mapping={"fixed_response": "fixedResponse", "forward": "forward"},
    )
    class ActionProperty:
        def __init__(
            self,
            *,
            fixed_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.FixedResponseProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            forward: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.ForwardProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes the action for a rule.

            Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

            :param fixed_response: Describes the rule action that returns a custom HTTP response.
            :param forward: The forward action. Traffic that matches the rule is forwarded to the specified target groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                action_property = vpclattice.CfnRule.ActionProperty(
                    fixed_response=vpclattice.CfnRule.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice.CfnRule.ForwardProperty(
                        target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
                
                            # the properties below are optional
                            weight=123
                        )]
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0a7636f2c1e092c4d185db7dcea003bb5cd7045207402560714659e1d3473f54)
                check_type(argname="argument fixed_response", value=fixed_response, expected_type=type_hints["fixed_response"])
                check_type(argname="argument forward", value=forward, expected_type=type_hints["forward"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if fixed_response is not None:
                self._values["fixed_response"] = fixed_response
            if forward is not None:
                self._values["forward"] = forward

        @builtins.property
        def fixed_response(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.FixedResponseProperty"]]:
            '''Describes the rule action that returns a custom HTTP response.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html#cfn-vpclattice-rule-action-fixedresponse
            '''
            result = self._values.get("fixed_response")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.FixedResponseProperty"]], result)

        @builtins.property
        def forward(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ForwardProperty"]]:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-action.html#cfn-vpclattice-rule-action-forward
            '''
            result = self._values.get("forward")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.ForwardProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.FixedResponseProperty",
        jsii_struct_bases=[],
        name_mapping={"status_code": "statusCode"},
    )
    class FixedResponseProperty:
        def __init__(self, *, status_code: jsii.Number) -> None:
            '''Information about an action that returns a custom HTTP response.

            :param status_code: The HTTP response code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-fixedresponse.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                fixed_response_property = vpclattice.CfnRule.FixedResponseProperty(
                    status_code=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__fa671287577ce7d7058b29cf609e1c5e01afed04e36883edef5c2245dd755289)
                check_type(argname="argument status_code", value=status_code, expected_type=type_hints["status_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "status_code": status_code,
            }

        @builtins.property
        def status_code(self) -> jsii.Number:
            '''The HTTP response code.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-fixedresponse.html#cfn-vpclattice-rule-fixedresponse-statuscode
            '''
            result = self._values.get("status_code")
            assert result is not None, "Required property 'status_code' is missing"
            return typing.cast(jsii.Number, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "FixedResponseProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.ForwardProperty",
        jsii_struct_bases=[],
        name_mapping={"target_groups": "targetGroups"},
    )
    class ForwardProperty:
        def __init__(
            self,
            *,
            target_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.WeightedTargetGroupProperty", typing.Dict[builtins.str, typing.Any]]]]],
        ) -> None:
            '''The forward action.

            Traffic that matches the rule is forwarded to the specified target groups.

            :param target_groups: The target groups. Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic. The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of traffic will go to that target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                forward_property = vpclattice.CfnRule.ForwardProperty(
                    target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                        target_group_identifier="targetGroupIdentifier",
                
                        # the properties below are optional
                        weight=123
                    )]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b80cd57c837960266ed58cdf4639c584e66a9112623d660bf6fad9a74f04dbaf)
                check_type(argname="argument target_groups", value=target_groups, expected_type=type_hints["target_groups"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_groups": target_groups,
            }

        @builtins.property
        def target_groups(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.WeightedTargetGroupProperty"]]]:
            '''The target groups.

            Traffic matching the rule is forwarded to the specified target groups. With forward actions, you can assign a weight that controls the prioritization and selection of each target group. This means that requests are distributed to individual target groups based on their weights. For example, if two target groups have the same weight, each target group receives half of the traffic.

            The default value is 1. This means that if only one target group is provided, there is no need to set the weight; 100% of traffic will go to that target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-forward.html#cfn-vpclattice-rule-forward-targetgroups
            '''
            result = self._values.get("target_groups")
            assert result is not None, "Required property 'target_groups' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.WeightedTargetGroupProperty"]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ForwardProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.HeaderMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "match": "match",
            "name": "name",
            "case_sensitive": "caseSensitive",
        },
    )
    class HeaderMatchProperty:
        def __init__(
            self,
            *,
            match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.HeaderMatchTypeProperty", typing.Dict[builtins.str, typing.Any]]],
            name: builtins.str,
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes the constraints for a header match.

            Matches incoming requests with rule based on request header value before applying rule action.

            :param match: The header match type.
            :param name: The name of the header.
            :param case_sensitive: Indicates whether the match is case sensitive. Defaults to false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                header_match_property = vpclattice.CfnRule.HeaderMatchProperty(
                    match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                        contains="contains",
                        exact="exact",
                        prefix="prefix"
                    ),
                    name="name",
                
                    # the properties below are optional
                    case_sensitive=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f8e23f5a1cc6130bd5632a87a2ce0e1341a017ea4acc46d48787bb148eab30ef)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument name", value=name, expected_type=type_hints["name"])
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "match": match,
                "name": name,
            }
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HeaderMatchTypeProperty"]:
            '''The header match type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HeaderMatchTypeProperty"], result)

        @builtins.property
        def name(self) -> builtins.str:
            '''The name of the header.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-name
            '''
            result = self._values.get("name")
            assert result is not None, "Required property 'name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the match is case sensitive.

            Defaults to false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatch.html#cfn-vpclattice-rule-headermatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.HeaderMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"contains": "contains", "exact": "exact", "prefix": "prefix"},
    )
    class HeaderMatchTypeProperty:
        def __init__(
            self,
            *,
            contains: typing.Optional[builtins.str] = None,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a header match type.

            Only one can be provided.

            :param contains: Specifies a contains type match.
            :param exact: Specifies an exact type match.
            :param prefix: Specifies a prefix type match. Matches the value with the prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                header_match_type_property = vpclattice.CfnRule.HeaderMatchTypeProperty(
                    contains="contains",
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d03297d1a6a9c36744af6134cbe142b2afa806b8017b921ebdebbb0e575a4bcd)
                check_type(argname="argument contains", value=contains, expected_type=type_hints["contains"])
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if contains is not None:
                self._values["contains"] = contains
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def contains(self) -> typing.Optional[builtins.str]:
            '''Specifies a contains type match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-contains
            '''
            result = self._values.get("contains")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''Specifies an exact type match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''Specifies a prefix type match.

            Matches the value with the prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-headermatchtype.html#cfn-vpclattice-rule-headermatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HeaderMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.HttpMatchProperty",
        jsii_struct_bases=[],
        name_mapping={
            "header_matches": "headerMatches",
            "method": "method",
            "path_match": "pathMatch",
        },
    )
    class HttpMatchProperty:
        def __init__(
            self,
            *,
            header_matches: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.HeaderMatchProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            method: typing.Optional[builtins.str] = None,
            path_match: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.PathMatchProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Describes criteria that can be applied to incoming requests.

            :param header_matches: The header matches. Matches incoming requests with rule based on request header value before applying rule action.
            :param method: The HTTP method type.
            :param path_match: The path match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                http_match_property = vpclattice.CfnRule.HttpMatchProperty(
                    header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                        match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                            contains="contains",
                            exact="exact",
                            prefix="prefix"
                        ),
                        name="name",
                
                        # the properties below are optional
                        case_sensitive=False
                    )],
                    method="method",
                    path_match=vpclattice.CfnRule.PathMatchProperty(
                        match=vpclattice.CfnRule.PathMatchTypeProperty(
                            exact="exact",
                            prefix="prefix"
                        ),
                
                        # the properties below are optional
                        case_sensitive=False
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ace69d7b1df81bf1f297efe4b3972c65d727c7dde4a3926fd1d446ff8cf20a8e)
                check_type(argname="argument header_matches", value=header_matches, expected_type=type_hints["header_matches"])
                check_type(argname="argument method", value=method, expected_type=type_hints["method"])
                check_type(argname="argument path_match", value=path_match, expected_type=type_hints["path_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if header_matches is not None:
                self._values["header_matches"] = header_matches
            if method is not None:
                self._values["method"] = method
            if path_match is not None:
                self._values["path_match"] = path_match

        @builtins.property
        def header_matches(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HeaderMatchProperty"]]]]:
            '''The header matches.

            Matches incoming requests with rule based on request header value before applying rule action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-headermatches
            '''
            result = self._values.get("header_matches")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HeaderMatchProperty"]]]], result)

        @builtins.property
        def method(self) -> typing.Optional[builtins.str]:
            '''The HTTP method type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-method
            '''
            result = self._values.get("method")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def path_match(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PathMatchProperty"]]:
            '''The path match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-httpmatch.html#cfn-vpclattice-rule-httpmatch-pathmatch
            '''
            result = self._values.get("path_match")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PathMatchProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HttpMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.MatchProperty",
        jsii_struct_bases=[],
        name_mapping={"http_match": "httpMatch"},
    )
    class MatchProperty:
        def __init__(
            self,
            *,
            http_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.HttpMatchProperty", typing.Dict[builtins.str, typing.Any]]],
        ) -> None:
            '''Describes a rule match.

            :param http_match: The HTTP criteria that a rule must match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                match_property = vpclattice.CfnRule.MatchProperty(
                    http_match=vpclattice.CfnRule.HttpMatchProperty(
                        header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                            match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name",
                
                            # the properties below are optional
                            case_sensitive=False
                        )],
                        method="method",
                        path_match=vpclattice.CfnRule.PathMatchProperty(
                            match=vpclattice.CfnRule.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            ),
                
                            # the properties below are optional
                            case_sensitive=False
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__322643cd06fdf5bd3a2477b093a654dd58ac591eba88be254b56c3790c21b79e)
                check_type(argname="argument http_match", value=http_match, expected_type=type_hints["http_match"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "http_match": http_match,
            }

        @builtins.property
        def http_match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HttpMatchProperty"]:
            '''The HTTP criteria that a rule must match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-match.html#cfn-vpclattice-rule-match-httpmatch
            '''
            result = self._values.get("http_match")
            assert result is not None, "Required property 'http_match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.HttpMatchProperty"], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.PathMatchProperty",
        jsii_struct_bases=[],
        name_mapping={"match": "match", "case_sensitive": "caseSensitive"},
    )
    class PathMatchProperty:
        def __init__(
            self,
            *,
            match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnRule.PathMatchTypeProperty", typing.Dict[builtins.str, typing.Any]]],
            case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        ) -> None:
            '''Describes the conditions that can be applied when matching a path for incoming requests.

            :param match: The type of path match.
            :param case_sensitive: Indicates whether the match is case sensitive. Defaults to false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                path_match_property = vpclattice.CfnRule.PathMatchProperty(
                    match=vpclattice.CfnRule.PathMatchTypeProperty(
                        exact="exact",
                        prefix="prefix"
                    ),
                
                    # the properties below are optional
                    case_sensitive=False
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__689b2016adad8bf157bdb2290c2bd18a5bf6f18cb41b84efeedd18f85c1cc3c0)
                check_type(argname="argument match", value=match, expected_type=type_hints["match"])
                check_type(argname="argument case_sensitive", value=case_sensitive, expected_type=type_hints["case_sensitive"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "match": match,
            }
            if case_sensitive is not None:
                self._values["case_sensitive"] = case_sensitive

        @builtins.property
        def match(
            self,
        ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PathMatchTypeProperty"]:
            '''The type of path match.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-match
            '''
            result = self._values.get("match")
            assert result is not None, "Required property 'match' is missing"
            return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnRule.PathMatchTypeProperty"], result)

        @builtins.property
        def case_sensitive(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether the match is case sensitive.

            Defaults to false.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatch.html#cfn-vpclattice-rule-pathmatch-casesensitive
            '''
            result = self._values.get("case_sensitive")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.PathMatchTypeProperty",
        jsii_struct_bases=[],
        name_mapping={"exact": "exact", "prefix": "prefix"},
    )
    class PathMatchTypeProperty:
        def __init__(
            self,
            *,
            exact: typing.Optional[builtins.str] = None,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes a path match type.

            Each rule can include only one of the following types of paths.

            :param exact: An exact match of the path.
            :param prefix: A prefix match of the path.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                path_match_type_property = vpclattice.CfnRule.PathMatchTypeProperty(
                    exact="exact",
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__271814c8dfb45c778ed9f0693250e0448398d761ce2928ea0325c1ad2535383d)
                check_type(argname="argument exact", value=exact, expected_type=type_hints["exact"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if exact is not None:
                self._values["exact"] = exact
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def exact(self) -> typing.Optional[builtins.str]:
            '''An exact match of the path.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-exact
            '''
            result = self._values.get("exact")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''A prefix match of the path.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-pathmatchtype.html#cfn-vpclattice-rule-pathmatchtype-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PathMatchTypeProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnRule.WeightedTargetGroupProperty",
        jsii_struct_bases=[],
        name_mapping={
            "target_group_identifier": "targetGroupIdentifier",
            "weight": "weight",
        },
    )
    class WeightedTargetGroupProperty:
        def __init__(
            self,
            *,
            target_group_identifier: builtins.str,
            weight: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes the weight of a target group.

            :param target_group_identifier: The ID of the target group.
            :param weight: Only required if you specify multiple target groups for a forward action. The "weight" determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                weighted_target_group_property = vpclattice.CfnRule.WeightedTargetGroupProperty(
                    target_group_identifier="targetGroupIdentifier",
                
                    # the properties below are optional
                    weight=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__e36be1c2a6fbc4f36b79ea32dc3b8a682844db6ad04181ad8e6c98172d55f160)
                check_type(argname="argument target_group_identifier", value=target_group_identifier, expected_type=type_hints["target_group_identifier"])
                check_type(argname="argument weight", value=weight, expected_type=type_hints["weight"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "target_group_identifier": target_group_identifier,
            }
            if weight is not None:
                self._values["weight"] = weight

        @builtins.property
        def target_group_identifier(self) -> builtins.str:
            '''The ID of the target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-targetgroupidentifier
            '''
            result = self._values.get("target_group_identifier")
            assert result is not None, "Required property 'target_group_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def weight(self) -> typing.Optional[jsii.Number]:
            '''Only required if you specify multiple target groups for a forward action.

            The "weight" determines how requests are distributed to the target group. For example, if you specify two target groups, each with a weight of 10, each target group receives half the requests. If you specify two target groups, one with a weight of 10 and the other with a weight of 20, the target group with a weight of 20 receives twice as many requests as the other target group. If there's only one target group specified, then the default value is 100.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-rule-weightedtargetgroup.html#cfn-vpclattice-rule-weightedtargetgroup-weight
            '''
            result = self._values.get("weight")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "WeightedTargetGroupProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnRuleProps",
    jsii_struct_bases=[],
    name_mapping={
        "action": "action",
        "match": "match",
        "priority": "priority",
        "listener_identifier": "listenerIdentifier",
        "name": "name",
        "service_identifier": "serviceIdentifier",
        "tags": "tags",
    },
)
class CfnRuleProps:
    def __init__(
        self,
        *,
        action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
        match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]]],
        priority: jsii.Number,
        listener_identifier: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnRule``.

        :param action: Describes the action for a rule. Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.
        :param match: The rule match.
        :param priority: The priority assigned to the rule. Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.
        :param listener_identifier: The ID or Amazon Resource Name (ARN) of the listener.
        :param name: The name of the rule. The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param tags: The tags for the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_rule_props = vpclattice.CfnRuleProps(
                action=vpclattice.CfnRule.ActionProperty(
                    fixed_response=vpclattice.CfnRule.FixedResponseProperty(
                        status_code=123
                    ),
                    forward=vpclattice.CfnRule.ForwardProperty(
                        target_groups=[vpclattice.CfnRule.WeightedTargetGroupProperty(
                            target_group_identifier="targetGroupIdentifier",
            
                            # the properties below are optional
                            weight=123
                        )]
                    )
                ),
                match=vpclattice.CfnRule.MatchProperty(
                    http_match=vpclattice.CfnRule.HttpMatchProperty(
                        header_matches=[vpclattice.CfnRule.HeaderMatchProperty(
                            match=vpclattice.CfnRule.HeaderMatchTypeProperty(
                                contains="contains",
                                exact="exact",
                                prefix="prefix"
                            ),
                            name="name",
            
                            # the properties below are optional
                            case_sensitive=False
                        )],
                        method="method",
                        path_match=vpclattice.CfnRule.PathMatchProperty(
                            match=vpclattice.CfnRule.PathMatchTypeProperty(
                                exact="exact",
                                prefix="prefix"
                            ),
            
                            # the properties below are optional
                            case_sensitive=False
                        )
                    )
                ),
                priority=123,
            
                # the properties below are optional
                listener_identifier="listenerIdentifier",
                name="name",
                service_identifier="serviceIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__42762c23e983fcbf07f7dc222e57f41928eeb28308d39c51c5cad23f5eaadd0b)
            check_type(argname="argument action", value=action, expected_type=type_hints["action"])
            check_type(argname="argument match", value=match, expected_type=type_hints["match"])
            check_type(argname="argument priority", value=priority, expected_type=type_hints["priority"])
            check_type(argname="argument listener_identifier", value=listener_identifier, expected_type=type_hints["listener_identifier"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "action": action,
            "match": match,
            "priority": priority,
        }
        if listener_identifier is not None:
            self._values["listener_identifier"] = listener_identifier
        if name is not None:
            self._values["name"] = name
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def action(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionProperty]:
        '''Describes the action for a rule.

        Each rule must include exactly one of the following types of actions: ``forward`` or ``fixed-response`` , and it must be the last action to be performed.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-action
        '''
        result = self._values.get("action")
        assert result is not None, "Required property 'action' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionProperty], result)

    @builtins.property
    def match(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.MatchProperty]:
        '''The rule match.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-match
        '''
        result = self._values.get("match")
        assert result is not None, "Required property 'match' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.MatchProperty], result)

    @builtins.property
    def priority(self) -> jsii.Number:
        '''The priority assigned to the rule.

        Each rule for a specific listener must have a unique priority. The lower the priority number the higher the priority.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-priority
        '''
        result = self._values.get("priority")
        assert result is not None, "Required property 'priority' is missing"
        return typing.cast(jsii.Number, result)

    @builtins.property
    def listener_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the listener.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-listeneridentifier
        '''
        result = self._values.get("listener_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the rule.

        The name must be unique within the listener. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the rule.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-rule.html#cfn-vpclattice-rule-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnRuleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnService(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnService",
):
    '''A CloudFormation ``AWS::VpcLattice::Service``.

    Creates a service. A service is any software application that can run on instances containers, or serverless functions within an account or virtual private cloud (VPC).

    For more information, see `Services <https://docs.aws.amazon.com/vpc-lattice/latest/ug/services.html>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::Service
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_service = vpclattice.CfnService(self, "MyCfnService",
            auth_type="authType",
            certificate_arn="certificateArn",
            custom_domain_name="customDomainName",
            dns_entry=vpclattice.CfnService.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnService.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::Service``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.
        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate.
        :param custom_domain_name: The custom domain name of the service.
        :param dns_entry: ``AWS::VpcLattice::Service.DnsEntry``.
        :param name: The name of the service. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the service.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__574a9fc7fbfd4823f696563f89b0102cc0f6583c712edcaf1ecb150cbcc76a73)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceProps(
            auth_type=auth_type,
            certificate_arn=certificate_arn,
            custom_domain_name=custom_domain_name,
            dns_entry=dns_entry,
            name=name,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__363d7113f186d64cb19a002eccc489e303250c3fdacfc7148a68073429b1d3ca)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e18adbacd4ff6c812cb081d4b16288cfe8c9a3e290141e16cd903040253f5279)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time that the service was created, specified in ISO-8601 format.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryDomainName")
    def attr_dns_entry_domain_name(self) -> builtins.str:
        '''The domain name of the service.

        :cloudformationAttribute: DnsEntry.DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryHostedZoneId")
    def attr_dns_entry_hosted_zone_id(self) -> builtins.str:
        '''The ID of the hosted zone.

        :cloudformationAttribute: DnsEntry.HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the service.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''The date and time that the service was last updated, specified in ISO-8601 format.

        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the service.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-authtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__34adbe2b62d87281978a226c9372355bb2d3e807d44d0c2864f2e56ed5b96330)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="certificateArn")
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-certificatearn
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "certificateArn"))

    @certificate_arn.setter
    def certificate_arn(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__97271e8f62efdbac1637a3dbaee6fd46350f99f443897aea1f0c35bdea726880)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "certificateArn", value)

    @builtins.property
    @jsii.member(jsii_name="customDomainName")
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The custom domain name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-customdomainname
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "customDomainName"))

    @custom_domain_name.setter
    def custom_domain_name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__36235e17375fd8756324abec6e1d0541cdc4ffe0e06d8c3a4cfecd1f0394cf76)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "customDomainName", value)

    @builtins.property
    @jsii.member(jsii_name="dnsEntry")
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsEntryProperty"]]:
        '''``AWS::VpcLattice::Service.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-dnsentry
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsEntryProperty"]], jsii.get(self, "dnsEntry"))

    @dns_entry.setter
    def dns_entry(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnService.DnsEntryProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__86331259a92160f0cd63dbc4aab784bed2c1d7ed59e79a25ba5003164e44283b)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEntry", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e6d952c67f75aa6f1686ce409690bdb1e9b683e8516c4842eed66a7e31358d29)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnService.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the DNS information of a service.

            :param domain_name: The domain name of the service.
            :param hosted_zone_id: The ID of the hosted zone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                dns_entry_property = vpclattice.CfnService.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b65282857e662c4b074767c1cc3d9d545d5d1cd40b51ed7ca75b63c2337997f)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name of the service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hosted zone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-service-dnsentry.html#cfn-vpclattice-service-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServiceNetwork(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetwork",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetwork``.

    Creates a service network. A service network is a logical boundary for a collection of services. You can associate services and VPCs with a service network.

    For more information, see `Service networks <https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-networks.html>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::ServiceNetwork
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_service_network = vpclattice.CfnServiceNetwork(self, "MyCfnServiceNetwork",
            auth_type="authType",
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetwork``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.
        :param name: The name of the service network. The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the service network.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cf9e980e993af8f7fa107ecb42a9f54ba4206aa20d89a5d465c68ac523c26dcb)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkProps(auth_type=auth_type, name=name, tags=tags)

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e97a2294e65c5976c9ca7e8f584b3ecf913f35c7fe4abe9771df269960960bb5)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9a40dc59d6df6fac2bdb2d133d19bf20fae8a7d14bedf0e4f6cad8f5511c9c3f)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service network.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time that the service network was created, specified in ISO-8601 format.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the service network.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''The date and time of the last update, specified in ISO-8601 format.

        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the service network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="authType")
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-authtype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "authType"))

    @auth_type.setter
    def auth_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c06098786978ca47bd316c848db6890bab981efa66b884ed7bd992f91d933a10)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "authType", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service network.

        The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0c1243a59c334b22e93d8c8e21aa09a8bca564fda7479f2c980b9a64a791f2b5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkProps",
    jsii_struct_bases=[],
    name_mapping={"auth_type": "authType", "name": "name", "tags": "tags"},
)
class CfnServiceNetworkProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetwork``.

        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.
        :param name: The name of the service network. The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the service network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_service_network_props = vpclattice.CfnServiceNetworkProps(
                auth_type="authType",
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__d90fcb9ad7227e77958171d1511828ad181196daf3cc4389f6a52b57ca1a3500)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service network.

        The name must be unique to the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the service network.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetwork.html#cfn-vpclattice-servicenetwork-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServiceNetworkServiceAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkServiceAssociation",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetworkServiceAssociation``.

    Associates a service with a service network.

    You can't use this operation if the service and service network are already associated or if there is a disassociation or deletion in progress. If the association fails, you can retry the operation by deleting the association and recreating it.

    You cannot associate a service and service network that are shared with a caller. The caller must own either the service or the service network.

    As a result of this operation, the association is created in the service network account and the association owner account.

    :cloudformationResource: AWS::VpcLattice::ServiceNetworkServiceAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_service_network_service_association = vpclattice.CfnServiceNetworkServiceAssociation(self, "MyCfnServiceNetworkServiceAssociation",
            dns_entry=vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                domain_name="domainName",
                hosted_zone_id="hostedZoneId"
            ),
            service_identifier="serviceIdentifier",
            service_network_identifier="serviceNetworkIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnServiceNetworkServiceAssociation.DnsEntryProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetworkServiceAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param dns_entry: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param service_network_identifier: The ID or Amazon Resource Name (ARN) of the service network. You must use the ARN if the resources specified in the operation are in different accounts.
        :param tags: The tags for the association.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__725216d9e151e558fef4ee185a2250a5071d6159c22db7b512e98514c6f09e3f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkServiceAssociationProps(
            dns_entry=dns_entry,
            service_identifier=service_identifier,
            service_network_identifier=service_network_identifier,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e5217fecc0205495947f33aae71e31b7d764477fac93ce91d651bad8b1c5983)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__74c342d7bd4a5c4d3d62426cf092bcfcd27641ede95b333b5f04efe443ed7203)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the association between the service network and the service.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time that the association was created, specified in ISO-8601 format.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryDomainName")
    def attr_dns_entry_domain_name(self) -> builtins.str:
        '''The domain name of the service.

        :cloudformationAttribute: DnsEntry.DomainName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryDomainName"))

    @builtins.property
    @jsii.member(jsii_name="attrDnsEntryHostedZoneId")
    def attr_dns_entry_hosted_zone_id(self) -> builtins.str:
        '''The ID of the hosted zone.

        :cloudformationAttribute: DnsEntry.HostedZoneId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrDnsEntryHostedZoneId"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the of the association between the service network and the service.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceArn")
    def attr_service_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service.

        :cloudformationAttribute: ServiceArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceId")
    def attr_service_id(self) -> builtins.str:
        '''The ID of the service.

        :cloudformationAttribute: ServiceId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceName")
    def attr_service_name(self) -> builtins.str:
        '''The name of the service.

        :cloudformationAttribute: ServiceName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceName"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkArn")
    def attr_service_network_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service network.

        :cloudformationAttribute: ServiceNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkId")
    def attr_service_network_id(self) -> builtins.str:
        '''The ID of the service network.

        :cloudformationAttribute: ServiceNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkName")
    def attr_service_network_name(self) -> builtins.str:
        '''The name of the service network.

        :cloudformationAttribute: ServiceNetworkName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the association between the service network and the service.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="dnsEntry")
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServiceNetworkServiceAssociation.DnsEntryProperty"]]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServiceNetworkServiceAssociation.DnsEntryProperty"]], jsii.get(self, "dnsEntry"))

    @dns_entry.setter
    def dns_entry(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnServiceNetworkServiceAssociation.DnsEntryProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__75407ce59d1c225c82424a53c51a9dc98fd99a8760c2356feed36faf3b7f2ef3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "dnsEntry", value)

    @builtins.property
    @jsii.member(jsii_name="serviceIdentifier")
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-serviceidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceIdentifier"))

    @service_identifier.setter
    def service_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cc145dd6109e6aabc8144c9e009f031414aef280d1dba52b642a580208dcb0d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network.

        You must use the ARN if the resources specified in the operation are in different accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-servicenetworkidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkIdentifier"))

    @service_network_identifier.setter
    def service_network_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a8dc5f20ba5a3082774195b7fce34bc7111b2f6199a0d9e5f0e03d252d4a0172)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNetworkIdentifier", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty",
        jsii_struct_bases=[],
        name_mapping={"domain_name": "domainName", "hosted_zone_id": "hostedZoneId"},
    )
    class DnsEntryProperty:
        def __init__(
            self,
            *,
            domain_name: typing.Optional[builtins.str] = None,
            hosted_zone_id: typing.Optional[builtins.str] = None,
        ) -> None:
            '''DNS information about the service.

            :param domain_name: The domain name of the service.
            :param hosted_zone_id: The ID of the hosted zone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                dns_entry_property = vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bc0e9982b4fa1e75bd51f775a1c566a55f792f725e1ddf2b90edc3edeae2edf9)
                check_type(argname="argument domain_name", value=domain_name, expected_type=type_hints["domain_name"])
                check_type(argname="argument hosted_zone_id", value=hosted_zone_id, expected_type=type_hints["hosted_zone_id"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if domain_name is not None:
                self._values["domain_name"] = domain_name
            if hosted_zone_id is not None:
                self._values["hosted_zone_id"] = hosted_zone_id

        @builtins.property
        def domain_name(self) -> typing.Optional[builtins.str]:
            '''The domain name of the service.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-domainname
            '''
            result = self._values.get("domain_name")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def hosted_zone_id(self) -> typing.Optional[builtins.str]:
            '''The ID of the hosted zone.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-servicenetworkserviceassociation-dnsentry.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry-hostedzoneid
            '''
            result = self._values.get("hosted_zone_id")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "DnsEntryProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkServiceAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "dns_entry": "dnsEntry",
        "service_identifier": "serviceIdentifier",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
    },
)
class CfnServiceNetworkServiceAssociationProps:
    def __init__(
        self,
        *,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        service_identifier: typing.Optional[builtins.str] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetworkServiceAssociation``.

        :param dns_entry: ``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.
        :param service_identifier: The ID or Amazon Resource Name (ARN) of the service.
        :param service_network_identifier: The ID or Amazon Resource Name (ARN) of the service network. You must use the ARN if the resources specified in the operation are in different accounts.
        :param tags: The tags for the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_service_network_service_association_props = vpclattice.CfnServiceNetworkServiceAssociationProps(
                dns_entry=vpclattice.CfnServiceNetworkServiceAssociation.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                service_identifier="serviceIdentifier",
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cbd27ac9bacaa2bb68de68c8b7e1590df098073a6694f4adbe8e3b2c234c901c)
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument service_identifier", value=service_identifier, expected_type=type_hints["service_identifier"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if service_identifier is not None:
            self._values["service_identifier"] = service_identifier
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServiceNetworkServiceAssociation.DnsEntryProperty]]:
        '''``AWS::VpcLattice::ServiceNetworkServiceAssociation.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServiceNetworkServiceAssociation.DnsEntryProperty]], result)

    @builtins.property
    def service_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-serviceidentifier
        '''
        result = self._values.get("service_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network.

        You must use the ARN if the resources specified in the operation are in different accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkserviceassociation.html#cfn-vpclattice-servicenetworkserviceassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkServiceAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnServiceNetworkVpcAssociation(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkVpcAssociation",
):
    '''A CloudFormation ``AWS::VpcLattice::ServiceNetworkVpcAssociation``.

    Associates a VPC with a service network. When you associate a VPC with the service network, it enables all the resources within that VPC to be clients and communicate with other services in the service network. For more information, see `Manage VPC associations <https://docs.aws.amazon.com/vpc-lattice/latest/ug/service-network-associations.html#service-network-vpc-associations>`_ in the *Amazon VPC Lattice User Guide* .

    You can't use this operation if there is a disassociation in progress. If the association fails, retry by deleting the association and recreating it.

    As a result of this operation, the association gets created in the service network account and the VPC owner account.

    If you add a security group to the service network and VPC association, the association must continue to always have at least one security group. You can add or edit security groups at any time. However, to remove all security groups, you must first delete the association and recreate it without security groups.

    :cloudformationResource: AWS::VpcLattice::ServiceNetworkVpcAssociation
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_service_network_vpc_association = vpclattice.CfnServiceNetworkVpcAssociation(self, "MyCfnServiceNetworkVpcAssociation",
            security_group_ids=["securityGroupIds"],
            service_network_identifier="serviceNetworkIdentifier",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            vpc_identifier="vpcIdentifier"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::ServiceNetworkVpcAssociation``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param security_group_ids: The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
        :param service_network_identifier: The ID or Amazon Resource Name (ARN) of the service network. You must use the ARN when the resources specified in the operation are in different accounts.
        :param tags: The tags for the association.
        :param vpc_identifier: The ID of the VPC.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b013dda832236717519889ff6a2a2a5417720106cf5a7739a5881fa4abf83ec)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnServiceNetworkVpcAssociationProps(
            security_group_ids=security_group_ids,
            service_network_identifier=service_network_identifier,
            tags=tags,
            vpc_identifier=vpc_identifier,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed4e55a3f0b029c5560c7497739808da68a12f1cd2548f324656c556b8d7d02c)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3cd4c9386c4eb083c995c2a77d6d57793179b2895e73119f7ed567a5423d0256)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the association between the service network and the VPC.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time that the association was created, specified in ISO-8601 format.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the specified association between the service network and the VPC.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkArn")
    def attr_service_network_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the service network.

        :cloudformationAttribute: ServiceNetworkArn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkArn"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkId")
    def attr_service_network_id(self) -> builtins.str:
        '''The ID of the service network.

        :cloudformationAttribute: ServiceNetworkId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkId"))

    @builtins.property
    @jsii.member(jsii_name="attrServiceNetworkName")
    def attr_service_network_name(self) -> builtins.str:
        '''The name of the service network.

        :cloudformationAttribute: ServiceNetworkName
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrServiceNetworkName"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The status of the association.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="attrVpcId")
    def attr_vpc_id(self) -> builtins.str:
        '''The ID of the VPC.

        :cloudformationAttribute: VpcId
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrVpcId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="securityGroupIds")
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the security groups.

        Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-securitygroupids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "securityGroupIds"))

    @security_group_ids.setter
    def security_group_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7960201a023956861ca6515cdcd6b3f6bdf67e620a6b98686654abf28247485a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityGroupIds", value)

    @builtins.property
    @jsii.member(jsii_name="serviceNetworkIdentifier")
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network.

        You must use the ARN when the resources specified in the operation are in different accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-servicenetworkidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "serviceNetworkIdentifier"))

    @service_network_identifier.setter
    def service_network_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c1a38a8f56a0695400751ddd41a117113dc0c37a8da47f640d650355a7415757)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "serviceNetworkIdentifier", value)

    @builtins.property
    @jsii.member(jsii_name="vpcIdentifier")
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-vpcidentifier
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "vpcIdentifier"))

    @vpc_identifier.setter
    def vpc_identifier(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ff70883576aaa3e643301d62ae690c73188d51630b5c4e0b1095e021db5c9747)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "vpcIdentifier", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceNetworkVpcAssociationProps",
    jsii_struct_bases=[],
    name_mapping={
        "security_group_ids": "securityGroupIds",
        "service_network_identifier": "serviceNetworkIdentifier",
        "tags": "tags",
        "vpc_identifier": "vpcIdentifier",
    },
)
class CfnServiceNetworkVpcAssociationProps:
    def __init__(
        self,
        *,
        security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        service_network_identifier: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        vpc_identifier: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for defining a ``CfnServiceNetworkVpcAssociation``.

        :param security_group_ids: The IDs of the security groups. Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .
        :param service_network_identifier: The ID or Amazon Resource Name (ARN) of the service network. You must use the ARN when the resources specified in the operation are in different accounts.
        :param tags: The tags for the association.
        :param vpc_identifier: The ID of the VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_service_network_vpc_association_props = vpclattice.CfnServiceNetworkVpcAssociationProps(
                security_group_ids=["securityGroupIds"],
                service_network_identifier="serviceNetworkIdentifier",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                vpc_identifier="vpcIdentifier"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc4fb5504358e07a3ff8163f2c9a538bc66dddf828e2095a7284cb7fd1f9c437)
            check_type(argname="argument security_group_ids", value=security_group_ids, expected_type=type_hints["security_group_ids"])
            check_type(argname="argument service_network_identifier", value=service_network_identifier, expected_type=type_hints["service_network_identifier"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if security_group_ids is not None:
            self._values["security_group_ids"] = security_group_ids
        if service_network_identifier is not None:
            self._values["service_network_identifier"] = service_network_identifier
        if tags is not None:
            self._values["tags"] = tags
        if vpc_identifier is not None:
            self._values["vpc_identifier"] = vpc_identifier

    @builtins.property
    def security_group_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The IDs of the security groups.

        Security groups aren't added by default. You can add a security group to apply network level controls to control which resources in a VPC are allowed to access the service network and its services. For more information, see `Control traffic to resources using security groups <https://docs.aws.amazon.com//vpc/latest/userguide/VPC_SecurityGroups.html>`_ in the *Amazon VPC User Guide* .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-securitygroupids
        '''
        result = self._values.get("security_group_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def service_network_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID or Amazon Resource Name (ARN) of the service network.

        You must use the ARN when the resources specified in the operation are in different accounts.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-servicenetworkidentifier
        '''
        result = self._values.get("service_network_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the association.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def vpc_identifier(self) -> typing.Optional[builtins.str]:
        '''The ID of the VPC.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-servicenetworkvpcassociation.html#cfn-vpclattice-servicenetworkvpcassociation-vpcidentifier
        '''
        result = self._values.get("vpc_identifier")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceNetworkVpcAssociationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnServiceProps",
    jsii_struct_bases=[],
    name_mapping={
        "auth_type": "authType",
        "certificate_arn": "certificateArn",
        "custom_domain_name": "customDomainName",
        "dns_entry": "dnsEntry",
        "name": "name",
        "tags": "tags",
    },
)
class CfnServiceProps:
    def __init__(
        self,
        *,
        auth_type: typing.Optional[builtins.str] = None,
        certificate_arn: typing.Optional[builtins.str] = None,
        custom_domain_name: typing.Optional[builtins.str] = None,
        dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnService``.

        :param auth_type: The type of IAM policy. - ``NONE`` : The resource does not use an IAM policy. This is the default. - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.
        :param certificate_arn: The Amazon Resource Name (ARN) of the certificate.
        :param custom_domain_name: The custom domain name of the service.
        :param dns_entry: ``AWS::VpcLattice::Service.DnsEntry``.
        :param name: The name of the service. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_service_props = vpclattice.CfnServiceProps(
                auth_type="authType",
                certificate_arn="certificateArn",
                custom_domain_name="customDomainName",
                dns_entry=vpclattice.CfnService.DnsEntryProperty(
                    domain_name="domainName",
                    hosted_zone_id="hostedZoneId"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3c70dbf55fe6de1f9f48537226929a933c45ab3eb25cad8e55fcb0c557e9ecae)
            check_type(argname="argument auth_type", value=auth_type, expected_type=type_hints["auth_type"])
            check_type(argname="argument certificate_arn", value=certificate_arn, expected_type=type_hints["certificate_arn"])
            check_type(argname="argument custom_domain_name", value=custom_domain_name, expected_type=type_hints["custom_domain_name"])
            check_type(argname="argument dns_entry", value=dns_entry, expected_type=type_hints["dns_entry"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {}
        if auth_type is not None:
            self._values["auth_type"] = auth_type
        if certificate_arn is not None:
            self._values["certificate_arn"] = certificate_arn
        if custom_domain_name is not None:
            self._values["custom_domain_name"] = custom_domain_name
        if dns_entry is not None:
            self._values["dns_entry"] = dns_entry
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def auth_type(self) -> typing.Optional[builtins.str]:
        '''The type of IAM policy.

        - ``NONE`` : The resource does not use an IAM policy. This is the default.
        - ``AWS_IAM`` : The resource uses an IAM policy. When this type is used, auth is enabled and an auth policy is required.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-authtype
        '''
        result = self._values.get("auth_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def certificate_arn(self) -> typing.Optional[builtins.str]:
        '''The Amazon Resource Name (ARN) of the certificate.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-certificatearn
        '''
        result = self._values.get("certificate_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def custom_domain_name(self) -> typing.Optional[builtins.str]:
        '''The custom domain name of the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-customdomainname
        '''
        result = self._values.get("custom_domain_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def dns_entry(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsEntryProperty]]:
        '''``AWS::VpcLattice::Service.DnsEntry``.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-dnsentry
        '''
        result = self._values.get("dns_entry")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsEntryProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the service.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the service.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-service.html#cfn-vpclattice-service-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnServiceProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnTargetGroup(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroup",
):
    '''A CloudFormation ``AWS::VpcLattice::TargetGroup``.

    Creates a target group. A target group is a collection of targets, or compute resources, that run your application or service. A target group can only be used by a single service.

    For more information, see `Target groups <https://docs.aws.amazon.com/vpc-lattice/latest/ug/target-groups.html>`_ in the *Amazon VPC Lattice User Guide* .

    :cloudformationResource: AWS::VpcLattice::TargetGroup
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_vpclattice as vpclattice
        
        cfn_target_group = vpclattice.CfnTargetGroup(self, "MyCfnTargetGroup",
            type="type",
        
            # the properties below are optional
            config=vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                port=123,
                protocol="protocol",
                vpc_identifier="vpcIdentifier",
        
                # the properties below are optional
                health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    unhealthy_threshold_count=123
                ),
                ip_address_type="ipAddressType",
                protocol_version="protocolVersion"
            ),
            name="name",
            tags=[CfnTag(
                key="key",
                value="value"
            )],
            targets=[vpclattice.CfnTargetGroup.TargetProperty(
                id="id",
        
                # the properties below are optional
                port=123
            )]
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        type: builtins.str,
        config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTargetGroup.TargetGroupConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTargetGroup.TargetProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Create a new ``AWS::VpcLattice::TargetGroup``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param type: The type of target group.
        :param config: The target group configuration. If ``type`` is set to ``LAMBDA`` , this parameter doesn't apply.
        :param name: The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the target group.
        :param targets: Describes a target.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b05185c1a1857eb7b33163874a4d3222265f7f289e5d7e128b19e4baf7ef4e44)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnTargetGroupProps(
            type=type, config=config, name=name, tags=tags, targets=targets
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e3645841eb71b4fe74ce2cdd1d146078da1ca88371990f1ed78c4a55070c4ce9)
            check_type(argname="argument inspector", value=inspector, expected_type=type_hints["inspector"])
        return typing.cast(None, jsii.invoke(self, "inspect", [inspector]))

    @jsii.member(jsii_name="renderProperties")
    def _render_properties(
        self,
        props: typing.Mapping[builtins.str, typing.Any],
    ) -> typing.Mapping[builtins.str, typing.Any]:
        '''
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__94d2c637f3313bded157ddeb05c0c353d7fba980b2f47db20327c198d96ff992)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrArn")
    def attr_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the target group.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrCreatedAt")
    def attr_created_at(self) -> builtins.str:
        '''The date and time that the target group was created, specified in ISO-8601 format.

        :cloudformationAttribute: CreatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrCreatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the target group.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="attrLastUpdatedAt")
    def attr_last_updated_at(self) -> builtins.str:
        '''The date and time that the target group was last updated, specified in ISO-8601 format.

        :cloudformationAttribute: LastUpdatedAt
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrLastUpdatedAt"))

    @builtins.property
    @jsii.member(jsii_name="attrStatus")
    def attr_status(self) -> builtins.str:
        '''The operation's status.

        You can retry the operation if the status is ``CREATE_FAILED`` . However, if you retry it while the status is ``CREATE_IN_PROGRESS`` , there is no change in the status.

        :cloudformationAttribute: Status
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrStatus"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> _aws_cdk_core_f4b25747.TagManager:
        '''The tags for the target group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="type")
    def type(self) -> builtins.str:
        '''The type of target group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-type
        '''
        return typing.cast(builtins.str, jsii.get(self, "type"))

    @type.setter
    def type(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ab2107f6e8cd60cf543bf315c7f69f15d0cbb84852008000287e26ed9d9c6973)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "type", value)

    @builtins.property
    @jsii.member(jsii_name="config")
    def config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetGroupConfigProperty"]]:
        '''The target group configuration.

        If ``type`` is set to ``LAMBDA`` , this parameter doesn't apply.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-config
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetGroupConfigProperty"]], jsii.get(self, "config"))

    @config.setter
    def config(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetGroupConfigProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__50500473367b5a46e24d044121bdf2b98d91d91cce6c36bf199ba4a931915e74)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "config", value)

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the target group.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-name
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "name"))

    @name.setter
    def name(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__950d4d168f1ee83c295e6cfb36be86bf3f917dd79a61002d2ed82fed9f933ed8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetProperty"]]]]:
        '''Describes a target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-targets
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetProperty"]]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.TargetProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c5e865fb93de05ab42d6ee7720d9ee2f7bb7fe336a77ab9d71393120d775bd2c)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroup.HealthCheckConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "enabled": "enabled",
            "health_check_interval_seconds": "healthCheckIntervalSeconds",
            "health_check_timeout_seconds": "healthCheckTimeoutSeconds",
            "healthy_threshold_count": "healthyThresholdCount",
            "matcher": "matcher",
            "path": "path",
            "port": "port",
            "protocol": "protocol",
            "protocol_version": "protocolVersion",
            "unhealthy_threshold_count": "unhealthyThresholdCount",
        },
    )
    class HealthCheckConfigProperty:
        def __init__(
            self,
            *,
            enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
            health_check_interval_seconds: typing.Optional[jsii.Number] = None,
            health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
            healthy_threshold_count: typing.Optional[jsii.Number] = None,
            matcher: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTargetGroup.MatcherProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            path: typing.Optional[builtins.str] = None,
            port: typing.Optional[jsii.Number] = None,
            protocol: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
            unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''The health check configuration of a target group.

            Health check configurations aren't used for ``LAMBDA`` and ``ALB`` target groups.

            :param enabled: Indicates whether health checking is enabled.
            :param health_check_interval_seconds: The approximate amount of time, in seconds, between health checks of an individual target. The range is 5–300 seconds. The default is 30 seconds.
            :param health_check_timeout_seconds: The amount of time, in seconds, to wait before reporting a target as unhealthy. The range is 1–120 seconds. The default is 5 seconds.
            :param healthy_threshold_count: The number of consecutive successful health checks required before considering an unhealthy target healthy. The range is 2–10. The default is 5.
            :param matcher: The codes to use when checking for a successful response from a target. These are called *Success codes* in the console.
            :param path: The destination for health checks on the targets. If the protocol version is ``HTTP/1.1`` or ``HTTP/2`` , specify a valid URI (for example, ``/path?query`` ). The default path is ``/`` . Health checks are not supported if the protocol version is ``gRPC`` , however, you can choose ``HTTP/1.1`` or ``HTTP/2`` and specify a valid URI.
            :param port: The port used when performing health checks on targets. The default setting is the port that a target receives traffic on.
            :param protocol: The protocol used when performing health checks on targets. The possible protocols are ``HTTP`` and ``HTTPS`` . The default is ``HTTP`` .
            :param protocol_version: The protocol version used when performing health checks on targets. The possible protocol versions are ``HTTP1`` and ``HTTP2`` .
            :param unhealthy_threshold_count: The number of consecutive failed health checks required before considering a target unhealthy. The range is 2–10. The default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                health_check_config_property = vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                    enabled=False,
                    health_check_interval_seconds=123,
                    health_check_timeout_seconds=123,
                    healthy_threshold_count=123,
                    matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                        http_code="httpCode"
                    ),
                    path="path",
                    port=123,
                    protocol="protocol",
                    protocol_version="protocolVersion",
                    unhealthy_threshold_count=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__5b5de48c050593c7ad59b536b71ce768f5d3d4f25ca961857c8086b8b5c90174)
                check_type(argname="argument enabled", value=enabled, expected_type=type_hints["enabled"])
                check_type(argname="argument health_check_interval_seconds", value=health_check_interval_seconds, expected_type=type_hints["health_check_interval_seconds"])
                check_type(argname="argument health_check_timeout_seconds", value=health_check_timeout_seconds, expected_type=type_hints["health_check_timeout_seconds"])
                check_type(argname="argument healthy_threshold_count", value=healthy_threshold_count, expected_type=type_hints["healthy_threshold_count"])
                check_type(argname="argument matcher", value=matcher, expected_type=type_hints["matcher"])
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
                check_type(argname="argument unhealthy_threshold_count", value=unhealthy_threshold_count, expected_type=type_hints["unhealthy_threshold_count"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if enabled is not None:
                self._values["enabled"] = enabled
            if health_check_interval_seconds is not None:
                self._values["health_check_interval_seconds"] = health_check_interval_seconds
            if health_check_timeout_seconds is not None:
                self._values["health_check_timeout_seconds"] = health_check_timeout_seconds
            if healthy_threshold_count is not None:
                self._values["healthy_threshold_count"] = healthy_threshold_count
            if matcher is not None:
                self._values["matcher"] = matcher
            if path is not None:
                self._values["path"] = path
            if port is not None:
                self._values["port"] = port
            if protocol is not None:
                self._values["protocol"] = protocol
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version
            if unhealthy_threshold_count is not None:
                self._values["unhealthy_threshold_count"] = unhealthy_threshold_count

        @builtins.property
        def enabled(
            self,
        ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
            '''Indicates whether health checking is enabled.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-enabled
            '''
            result = self._values.get("enabled")
            return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

        @builtins.property
        def health_check_interval_seconds(self) -> typing.Optional[jsii.Number]:
            '''The approximate amount of time, in seconds, between health checks of an individual target.

            The range is 5–300 seconds. The default is 30 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthcheckintervalseconds
            '''
            result = self._values.get("health_check_interval_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def health_check_timeout_seconds(self) -> typing.Optional[jsii.Number]:
            '''The amount of time, in seconds, to wait before reporting a target as unhealthy.

            The range is 1–120 seconds. The default is 5 seconds.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthchecktimeoutseconds
            '''
            result = self._values.get("health_check_timeout_seconds")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def healthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive successful health checks required before considering an unhealthy target healthy.

            The range is 2–10. The default is 5.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-healthythresholdcount
            '''
            result = self._values.get("healthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def matcher(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.MatcherProperty"]]:
            '''The codes to use when checking for a successful response from a target.

            These are called *Success codes* in the console.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-matcher
            '''
            result = self._values.get("matcher")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.MatcherProperty"]], result)

        @builtins.property
        def path(self) -> typing.Optional[builtins.str]:
            '''The destination for health checks on the targets.

            If the protocol version is ``HTTP/1.1`` or ``HTTP/2`` , specify a valid URI (for example, ``/path?query`` ). The default path is ``/`` . Health checks are not supported if the protocol version is ``gRPC`` , however, you can choose ``HTTP/1.1`` or ``HTTP/2`` and specify a valid URI.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-path
            '''
            result = self._values.get("path")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port used when performing health checks on targets.

            The default setting is the port that a target receives traffic on.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        @builtins.property
        def protocol(self) -> typing.Optional[builtins.str]:
            '''The protocol used when performing health checks on targets.

            The possible protocols are ``HTTP`` and ``HTTPS`` . The default is ``HTTP`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-protocol
            '''
            result = self._values.get("protocol")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The protocol version used when performing health checks on targets.

            The possible protocol versions are ``HTTP1`` and ``HTTP2`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def unhealthy_threshold_count(self) -> typing.Optional[jsii.Number]:
            '''The number of consecutive failed health checks required before considering a target unhealthy.

            The range is 2–10. The default is 2.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-healthcheckconfig.html#cfn-vpclattice-targetgroup-healthcheckconfig-unhealthythresholdcount
            '''
            result = self._values.get("unhealthy_threshold_count")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "HealthCheckConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroup.MatcherProperty",
        jsii_struct_bases=[],
        name_mapping={"http_code": "httpCode"},
    )
    class MatcherProperty:
        def __init__(self, *, http_code: builtins.str) -> None:
            '''The codes to use when checking for a successful response from a target for health checks.

            :param http_code: The HTTP code to use when checking for a successful response from a target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                matcher_property = vpclattice.CfnTargetGroup.MatcherProperty(
                    http_code="httpCode"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9369072d5ce2f3037cacf31f36b1c6bc21db04f99b3c9d87edc5c0102ee5a97a)
                check_type(argname="argument http_code", value=http_code, expected_type=type_hints["http_code"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "http_code": http_code,
            }

        @builtins.property
        def http_code(self) -> builtins.str:
            '''The HTTP code to use when checking for a successful response from a target.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-matcher.html#cfn-vpclattice-targetgroup-matcher-httpcode
            '''
            result = self._values.get("http_code")
            assert result is not None, "Required property 'http_code' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "MatcherProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroup.TargetGroupConfigProperty",
        jsii_struct_bases=[],
        name_mapping={
            "port": "port",
            "protocol": "protocol",
            "vpc_identifier": "vpcIdentifier",
            "health_check": "healthCheck",
            "ip_address_type": "ipAddressType",
            "protocol_version": "protocolVersion",
        },
    )
    class TargetGroupConfigProperty:
        def __init__(
            self,
            *,
            port: jsii.Number,
            protocol: builtins.str,
            vpc_identifier: builtins.str,
            health_check: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnTargetGroup.HealthCheckConfigProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            ip_address_type: typing.Optional[builtins.str] = None,
            protocol_version: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Describes the configuration of a target group.

            Lambda functions don't support target group configuration.

            :param port: The port on which the targets are listening. For HTTP, the default is ``80`` . For HTTPS, the default is ``443``
            :param protocol: The protocol to use for routing traffic to the targets. Default is the protocol of a target group.
            :param vpc_identifier: The ID of the VPC.
            :param health_check: The health check configuration.
            :param ip_address_type: The type of IP address used for the target group. The possible values are ``ipv4`` and ``ipv6`` . This is an optional parameter. If not specified, the IP address type defaults to ``ipv4`` .
            :param protocol_version: The protocol version. Default value is ``HTTP1`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                target_group_config_property = vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                    port=123,
                    protocol="protocol",
                    vpc_identifier="vpcIdentifier",
                
                    # the properties below are optional
                    health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        protocol_version="protocolVersion",
                        unhealthy_threshold_count=123
                    ),
                    ip_address_type="ipAddressType",
                    protocol_version="protocolVersion"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__876d589d393e4888a42d0a629a4c97318f3070228350ffe3caac4fc6b9c1a0f2)
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
                check_type(argname="argument protocol", value=protocol, expected_type=type_hints["protocol"])
                check_type(argname="argument vpc_identifier", value=vpc_identifier, expected_type=type_hints["vpc_identifier"])
                check_type(argname="argument health_check", value=health_check, expected_type=type_hints["health_check"])
                check_type(argname="argument ip_address_type", value=ip_address_type, expected_type=type_hints["ip_address_type"])
                check_type(argname="argument protocol_version", value=protocol_version, expected_type=type_hints["protocol_version"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "port": port,
                "protocol": protocol,
                "vpc_identifier": vpc_identifier,
            }
            if health_check is not None:
                self._values["health_check"] = health_check
            if ip_address_type is not None:
                self._values["ip_address_type"] = ip_address_type
            if protocol_version is not None:
                self._values["protocol_version"] = protocol_version

        @builtins.property
        def port(self) -> jsii.Number:
            '''The port on which the targets are listening.

            For HTTP, the default is ``80`` . For HTTPS, the default is ``443``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-port
            '''
            result = self._values.get("port")
            assert result is not None, "Required property 'port' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def protocol(self) -> builtins.str:
            '''The protocol to use for routing traffic to the targets.

            Default is the protocol of a target group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocol
            '''
            result = self._values.get("protocol")
            assert result is not None, "Required property 'protocol' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def vpc_identifier(self) -> builtins.str:
            '''The ID of the VPC.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-vpcidentifier
            '''
            result = self._values.get("vpc_identifier")
            assert result is not None, "Required property 'vpc_identifier' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def health_check(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.HealthCheckConfigProperty"]]:
            '''The health check configuration.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-healthcheck
            '''
            result = self._values.get("health_check")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnTargetGroup.HealthCheckConfigProperty"]], result)

        @builtins.property
        def ip_address_type(self) -> typing.Optional[builtins.str]:
            '''The type of IP address used for the target group.

            The possible values are ``ipv4`` and ``ipv6`` . This is an optional parameter. If not specified, the IP address type defaults to ``ipv4`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-ipaddresstype
            '''
            result = self._values.get("ip_address_type")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def protocol_version(self) -> typing.Optional[builtins.str]:
            '''The protocol version.

            Default value is ``HTTP1`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-targetgroupconfig.html#cfn-vpclattice-targetgroup-targetgroupconfig-protocolversion
            '''
            result = self._values.get("protocol_version")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetGroupConfigProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroup.TargetProperty",
        jsii_struct_bases=[],
        name_mapping={"id": "id", "port": "port"},
    )
    class TargetProperty:
        def __init__(
            self,
            *,
            id: builtins.str,
            port: typing.Optional[jsii.Number] = None,
        ) -> None:
            '''Describes a target.

            :param id: The ID of the target. If the target type of the target group is ``INSTANCE`` , this is an instance ID. If the target type is ``IP`` , this is an IP address. If the target type is ``LAMBDA`` , this is the ARN of the Lambda function. If the target type is ``ALB`` , this is the ARN of the Application Load Balancer.
            :param port: The port on which the target is listening. For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_vpclattice as vpclattice
                
                target_property = vpclattice.CfnTargetGroup.TargetProperty(
                    id="id",
                
                    # the properties below are optional
                    port=123
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__f1e838db63db1835917dbae8ea7d18027378aacf5784ee5abeeebeb6d351caa7)
                check_type(argname="argument id", value=id, expected_type=type_hints["id"])
                check_type(argname="argument port", value=port, expected_type=type_hints["port"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "id": id,
            }
            if port is not None:
                self._values["port"] = port

        @builtins.property
        def id(self) -> builtins.str:
            '''The ID of the target.

            If the target type of the target group is ``INSTANCE`` , this is an instance ID. If the target type is ``IP`` , this is an IP address. If the target type is ``LAMBDA`` , this is the ARN of the Lambda function. If the target type is ``ALB`` , this is the ARN of the Application Load Balancer.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-id
            '''
            result = self._values.get("id")
            assert result is not None, "Required property 'id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def port(self) -> typing.Optional[jsii.Number]:
            '''The port on which the target is listening.

            For HTTP, the default is ``80`` . For HTTPS, the default is ``443`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-vpclattice-targetgroup-target.html#cfn-vpclattice-targetgroup-target-port
            '''
            result = self._values.get("port")
            return typing.cast(typing.Optional[jsii.Number], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "TargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-vpclattice.CfnTargetGroupProps",
    jsii_struct_bases=[],
    name_mapping={
        "type": "type",
        "config": "config",
        "name": "name",
        "tags": "tags",
        "targets": "targets",
    },
)
class CfnTargetGroupProps:
    def __init__(
        self,
        *,
        type: builtins.str,
        config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        name: typing.Optional[builtins.str] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
        targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnTargetGroup``.

        :param type: The type of target group.
        :param config: The target group configuration. If ``type`` is set to ``LAMBDA`` , this parameter doesn't apply.
        :param name: The name of the target group. The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen. If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.
        :param tags: The tags for the target group.
        :param targets: Describes a target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_vpclattice as vpclattice
            
            cfn_target_group_props = vpclattice.CfnTargetGroupProps(
                type="type",
            
                # the properties below are optional
                config=vpclattice.CfnTargetGroup.TargetGroupConfigProperty(
                    port=123,
                    protocol="protocol",
                    vpc_identifier="vpcIdentifier",
            
                    # the properties below are optional
                    health_check=vpclattice.CfnTargetGroup.HealthCheckConfigProperty(
                        enabled=False,
                        health_check_interval_seconds=123,
                        health_check_timeout_seconds=123,
                        healthy_threshold_count=123,
                        matcher=vpclattice.CfnTargetGroup.MatcherProperty(
                            http_code="httpCode"
                        ),
                        path="path",
                        port=123,
                        protocol="protocol",
                        protocol_version="protocolVersion",
                        unhealthy_threshold_count=123
                    ),
                    ip_address_type="ipAddressType",
                    protocol_version="protocolVersion"
                ),
                name="name",
                tags=[CfnTag(
                    key="key",
                    value="value"
                )],
                targets=[vpclattice.CfnTargetGroup.TargetProperty(
                    id="id",
            
                    # the properties below are optional
                    port=123
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6f3efbe3ddaa180317366c4c0eb73307f4b44fbbaf3f66c55538137899b52eea)
            check_type(argname="argument type", value=type, expected_type=type_hints["type"])
            check_type(argname="argument config", value=config, expected_type=type_hints["config"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "type": type,
        }
        if config is not None:
            self._values["config"] = config
        if name is not None:
            self._values["name"] = name
        if tags is not None:
            self._values["tags"] = tags
        if targets is not None:
            self._values["targets"] = targets

    @builtins.property
    def type(self) -> builtins.str:
        '''The type of target group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-type
        '''
        result = self._values.get("type")
        assert result is not None, "Required property 'type' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def config(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetGroupConfigProperty]]:
        '''The target group configuration.

        If ``type`` is set to ``LAMBDA`` , this parameter doesn't apply.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-config
        '''
        result = self._values.get("config")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetGroupConfigProperty]], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the target group.

        The name must be unique within the account. The valid characters are a-z, 0-9, and hyphens (-). You can't use a hyphen as the first or last character, or immediately after another hyphen.

        If you don't specify a name, CloudFormation generates one. However, if you specify a name, and later want to replace the resource, you must specify a new name.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-name
        '''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''The tags for the target group.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetProperty]]]]:
        '''Describes a target.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-vpclattice-targetgroup.html#cfn-vpclattice-targetgroup-targets
        '''
        result = self._values.get("targets")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetProperty]]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnTargetGroupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnAccessLogSubscription",
    "CfnAccessLogSubscriptionProps",
    "CfnAuthPolicy",
    "CfnAuthPolicyProps",
    "CfnListener",
    "CfnListenerProps",
    "CfnResourcePolicy",
    "CfnResourcePolicyProps",
    "CfnRule",
    "CfnRuleProps",
    "CfnService",
    "CfnServiceNetwork",
    "CfnServiceNetworkProps",
    "CfnServiceNetworkServiceAssociation",
    "CfnServiceNetworkServiceAssociationProps",
    "CfnServiceNetworkVpcAssociation",
    "CfnServiceNetworkVpcAssociationProps",
    "CfnServiceProps",
    "CfnTargetGroup",
    "CfnTargetGroupProps",
]

publication.publish()

def _typecheckingstub__820e5beddf8e42bf43fff6a76594a893625daee50727ba238549056bbb8ef8b8(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    destination_arn: builtins.str,
    resource_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__798775518c10513eb0e4aec15f38faca5af7f050010816cf34ad9466870ddadc(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fdd6e394be12ec3be1410128dcbd4cfa81ad2234a0a8151fb579601b6b9f88e0(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8d662aa3158dde46f8905a1b0e44e6a80aeb005bec161af3b447272ad238f754(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4422b3b30eca9b93cce8d457b3664a951be8c32f67ed6d703d76860fe91e3d99(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c833b9cbd47a408654254b9b3a6a98e83dc48cd6ef2a2bef9300a23549738f5d(
    *,
    destination_arn: builtins.str,
    resource_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97934b5b96195967fd5ac0686c4db1587ec155ac0b310f638a7dc22335dd0598(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy: typing.Any,
    resource_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__291be3dc9fd26d96a38bd1521783c31d36466bee645edb11f0c06a449cec4fc0(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2ffb8cc8262523a33d9eb4b5a4348e673b35d311b5175fd275728fd44fb6692c(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1854d1e596ae3e2e0c5089200e45e24a5512c05c13f2cc5e3d0444308afa1745(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f287ff1f62e737127a1ce4a62d2f6abf5e4021eba0aa78568bc16cb039fa01d0(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__04c2bc9f2f126d1bd9265c062de7475bbc03c205b57535facfe6e1ea63446d0a(
    *,
    policy: typing.Any,
    resource_identifier: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__73c2e416141e7ef0222f1f1653a309562bea8e8506b9533bdf17330d43a55e5b(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]]],
    protocol: builtins.str,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__12326ee41041465d2ba4da8b8ad4fde7ebba4ecae33893d007d9ccd35a96e583(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__af0732b404002622f3a0865c1e4c8538905f3b87bc5969b6b8453871072f745d(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__59cf95e2aa67f632d4dab721c41f6508baebb19658e79b89c2e07da445e5f1e1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnListener.DefaultActionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f7c52e549bd6fb6641d37006b522005d505dfe672ab7e545bdd7502ed74c420c(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4fa463ad8da953297419b70e31b57351de2348e405ace086f192861a997245(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__72ca6d7d647098025bbd81d7a18931f2e671a9e08ad86af511a05c973d05aca9(
    value: typing.Optional[jsii.Number],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__8c147db701f108bf950b4c5a2af16e6ef53e8891f637adb3262fe302a15acc12(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0287abc785fecab6ab1087702d4a6cca9b64c71acbd133d0e2bbdc1de81595ff(
    *,
    fixed_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.FixedResponseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.ForwardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__81d112c1d223587396b51fc8f7ea66cf1311467ab28fa8307bc6bf5871bca8fe(
    *,
    status_code: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0edc0eac6cf08dfafca941a895b9235e1388afd91b819a1cb4242c95e6969cec(
    *,
    target_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d4065ce9456c818a8231706c6240cf8ec601eb4a697f680c46cf226eb5bd7e09(
    *,
    target_group_identifier: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9ff2dd627386327f2b9b79c6458e2d44d1394267c935a5eae9ddfe867f634806(
    *,
    default_action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnListener.DefaultActionProperty, typing.Dict[builtins.str, typing.Any]]],
    protocol: builtins.str,
    name: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6ac4e206f522d10e45ed8695c98aa7d4578801cc302793ab783a4fb01f470996(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e263ac65b58fc049d4c19474eb5e6ef4cbfe321c0b44a3622ebbdb7a05fa86c1(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__16cf3f0d7c924801d4224e9bc1a5a3de3f58d2630ee09d51de4ffa940c47bcb4(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d8cd48c4b55dbc12516d3f066876df333b023212852663cce22a4dd67b235628(
    value: typing.Any,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4559a915c278a3327c146870342a0e253462cec97a88340af321abf9513af9bb(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e31bafa278251cc933c6a6803b660f75813c3b162992cff3093896a8cacdcae(
    *,
    policy: typing.Any,
    resource_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__449a68437024cae294f2a7c8eab201a5ef1ea3160260d7ae9d0157d7eccc4cbf(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]]],
    priority: jsii.Number,
    listener_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f930114bcf2b12fea371498e5b19a32f6acd368dc4154e1e097d7321a3925085(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ea7ae3dc0625947bab64ba7e822719c3e517563f3824f5f9ba85e64041b92e4e(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2e32eb6ee9dcb9009c73db8fca2988a7b4aead84cb028572ddd439898ddaa4ca(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.ActionProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d5fe1d8208e0e1751bef2f95e6b8ebf5d940d6cd1f301fde28983b5677280181(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnRule.MatchProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f73272751ae6cbf92bfb950a6ad165cc0d44d9aadfb471b02d23f4f75bde89c7(
    value: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bad509bb92805c4fd1cb398cc3f5f0f8aced007a58fe592e5fd563c4b9d091f4(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__466901c7a357c7de931d773fd28b10eee0befec10228407d6273802148a74586(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__dc44908fa7a0058a0f5b82695f7acdcfcba9bd43fe7ca0287d2a031d475e1894(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a7636f2c1e092c4d185db7dcea003bb5cd7045207402560714659e1d3473f54(
    *,
    fixed_response: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.FixedResponseProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    forward: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ForwardProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fa671287577ce7d7058b29cf609e1c5e01afed04e36883edef5c2245dd755289(
    *,
    status_code: jsii.Number,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b80cd57c837960266ed58cdf4639c584e66a9112623d660bf6fad9a74f04dbaf(
    *,
    target_groups: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.WeightedTargetGroupProperty, typing.Dict[builtins.str, typing.Any]]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f8e23f5a1cc6130bd5632a87a2ce0e1341a017ea4acc46d48787bb148eab30ef(
    *,
    match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.HeaderMatchTypeProperty, typing.Dict[builtins.str, typing.Any]]],
    name: builtins.str,
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d03297d1a6a9c36744af6134cbe142b2afa806b8017b921ebdebbb0e575a4bcd(
    *,
    contains: typing.Optional[builtins.str] = None,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ace69d7b1df81bf1f297efe4b3972c65d727c7dde4a3926fd1d446ff8cf20a8e(
    *,
    header_matches: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.HeaderMatchProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    method: typing.Optional[builtins.str] = None,
    path_match: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PathMatchProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__322643cd06fdf5bd3a2477b093a654dd58ac591eba88be254b56c3790c21b79e(
    *,
    http_match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.HttpMatchProperty, typing.Dict[builtins.str, typing.Any]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__689b2016adad8bf157bdb2290c2bd18a5bf6f18cb41b84efeedd18f85c1cc3c0(
    *,
    match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.PathMatchTypeProperty, typing.Dict[builtins.str, typing.Any]]],
    case_sensitive: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__271814c8dfb45c778ed9f0693250e0448398d761ce2928ea0325c1ad2535383d(
    *,
    exact: typing.Optional[builtins.str] = None,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e36be1c2a6fbc4f36b79ea32dc3b8a682844db6ad04181ad8e6c98172d55f160(
    *,
    target_group_identifier: builtins.str,
    weight: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__42762c23e983fcbf07f7dc222e57f41928eeb28308d39c51c5cad23f5eaadd0b(
    *,
    action: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.ActionProperty, typing.Dict[builtins.str, typing.Any]]],
    match: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnRule.MatchProperty, typing.Dict[builtins.str, typing.Any]]],
    priority: jsii.Number,
    listener_identifier: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__574a9fc7fbfd4823f696563f89b0102cc0f6583c712edcaf1ecb150cbcc76a73(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__363d7113f186d64cb19a002eccc489e303250c3fdacfc7148a68073429b1d3ca(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e18adbacd4ff6c812cb081d4b16288cfe8c9a3e290141e16cd903040253f5279(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__34adbe2b62d87281978a226c9372355bb2d3e807d44d0c2864f2e56ed5b96330(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__97271e8f62efdbac1637a3dbaee6fd46350f99f443897aea1f0c35bdea726880(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__36235e17375fd8756324abec6e1d0541cdc4ffe0e06d8c3a4cfecd1f0394cf76(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__86331259a92160f0cd63dbc4aab784bed2c1d7ed59e79a25ba5003164e44283b(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnService.DnsEntryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e6d952c67f75aa6f1686ce409690bdb1e9b683e8516c4842eed66a7e31358d29(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b65282857e662c4b074767c1cc3d9d545d5d1cd40b51ed7ca75b63c2337997f(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cf9e980e993af8f7fa107ecb42a9f54ba4206aa20d89a5d465c68ac523c26dcb(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    auth_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e97a2294e65c5976c9ca7e8f584b3ecf913f35c7fe4abe9771df269960960bb5(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9a40dc59d6df6fac2bdb2d133d19bf20fae8a7d14bedf0e4f6cad8f5511c9c3f(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c06098786978ca47bd316c848db6890bab981efa66b884ed7bd992f91d933a10(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0c1243a59c334b22e93d8c8e21aa09a8bca564fda7479f2c980b9a64a791f2b5(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d90fcb9ad7227e77958171d1511828ad181196daf3cc4389f6a52b57ca1a3500(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__725216d9e151e558fef4ee185a2250a5071d6159c22db7b512e98514c6f09e3f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e5217fecc0205495947f33aae71e31b7d764477fac93ce91d651bad8b1c5983(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__74c342d7bd4a5c4d3d62426cf092bcfcd27641ede95b333b5f04efe443ed7203(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__75407ce59d1c225c82424a53c51a9dc98fd99a8760c2356feed36faf3b7f2ef3(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnServiceNetworkServiceAssociation.DnsEntryProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cc145dd6109e6aabc8144c9e009f031414aef280d1dba52b642a580208dcb0d(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a8dc5f20ba5a3082774195b7fce34bc7111b2f6199a0d9e5f0e03d252d4a0172(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bc0e9982b4fa1e75bd51f775a1c566a55f792f725e1ddf2b90edc3edeae2edf9(
    *,
    domain_name: typing.Optional[builtins.str] = None,
    hosted_zone_id: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cbd27ac9bacaa2bb68de68c8b7e1590df098073a6694f4adbe8e3b2c234c901c(
    *,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnServiceNetworkServiceAssociation.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    service_identifier: typing.Optional[builtins.str] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b013dda832236717519889ff6a2a2a5417720106cf5a7739a5881fa4abf83ec(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed4e55a3f0b029c5560c7497739808da68a12f1cd2548f324656c556b8d7d02c(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cd4c9386c4eb083c995c2a77d6d57793179b2895e73119f7ed567a5423d0256(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7960201a023956861ca6515cdcd6b3f6bdf67e620a6b98686654abf28247485a(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c1a38a8f56a0695400751ddd41a117113dc0c37a8da47f640d650355a7415757(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ff70883576aaa3e643301d62ae690c73188d51630b5c4e0b1095e021db5c9747(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc4fb5504358e07a3ff8163f2c9a538bc66dddf828e2095a7284cb7fd1f9c437(
    *,
    security_group_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    service_network_identifier: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    vpc_identifier: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3c70dbf55fe6de1f9f48537226929a933c45ab3eb25cad8e55fcb0c557e9ecae(
    *,
    auth_type: typing.Optional[builtins.str] = None,
    certificate_arn: typing.Optional[builtins.str] = None,
    custom_domain_name: typing.Optional[builtins.str] = None,
    dns_entry: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnService.DnsEntryProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b05185c1a1857eb7b33163874a4d3222265f7f289e5d7e128b19e4baf7ef4e44(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    type: builtins.str,
    config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e3645841eb71b4fe74ce2cdd1d146078da1ca88371990f1ed78c4a55070c4ce9(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94d2c637f3313bded157ddeb05c0c353d7fba980b2f47db20327c198d96ff992(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ab2107f6e8cd60cf543bf315c7f69f15d0cbb84852008000287e26ed9d9c6973(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__50500473367b5a46e24d044121bdf2b98d91d91cce6c36bf199ba4a931915e74(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetGroupConfigProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__950d4d168f1ee83c295e6cfb36be86bf3f917dd79a61002d2ed82fed9f933ed8(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c5e865fb93de05ab42d6ee7720d9ee2f7bb7fe336a77ab9d71393120d775bd2c(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnTargetGroup.TargetProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__5b5de48c050593c7ad59b536b71ce768f5d3d4f25ca961857c8086b8b5c90174(
    *,
    enabled: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    health_check_interval_seconds: typing.Optional[jsii.Number] = None,
    health_check_timeout_seconds: typing.Optional[jsii.Number] = None,
    healthy_threshold_count: typing.Optional[jsii.Number] = None,
    matcher: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.MatcherProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    path: typing.Optional[builtins.str] = None,
    port: typing.Optional[jsii.Number] = None,
    protocol: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
    unhealthy_threshold_count: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9369072d5ce2f3037cacf31f36b1c6bc21db04f99b3c9d87edc5c0102ee5a97a(
    *,
    http_code: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__876d589d393e4888a42d0a629a4c97318f3070228350ffe3caac4fc6b9c1a0f2(
    *,
    port: jsii.Number,
    protocol: builtins.str,
    vpc_identifier: builtins.str,
    health_check: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.HealthCheckConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ip_address_type: typing.Optional[builtins.str] = None,
    protocol_version: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__f1e838db63db1835917dbae8ea7d18027378aacf5784ee5abeeebeb6d351caa7(
    *,
    id: builtins.str,
    port: typing.Optional[jsii.Number] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6f3efbe3ddaa180317366c4c0eb73307f4b44fbbaf3f66c55538137899b52eea(
    *,
    type: builtins.str,
    config: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetGroupConfigProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    name: typing.Optional[builtins.str] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnTargetGroup.TargetProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
