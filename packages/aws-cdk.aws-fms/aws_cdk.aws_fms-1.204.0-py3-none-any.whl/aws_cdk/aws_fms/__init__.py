'''
# AWS::FMS Construct Library

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
import aws_cdk.aws_fms as fms
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for FMS construct libraries](https://constructs.dev/search?q=fms)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::FMS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FMS.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::FMS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FMS.html).

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
class CfnNotificationChannel(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-fms.CfnNotificationChannel",
):
    '''A CloudFormation ``AWS::FMS::NotificationChannel``.

    Designates the IAM role and Amazon Simple Notification Service (SNS) topic to use to record SNS logs.

    To perform this action outside of the console, you must configure the SNS topic to allow the role ``AWSServiceRoleForFMS`` to publish SNS logs. For more information, see `Firewall Manager required permissions for API actions <https://docs.aws.amazon.com/waf/latest/developerguide/fms-api-permissions-ref.html>`_ in the *AWS Firewall Manager Developer Guide* .

    :cloudformationResource: AWS::FMS::NotificationChannel
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_fms as fms
        
        cfn_notification_channel = fms.CfnNotificationChannel(self, "MyCfnNotificationChannel",
            sns_role_name="snsRoleName",
            sns_topic_arn="snsTopicArn"
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        sns_role_name: builtins.str,
        sns_topic_arn: builtins.str,
    ) -> None:
        '''Create a new ``AWS::FMS::NotificationChannel``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param sns_role_name: The Amazon Resource Name (ARN) of the IAM role that allows Amazon SNS to record AWS Firewall Manager activity.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__8ff279983102395e835cba03517123ba997c5ee38d76f486bb968b17a50dcb54)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnNotificationChannelProps(
            sns_role_name=sns_role_name, sns_topic_arn=sns_topic_arn
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6cab35781d8442e68a1bfb6e56a1a0dcae49a50a179c13c7ecf92da02d760a11)
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
            type_hints = typing.get_type_hints(_typecheckingstub__279da44e5ec9ea0507100ac289410ff4cc504ca18237d85d8954c9a78433ad47)
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
    @jsii.member(jsii_name="snsRoleName")
    def sns_role_name(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role that allows Amazon SNS to record AWS Firewall Manager activity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snsrolename
        '''
        return typing.cast(builtins.str, jsii.get(self, "snsRoleName"))

    @sns_role_name.setter
    def sns_role_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b2fdf7bedb2b022e68ea1bcead602b02a5155c988c2910c2bd33b606350fc4b3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsRoleName", value)

    @builtins.property
    @jsii.member(jsii_name="snsTopicArn")
    def sns_topic_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snstopicarn
        '''
        return typing.cast(builtins.str, jsii.get(self, "snsTopicArn"))

    @sns_topic_arn.setter
    def sns_topic_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c37dbc28c9d0a54dde80d153aaf0a63a9929a7db01cbc8c8286a10317adff181)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "snsTopicArn", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-fms.CfnNotificationChannelProps",
    jsii_struct_bases=[],
    name_mapping={"sns_role_name": "snsRoleName", "sns_topic_arn": "snsTopicArn"},
)
class CfnNotificationChannelProps:
    def __init__(
        self,
        *,
        sns_role_name: builtins.str,
        sns_topic_arn: builtins.str,
    ) -> None:
        '''Properties for defining a ``CfnNotificationChannel``.

        :param sns_role_name: The Amazon Resource Name (ARN) of the IAM role that allows Amazon SNS to record AWS Firewall Manager activity.
        :param sns_topic_arn: The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_fms as fms
            
            cfn_notification_channel_props = fms.CfnNotificationChannelProps(
                sns_role_name="snsRoleName",
                sns_topic_arn="snsTopicArn"
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1c88d258327730c7503c9c7ef8312754e0a23f227da6b17d0c65f291a7203095)
            check_type(argname="argument sns_role_name", value=sns_role_name, expected_type=type_hints["sns_role_name"])
            check_type(argname="argument sns_topic_arn", value=sns_topic_arn, expected_type=type_hints["sns_topic_arn"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "sns_role_name": sns_role_name,
            "sns_topic_arn": sns_topic_arn,
        }

    @builtins.property
    def sns_role_name(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the IAM role that allows Amazon SNS to record AWS Firewall Manager activity.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snsrolename
        '''
        result = self._values.get("sns_role_name")
        assert result is not None, "Required property 'sns_role_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def sns_topic_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of the SNS topic that collects notifications from AWS Firewall Manager .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-notificationchannel.html#cfn-fms-notificationchannel-snstopicarn
        '''
        result = self._values.get("sns_topic_arn")
        assert result is not None, "Required property 'sns_topic_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnNotificationChannelProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnPolicy(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-fms.CfnPolicy",
):
    '''A CloudFormation ``AWS::FMS::Policy``.

    An AWS Firewall Manager policy.

    Firewall Manager provides the following types of policies:

    - An AWS Shield Advanced policy, which applies Shield Advanced protection to specified accounts and resources.
    - An AWS WAF policy (type WAFV2), which defines rule groups to run first in the corresponding AWS WAF web ACL and rule groups to run last in the web ACL.
    - An AWS WAF Classic policy, which defines a rule group. AWS WAF Classic doesn't support rule groups in Amazon CloudFront , so, to create AWS WAF Classic policies through CloudFront , you first need to create your rule groups outside of CloudFront .
    - A security group policy, which manages VPC security groups across your AWS organization.
    - An AWS Network Firewall policy, which provides firewall rules to filter network traffic in specified Amazon VPCs.
    - A DNS Firewall policy, which provides Amazon Route 53 Resolver DNS Firewall rules to filter DNS queries for specified Amazon VPCs.
    - A third-party firewall policy, which manages a third-party firewall service such as the Palo Alto Networks Cloud Next-Generation Firewall.

    Each policy is specific to one of the types. If you want to enforce more than one policy type across accounts, create multiple policies. You can create multiple policies for each type.

    These policies require some setup to use. For more information, see the sections on prerequisites and getting started under `AWS Firewall Manager <https://docs.aws.amazon.com/waf/latest/developerguide/fms-prereq.html>`_ .

    :cloudformationResource: AWS::FMS::Policy
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_fms as fms
        
        cfn_policy = fms.CfnPolicy(self, "MyCfnPolicy",
            exclude_resource_tags=False,
            policy_name="policyName",
            remediation_enabled=False,
            security_service_policy_data=fms.CfnPolicy.SecurityServicePolicyDataProperty(
                type="type",
        
                # the properties below are optional
                managed_service_data="managedServiceData",
                policy_option=fms.CfnPolicy.PolicyOptionProperty(
                    network_firewall_policy=fms.CfnPolicy.NetworkFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    ),
                    third_party_firewall_policy=fms.CfnPolicy.ThirdPartyFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    )
                )
            ),
        
            # the properties below are optional
            delete_all_policy_resources=False,
            exclude_map={
                "account": ["account"],
                "orgunit": ["orgunit"]
            },
            include_map={
                "account": ["account"],
                "orgunit": ["orgunit"]
            },
            policy_description="policyDescription",
            resources_clean_up=False,
            resource_set_ids=["resourceSetIds"],
            resource_tags=[fms.CfnPolicy.ResourceTagProperty(
                key="key",
        
                # the properties below are optional
                value="value"
            )],
            resource_type="resourceType",
            resource_type_list=["resourceTypeList"],
            tags=[fms.CfnPolicy.PolicyTagProperty(
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
        exclude_resource_tags: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        policy_name: builtins.str,
        remediation_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        security_service_policy_data: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.SecurityServicePolicyDataProperty", typing.Dict[builtins.str, typing.Any]]],
        delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        exclude_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.IEMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        include_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.IEMapProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.ResourceTagProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union["CfnPolicy.PolicyTagProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FMS::Policy``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param exclude_resource_tags: Used only when tags are specified in the ``ResourceTags`` property. If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.
        :param policy_name: The name of the AWS Firewall Manager policy.
        :param remediation_enabled: Indicates if the policy should be automatically applied to new resources.
        :param security_service_policy_data: Details about the security service that is being used to protect the resources. This contains the following settings: - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support . Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF`` - ManagedServiceData - Details about the service that are specific to the service type, in JSON format. - Example: ``DNS_FIREWALL`` ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`` .. epigraph:: Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000. - Example: ``NETWORK_FIREWALL`` - Centralized deployment model ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`` For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`` The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` . For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string. - Example: ``WAFV2`` ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` . - Example: ``AWS WAF Classic`` ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`` - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group. - Example: ``SECURITY_GROUPS_COMMON`` ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: ``SECURITY_GROUPS_CONTENT_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`` The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group. - Example: ``SECURITY_GROUPS_USAGE_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``
        :param delete_all_policy_resources: Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type. For AWS WAF and Shield Advanced policies, Firewall Manager does the following: - Deletes rule groups created by Firewall Manager - Removes web ACLs from in-scope resources - Deletes web ACLs that contain no rules or rule groups For security group policies, Firewall Manager does the following for each security group in the policy: - Disassociates the security group from in-scope resources - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.
        :param exclude_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param include_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param policy_description: The definition of the AWS Network Firewall firewall policy.
        :param resources_clean_up: Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope. For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope. By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources. This option is not available for Shield Advanced or AWS WAF Classic policies.
        :param resource_set_ids: The unique identifiers of the resource sets used by the policy.
        :param resource_tags: An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them. If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .
        :param resource_type: The type of resource protected by or in scope of the policy. This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` . For AWS WAF and Shield Advanced, example resource types include ``AWS::ElasticLoadBalancingV2::LoadBalancer`` and ``AWS::CloudFront::Distribution`` . For a security group common policy, valid values are ``AWS::EC2::NetworkInterface`` and ``AWS::EC2::Instance`` . For a security group content audit policy, valid values are ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` . For a security group usage audit policy, the value is ``AWS::EC2::SecurityGroup`` . For an AWS Network Firewall policy or DNS Firewall policy, the value is ``AWS::EC2::VPC`` .
        :param resource_type_list: An array of ``ResourceType`` objects. Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .
        :param tags: A collection of key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__bae85f07e9a4b7948a93b7caa49d396c532c225934f54619b539a0666b4a5c16)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnPolicyProps(
            exclude_resource_tags=exclude_resource_tags,
            policy_name=policy_name,
            remediation_enabled=remediation_enabled,
            security_service_policy_data=security_service_policy_data,
            delete_all_policy_resources=delete_all_policy_resources,
            exclude_map=exclude_map,
            include_map=include_map,
            policy_description=policy_description,
            resources_clean_up=resources_clean_up,
            resource_set_ids=resource_set_ids,
            resource_tags=resource_tags,
            resource_type=resource_type,
            resource_type_list=resource_type_list,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0a10dc4e67f6dd2662ab529a5772075ea92d1ca7857540f785cefb984c333851)
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
            type_hints = typing.get_type_hints(_typecheckingstub__d94ae7eb859ca5608a74c9d191dcd27283c0b5aab434b1b8ab273d2de2dbd98b)
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
        '''The Amazon Resource Name (ARN) of the policy.

        :cloudformationAttribute: Arn
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrArn"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the policy.

        :cloudformationAttribute: Id
        '''
        return typing.cast(builtins.str, jsii.get(self, "attrId"))

    @builtins.property
    @jsii.member(jsii_name="cfnProperties")
    def _cfn_properties(self) -> typing.Mapping[builtins.str, typing.Any]:
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.get(self, "cfnProperties"))

    @builtins.property
    @jsii.member(jsii_name="excludeResourceTags")
    def exclude_resource_tags(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Used only when tags are specified in the ``ResourceTags`` property.

        If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excluderesourcetags
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "excludeResourceTags"))

    @exclude_resource_tags.setter
    def exclude_resource_tags(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__7e5e6dab7e64bdb8fa671cad14e84a407f2a3c5e184c8ad1f740cf363e8803e0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeResourceTags", value)

    @builtins.property
    @jsii.member(jsii_name="policyName")
    def policy_name(self) -> builtins.str:
        '''The name of the AWS Firewall Manager policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policyname
        '''
        return typing.cast(builtins.str, jsii.get(self, "policyName"))

    @policy_name.setter
    def policy_name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a20a3630b091dfe277770cb194ee3d5356b3c489618e470fa8640e2c987e80bd)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyName", value)

    @builtins.property
    @jsii.member(jsii_name="remediationEnabled")
    def remediation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Indicates if the policy should be automatically applied to new resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-remediationenabled
        '''
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], jsii.get(self, "remediationEnabled"))

    @remediation_enabled.setter
    def remediation_enabled(
        self,
        value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e7df22df367cd9b9515152a2c09c4345288c2fe269596197a865e4ab915834e3)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "remediationEnabled", value)

    @builtins.property
    @jsii.member(jsii_name="securityServicePolicyData")
    def security_service_policy_data(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.SecurityServicePolicyDataProperty"]:
        '''Details about the security service that is being used to protect the resources.

        This contains the following settings:

        - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support .

        Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF``

        - ManagedServiceData - Details about the service that are specific to the service type, in JSON format.
        - Example: ``DNS_FIREWALL``

        ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"``
        .. epigraph::

           Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000.

        - Example: ``NETWORK_FIREWALL`` - Centralized deployment model

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters.

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

        ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

        ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions

        ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"``

        For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"``

        The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` .

        For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string.

        - Example: ``WAFV2``

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` .

        - Example: ``AWS WAF Classic``

        ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"``

        - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group.

        - Example: ``SECURITY_GROUPS_COMMON``

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: ``SECURITY_GROUPS_CONTENT_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"``

        The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.

        - Example: ``SECURITY_GROUPS_USAGE_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-securityservicepolicydata
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.SecurityServicePolicyDataProperty"], jsii.get(self, "securityServicePolicyData"))

    @security_service_policy_data.setter
    def security_service_policy_data(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.SecurityServicePolicyDataProperty"],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__081c25303bec09d80d22f276114cd2bf76703ce6cef273579ce49bda48e5ece1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "securityServicePolicyData", value)

    @builtins.property
    @jsii.member(jsii_name="deleteAllPolicyResources")
    def delete_all_policy_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type.

        For AWS WAF and Shield Advanced policies, Firewall Manager does the following:

        - Deletes rule groups created by Firewall Manager
        - Removes web ACLs from in-scope resources
        - Deletes web ACLs that contain no rules or rule groups

        For security group policies, Firewall Manager does the following for each security group in the policy:

        - Disassociates the security group from in-scope resources
        - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy

        After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-deleteallpolicyresources
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "deleteAllPolicyResources"))

    @delete_all_policy_resources.setter
    def delete_all_policy_resources(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2517807ae96bd94a3aa78c828632e3dedde0e2b5c94a8cb823e481706d5f2e6d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "deleteAllPolicyResources", value)

    @builtins.property
    @jsii.member(jsii_name="excludeMap")
    def exclude_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excludemap
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]], jsii.get(self, "excludeMap"))

    @exclude_map.setter
    def exclude_map(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__9fc1c4f1b99bc22ff8c1eb6c95e268d068bbc754bd13055d3fdf50c2610d34c5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "excludeMap", value)

    @builtins.property
    @jsii.member(jsii_name="includeMap")
    def include_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-includemap
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]], jsii.get(self, "includeMap"))

    @include_map.setter
    def include_map(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.IEMapProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1d466d06e98a9b6717d8cdd2357214de30a366fe4c7b61e9e51ebd965522a3e5)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "includeMap", value)

    @builtins.property
    @jsii.member(jsii_name="policyDescription")
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''The definition of the AWS Network Firewall firewall policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policydescription
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "policyDescription"))

    @policy_description.setter
    def policy_description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1da04897bded9380ad48a049819b07d39659630b1960daf6018ee06172cae8ad)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "policyDescription", value)

    @builtins.property
    @jsii.member(jsii_name="resourcesCleanUp")
    def resources_clean_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope.

        For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope.

        By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources.

        This option is not available for Shield Advanced or AWS WAF Classic policies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcescleanup
        '''
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], jsii.get(self, "resourcesCleanUp"))

    @resources_clean_up.setter
    def resources_clean_up(
        self,
        value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c0e7f501b22ba5eaedd91d7a51b637ca6bcf36937b4952fd675a2fab2813c555)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourcesCleanUp", value)

    @builtins.property
    @jsii.member(jsii_name="resourceSetIds")
    def resource_set_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the resource sets used by the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcesetids
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceSetIds"))

    @resource_set_ids.setter
    def resource_set_ids(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__01b479f26aac79366c2811883c20f0ffc367a9a86afbf4e0d7742fe204a467e8)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceSetIds", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTags")
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.ResourceTagProperty"]]]]:
        '''An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them.

        If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetags
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.ResourceTagProperty"]]]], jsii.get(self, "resourceTags"))

    @resource_tags.setter
    def resource_tags(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.ResourceTagProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4583ee7124b934671566e72e43dcefed38b13be1c0d2a210feed5965cd8b97f0)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTags", value)

    @builtins.property
    @jsii.member(jsii_name="resourceType")
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource protected by or in scope of the policy.

        This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` .

        For AWS WAF and Shield Advanced, example resource types include ``AWS::ElasticLoadBalancingV2::LoadBalancer`` and ``AWS::CloudFront::Distribution`` . For a security group common policy, valid values are ``AWS::EC2::NetworkInterface`` and ``AWS::EC2::Instance`` . For a security group content audit policy, valid values are ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` . For a security group usage audit policy, the value is ``AWS::EC2::SecurityGroup`` . For an AWS Network Firewall policy or DNS Firewall policy, the value is ``AWS::EC2::VPC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetype
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "resourceType"))

    @resource_type.setter
    def resource_type(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__400e27ce21d50d9f853e2c4194c792690e1dcf4cc4e02b104053a0ecce4cda03)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceType", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTypeList")
    def resource_type_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of ``ResourceType`` objects.

        Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetypelist
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resourceTypeList"))

    @resource_type_list.setter
    def resource_type_list(
        self,
        value: typing.Optional[typing.List[builtins.str]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c99e5e58285d9a8279a5b206a15b067a11a6a97244b7ecfa4104c2b55d99dad7)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypeList", value)

    @builtins.property
    @jsii.member(jsii_name="tags")
    def tags(self) -> typing.Optional[typing.List["CfnPolicy.PolicyTagProperty"]]:
        '''A collection of key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-tags
        '''
        return typing.cast(typing.Optional[typing.List["CfnPolicy.PolicyTagProperty"]], jsii.get(self, "tags"))

    @tags.setter
    def tags(
        self,
        value: typing.Optional[typing.List["CfnPolicy.PolicyTagProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__ed3eabd5c6dfb8831e82da1b9504c6c3f2e455d7f22d160f153f2571aba4cd6a)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "tags", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.IEMapProperty",
        jsii_struct_bases=[],
        name_mapping={"account": "account", "orgunit": "orgunit"},
    )
    class IEMapProperty:
        def __init__(
            self,
            *,
            account: typing.Optional[typing.Sequence[builtins.str]] = None,
            orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
        ) -> None:
            '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in or exclude from the policy.

            Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

            This is used for the policy's ``IncludeMap`` and ``ExcludeMap`` .

            You can specify account IDs, OUs, or a combination:

            - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
            - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
            - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

            :param account: The account list for the map.
            :param orgunit: The organizational unit list for the map.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                i_eMap_property = {
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                }
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__b1dd94f8fd7703fc32e4bdf18d28da1d7b36828b914575eef99c5b107a6d6cd0)
                check_type(argname="argument account", value=account, expected_type=type_hints["account"])
                check_type(argname="argument orgunit", value=orgunit, expected_type=type_hints["orgunit"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if account is not None:
                self._values["account"] = account
            if orgunit is not None:
                self._values["orgunit"] = orgunit

        @builtins.property
        def account(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The account list for the map.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html#cfn-fms-policy-iemap-account
            '''
            result = self._values.get("account")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def orgunit(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The organizational unit list for the map.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-iemap.html#cfn-fms-policy-iemap-orgunit
            '''
            result = self._values.get("orgunit")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "IEMapProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.NetworkFirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"firewall_deployment_model": "firewallDeploymentModel"},
    )
    class NetworkFirewallPolicyProperty:
        def __init__(self, *, firewall_deployment_model: builtins.str) -> None:
            '''Configures the firewall policy deployment model of AWS Network Firewall .

            For information about Network Firewall deployment models, see `AWS Network Firewall example architectures with routing <https://docs.aws.amazon.com/network-firewall/latest/developerguide/architectures.html>`_ in the *Network Firewall Developer Guide* .

            :param firewall_deployment_model: Defines the deployment model to use for the firewall policy. To use a distributed model, set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                network_firewall_policy_property = fms.CfnPolicy.NetworkFirewallPolicyProperty(
                    firewall_deployment_model="firewallDeploymentModel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__7160b82f49774a878f27b229efe46344a93215739d4ea16240ecb1185e710700)
                check_type(argname="argument firewall_deployment_model", value=firewall_deployment_model, expected_type=type_hints["firewall_deployment_model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "firewall_deployment_model": firewall_deployment_model,
            }

        @builtins.property
        def firewall_deployment_model(self) -> builtins.str:
            '''Defines the deployment model to use for the firewall policy.

            To use a distributed model, set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html#cfn-fms-policy-networkfirewallpolicy-firewalldeploymentmodel
            '''
            result = self._values.get("firewall_deployment_model")
            assert result is not None, "Required property 'firewall_deployment_model' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "NetworkFirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.PolicyOptionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "network_firewall_policy": "networkFirewallPolicy",
            "third_party_firewall_policy": "thirdPartyFirewallPolicy",
        },
    )
    class PolicyOptionProperty:
        def __init__(
            self,
            *,
            network_firewall_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.NetworkFirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
            third_party_firewall_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.ThirdPartyFirewallPolicyProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Contains the AWS Network Firewall firewall policy options to configure the policy's deployment model and third-party firewall policy settings.

            :param network_firewall_policy: Defines the deployment model to use for the firewall policy.
            :param third_party_firewall_policy: Defines the policy options for a third-party firewall policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                policy_option_property = fms.CfnPolicy.PolicyOptionProperty(
                    network_firewall_policy=fms.CfnPolicy.NetworkFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    ),
                    third_party_firewall_policy=fms.CfnPolicy.ThirdPartyFirewallPolicyProperty(
                        firewall_deployment_model="firewallDeploymentModel"
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__0bf21d6d7b5ee9960672f85bcfe5ee73dcda26e58358749eb304bc52c045b884)
                check_type(argname="argument network_firewall_policy", value=network_firewall_policy, expected_type=type_hints["network_firewall_policy"])
                check_type(argname="argument third_party_firewall_policy", value=third_party_firewall_policy, expected_type=type_hints["third_party_firewall_policy"])
            self._values: typing.Dict[builtins.str, typing.Any] = {}
            if network_firewall_policy is not None:
                self._values["network_firewall_policy"] = network_firewall_policy
            if third_party_firewall_policy is not None:
                self._values["third_party_firewall_policy"] = third_party_firewall_policy

        @builtins.property
        def network_firewall_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.NetworkFirewallPolicyProperty"]]:
            '''Defines the deployment model to use for the firewall policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html#cfn-fms-policy-policyoption-networkfirewallpolicy
            '''
            result = self._values.get("network_firewall_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.NetworkFirewallPolicyProperty"]], result)

        @builtins.property
        def third_party_firewall_policy(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.ThirdPartyFirewallPolicyProperty"]]:
            '''Defines the policy options for a third-party firewall policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policyoption.html#cfn-fms-policy-policyoption-thirdpartyfirewallpolicy
            '''
            result = self._values.get("third_party_firewall_policy")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.ThirdPartyFirewallPolicyProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyOptionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.PolicyTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class PolicyTagProperty:
        def __init__(self, *, key: builtins.str, value: builtins.str) -> None:
            '''A collection of key:value pairs associated with an AWS resource.

            The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

            :param key: Part of the key:value pair that defines a tag. You can use a tag key to describe a category of information, such as "customer." Tag keys are case-sensitive.
            :param value: Part of the key:value pair that defines a tag. You can use a tag value to describe a specific value within a category, such as "companyA" or "companyB." Tag values are case-sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                policy_tag_property = fms.CfnPolicy.PolicyTagProperty(
                    key="key",
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__eba627097921973ca66d96916c81bb9a8135aefccaaad0ec264b1565678aa7fb)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
                "value": value,
            }

        @builtins.property
        def key(self) -> builtins.str:
            '''Part of the key:value pair that defines a tag.

            You can use a tag key to describe a category of information, such as "customer." Tag keys are case-sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html#cfn-fms-policy-policytag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> builtins.str:
            '''Part of the key:value pair that defines a tag.

            You can use a tag value to describe a specific value within a category, such as "companyA" or "companyB." Tag values are case-sensitive.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-policytag.html#cfn-fms-policy-policytag-value
            '''
            result = self._values.get("value")
            assert result is not None, "Required property 'value' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "PolicyTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.ResourceTagProperty",
        jsii_struct_bases=[],
        name_mapping={"key": "key", "value": "value"},
    )
    class ResourceTagProperty:
        def __init__(
            self,
            *,
            key: builtins.str,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''The resource tags that AWS Firewall Manager uses to determine if a particular resource should be included or excluded from the AWS Firewall Manager policy.

            Tags enable you to categorize your AWS resources in different ways, for example, by purpose, owner, or environment. Each tag consists of a key and an optional value. Firewall Manager combines the tags with "AND" so that, if you add more than one tag to a policy scope, a resource must have all the specified tags to be included or excluded. For more information, see `Working with Tag Editor <https://docs.aws.amazon.com/awsconsolehelpdocs/latest/gsg/tag-editor.html>`_ .

            :param key: The resource tag key.
            :param value: The resource tag value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                resource_tag_property = fms.CfnPolicy.ResourceTagProperty(
                    key="key",
                
                    # the properties below are optional
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__4a8a32db23e25f263c7ad590f9fc8b07688b5a79d659d256b4affef87613a0d9)
                check_type(argname="argument key", value=key, expected_type=type_hints["key"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "key": key,
            }
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def key(self) -> builtins.str:
            '''The resource tag key.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html#cfn-fms-policy-resourcetag-key
            '''
            result = self._values.get("key")
            assert result is not None, "Required property 'key' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The resource tag value.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-resourcetag.html#cfn-fms-policy-resourcetag-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ResourceTagProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.SecurityServicePolicyDataProperty",
        jsii_struct_bases=[],
        name_mapping={
            "type": "type",
            "managed_service_data": "managedServiceData",
            "policy_option": "policyOption",
        },
    )
    class SecurityServicePolicyDataProperty:
        def __init__(
            self,
            *,
            type: builtins.str,
            managed_service_data: typing.Optional[builtins.str] = None,
            policy_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnPolicy.PolicyOptionProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
        ) -> None:
            '''Details about the security service that is being used to protect the resources.

            :param type: The service that the policy is using to protect the resources. This specifies the type of policy that is created, either an AWS WAF policy, a Shield Advanced policy, or a security group policy. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support .
            :param managed_service_data: Details about the service that are specific to the service type, in JSON format. - Example: ``DNS_FIREWALL`` ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`` .. epigraph:: Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000. - Example: ``NETWORK_FIREWALL`` - Centralized deployment model ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`` For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`` The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` . For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string. - Example: ``WAFV2`` ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` . - Example: ``AWS WAF Classic`` ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`` - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group. - Example: ``SECURITY_GROUPS_COMMON`` ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: ``SECURITY_GROUPS_CONTENT_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`` The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group. - Example: ``SECURITY_GROUPS_USAGE_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``
            :param policy_option: Contains the Network Firewall firewall policy options to configure a centralized deployment model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                security_service_policy_data_property = fms.CfnPolicy.SecurityServicePolicyDataProperty(
                    type="type",
                
                    # the properties below are optional
                    managed_service_data="managedServiceData",
                    policy_option=fms.CfnPolicy.PolicyOptionProperty(
                        network_firewall_policy=fms.CfnPolicy.NetworkFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        ),
                        third_party_firewall_policy=fms.CfnPolicy.ThirdPartyFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        )
                    )
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__328e691ffdb3c5debafa1be5a8b8d262600ebcb9536eb8a22cc4531a46eb06e1)
                check_type(argname="argument type", value=type, expected_type=type_hints["type"])
                check_type(argname="argument managed_service_data", value=managed_service_data, expected_type=type_hints["managed_service_data"])
                check_type(argname="argument policy_option", value=policy_option, expected_type=type_hints["policy_option"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "type": type,
            }
            if managed_service_data is not None:
                self._values["managed_service_data"] = managed_service_data
            if policy_option is not None:
                self._values["policy_option"] = policy_option

        @builtins.property
        def type(self) -> builtins.str:
            '''The service that the policy is using to protect the resources.

            This specifies the type of policy that is created, either an AWS WAF policy, a Shield Advanced policy, or a security group policy. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-type
            '''
            result = self._values.get("type")
            assert result is not None, "Required property 'type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def managed_service_data(self) -> typing.Optional[builtins.str]:
            '''Details about the service that are specific to the service type, in JSON format.

            - Example: ``DNS_FIREWALL``

            ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"``
            .. epigraph::

               Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000.

            - Example: ``NETWORK_FIREWALL`` - Centralized deployment model

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

            With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

            With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters.

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management

            ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

            ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` .

            - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

            ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"``

            To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

            - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions

            ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"``

            For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"``

            The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` .

            For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string.

            - Example: ``WAFV2``

            ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

            In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` .

            - Example: ``AWS WAF Classic``

            ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"``

            - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning

            ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

            To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group.

            - Example: ``SECURITY_GROUPS_COMMON``

            ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

            - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

            ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

            - Example: ``SECURITY_GROUPS_CONTENT_AUDIT``

            ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"``

            The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.

            - Example: ``SECURITY_GROUPS_USAGE_AUDIT``

            ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-managedservicedata
            '''
            result = self._values.get("managed_service_data")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def policy_option(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.PolicyOptionProperty"]]:
            '''Contains the Network Firewall firewall policy options to configure a centralized deployment model.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-securityservicepolicydata.html#cfn-fms-policy-securityservicepolicydata-policyoption
            '''
            result = self._values.get("policy_option")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnPolicy.PolicyOptionProperty"]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "SecurityServicePolicyDataProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fms.CfnPolicy.ThirdPartyFirewallPolicyProperty",
        jsii_struct_bases=[],
        name_mapping={"firewall_deployment_model": "firewallDeploymentModel"},
    )
    class ThirdPartyFirewallPolicyProperty:
        def __init__(self, *, firewall_deployment_model: builtins.str) -> None:
            '''Configures the deployment model for the third-party firewall.

            :param firewall_deployment_model: Defines the deployment model to use for the third-party firewall policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fms as fms
                
                third_party_firewall_policy_property = fms.CfnPolicy.ThirdPartyFirewallPolicyProperty(
                    firewall_deployment_model="firewallDeploymentModel"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d662c384d3f63f54b65a8a23a65f04ba1a458c4867404d3b5cb2cb088048dd4b)
                check_type(argname="argument firewall_deployment_model", value=firewall_deployment_model, expected_type=type_hints["firewall_deployment_model"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "firewall_deployment_model": firewall_deployment_model,
            }

        @builtins.property
        def firewall_deployment_model(self) -> builtins.str:
            '''Defines the deployment model to use for the third-party firewall policy.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html#cfn-fms-policy-thirdpartyfirewallpolicy-firewalldeploymentmodel
            '''
            result = self._values.get("firewall_deployment_model")
            assert result is not None, "Required property 'firewall_deployment_model' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ThirdPartyFirewallPolicyProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-fms.CfnPolicyProps",
    jsii_struct_bases=[],
    name_mapping={
        "exclude_resource_tags": "excludeResourceTags",
        "policy_name": "policyName",
        "remediation_enabled": "remediationEnabled",
        "security_service_policy_data": "securityServicePolicyData",
        "delete_all_policy_resources": "deleteAllPolicyResources",
        "exclude_map": "excludeMap",
        "include_map": "includeMap",
        "policy_description": "policyDescription",
        "resources_clean_up": "resourcesCleanUp",
        "resource_set_ids": "resourceSetIds",
        "resource_tags": "resourceTags",
        "resource_type": "resourceType",
        "resource_type_list": "resourceTypeList",
        "tags": "tags",
    },
)
class CfnPolicyProps:
    def __init__(
        self,
        *,
        exclude_resource_tags: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        policy_name: builtins.str,
        remediation_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
        security_service_policy_data: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.SecurityServicePolicyDataProperty, typing.Dict[builtins.str, typing.Any]]],
        delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        exclude_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        include_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
        policy_description: typing.Optional[builtins.str] = None,
        resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
        resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
        resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        resource_type: typing.Optional[builtins.str] = None,
        resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[CfnPolicy.PolicyTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnPolicy``.

        :param exclude_resource_tags: Used only when tags are specified in the ``ResourceTags`` property. If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.
        :param policy_name: The name of the AWS Firewall Manager policy.
        :param remediation_enabled: Indicates if the policy should be automatically applied to new resources.
        :param security_service_policy_data: Details about the security service that is being used to protect the resources. This contains the following settings: - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support . Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF`` - ManagedServiceData - Details about the service that are specific to the service type, in JSON format. - Example: ``DNS_FIREWALL`` ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"`` .. epigraph:: Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000. - Example: ``NETWORK_FIREWALL`` - Centralized deployment model ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` . - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"`` To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` . - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"`` For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"`` The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` . For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string. - Example: ``WAFV2`` ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` . - Example: ``AWS WAF Classic`` ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"`` - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"`` To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group. - Example: ``SECURITY_GROUPS_COMMON`` ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"`` - Example: ``SECURITY_GROUPS_CONTENT_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"`` The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group. - Example: ``SECURITY_GROUPS_USAGE_AUDIT`` ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``
        :param delete_all_policy_resources: Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type. For AWS WAF and Shield Advanced policies, Firewall Manager does the following: - Deletes rule groups created by Firewall Manager - Removes web ACLs from in-scope resources - Deletes web ACLs that contain no rules or rule groups For security group policies, Firewall Manager does the following for each security group in the policy: - Disassociates the security group from in-scope resources - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.
        :param exclude_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param include_map: Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy. Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time. You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` . You can specify account IDs, OUs, or a combination: - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` . - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` . - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        :param policy_description: The definition of the AWS Network Firewall firewall policy.
        :param resources_clean_up: Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope. For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope. By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources. This option is not available for Shield Advanced or AWS WAF Classic policies.
        :param resource_set_ids: The unique identifiers of the resource sets used by the policy.
        :param resource_tags: An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them. If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .
        :param resource_type: The type of resource protected by or in scope of the policy. This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` . For AWS WAF and Shield Advanced, example resource types include ``AWS::ElasticLoadBalancingV2::LoadBalancer`` and ``AWS::CloudFront::Distribution`` . For a security group common policy, valid values are ``AWS::EC2::NetworkInterface`` and ``AWS::EC2::Instance`` . For a security group content audit policy, valid values are ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` . For a security group usage audit policy, the value is ``AWS::EC2::SecurityGroup`` . For an AWS Network Firewall policy or DNS Firewall policy, the value is ``AWS::EC2::VPC`` .
        :param resource_type_list: An array of ``ResourceType`` objects. Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .
        :param tags: A collection of key:value pairs associated with an AWS resource. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_fms as fms
            
            cfn_policy_props = fms.CfnPolicyProps(
                exclude_resource_tags=False,
                policy_name="policyName",
                remediation_enabled=False,
                security_service_policy_data=fms.CfnPolicy.SecurityServicePolicyDataProperty(
                    type="type",
            
                    # the properties below are optional
                    managed_service_data="managedServiceData",
                    policy_option=fms.CfnPolicy.PolicyOptionProperty(
                        network_firewall_policy=fms.CfnPolicy.NetworkFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        ),
                        third_party_firewall_policy=fms.CfnPolicy.ThirdPartyFirewallPolicyProperty(
                            firewall_deployment_model="firewallDeploymentModel"
                        )
                    )
                ),
            
                # the properties below are optional
                delete_all_policy_resources=False,
                exclude_map={
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                },
                include_map={
                    "account": ["account"],
                    "orgunit": ["orgunit"]
                },
                policy_description="policyDescription",
                resources_clean_up=False,
                resource_set_ids=["resourceSetIds"],
                resource_tags=[fms.CfnPolicy.ResourceTagProperty(
                    key="key",
            
                    # the properties below are optional
                    value="value"
                )],
                resource_type="resourceType",
                resource_type_list=["resourceTypeList"],
                tags=[fms.CfnPolicy.PolicyTagProperty(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1e859a7affb0da7ac669b89117464dcc24190fa4abe01d9875e6c5a4277f525b)
            check_type(argname="argument exclude_resource_tags", value=exclude_resource_tags, expected_type=type_hints["exclude_resource_tags"])
            check_type(argname="argument policy_name", value=policy_name, expected_type=type_hints["policy_name"])
            check_type(argname="argument remediation_enabled", value=remediation_enabled, expected_type=type_hints["remediation_enabled"])
            check_type(argname="argument security_service_policy_data", value=security_service_policy_data, expected_type=type_hints["security_service_policy_data"])
            check_type(argname="argument delete_all_policy_resources", value=delete_all_policy_resources, expected_type=type_hints["delete_all_policy_resources"])
            check_type(argname="argument exclude_map", value=exclude_map, expected_type=type_hints["exclude_map"])
            check_type(argname="argument include_map", value=include_map, expected_type=type_hints["include_map"])
            check_type(argname="argument policy_description", value=policy_description, expected_type=type_hints["policy_description"])
            check_type(argname="argument resources_clean_up", value=resources_clean_up, expected_type=type_hints["resources_clean_up"])
            check_type(argname="argument resource_set_ids", value=resource_set_ids, expected_type=type_hints["resource_set_ids"])
            check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
            check_type(argname="argument resource_type_list", value=resource_type_list, expected_type=type_hints["resource_type_list"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "exclude_resource_tags": exclude_resource_tags,
            "policy_name": policy_name,
            "remediation_enabled": remediation_enabled,
            "security_service_policy_data": security_service_policy_data,
        }
        if delete_all_policy_resources is not None:
            self._values["delete_all_policy_resources"] = delete_all_policy_resources
        if exclude_map is not None:
            self._values["exclude_map"] = exclude_map
        if include_map is not None:
            self._values["include_map"] = include_map
        if policy_description is not None:
            self._values["policy_description"] = policy_description
        if resources_clean_up is not None:
            self._values["resources_clean_up"] = resources_clean_up
        if resource_set_ids is not None:
            self._values["resource_set_ids"] = resource_set_ids
        if resource_tags is not None:
            self._values["resource_tags"] = resource_tags
        if resource_type is not None:
            self._values["resource_type"] = resource_type
        if resource_type_list is not None:
            self._values["resource_type_list"] = resource_type_list
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def exclude_resource_tags(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Used only when tags are specified in the ``ResourceTags`` property.

        If this property is ``True`` , resources with the specified tags are not in scope of the policy. If it's ``False`` , only resources with the specified tags are in scope of the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excluderesourcetags
        '''
        result = self._values.get("exclude_resource_tags")
        assert result is not None, "Required property 'exclude_resource_tags' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def policy_name(self) -> builtins.str:
        '''The name of the AWS Firewall Manager policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policyname
        '''
        result = self._values.get("policy_name")
        assert result is not None, "Required property 'policy_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def remediation_enabled(
        self,
    ) -> typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]:
        '''Indicates if the policy should be automatically applied to new resources.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-remediationenabled
        '''
        result = self._values.get("remediation_enabled")
        assert result is not None, "Required property 'remediation_enabled' is missing"
        return typing.cast(typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable], result)

    @builtins.property
    def security_service_policy_data(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.SecurityServicePolicyDataProperty]:
        '''Details about the security service that is being used to protect the resources.

        This contains the following settings:

        - Type - Indicates the service type that the policy uses to protect the resource. For security group policies, Firewall Manager supports one security group for each common policy and for each content audit policy. This is an adjustable limit that you can increase by contacting AWS Support .

        Valid values: ``DNS_FIREWALL`` | ``NETWORK_FIREWALL`` | ``SECURITY_GROUPS_COMMON`` | ``SECURITY_GROUPS_CONTENT_AUDIT`` | ``SECURITY_GROUPS_USAGE_AUDIT`` | ``SHIELD_ADVANCED`` | ``THIRD_PARTY_FIREWALL`` | ``WAFV2`` | ``WAF``

        - ManagedServiceData - Details about the service that are specific to the service type, in JSON format.
        - Example: ``DNS_FIREWALL``

        ``"{\\"type\\":\\"DNS_FIREWALL\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-1\\",\\"priority\\":10}],\\"postProcessRuleGroups\\":[{\\"ruleGroupId\\":\\"rslvr-frg-2\\",\\"priority\\":9911}]}"``
        .. epigraph::

           Valid values for ``preProcessRuleGroups`` are between 1 and 99. Valid values for ``postProcessRuleGroups`` are between 9901 and 10000.

        - Example: ``NETWORK_FIREWALL`` - Centralized deployment model

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"awsNetworkFirewallConfig\\":{\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}},\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"OFF\\"},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        With automatic Availbility Zone configuration, Firewall Manager chooses which Availability Zones to create the endpoints in. To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with automatic Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\",\\"192.168.0.0/28\\"],\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"]},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\": \\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":true}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\", \\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{ \\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[ \\"10.0.0.0/28\\"]}]} },\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"OFF\\",\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        With custom Availability Zone configuration, you define which specific Availability Zones to create endpoints in by configuring ``firewallCreationConfig`` . To configure the Availability Zones in ``firewallCreationConfig`` , specify either the ``availabilityZoneName`` or ``availabilityZoneId`` parameter, not both parameters.

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``NETWORK_FIREWALL`` - Distributed deployment model with custom Availability Zone configuration and route management

        ``"{\\"type\\":\\"NETWORK_FIREWALL\\",\\"networkFirewallStatelessRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateless-rulegroup/test\\",\\"priority\\":1}],\\"networkFirewallStatelessDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"customActionName\\"],\\"networkFirewallStatelessFragmentDefaultActions\\":[\\"aws:forward_to_sfe\\",\\"fragmentcustomactionname\\"],\\"networkFirewallStatelessCustomActions\\":[{\\"actionName\\":\\"customActionName\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"metricdimensionvalue\\"}]}}},{\\"actionName\\":\\"fragmentcustomactionname\\",\\"actionDefinition\\":{\\"publishMetricAction\\":{\\"dimensions\\":[{\\"value\\":\\"fragmentmetricdimensionvalue\\"}]}}}],\\"networkFirewallStatefulRuleGroupReferences\\":[{\\"resourceARN\\":\\"arn:aws:network-firewall:us-east-1:123456789011:stateful-rulegroup/test\\"}],\\"networkFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]},{\\"availabilityZoneName\\":\\"us-east-1b\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"singleFirewallEndpointPerVPC\\":false,\\"allowedIPV4CidrList\\":null,\\"routeManagementAction\\":\\"MONITOR\\",\\"routeManagementTargetTypes\\":[\\"InternetGateway\\"],\\"routeManagementConfig\\":{\\"allowCrossAZTrafficIfNoEndpoint\\":true}},\\"networkFirewallLoggingConfiguration\\":{\\"logDestinationConfigs\\":[{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"ALERT\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}},{\\"logDestinationType\\":\\"S3\\",\\"logType\\":\\"FLOW\\",\\"logDestination\\":{\\"bucketName\\":\\"s3-bucket-name\\"}}],\\"overrideExistingConfig\\":boolean}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-networkfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall centralized deployment model

        ``"{ \\"type\\":\\"THIRD_PARTY_FIREWALL\\", \\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\", \\"thirdPartyFirewallConfig\\":{ \\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{\\"centralizedFirewallDeploymentModel\\":{\\"centralizedFirewallOrchestrationConfig\\":{\\"inspectionVpcIds\\":[{\\"resourceId\\":\\"vpc-1234\\",\\"accountId\\":\\"123456789011\\"}],\\"firewallCreationConfig\\":{\\"endpointLocation\\":{\\"availabilityZoneConfigList\\":[{\\"availabilityZoneId\\":null,\\"availabilityZoneName\\":\\"us-east-1a\\",\\"allowedIPV4CidrList\\":[\\"10.0.0.0/28\\"]}]}},\\"allowedIPV4CidrList\\":[]}}}}"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``CENTRALIZED`` .

        - Example: ``THIRD_PARTY_FIREWALL`` - Palo Alto Networks Cloud Next-Generation Firewall distributed deployment model

        ``"{\\"type\\":\\"THIRD_PARTY_FIREWALL\\",\\"thirdPartyFirewall\\":\\"PALO_ALTO_NETWORKS_CLOUD_NGFW\\",\\"thirdPartyFirewallConfig\\":{\\"thirdPartyFirewallPolicyList\\":[\\"global-1\\"] },\\"firewallDeploymentModel\\":{ \\"distributedFirewallDeploymentModel\\":{ \\"distributedFirewallOrchestrationConfig\\":{\\"firewallCreationConfig\\":{\\"endpointLocation\\":{ \\"availabilityZoneConfigList\\":[ {\\"availabilityZoneName\\":\\"${AvailabilityZone}\\" } ] } }, \\"allowedIPV4CidrList\\":[ ] } } } }"``

        To use the distributed deployment model, you must set `FirewallDeploymentModel <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fms-policy-thirdpartyfirewallpolicy.html>`_ to ``DISTRIBUTED`` .

        - Specification for ``SHIELD_ADVANCED`` for Amazon CloudFront distributions

        ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED|IGNORED|DISABLED\\", \\"automaticResponseAction\\":\\"BLOCK|COUNT\\"}, \\"overrideCustomerWebaclClassic\\":true|false}"``

        For example: ``"{\\"type\\":\\"SHIELD_ADVANCED\\",\\"automaticResponseConfiguration\\": {\\"automaticResponseStatus\\":\\"ENABLED\\", \\"automaticResponseAction\\":\\"COUNT\\"}}"``

        The default value for ``automaticResponseStatus`` is ``IGNORED`` . The value for ``automaticResponseAction`` is only required when ``automaticResponseStatus`` is set to ``ENABLED`` . The default value for ``overrideCustomerWebaclClassic`` is ``false`` .

        For other resource types that you can protect with a Shield Advanced policy, this ``ManagedServiceData`` configuration is an empty string.

        - Example: ``WAFV2``

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"version\\":null,\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesAmazonIpReputationList\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        In the ``loggingConfiguration`` , you can specify one ``logDestinationConfigs`` , you can optionally provide up to 20 ``redactedFields`` , and the ``RedactedFieldType`` must be one of ``URI`` , ``QUERY_STRING`` , ``HEADER`` , or ``METHOD`` .

        - Example: ``AWS WAF Classic``

        ``"{\\"type\\": \\"WAF\\", \\"ruleGroups\\": [{\\"id\\":\\"12345678-1bcd-9012-efga-0987654321ab\\", \\"overrideAction\\" : {\\"type\\": \\"COUNT\\"}}], \\"defaultAction\\": {\\"type\\": \\"BLOCK\\"}}"``

        - Example: ``WAFV2`` - AWS Firewall Manager support for AWS WAF managed rule group versioning

        ``"{\\"type\\":\\"WAFV2\\",\\"preProcessRuleGroups\\":[{\\"ruleGroupArn\\":null,\\"overrideAction\\":{\\"type\\":\\"NONE\\"},\\"managedRuleGroupIdentifier\\":{\\"versionEnabled\\":true,\\"version\\":\\"Version_2.0\\",\\"vendorName\\":\\"AWS\\",\\"managedRuleGroupName\\":\\"AWSManagedRulesCommonRuleSet\\"},\\"ruleGroupType\\":\\"ManagedRuleGroup\\",\\"excludeRules\\":[{\\"name\\":\\"NoUserAgent_HEADER\\"}]}],\\"postProcessRuleGroups\\":[],\\"defaultAction\\":{\\"type\\":\\"ALLOW\\"},\\"overrideCustomerWebACLAssociation\\":false,\\"loggingConfiguration\\":{\\"logDestinationConfigs\\":[\\"arn:aws:firehose:us-west-2:12345678912:deliverystream/aws-waf-logs-fms-admin-destination\\"],\\"redactedFields\\":[{\\"redactedFieldType\\":\\"SingleHeader\\",\\"redactedFieldValue\\":\\"Cookies\\"},{\\"redactedFieldType\\":\\"Method\\"}]}}"``

        To use a specific version of a AWS WAF managed rule group in your Firewall Manager policy, you must set ``versionEnabled`` to ``true`` , and set ``version`` to the version you'd like to use. If you don't set ``versionEnabled`` to ``true`` , or if you omit ``versionEnabled`` , then Firewall Manager uses the default version of the AWS WAF managed rule group.

        - Example: ``SECURITY_GROUPS_COMMON``

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: Shared VPCs. Apply the preceding policy to resources in shared VPCs as well as to those in VPCs that the account owns

        ``"{\\"type\\":\\"SECURITY_GROUPS_COMMON\\",\\"revertManualSecurityGroupChanges\\":false,\\"exclusiveResourceSecurityGroupManagement\\":false, \\"applyToAllEC2InstanceENIs\\":false,\\"includeSharedVPC\\":true,\\"securityGroups\\":[{\\"id\\":\\" sg-000e55995d61a06bd\\"}]}"``

        - Example: ``SECURITY_GROUPS_CONTENT_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_CONTENT_AUDIT\\",\\"securityGroups\\":[{\\"id\\":\\"sg-000e55995d61a06bd\\"}],\\"securityGroupAction\\":{\\"type\\":\\"ALLOW\\"}}"``

        The security group action for content audit can be ``ALLOW`` or ``DENY`` . For ``ALLOW`` , all in-scope security group rules must be within the allowed range of the policy's security group rules. For ``DENY`` , all in-scope security group rules must not contain a value or a range that matches a rule value or range in the policy security group.

        - Example: ``SECURITY_GROUPS_USAGE_AUDIT``

        ``"{\\"type\\":\\"SECURITY_GROUPS_USAGE_AUDIT\\",\\"deleteUnusedSecurityGroups\\":true,\\"coalesceRedundantSecurityGroups\\":true}"``

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-securityservicepolicydata
        '''
        result = self._values.get("security_service_policy_data")
        assert result is not None, "Required property 'security_service_policy_data' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.SecurityServicePolicyDataProperty], result)

    @builtins.property
    def delete_all_policy_resources(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Used when deleting a policy. If ``true`` , Firewall Manager performs cleanup according to the policy type.

        For AWS WAF and Shield Advanced policies, Firewall Manager does the following:

        - Deletes rule groups created by Firewall Manager
        - Removes web ACLs from in-scope resources
        - Deletes web ACLs that contain no rules or rule groups

        For security group policies, Firewall Manager does the following for each security group in the policy:

        - Disassociates the security group from in-scope resources
        - Deletes the security group if it was created through Firewall Manager and if it's no longer associated with any resources through another policy

        After the cleanup, in-scope resources are no longer protected by web ACLs in this policy. Protection of out-of-scope resources remains unchanged. Scope is determined by tags that you create and accounts that you associate with the policy. When creating the policy, if you specify that only resources in specific accounts or with specific tags are in scope of the policy, those accounts and resources are handled by the policy. All others are out of scope. If you don't specify tags or accounts, all resources are in scope.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-deleteallpolicyresources
        '''
        result = self._values.get("delete_all_policy_resources")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def exclude_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to exclude from the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-excludemap
        '''
        result = self._values.get("exclude_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]], result)

    @builtins.property
    def include_map(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]]:
        '''Specifies the AWS account IDs and AWS Organizations organizational units (OUs) to include in the policy.

        Specifying an OU is the equivalent of specifying all accounts in the OU and in any of its child OUs, including any child OUs and accounts that are added at a later time.

        You can specify inclusions or exclusions, but not both. If you specify an ``IncludeMap`` , AWS Firewall Manager applies the policy to all accounts specified by the ``IncludeMap`` , and does not evaluate any ``ExcludeMap`` specifications. If you do not specify an ``IncludeMap`` , then Firewall Manager applies the policy to all accounts except for those specified by the ``ExcludeMap`` .

        You can specify account IDs, OUs, or a combination:

        - Specify account IDs by setting the key to ``ACCOUNT`` . For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”]}`` .
        - Specify OUs by setting the key to ``ORGUNIT`` . For example, the following is a valid map: ``{“ORGUNIT” : [“ouid111”, “ouid112”]}`` .
        - Specify accounts and OUs together in a single map, separated with a comma. For example, the following is a valid map: ``{“ACCOUNT” : [“accountID1”, “accountID2”], “ORGUNIT” : [“ouid111”, “ouid112”]}`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-includemap
        '''
        result = self._values.get("include_map")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]], result)

    @builtins.property
    def policy_description(self) -> typing.Optional[builtins.str]:
        '''The definition of the AWS Network Firewall firewall policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-policydescription
        '''
        result = self._values.get("policy_description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources_clean_up(
        self,
    ) -> typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]]:
        '''Indicates whether AWS Firewall Manager should automatically remove protections from resources that leave the policy scope and clean up resources that Firewall Manager is managing for accounts when those accounts leave policy scope.

        For example, Firewall Manager will disassociate a Firewall Manager managed web ACL from a protected customer resource when the customer resource leaves policy scope.

        By default, Firewall Manager doesn't remove protections or delete Firewall Manager managed resources.

        This option is not available for Shield Advanced or AWS WAF Classic policies.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcescleanup
        '''
        result = self._values.get("resources_clean_up")
        return typing.cast(typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]], result)

    @builtins.property
    def resource_set_ids(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The unique identifiers of the resource sets used by the policy.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcesetids
        '''
        result = self._values.get("resource_set_ids")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def resource_tags(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.ResourceTagProperty]]]]:
        '''An array of ``ResourceTag`` objects, used to explicitly include resources in the policy scope or explicitly exclude them.

        If this isn't set, then tags aren't used to modify policy scope. See also ``ExcludeResourceTags`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetags
        '''
        result = self._values.get("resource_tags")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.ResourceTagProperty]]]], result)

    @builtins.property
    def resource_type(self) -> typing.Optional[builtins.str]:
        '''The type of resource protected by or in scope of the policy.

        This is in the format shown in the `AWS Resource Types Reference <https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-template-resource-type-ref.html>`_ . To apply this policy to multiple resource types, specify a resource type of ``ResourceTypeList`` and then specify the resource types in a ``ResourceTypeList`` .

        For AWS WAF and Shield Advanced, example resource types include ``AWS::ElasticLoadBalancingV2::LoadBalancer`` and ``AWS::CloudFront::Distribution`` . For a security group common policy, valid values are ``AWS::EC2::NetworkInterface`` and ``AWS::EC2::Instance`` . For a security group content audit policy, valid values are ``AWS::EC2::SecurityGroup`` , ``AWS::EC2::NetworkInterface`` , and ``AWS::EC2::Instance`` . For a security group usage audit policy, the value is ``AWS::EC2::SecurityGroup`` . For an AWS Network Firewall policy or DNS Firewall policy, the value is ``AWS::EC2::VPC`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetype
        '''
        result = self._values.get("resource_type")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resource_type_list(self) -> typing.Optional[typing.List[builtins.str]]:
        '''An array of ``ResourceType`` objects.

        Use this only to specify multiple resource types. To specify a single resource type, use ``ResourceType`` .

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-resourcetypelist
        '''
        result = self._values.get("resource_type_list")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[CfnPolicy.PolicyTagProperty]]:
        '''A collection of key:value pairs associated with an AWS resource.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-policy.html#cfn-fms-policy-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[CfnPolicy.PolicyTagProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnPolicyProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(_aws_cdk_core_f4b25747.IInspectable)
class CfnResourceSet(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-fms.CfnResourceSet",
):
    '''A CloudFormation ``AWS::FMS::ResourceSet``.

    A set of resources to include in a policy.

    :cloudformationResource: AWS::FMS::ResourceSet
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_fms as fms
        
        cfn_resource_set = fms.CfnResourceSet(self, "MyCfnResourceSet",
            name="name",
            resource_type_list=["resourceTypeList"],
        
            # the properties below are optional
            description="description",
            resources=["resources"],
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
        name: builtins.str,
        resource_type_list: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FMS::ResourceSet``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param name: The descriptive name of the resource set. You can't change the name of a resource set after you create it.
        :param resource_type_list: Determines the resources that can be associated to the resource set. Depending on your setting for max results and the number of resource sets, a single call might not return the full list.
        :param description: A description of the resource set.
        :param resources: The resources included in the resource set.
        :param tags: A collection of key:value pairs associated with a resource set. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__98c73c6c65b2647928705d4762f769d412f2a417eee6e42fd891b0ca5aec2e8f)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnResourceSetProps(
            name=name,
            resource_type_list=resource_type_list,
            description=description,
            resources=resources,
            tags=tags,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__cfc47edb414d5a614bfe4f9805d04409b4d3c6ff2c5dae63d9e9e6f9724ba813)
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
            type_hints = typing.get_type_hints(_typecheckingstub__3cae01073d3ebeb21f5aa34ca3047605e85490943312da78652f7141b7717d59)
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        return typing.cast(typing.Mapping[builtins.str, typing.Any], jsii.invoke(self, "renderProperties", [props]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="CFN_RESOURCE_TYPE_NAME")
    def CFN_RESOURCE_TYPE_NAME(cls) -> builtins.str:
        '''The CloudFormation resource type name for this resource class.'''
        return typing.cast(builtins.str, jsii.sget(cls, "CFN_RESOURCE_TYPE_NAME"))

    @builtins.property
    @jsii.member(jsii_name="attrId")
    def attr_id(self) -> builtins.str:
        '''The ID of the resource set.

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
        '''A collection of key:value pairs associated with a resource set.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        '''The descriptive name of the resource set.

        You can't change the name of a resource set after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-name
        '''
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @name.setter
    def name(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__6b66266caed508346034b3a18667f6679bb95c3e47f379eec7114c45b89c7418)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "name", value)

    @builtins.property
    @jsii.member(jsii_name="resourceTypeList")
    def resource_type_list(self) -> typing.List[builtins.str]:
        '''Determines the resources that can be associated to the resource set.

        Depending on your setting for max results and the number of resource sets, a single call might not return the full list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resourcetypelist
        '''
        return typing.cast(typing.List[builtins.str], jsii.get(self, "resourceTypeList"))

    @resource_type_list.setter
    def resource_type_list(self, value: typing.List[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__4484c6b9ac815cb42d9c482a2433569c7c02b3ccaf6e51370068dc024cc1bb2d)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resourceTypeList", value)

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-description
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "description"))

    @description.setter
    def description(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__fc69028cdfed433e309b7070b678f0bd14a44c0496de11776970a50a3df79f2e)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="resources")
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources included in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resources
        '''
        return typing.cast(typing.Optional[typing.List[builtins.str]], jsii.get(self, "resources"))

    @resources.setter
    def resources(self, value: typing.Optional[typing.List[builtins.str]]) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__b046494214f1216aabe7b0105aad52385f23ff3dd1bd9f85a568d4d428d1341f)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "resources", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-fms.CfnResourceSetProps",
    jsii_struct_bases=[],
    name_mapping={
        "name": "name",
        "resource_type_list": "resourceTypeList",
        "description": "description",
        "resources": "resources",
        "tags": "tags",
    },
)
class CfnResourceSetProps:
    def __init__(
        self,
        *,
        name: builtins.str,
        resource_type_list: typing.Sequence[builtins.str],
        description: typing.Optional[builtins.str] = None,
        resources: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnResourceSet``.

        :param name: The descriptive name of the resource set. You can't change the name of a resource set after you create it.
        :param resource_type_list: Determines the resources that can be associated to the resource set. Depending on your setting for max results and the number of resource sets, a single call might not return the full list.
        :param description: A description of the resource set.
        :param resources: The resources included in the resource set.
        :param tags: A collection of key:value pairs associated with a resource set. The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_fms as fms
            
            cfn_resource_set_props = fms.CfnResourceSetProps(
                name="name",
                resource_type_list=["resourceTypeList"],
            
                # the properties below are optional
                description="description",
                resources=["resources"],
                tags=[CfnTag(
                    key="key",
                    value="value"
                )]
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__839357871e08ce685c1c842e656c1099c2ad72286a9d16c0835a713ad7a1f528)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument resource_type_list", value=resource_type_list, expected_type=type_hints["resource_type_list"])
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "name": name,
            "resource_type_list": resource_type_list,
        }
        if description is not None:
            self._values["description"] = description
        if resources is not None:
            self._values["resources"] = resources
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def name(self) -> builtins.str:
        '''The descriptive name of the resource set.

        You can't change the name of a resource set after you create it.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-name
        '''
        result = self._values.get("name")
        assert result is not None, "Required property 'name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resource_type_list(self) -> typing.List[builtins.str]:
        '''Determines the resources that can be associated to the resource set.

        Depending on your setting for max results and the number of resource sets, a single call might not return the full list.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resourcetypelist
        '''
        result = self._values.get("resource_type_list")
        assert result is not None, "Required property 'resource_type_list' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def description(self) -> typing.Optional[builtins.str]:
        '''A description of the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-description
        '''
        result = self._values.get("description")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def resources(self) -> typing.Optional[typing.List[builtins.str]]:
        '''The resources included in the resource set.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-resources
        '''
        result = self._values.get("resources")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]]:
        '''A collection of key:value pairs associated with a resource set.

        The key:value pair can be anything you define. Typically, the tag key represents a category (such as "environment") and the tag value represents a specific value within that category (such as "test," "development," or "production"). You can add up to 50 tags to each AWS resource.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fms-resourceset.html#cfn-fms-resourceset-tags
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_core_f4b25747.CfnTag]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnResourceSetProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnNotificationChannel",
    "CfnNotificationChannelProps",
    "CfnPolicy",
    "CfnPolicyProps",
    "CfnResourceSet",
    "CfnResourceSetProps",
]

publication.publish()

def _typecheckingstub__8ff279983102395e835cba03517123ba997c5ee38d76f486bb968b17a50dcb54(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    sns_role_name: builtins.str,
    sns_topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6cab35781d8442e68a1bfb6e56a1a0dcae49a50a179c13c7ecf92da02d760a11(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__279da44e5ec9ea0507100ac289410ff4cc504ca18237d85d8954c9a78433ad47(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b2fdf7bedb2b022e68ea1bcead602b02a5155c988c2910c2bd33b606350fc4b3(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c37dbc28c9d0a54dde80d153aaf0a63a9929a7db01cbc8c8286a10317adff181(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1c88d258327730c7503c9c7ef8312754e0a23f227da6b17d0c65f291a7203095(
    *,
    sns_role_name: builtins.str,
    sns_topic_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bae85f07e9a4b7948a93b7caa49d396c532c225934f54619b539a0666b4a5c16(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    exclude_resource_tags: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    policy_name: builtins.str,
    remediation_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    security_service_policy_data: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.SecurityServicePolicyDataProperty, typing.Dict[builtins.str, typing.Any]]],
    delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    exclude_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnPolicy.PolicyTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0a10dc4e67f6dd2662ab529a5772075ea92d1ca7857540f785cefb984c333851(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d94ae7eb859ca5608a74c9d191dcd27283c0b5aab434b1b8ab273d2de2dbd98b(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7e5e6dab7e64bdb8fa671cad14e84a407f2a3c5e184c8ad1f740cf363e8803e0(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a20a3630b091dfe277770cb194ee3d5356b3c489618e470fa8640e2c987e80bd(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e7df22df367cd9b9515152a2c09c4345288c2fe269596197a865e4ab915834e3(
    value: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__081c25303bec09d80d22f276114cd2bf76703ce6cef273579ce49bda48e5ece1(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.SecurityServicePolicyDataProperty],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2517807ae96bd94a3aa78c828632e3dedde0e2b5c94a8cb823e481706d5f2e6d(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9fc1c4f1b99bc22ff8c1eb6c95e268d068bbc754bd13055d3fdf50c2610d34c5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1d466d06e98a9b6717d8cdd2357214de30a366fe4c7b61e9e51ebd965522a3e5(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.IEMapProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1da04897bded9380ad48a049819b07d39659630b1960daf6018ee06172cae8ad(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c0e7f501b22ba5eaedd91d7a51b637ca6bcf36937b4952fd675a2fab2813c555(
    value: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__01b479f26aac79366c2811883c20f0ffc367a9a86afbf4e0d7742fe204a467e8(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4583ee7124b934671566e72e43dcefed38b13be1c0d2a210feed5965cd8b97f0(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnPolicy.ResourceTagProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__400e27ce21d50d9f853e2c4194c792690e1dcf4cc4e02b104053a0ecce4cda03(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c99e5e58285d9a8279a5b206a15b067a11a6a97244b7ecfa4104c2b55d99dad7(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ed3eabd5c6dfb8831e82da1b9504c6c3f2e455d7f22d160f153f2571aba4cd6a(
    value: typing.Optional[typing.List[CfnPolicy.PolicyTagProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b1dd94f8fd7703fc32e4bdf18d28da1d7b36828b914575eef99c5b107a6d6cd0(
    *,
    account: typing.Optional[typing.Sequence[builtins.str]] = None,
    orgunit: typing.Optional[typing.Sequence[builtins.str]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__7160b82f49774a878f27b229efe46344a93215739d4ea16240ecb1185e710700(
    *,
    firewall_deployment_model: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0bf21d6d7b5ee9960672f85bcfe5ee73dcda26e58358749eb304bc52c045b884(
    *,
    network_firewall_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.NetworkFirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    third_party_firewall_policy: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.ThirdPartyFirewallPolicyProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eba627097921973ca66d96916c81bb9a8135aefccaaad0ec264b1565678aa7fb(
    *,
    key: builtins.str,
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4a8a32db23e25f263c7ad590f9fc8b07688b5a79d659d256b4affef87613a0d9(
    *,
    key: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__328e691ffdb3c5debafa1be5a8b8d262600ebcb9536eb8a22cc4531a46eb06e1(
    *,
    type: builtins.str,
    managed_service_data: typing.Optional[builtins.str] = None,
    policy_option: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.PolicyOptionProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d662c384d3f63f54b65a8a23a65f04ba1a458c4867404d3b5cb2cb088048dd4b(
    *,
    firewall_deployment_model: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1e859a7affb0da7ac669b89117464dcc24190fa4abe01d9875e6c5a4277f525b(
    *,
    exclude_resource_tags: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    policy_name: builtins.str,
    remediation_enabled: typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable],
    security_service_policy_data: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.SecurityServicePolicyDataProperty, typing.Dict[builtins.str, typing.Any]]],
    delete_all_policy_resources: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    exclude_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    include_map: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.IEMapProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    policy_description: typing.Optional[builtins.str] = None,
    resources_clean_up: typing.Optional[typing.Union[builtins.bool, _aws_cdk_core_f4b25747.IResolvable]] = None,
    resource_set_ids: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnPolicy.ResourceTagProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    resource_type: typing.Optional[builtins.str] = None,
    resource_type_list: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[CfnPolicy.PolicyTagProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__98c73c6c65b2647928705d4762f769d412f2a417eee6e42fd891b0ca5aec2e8f(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    name: builtins.str,
    resource_type_list: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__cfc47edb414d5a614bfe4f9805d04409b4d3c6ff2c5dae63d9e9e6f9724ba813(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3cae01073d3ebeb21f5aa34ca3047605e85490943312da78652f7141b7717d59(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__6b66266caed508346034b3a18667f6679bb95c3e47f379eec7114c45b89c7418(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__4484c6b9ac815cb42d9c482a2433569c7c02b3ccaf6e51370068dc024cc1bb2d(
    value: typing.List[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__fc69028cdfed433e309b7070b678f0bd14a44c0496de11776970a50a3df79f2e(
    value: typing.Optional[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__b046494214f1216aabe7b0105aad52385f23ff3dd1bd9f85a568d4d428d1341f(
    value: typing.Optional[typing.List[builtins.str]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__839357871e08ce685c1c842e656c1099c2ad72286a9d16c0835a713ad7a1f528(
    *,
    name: builtins.str,
    resource_type_list: typing.Sequence[builtins.str],
    description: typing.Optional[builtins.str] = None,
    resources: typing.Optional[typing.Sequence[builtins.str]] = None,
    tags: typing.Optional[typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.CfnTag, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
