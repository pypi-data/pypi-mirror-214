'''
# AWS::FIS Construct Library

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
import aws_cdk.aws_fis as fis
```

<!--BEGIN CFNONLY DISCLAIMER-->

There are no official hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet. Here are some suggestions on how to proceed:

* Search [Construct Hub for FIS construct libraries](https://constructs.dev/search?q=fis)
* Use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, in the same way you would use [the CloudFormation AWS::FIS resources](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FIS.html) directly.

<!--BEGIN CFNONLY DISCLAIMER-->

There are no hand-written ([L2](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_lib)) constructs for this service yet.
However, you can still use the automatically generated [L1](https://docs.aws.amazon.com/cdk/latest/guide/constructs.html#constructs_l1_using) constructs, and use this service exactly as you would using CloudFormation directly.

For more information on the resources and properties available for this service, see the [CloudFormation documentation for AWS::FIS](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/AWS_FIS.html).

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
class CfnExperimentTemplate(
    _aws_cdk_core_f4b25747.CfnResource,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate",
):
    '''A CloudFormation ``AWS::FIS::ExperimentTemplate``.

    Specifies an experiment template.

    An experiment template includes the following components:

    - *Targets* : A target can be a specific resource in your AWS environment, or one or more resources that match criteria that you specify, for example, resources that have specific tags.
    - *Actions* : The actions to carry out on the target. You can specify multiple actions, the duration of each action, and when to start each action during an experiment.
    - *Stop conditions* : If a stop condition is triggered while an experiment is running, the experiment is automatically stopped. You can define a stop condition as a CloudWatch alarm.

    For more information, see `Experiment templates <https://docs.aws.amazon.com/fis/latest/userguide/experiment-templates.html>`_ in the *AWS Fault Injection Simulator User Guide* .

    :cloudformationResource: AWS::FIS::ExperimentTemplate
    :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html
    :exampleMetadata: fixture=_generated

    Example::

        # The code below shows an example of how to instantiate this type.
        # The values are placeholders you should change.
        import aws_cdk.aws_fis as fis
        
        # cloud_watch_logs_configuration: Any
        # s3_configuration: Any
        
        cfn_experiment_template = fis.CfnExperimentTemplate(self, "MyCfnExperimentTemplate",
            description="description",
            role_arn="roleArn",
            stop_conditions=[fis.CfnExperimentTemplate.ExperimentTemplateStopConditionProperty(
                source="source",
        
                # the properties below are optional
                value="value"
            )],
            tags={
                "tags_key": "tags"
            },
            targets={
                "targets_key": fis.CfnExperimentTemplate.ExperimentTemplateTargetProperty(
                    resource_type="resourceType",
                    selection_mode="selectionMode",
        
                    # the properties below are optional
                    filters=[fis.CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty(
                        path="path",
                        values=["values"]
                    )],
                    parameters={
                        "parameters_key": "parameters"
                    },
                    resource_arns=["resourceArns"],
                    resource_tags={
                        "resource_tags_key": "resourceTags"
                    }
                )
            },
        
            # the properties below are optional
            actions={
                "actions_key": fis.CfnExperimentTemplate.ExperimentTemplateActionProperty(
                    action_id="actionId",
        
                    # the properties below are optional
                    description="description",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    start_after=["startAfter"],
                    targets={
                        "targets_key": "targets"
                    }
                )
            },
            log_configuration=fis.CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty(
                log_schema_version=123,
        
                # the properties below are optional
                cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                s3_configuration=s3_configuration
            )
        )
    '''

    def __init__(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        id: builtins.str,
        *,
        description: builtins.str,
        role_arn: builtins.str,
        stop_conditions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union["CfnExperimentTemplate.ExperimentTemplateStopConditionProperty", typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        tags: typing.Mapping[builtins.str, builtins.str],
        targets: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnExperimentTemplate.ExperimentTemplateTargetProperty", typing.Dict[builtins.str, typing.Any]]]]],
        actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnExperimentTemplate.ExperimentTemplateActionProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty", typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Create a new ``AWS::FIS::ExperimentTemplate``.

        :param scope: - scope in which this resource is defined.
        :param id: - scoped id of the resource.
        :param description: A description for the experiment template.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that grants the AWS FIS service permission to perform service actions on your behalf.
        :param stop_conditions: The stop conditions.
        :param tags: The tags to apply to the experiment template.
        :param targets: The targets for the experiment.
        :param actions: The actions for the experiment.
        :param log_configuration: The configuration for experiment logging.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__336b2aec9029077afa3dd3998bda43df47601e3fe373b4e0bbe3a234a8e53088)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = CfnExperimentTemplateProps(
            description=description,
            role_arn=role_arn,
            stop_conditions=stop_conditions,
            tags=tags,
            targets=targets,
            actions=actions,
            log_configuration=log_configuration,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="inspect")
    def inspect(self, inspector: _aws_cdk_core_f4b25747.TreeInspector) -> None:
        '''Examines the CloudFormation resource and discloses attributes.

        :param inspector: - tree inspector to collect and process attributes.
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__0373699f24a88bb445b61c07afe0839785641b70711ef56166e572a7d2b74115)
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
            type_hints = typing.get_type_hints(_typecheckingstub__475e6e7bc8a78c12929bd837e2e42a8664e5e29ca126b82f0b950506377e5c80)
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
        '''The ID of the experiment template.

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
        '''The tags to apply to the experiment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-tags
        '''
        return typing.cast(_aws_cdk_core_f4b25747.TagManager, jsii.get(self, "tags"))

    @builtins.property
    @jsii.member(jsii_name="description")
    def description(self) -> builtins.str:
        '''A description for the experiment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-description
        '''
        return typing.cast(builtins.str, jsii.get(self, "description"))

    @description.setter
    def description(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__3af0c1bd41ebc878fcd8e593d535b2e6135eea63a0505a732ba5a9e77a036571)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "description", value)

    @builtins.property
    @jsii.member(jsii_name="roleArn")
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an IAM role that grants the AWS FIS service permission to perform service actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-rolearn
        '''
        return typing.cast(builtins.str, jsii.get(self, "roleArn"))

    @role_arn.setter
    def role_arn(self, value: builtins.str) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__1f76098cc48aaee2e8a45465e697001c04b9b376f10e43b8af254cec7a3f7df1)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "roleArn", value)

    @builtins.property
    @jsii.member(jsii_name="stopConditions")
    def stop_conditions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnExperimentTemplate.ExperimentTemplateStopConditionProperty", _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The stop conditions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-stopconditions
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnExperimentTemplate.ExperimentTemplateStopConditionProperty", _aws_cdk_core_f4b25747.IResolvable]]], jsii.get(self, "stopConditions"))

    @stop_conditions.setter
    def stop_conditions(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union["CfnExperimentTemplate.ExperimentTemplateStopConditionProperty", _aws_cdk_core_f4b25747.IResolvable]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__09591a67842c449fe5aad62ac82fce85958a28a8ab67cbc388d49240873ffae2)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "stopConditions", value)

    @builtins.property
    @jsii.member(jsii_name="targets")
    def targets(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateTargetProperty"]]]:
        '''The targets for the experiment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-targets
        '''
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateTargetProperty"]]], jsii.get(self, "targets"))

    @targets.setter
    def targets(
        self,
        value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateTargetProperty"]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__e9b49fd1820064f13a4653b0375f0de79c7b3a3410a020322e05eb9a1ecc8424)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "targets", value)

    @builtins.property
    @jsii.member(jsii_name="actions")
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateActionProperty"]]]]:
        '''The actions for the experiment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-actions
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateActionProperty"]]]], jsii.get(self, "actions"))

    @actions.setter
    def actions(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateActionProperty"]]]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2a9415067374abbf4fe3231acad4e5f1bf8842f09f6231db1c0f60475b556e93)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "actions", value)

    @builtins.property
    @jsii.member(jsii_name="logConfiguration")
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty"]]:
        '''The configuration for experiment logging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-logconfiguration
        '''
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty"]], jsii.get(self, "logConfiguration"))

    @log_configuration.setter
    def log_configuration(
        self,
        value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty"]],
    ) -> None:
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__190268668ae25d12a8c8d75211a878b80523e457e021c05c4c4c7f4a82fc72e6)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "logConfiguration", value)

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.CloudWatchLogsConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"log_group_arn": "logGroupArn"},
    )
    class CloudWatchLogsConfigurationProperty:
        def __init__(self, *, log_group_arn: builtins.str) -> None:
            '''Specifies the configuration for experiment logging to CloudWatch Logs .

            :param log_group_arn: The Amazon Resource Name (ARN) of the destination Amazon CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-cloudwatchlogsconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                cloud_watch_logs_configuration_property = fis.CfnExperimentTemplate.CloudWatchLogsConfigurationProperty(
                    log_group_arn="logGroupArn"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__277005e885c2d16a633889c43b51ebc3f2105d853fe5eb8682e8c9958a070acb)
                check_type(argname="argument log_group_arn", value=log_group_arn, expected_type=type_hints["log_group_arn"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_group_arn": log_group_arn,
            }

        @builtins.property
        def log_group_arn(self) -> builtins.str:
            '''The Amazon Resource Name (ARN) of the destination Amazon CloudWatch Logs log group.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-cloudwatchlogsconfiguration.html#cfn-fis-experimenttemplate-cloudwatchlogsconfiguration-loggrouparn
            '''
            result = self._values.get("log_group_arn")
            assert result is not None, "Required property 'log_group_arn' is missing"
            return typing.cast(builtins.str, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "CloudWatchLogsConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.ExperimentTemplateActionProperty",
        jsii_struct_bases=[],
        name_mapping={
            "action_id": "actionId",
            "description": "description",
            "parameters": "parameters",
            "start_after": "startAfter",
            "targets": "targets",
        },
    )
    class ExperimentTemplateActionProperty:
        def __init__(
            self,
            *,
            action_id: builtins.str,
            description: typing.Optional[builtins.str] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
            targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''Specifies an action for an experiment template.

            For more information, see `Actions <https://docs.aws.amazon.com/fis/latest/userguide/actions.html>`_ in the *AWS Fault Injection Simulator User Guide* .

            :param action_id: The ID of the action. The format of the action ID is: aws: *service-name* : *action-type* .
            :param description: A description for the action.
            :param parameters: The parameters for the action, if applicable.
            :param start_after: The name of the action that must be completed before the current action starts. Omit this parameter to run the action at the start of the experiment.
            :param targets: The targets for the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                experiment_template_action_property = fis.CfnExperimentTemplate.ExperimentTemplateActionProperty(
                    action_id="actionId",
                
                    # the properties below are optional
                    description="description",
                    parameters={
                        "parameters_key": "parameters"
                    },
                    start_after=["startAfter"],
                    targets={
                        "targets_key": "targets"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__ca32fbe2cfc6bdac898b50cad0949b2e61ac7fb3c8c999d1d0ac4765f6615cd1)
                check_type(argname="argument action_id", value=action_id, expected_type=type_hints["action_id"])
                check_type(argname="argument description", value=description, expected_type=type_hints["description"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument start_after", value=start_after, expected_type=type_hints["start_after"])
                check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "action_id": action_id,
            }
            if description is not None:
                self._values["description"] = description
            if parameters is not None:
                self._values["parameters"] = parameters
            if start_after is not None:
                self._values["start_after"] = start_after
            if targets is not None:
                self._values["targets"] = targets

        @builtins.property
        def action_id(self) -> builtins.str:
            '''The ID of the action.

            The format of the action ID is: aws: *service-name* : *action-type* .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-actionid
            '''
            result = self._values.get("action_id")
            assert result is not None, "Required property 'action_id' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def description(self) -> typing.Optional[builtins.str]:
            '''A description for the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-description
            '''
            result = self._values.get("description")
            return typing.cast(typing.Optional[builtins.str], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The parameters for the action, if applicable.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def start_after(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The name of the action that must be completed before the current action starts.

            Omit this parameter to run the action at the start of the experiment.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-startafter
            '''
            result = self._values.get("start_after")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def targets(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The targets for the action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplateaction.html#cfn-fis-experimenttemplate-experimenttemplateaction-targets
            '''
            result = self._values.get("targets")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateActionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={
            "log_schema_version": "logSchemaVersion",
            "cloud_watch_logs_configuration": "cloudWatchLogsConfiguration",
            "s3_configuration": "s3Configuration",
        },
    )
    class ExperimentTemplateLogConfigurationProperty:
        def __init__(
            self,
            *,
            log_schema_version: jsii.Number,
            cloud_watch_logs_configuration: typing.Any = None,
            s3_configuration: typing.Any = None,
        ) -> None:
            '''Specifies the configuration for experiment logging.

            For more information, see `Experiment logging <https://docs.aws.amazon.com/fis/latest/userguide/monitoring-logging.html>`_ in the *AWS Fault Injection Simulator User Guide* .

            :param log_schema_version: The schema version.
            :param cloud_watch_logs_configuration: The configuration for experiment logging to CloudWatch Logs .
            :param s3_configuration: The configuration for experiment logging to Amazon S3 .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                # cloud_watch_logs_configuration: Any
                # s3_configuration: Any
                
                experiment_template_log_configuration_property = fis.CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty(
                    log_schema_version=123,
                
                    # the properties below are optional
                    cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                    s3_configuration=s3_configuration
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__d52643504c088f2cb465c8a9edd177aa2417a2b1ca4e17e70ac9774f0de0119d)
                check_type(argname="argument log_schema_version", value=log_schema_version, expected_type=type_hints["log_schema_version"])
                check_type(argname="argument cloud_watch_logs_configuration", value=cloud_watch_logs_configuration, expected_type=type_hints["cloud_watch_logs_configuration"])
                check_type(argname="argument s3_configuration", value=s3_configuration, expected_type=type_hints["s3_configuration"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "log_schema_version": log_schema_version,
            }
            if cloud_watch_logs_configuration is not None:
                self._values["cloud_watch_logs_configuration"] = cloud_watch_logs_configuration
            if s3_configuration is not None:
                self._values["s3_configuration"] = s3_configuration

        @builtins.property
        def log_schema_version(self) -> jsii.Number:
            '''The schema version.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-logschemaversion
            '''
            result = self._values.get("log_schema_version")
            assert result is not None, "Required property 'log_schema_version' is missing"
            return typing.cast(jsii.Number, result)

        @builtins.property
        def cloud_watch_logs_configuration(self) -> typing.Any:
            '''The configuration for experiment logging to CloudWatch Logs .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-cloudwatchlogsconfiguration
            '''
            result = self._values.get("cloud_watch_logs_configuration")
            return typing.cast(typing.Any, result)

        @builtins.property
        def s3_configuration(self) -> typing.Any:
            '''The configuration for experiment logging to Amazon S3 .

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatelogconfiguration.html#cfn-fis-experimenttemplate-experimenttemplatelogconfiguration-s3configuration
            '''
            result = self._values.get("s3_configuration")
            return typing.cast(typing.Any, result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateLogConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.ExperimentTemplateStopConditionProperty",
        jsii_struct_bases=[],
        name_mapping={"source": "source", "value": "value"},
    )
    class ExperimentTemplateStopConditionProperty:
        def __init__(
            self,
            *,
            source: builtins.str,
            value: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies a stop condition for an experiment template.

            For more information, see `Stop conditions <https://docs.aws.amazon.com/fis/latest/userguide/stop-conditions.html>`_ in the *AWS Fault Injection Simulator User Guide* .

            :param source: The source for the stop condition. Specify ``aws:cloudwatch:alarm`` if the stop condition is defined by a CloudWatch alarm. Specify ``none`` if there is no stop condition.
            :param value: The Amazon Resource Name (ARN) of the CloudWatch alarm. This is required if the source is a CloudWatch alarm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                experiment_template_stop_condition_property = fis.CfnExperimentTemplate.ExperimentTemplateStopConditionProperty(
                    source="source",
                
                    # the properties below are optional
                    value="value"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__9f77aa2eb5bdcd1af3f66a82b5e8022b1b4f82bcccd71af466faa005a2b7a669)
                check_type(argname="argument source", value=source, expected_type=type_hints["source"])
                check_type(argname="argument value", value=value, expected_type=type_hints["value"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "source": source,
            }
            if value is not None:
                self._values["value"] = value

        @builtins.property
        def source(self) -> builtins.str:
            '''The source for the stop condition.

            Specify ``aws:cloudwatch:alarm`` if the stop condition is defined by a CloudWatch alarm. Specify ``none`` if there is no stop condition.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html#cfn-fis-experimenttemplate-experimenttemplatestopcondition-source
            '''
            result = self._values.get("source")
            assert result is not None, "Required property 'source' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def value(self) -> typing.Optional[builtins.str]:
            '''The Amazon Resource Name (ARN) of the CloudWatch alarm.

            This is required if the source is a CloudWatch alarm.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatestopcondition.html#cfn-fis-experimenttemplate-experimenttemplatestopcondition-value
            '''
            result = self._values.get("value")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateStopConditionProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty",
        jsii_struct_bases=[],
        name_mapping={"path": "path", "values": "values"},
    )
    class ExperimentTemplateTargetFilterProperty:
        def __init__(
            self,
            *,
            path: builtins.str,
            values: typing.Sequence[builtins.str],
        ) -> None:
            '''Specifies a filter used for the target resource input in an experiment template.

            For more information, see `Resource filters <https://docs.aws.amazon.com/fis/latest/userguide/targets.html#target-filters>`_ in the *AWS Fault Injection Simulator User Guide* .

            :param path: The attribute path for the filter.
            :param values: The attribute values for the filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                experiment_template_target_filter_property = fis.CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty(
                    path="path",
                    values=["values"]
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__64fe6207f0d8001ed9ba8adb209b7e2cae7d37c40e877ee0539b0b20b6bf2d18)
                check_type(argname="argument path", value=path, expected_type=type_hints["path"])
                check_type(argname="argument values", value=values, expected_type=type_hints["values"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "path": path,
                "values": values,
            }

        @builtins.property
        def path(self) -> builtins.str:
            '''The attribute path for the filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html#cfn-fis-experimenttemplate-experimenttemplatetargetfilter-path
            '''
            result = self._values.get("path")
            assert result is not None, "Required property 'path' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def values(self) -> typing.List[builtins.str]:
            '''The attribute values for the filter.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetargetfilter.html#cfn-fis-experimenttemplate-experimenttemplatetargetfilter-values
            '''
            result = self._values.get("values")
            assert result is not None, "Required property 'values' is missing"
            return typing.cast(typing.List[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateTargetFilterProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.ExperimentTemplateTargetProperty",
        jsii_struct_bases=[],
        name_mapping={
            "resource_type": "resourceType",
            "selection_mode": "selectionMode",
            "filters": "filters",
            "parameters": "parameters",
            "resource_arns": "resourceArns",
            "resource_tags": "resourceTags",
        },
    )
    class ExperimentTemplateTargetProperty:
        def __init__(
            self,
            *,
            resource_type: builtins.str,
            selection_mode: builtins.str,
            filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union["CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty", typing.Dict[builtins.str, typing.Any]]]]]] = None,
            parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
            resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
            resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
        ) -> None:
            '''Specifies a target for an experiment.

            You must specify at least one Amazon Resource Name (ARN) or at least one resource tag. You cannot specify both ARNs and tags.

            For more information, see `Targets <https://docs.aws.amazon.com/fis/latest/userguide/targets.html>`_ in the *AWS Fault Injection Simulator User Guide* .

            :param resource_type: The resource type. The resource type must be supported for the specified action.
            :param selection_mode: Scopes the identified resources to a specific count of the resources at random, or a percentage of the resources. All identified resources are included in the target. - ALL - Run the action on all identified targets. This is the default. - COUNT(n) - Run the action on the specified number of targets, chosen from the identified targets at random. For example, COUNT(1) selects one of the targets. - PERCENT(n) - Run the action on the specified percentage of targets, chosen from the identified targets at random. For example, PERCENT(25) selects 25% of the targets.
            :param filters: The filters to apply to identify target resources using specific attributes.
            :param parameters: The parameters for the resource type.
            :param resource_arns: The Amazon Resource Names (ARNs) of the resources.
            :param resource_tags: The tags for the target resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                experiment_template_target_property = fis.CfnExperimentTemplate.ExperimentTemplateTargetProperty(
                    resource_type="resourceType",
                    selection_mode="selectionMode",
                
                    # the properties below are optional
                    filters=[fis.CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty(
                        path="path",
                        values=["values"]
                    )],
                    parameters={
                        "parameters_key": "parameters"
                    },
                    resource_arns=["resourceArns"],
                    resource_tags={
                        "resource_tags_key": "resourceTags"
                    }
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__bb1a35b488df529b88d75871857d7011f8b3c6327d37ccfa4371984bfde69e24)
                check_type(argname="argument resource_type", value=resource_type, expected_type=type_hints["resource_type"])
                check_type(argname="argument selection_mode", value=selection_mode, expected_type=type_hints["selection_mode"])
                check_type(argname="argument filters", value=filters, expected_type=type_hints["filters"])
                check_type(argname="argument parameters", value=parameters, expected_type=type_hints["parameters"])
                check_type(argname="argument resource_arns", value=resource_arns, expected_type=type_hints["resource_arns"])
                check_type(argname="argument resource_tags", value=resource_tags, expected_type=type_hints["resource_tags"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "resource_type": resource_type,
                "selection_mode": selection_mode,
            }
            if filters is not None:
                self._values["filters"] = filters
            if parameters is not None:
                self._values["parameters"] = parameters
            if resource_arns is not None:
                self._values["resource_arns"] = resource_arns
            if resource_tags is not None:
                self._values["resource_tags"] = resource_tags

        @builtins.property
        def resource_type(self) -> builtins.str:
            '''The resource type.

            The resource type must be supported for the specified action.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcetype
            '''
            result = self._values.get("resource_type")
            assert result is not None, "Required property 'resource_type' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def selection_mode(self) -> builtins.str:
            '''Scopes the identified resources to a specific count of the resources at random, or a percentage of the resources.

            All identified resources are included in the target.

            - ALL - Run the action on all identified targets. This is the default.
            - COUNT(n) - Run the action on the specified number of targets, chosen from the identified targets at random. For example, COUNT(1) selects one of the targets.
            - PERCENT(n) - Run the action on the specified percentage of targets, chosen from the identified targets at random. For example, PERCENT(25) selects 25% of the targets.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-selectionmode
            '''
            result = self._values.get("selection_mode")
            assert result is not None, "Required property 'selection_mode' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def filters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty"]]]]:
            '''The filters to apply to identify target resources using specific attributes.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-filters
            '''
            result = self._values.get("filters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[_aws_cdk_core_f4b25747.IResolvable, "CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty"]]]], result)

        @builtins.property
        def parameters(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The parameters for the resource type.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-parameters
            '''
            result = self._values.get("parameters")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        @builtins.property
        def resource_arns(self) -> typing.Optional[typing.List[builtins.str]]:
            '''The Amazon Resource Names (ARNs) of the resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcearns
            '''
            result = self._values.get("resource_arns")
            return typing.cast(typing.Optional[typing.List[builtins.str]], result)

        @builtins.property
        def resource_tags(
            self,
        ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]]:
            '''The tags for the target resources.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-experimenttemplatetarget.html#cfn-fis-experimenttemplate-experimenttemplatetarget-resourcetags
            '''
            result = self._values.get("resource_tags")
            return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "ExperimentTemplateTargetProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )

    @jsii.data_type(
        jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplate.S3ConfigurationProperty",
        jsii_struct_bases=[],
        name_mapping={"bucket_name": "bucketName", "prefix": "prefix"},
    )
    class S3ConfigurationProperty:
        def __init__(
            self,
            *,
            bucket_name: builtins.str,
            prefix: typing.Optional[builtins.str] = None,
        ) -> None:
            '''Specifies the configuration for experiment logging to Amazon S3 .

            :param bucket_name: The name of the destination bucket.
            :param prefix: The bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-s3configuration.html
            :exampleMetadata: fixture=_generated

            Example::

                # The code below shows an example of how to instantiate this type.
                # The values are placeholders you should change.
                import aws_cdk.aws_fis as fis
                
                s3_configuration_property = fis.CfnExperimentTemplate.S3ConfigurationProperty(
                    bucket_name="bucketName",
                
                    # the properties below are optional
                    prefix="prefix"
                )
            '''
            if __debug__:
                type_hints = typing.get_type_hints(_typecheckingstub__94c0c039680d7c67cc54077e82f748c0421f36c686a056a64b32de7bf3807982)
                check_type(argname="argument bucket_name", value=bucket_name, expected_type=type_hints["bucket_name"])
                check_type(argname="argument prefix", value=prefix, expected_type=type_hints["prefix"])
            self._values: typing.Dict[builtins.str, typing.Any] = {
                "bucket_name": bucket_name,
            }
            if prefix is not None:
                self._values["prefix"] = prefix

        @builtins.property
        def bucket_name(self) -> builtins.str:
            '''The name of the destination bucket.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-s3configuration.html#cfn-fis-experimenttemplate-s3configuration-bucketname
            '''
            result = self._values.get("bucket_name")
            assert result is not None, "Required property 'bucket_name' is missing"
            return typing.cast(builtins.str, result)

        @builtins.property
        def prefix(self) -> typing.Optional[builtins.str]:
            '''The bucket prefix.

            :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-fis-experimenttemplate-s3configuration.html#cfn-fis-experimenttemplate-s3configuration-prefix
            '''
            result = self._values.get("prefix")
            return typing.cast(typing.Optional[builtins.str], result)

        def __eq__(self, rhs: typing.Any) -> builtins.bool:
            return isinstance(rhs, self.__class__) and rhs._values == self._values

        def __ne__(self, rhs: typing.Any) -> builtins.bool:
            return not (rhs == self)

        def __repr__(self) -> str:
            return "S3ConfigurationProperty(%s)" % ", ".join(
                k + "=" + repr(v) for k, v in self._values.items()
            )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-fis.CfnExperimentTemplateProps",
    jsii_struct_bases=[],
    name_mapping={
        "description": "description",
        "role_arn": "roleArn",
        "stop_conditions": "stopConditions",
        "tags": "tags",
        "targets": "targets",
        "actions": "actions",
        "log_configuration": "logConfiguration",
    },
)
class CfnExperimentTemplateProps:
    def __init__(
        self,
        *,
        description: builtins.str,
        role_arn: builtins.str,
        stop_conditions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
        tags: typing.Mapping[builtins.str, builtins.str],
        targets: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateTargetProperty, typing.Dict[builtins.str, typing.Any]]]]],
        actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
        log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
    ) -> None:
        '''Properties for defining a ``CfnExperimentTemplate``.

        :param description: A description for the experiment template.
        :param role_arn: The Amazon Resource Name (ARN) of an IAM role that grants the AWS FIS service permission to perform service actions on your behalf.
        :param stop_conditions: The stop conditions.
        :param tags: The tags to apply to the experiment template.
        :param targets: The targets for the experiment.
        :param actions: The actions for the experiment.
        :param log_configuration: The configuration for experiment logging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html
        :exampleMetadata: fixture=_generated

        Example::

            # The code below shows an example of how to instantiate this type.
            # The values are placeholders you should change.
            import aws_cdk.aws_fis as fis
            
            # cloud_watch_logs_configuration: Any
            # s3_configuration: Any
            
            cfn_experiment_template_props = fis.CfnExperimentTemplateProps(
                description="description",
                role_arn="roleArn",
                stop_conditions=[fis.CfnExperimentTemplate.ExperimentTemplateStopConditionProperty(
                    source="source",
            
                    # the properties below are optional
                    value="value"
                )],
                tags={
                    "tags_key": "tags"
                },
                targets={
                    "targets_key": fis.CfnExperimentTemplate.ExperimentTemplateTargetProperty(
                        resource_type="resourceType",
                        selection_mode="selectionMode",
            
                        # the properties below are optional
                        filters=[fis.CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty(
                            path="path",
                            values=["values"]
                        )],
                        parameters={
                            "parameters_key": "parameters"
                        },
                        resource_arns=["resourceArns"],
                        resource_tags={
                            "resource_tags_key": "resourceTags"
                        }
                    )
                },
            
                # the properties below are optional
                actions={
                    "actions_key": fis.CfnExperimentTemplate.ExperimentTemplateActionProperty(
                        action_id="actionId",
            
                        # the properties below are optional
                        description="description",
                        parameters={
                            "parameters_key": "parameters"
                        },
                        start_after=["startAfter"],
                        targets={
                            "targets_key": "targets"
                        }
                    )
                },
                log_configuration=fis.CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty(
                    log_schema_version=123,
            
                    # the properties below are optional
                    cloud_watch_logs_configuration=cloud_watch_logs_configuration,
                    s3_configuration=s3_configuration
                )
            )
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__eea8b5a4d6cebf8529cc96708709289c5b4fcb530a4211ea2ed2bfd3d95b4827)
            check_type(argname="argument description", value=description, expected_type=type_hints["description"])
            check_type(argname="argument role_arn", value=role_arn, expected_type=type_hints["role_arn"])
            check_type(argname="argument stop_conditions", value=stop_conditions, expected_type=type_hints["stop_conditions"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument targets", value=targets, expected_type=type_hints["targets"])
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument log_configuration", value=log_configuration, expected_type=type_hints["log_configuration"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "description": description,
            "role_arn": role_arn,
            "stop_conditions": stop_conditions,
            "tags": tags,
            "targets": targets,
        }
        if actions is not None:
            self._values["actions"] = actions
        if log_configuration is not None:
            self._values["log_configuration"] = log_configuration

    @builtins.property
    def description(self) -> builtins.str:
        '''A description for the experiment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-description
        '''
        result = self._values.get("description")
        assert result is not None, "Required property 'description' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def role_arn(self) -> builtins.str:
        '''The Amazon Resource Name (ARN) of an IAM role that grants the AWS FIS service permission to perform service actions on your behalf.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-rolearn
        '''
        result = self._values.get("role_arn")
        assert result is not None, "Required property 'role_arn' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def stop_conditions(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, _aws_cdk_core_f4b25747.IResolvable]]]:
        '''The stop conditions.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-stopconditions
        '''
        result = self._values.get("stop_conditions")
        assert result is not None, "Required property 'stop_conditions' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, _aws_cdk_core_f4b25747.IResolvable]]], result)

    @builtins.property
    def tags(self) -> typing.Mapping[builtins.str, builtins.str]:
        '''The tags to apply to the experiment template.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-tags
        '''
        result = self._values.get("tags")
        assert result is not None, "Required property 'tags' is missing"
        return typing.cast(typing.Mapping[builtins.str, builtins.str], result)

    @builtins.property
    def targets(
        self,
    ) -> typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateTargetProperty]]]:
        '''The targets for the experiment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-targets
        '''
        result = self._values.get("targets")
        assert result is not None, "Required property 'targets' is missing"
        return typing.cast(typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateTargetProperty]]], result)

    @builtins.property
    def actions(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateActionProperty]]]]:
        '''The actions for the experiment.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-actions
        '''
        result = self._values.get("actions")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateActionProperty]]]], result)

    @builtins.property
    def log_configuration(
        self,
    ) -> typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty]]:
        '''The configuration for experiment logging.

        :link: http://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-resource-fis-experimenttemplate.html#cfn-fis-experimenttemplate-logconfiguration
        '''
        result = self._values.get("log_configuration")
        return typing.cast(typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CfnExperimentTemplateProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "CfnExperimentTemplate",
    "CfnExperimentTemplateProps",
]

publication.publish()

def _typecheckingstub__336b2aec9029077afa3dd3998bda43df47601e3fe373b4e0bbe3a234a8e53088(
    scope: _aws_cdk_core_f4b25747.Construct,
    id: builtins.str,
    *,
    description: builtins.str,
    role_arn: builtins.str,
    stop_conditions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    tags: typing.Mapping[builtins.str, builtins.str],
    targets: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateTargetProperty, typing.Dict[builtins.str, typing.Any]]]]],
    actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__0373699f24a88bb445b61c07afe0839785641b70711ef56166e572a7d2b74115(
    inspector: _aws_cdk_core_f4b25747.TreeInspector,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__475e6e7bc8a78c12929bd837e2e42a8664e5e29ca126b82f0b950506377e5c80(
    props: typing.Mapping[builtins.str, typing.Any],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__3af0c1bd41ebc878fcd8e593d535b2e6135eea63a0505a732ba5a9e77a036571(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__1f76098cc48aaee2e8a45465e697001c04b9b376f10e43b8af254cec7a3f7df1(
    value: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__09591a67842c449fe5aad62ac82fce85958a28a8ab67cbc388d49240873ffae2(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.List[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, _aws_cdk_core_f4b25747.IResolvable]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__e9b49fd1820064f13a4653b0375f0de79c7b3a3410a020322e05eb9a1ecc8424(
    value: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateTargetProperty]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__2a9415067374abbf4fe3231acad4e5f1bf8842f09f6231db1c0f60475b556e93(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateActionProperty]]]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__190268668ae25d12a8c8d75211a878b80523e457e021c05c4c4c7f4a82fc72e6(
    value: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty]],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__277005e885c2d16a633889c43b51ebc3f2105d853fe5eb8682e8c9958a070acb(
    *,
    log_group_arn: builtins.str,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__ca32fbe2cfc6bdac898b50cad0949b2e61ac7fb3c8c999d1d0ac4765f6615cd1(
    *,
    action_id: builtins.str,
    description: typing.Optional[builtins.str] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    start_after: typing.Optional[typing.Sequence[builtins.str]] = None,
    targets: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__d52643504c088f2cb465c8a9edd177aa2417a2b1ca4e17e70ac9774f0de0119d(
    *,
    log_schema_version: jsii.Number,
    cloud_watch_logs_configuration: typing.Any = None,
    s3_configuration: typing.Any = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__9f77aa2eb5bdcd1af3f66a82b5e8022b1b4f82bcccd71af466faa005a2b7a669(
    *,
    source: builtins.str,
    value: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__64fe6207f0d8001ed9ba8adb209b7e2cae7d37c40e877ee0539b0b20b6bf2d18(
    *,
    path: builtins.str,
    values: typing.Sequence[builtins.str],
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__bb1a35b488df529b88d75871857d7011f8b3c6327d37ccfa4371984bfde69e24(
    *,
    resource_type: builtins.str,
    selection_mode: builtins.str,
    filters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateTargetFilterProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    parameters: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
    resource_arns: typing.Optional[typing.Sequence[builtins.str]] = None,
    resource_tags: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, builtins.str]]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__94c0c039680d7c67cc54077e82f748c0421f36c686a056a64b32de7bf3807982(
    *,
    bucket_name: builtins.str,
    prefix: typing.Optional[builtins.str] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__eea8b5a4d6cebf8529cc96708709289c5b4fcb530a4211ea2ed2bfd3d95b4827(
    *,
    description: builtins.str,
    role_arn: builtins.str,
    stop_conditions: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Sequence[typing.Union[typing.Union[CfnExperimentTemplate.ExperimentTemplateStopConditionProperty, typing.Dict[builtins.str, typing.Any]], _aws_cdk_core_f4b25747.IResolvable]]],
    tags: typing.Mapping[builtins.str, builtins.str],
    targets: typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateTargetProperty, typing.Dict[builtins.str, typing.Any]]]]],
    actions: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Mapping[builtins.str, typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateActionProperty, typing.Dict[builtins.str, typing.Any]]]]]] = None,
    log_configuration: typing.Optional[typing.Union[_aws_cdk_core_f4b25747.IResolvable, typing.Union[CfnExperimentTemplate.ExperimentTemplateLogConfigurationProperty, typing.Dict[builtins.str, typing.Any]]]] = None,
) -> None:
    """Type checking stubs"""
    pass
