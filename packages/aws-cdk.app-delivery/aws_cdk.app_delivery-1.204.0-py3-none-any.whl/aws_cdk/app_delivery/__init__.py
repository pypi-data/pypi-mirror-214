'''
# Continuous Integration / Continuous Delivery for CDK Applications

<!--BEGIN STABILITY BANNER-->---


![Deprecated](https://img.shields.io/badge/deprecated-critical.svg?style=for-the-badge)

> This API may emit warnings. Backward compatibility is not guaranteed.

---
<!--END STABILITY BANNER-->

This library includes a *CodePipeline* composite Action for deploying AWS CDK Applications.

This module is part of the [AWS Cloud Development Kit](https://github.com/aws/aws-cdk) project.

## Replacement recommended

This library has been deprecated. We recommend you use the
[@aws-cdk/pipelines](https://docs.aws.amazon.com/cdk/api/latest/docs/pipelines-readme.html) module instead.

## Limitations

The construct library in it's current form has the following limitations:

1. It can only deploy stacks that are hosted in the same AWS account and region as the *CodePipeline* is.
2. Stacks that make use of `Asset`s cannot be deployed successfully.

## Getting Started

In order to add the `PipelineDeployStackAction` to your *CodePipeline*, you need to have a *CodePipeline* artifact that
contains the result of invoking `cdk synth -o <dir>` on your *CDK App*. You can for example achieve this using a
*CodeBuild* project.

The example below defines a *CDK App* that contains 3 stacks:

* `CodePipelineStack` manages the *CodePipeline* resources, and self-updates before deploying any other stack
* `ServiceStackA` and `ServiceStackB` are service infrastructure stacks, and need to be deployed in this order

```plaintext
  ┏━━━━━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━━━━┓  ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
  ┃     Source     ┃  ┃     Build      ┃  ┃  Self-Update    ┃  ┃             Deploy              ┃
  ┃                ┃  ┃                ┃  ┃                 ┃  ┃                                 ┃
  ┃ ┌────────────┐ ┃  ┃ ┌────────────┐ ┃  ┃ ┌─────────────┐ ┃  ┃ ┌─────────────┐ ┌─────────────┐ ┃
  ┃ │   GitHub   ┣━╋━━╋━▶ CodeBuild  ┣━╋━━╋━▶Deploy Stack ┣━╋━━╋━▶Deploy Stack ┣━▶Deploy Stack │ ┃
  ┃ │            │ ┃  ┃ │            │ ┃  ┃ │PipelineStack│ ┃  ┃ │ServiceStackA│ │ServiceStackB│ ┃
  ┃ └────────────┘ ┃  ┃ └────────────┘ ┃  ┃ └─────────────┘ ┃  ┃ └─────────────┘ └─────────────┘ ┃
  ┗━━━━━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━━━━┛  ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

### `index.ts`

```python
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
import aws_cdk.core as cdk
import aws_cdk.app_delivery as cicd
import aws_cdk.aws_iam as iam

class MyServiceStackA(cdk.Stack):
    pass
class MyServiceStackB(cdk.Stack):
    pass

app = cdk.App()

# We define a stack that contains the CodePipeline
pipeline_stack = cdk.Stack(app, "PipelineStack")
pipeline = codepipeline.Pipeline(pipeline_stack, "CodePipeline",
    # Mutating a CodePipeline can cause the currently propagating state to be
    # "lost". Ensure we re-run the latest change through the pipeline after it's
    # been mutated so we're sure the latest state is fully deployed through.
    restart_execution_on_update=True
)

# Configure the CodePipeline source - where your CDK App's source code is hosted
source_output = codepipeline.Artifact()
source = codepipeline_actions.GitHubSourceAction(
    action_name="GitHub",
    output=source_output,
    owner="myName",
    repo="myRepo",
    oauth_token=cdk.SecretValue.unsafe_plain_text("secret")
)
pipeline.add_stage(
    stage_name="source",
    actions=[source]
)

project = codebuild.PipelineProject(pipeline_stack, "CodeBuild")
synthesized_app = codepipeline.Artifact()
build_action = codepipeline_actions.CodeBuildAction(
    action_name="CodeBuild",
    project=project,
    input=source_output,
    outputs=[synthesized_app]
)
pipeline.add_stage(
    stage_name="build",
    actions=[build_action]
)

# Optionally, self-update the pipeline stack
self_update_stage = pipeline.add_stage(stage_name="SelfUpdate")
self_update_stage.add_action(cicd.PipelineDeployStackAction(
    stack=pipeline_stack,
    input=synthesized_app,
    admin_permissions=True
))

# Now add our service stacks
deploy_stage = pipeline.add_stage(stage_name="Deploy")
service_stack_a = MyServiceStackA(app, "ServiceStackA")
# Add actions to deploy the stacks in the deploy stage:
deploy_service_aAction = cicd.PipelineDeployStackAction(
    stack=service_stack_a,
    input=synthesized_app,
    # See the note below for details about this option.
    admin_permissions=False
)
deploy_stage.add_action(deploy_service_aAction)
# Add the necessary permissions for you service deploy action. This role is
# is passed to CloudFormation and needs the permissions necessary to deploy
# stack. Alternatively you can enable [Administrator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_administrator) permissions above,
# users should understand the privileged nature of this role.
my_resource_arn = "arn:partition:service:region:account-id:resource-id"
deploy_service_aAction.add_to_deployment_role_policy(iam.PolicyStatement(
    actions=["service:SomeAction"],
    resources=[my_resource_arn]
))

service_stack_b = MyServiceStackB(app, "ServiceStackB")
deploy_stage.add_action(cicd.PipelineDeployStackAction(
    stack=service_stack_b,
    input=synthesized_app,
    create_change_set_run_order=998,
    admin_permissions=True
))
```

### `buildspec.yml`

The repository can contain a file at the root level named `buildspec.yml`, or
you can in-line the buildspec. Note that `buildspec.yaml` is not compatible.

For example, a *TypeScript* or *Javascript* CDK App can add the following `buildspec.yml`
at the root of the repository:

```yml
version: 0.2
phases:
  install:
    commands:
      # Installs the npm dependencies as defined by the `package.json` file
      # present in the root directory of the package
      # (`cdk init app --language=typescript` would have created one for you)
      - npm install
  build:
    commands:
      # Builds the CDK App so it can be synthesized
      - npm run build
      # Synthesizes the CDK App and puts the resulting artifacts into `dist`
      - npm run cdk synth -- -o dist
artifacts:
  # The output artifact is all the files in the `dist` directory
  base-directory: dist
  files: '**/*'
```

The `PipelineDeployStackAction` expects it's `input` to contain the result of
synthesizing a CDK App using the `cdk synth -o <directory>`.
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

import aws_cdk.aws_cloudformation as _aws_cdk_aws_cloudformation_6e482e6f
import aws_cdk.aws_codepipeline as _aws_cdk_aws_codepipeline_0063e444
import aws_cdk.aws_events as _aws_cdk_aws_events_efcdfa54
import aws_cdk.aws_iam as _aws_cdk_aws_iam_940a1ce0
import aws_cdk.aws_s3 as _aws_cdk_aws_s3_55f001a5
import aws_cdk.core as _aws_cdk_core_f4b25747


@jsii.implements(_aws_cdk_aws_codepipeline_0063e444.IAction)
class PipelineDeployStackAction(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/app-delivery.PipelineDeployStackAction",
):
    '''(deprecated) A class to deploy a stack that is part of a CDK App, using CodePipeline.

    This composite Action takes care of preparing and executing a CloudFormation ChangeSet.

    It currently does *not* support stacks that make use of ``Asset``s, and
    requires the deployed stack is in the same account and region where the
    CodePipeline is hosted.

    :stability: deprecated
    :exampleMetadata: infused

    Example::

        import aws_cdk.aws_codebuild as codebuild
        import aws_cdk.aws_codepipeline as codepipeline
        import aws_cdk.aws_codepipeline_actions as codepipeline_actions
        import aws_cdk.core as cdk
        import aws_cdk.app_delivery as cicd
        import aws_cdk.aws_iam as iam
        
        class MyServiceStackA(cdk.Stack):
            pass
        class MyServiceStackB(cdk.Stack):
            pass
        
        app = cdk.App()
        
        # We define a stack that contains the CodePipeline
        pipeline_stack = cdk.Stack(app, "PipelineStack")
        pipeline = codepipeline.Pipeline(pipeline_stack, "CodePipeline",
            # Mutating a CodePipeline can cause the currently propagating state to be
            # "lost". Ensure we re-run the latest change through the pipeline after it's
            # been mutated so we're sure the latest state is fully deployed through.
            restart_execution_on_update=True
        )
        
        # Configure the CodePipeline source - where your CDK App's source code is hosted
        source_output = codepipeline.Artifact()
        source = codepipeline_actions.GitHubSourceAction(
            action_name="GitHub",
            output=source_output,
            owner="myName",
            repo="myRepo",
            oauth_token=cdk.SecretValue.unsafe_plain_text("secret")
        )
        pipeline.add_stage(
            stage_name="source",
            actions=[source]
        )
        
        project = codebuild.PipelineProject(pipeline_stack, "CodeBuild")
        synthesized_app = codepipeline.Artifact()
        build_action = codepipeline_actions.CodeBuildAction(
            action_name="CodeBuild",
            project=project,
            input=source_output,
            outputs=[synthesized_app]
        )
        pipeline.add_stage(
            stage_name="build",
            actions=[build_action]
        )
        
        # Optionally, self-update the pipeline stack
        self_update_stage = pipeline.add_stage(stage_name="SelfUpdate")
        self_update_stage.add_action(cicd.PipelineDeployStackAction(
            stack=pipeline_stack,
            input=synthesized_app,
            admin_permissions=True
        ))
        
        # Now add our service stacks
        deploy_stage = pipeline.add_stage(stage_name="Deploy")
        service_stack_a = MyServiceStackA(app, "ServiceStackA")
        # Add actions to deploy the stacks in the deploy stage:
        deploy_service_aAction = cicd.PipelineDeployStackAction(
            stack=service_stack_a,
            input=synthesized_app,
            # See the note below for details about this option.
            admin_permissions=False
        )
        deploy_stage.add_action(deploy_service_aAction)
        # Add the necessary permissions for you service deploy action. This role is
        # is passed to CloudFormation and needs the permissions necessary to deploy
        # stack. Alternatively you can enable [Administrator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_administrator) permissions above,
        # users should understand the privileged nature of this role.
        my_resource_arn = "arn:partition:service:region:account-id:resource-id"
        deploy_service_aAction.add_to_deployment_role_policy(iam.PolicyStatement(
            actions=["service:SomeAction"],
            resources=[my_resource_arn]
        ))
        
        service_stack_b = MyServiceStackB(app, "ServiceStackB")
        deploy_stage.add_action(cicd.PipelineDeployStackAction(
            stack=service_stack_b,
            input=synthesized_app,
            create_change_set_run_order=998,
            admin_permissions=True
        ))
    '''

    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        input: _aws_cdk_aws_codepipeline_0063e444.Artifact,
        stack: _aws_cdk_core_f4b25747.Stack,
        capabilities: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudformation_6e482e6f.CloudFormationCapabilities]] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        create_change_set_action_name: typing.Optional[builtins.str] = None,
        create_change_set_run_order: typing.Optional[jsii.Number] = None,
        execute_change_set_action_name: typing.Optional[builtins.str] = None,
        execute_change_set_run_order: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param admin_permissions: (deprecated) Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: (deprecated) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: (deprecated) The CDK stack to be deployed.
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: (deprecated) The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: (deprecated) The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: (deprecated) The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: (deprecated) The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: (deprecated) The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: (deprecated) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: deprecated
        '''
        props = PipelineDeployStackActionProps(
            admin_permissions=admin_permissions,
            input=input,
            stack=stack,
            capabilities=capabilities,
            change_set_name=change_set_name,
            create_change_set_action_name=create_change_set_action_name,
            create_change_set_run_order=create_change_set_run_order,
            execute_change_set_action_name=execute_change_set_action_name,
            execute_change_set_run_order=execute_change_set_run_order,
            role=role,
        )

        jsii.create(self.__class__, self, [props])

    @jsii.member(jsii_name="addToDeploymentRolePolicy")
    def add_to_deployment_role_policy(
        self,
        statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
    ) -> None:
        '''(deprecated) Add policy statements to the role deploying the stack.

        This role is passed to CloudFormation and must have the IAM permissions
        necessary to deploy the stack or you can grant this role ``adminPermissions``
        by using that option during creation. If you do not grant
        ``adminPermissions`` you need to identify the proper statements to add to
        this role based on the CloudFormation Resources in your stack.

        :param statement: -

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__551c6548b8015c43ee6bc945fc69bce7f6b5c1044d362d3d6c49904ca23c689c)
            check_type(argname="argument statement", value=statement, expected_type=type_hints["statement"])
        return typing.cast(None, jsii.invoke(self, "addToDeploymentRolePolicy", [statement]))

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        scope: _aws_cdk_core_f4b25747.Construct,
        stage: _aws_cdk_aws_codepipeline_0063e444.IStage,
        *,
        bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
        role: _aws_cdk_aws_iam_940a1ce0.IRole,
    ) -> _aws_cdk_aws_codepipeline_0063e444.ActionConfig:
        '''(deprecated) The callback invoked when this Action is added to a Pipeline.

        :param scope: -
        :param stage: -
        :param bucket: 
        :param role: 

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__a2bc0ce9e9abe819af4024e04338eb87c9b17f7f0aae3705e68980e8dda4ff9e)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = _aws_cdk_aws_codepipeline_0063e444.ActionBindOptions(
            bucket=bucket, role=role
        )

        return typing.cast(_aws_cdk_aws_codepipeline_0063e444.ActionConfig, jsii.invoke(self, "bind", [scope, stage, options]))

    @jsii.member(jsii_name="onStateChange")
    def on_state_change(
        self,
        name: builtins.str,
        target: typing.Optional[_aws_cdk_aws_events_efcdfa54.IRuleTarget] = None,
        *,
        description: typing.Optional[builtins.str] = None,
        enabled: typing.Optional[builtins.bool] = None,
        event_bus: typing.Optional[_aws_cdk_aws_events_efcdfa54.IEventBus] = None,
        event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_efcdfa54.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
        rule_name: typing.Optional[builtins.str] = None,
        schedule: typing.Optional[_aws_cdk_aws_events_efcdfa54.Schedule] = None,
        targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_efcdfa54.IRuleTarget]] = None,
    ) -> _aws_cdk_aws_events_efcdfa54.Rule:
        '''(deprecated) Creates an Event that will be triggered whenever the state of this Action changes.

        :param name: -
        :param target: -
        :param description: A description of the rule's purpose. Default: - No description.
        :param enabled: Indicates whether the rule is enabled. Default: true
        :param event_bus: The event bus to associate with this rule. Default: - The default event bus.
        :param event_pattern: Describes which events EventBridge routes to the specified target. These routed events are matched events. For more information, see Events and Event Patterns in the Amazon EventBridge User Guide. Default: - None.
        :param rule_name: A name for the rule. Default: - AWS CloudFormation generates a unique physical ID and uses that ID for the rule name. For more information, see Name Type.
        :param schedule: The schedule or rate (frequency) that determines when EventBridge runs the rule. For more information, see Schedule Expression Syntax for Rules in the Amazon EventBridge User Guide. Default: - None.
        :param targets: Targets to invoke when this rule matches an event. Input will be the full matched event. If you wish to specify custom target input, use ``addTarget(target[, inputOptions])``. Default: - No targets.

        :stability: deprecated
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__40d8fec746009ffcf86a8fb3903691ce859ed2719a6c414f7c9fd1991fb103f8)
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument target", value=target, expected_type=type_hints["target"])
        options = _aws_cdk_aws_events_efcdfa54.RuleProps(
            description=description,
            enabled=enabled,
            event_bus=event_bus,
            event_pattern=event_pattern,
            rule_name=rule_name,
            schedule=schedule,
            targets=targets,
        )

        return typing.cast(_aws_cdk_aws_events_efcdfa54.Rule, jsii.invoke(self, "onStateChange", [name, target, options]))

    @builtins.property
    @jsii.member(jsii_name="actionProperties")
    def action_properties(self) -> _aws_cdk_aws_codepipeline_0063e444.ActionProperties:
        '''(deprecated) The simple properties of the Action, like its Owner, name, etc.

        Note that this accessor will be called before the {@link bind} callback.

        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_codepipeline_0063e444.ActionProperties, jsii.get(self, "actionProperties"))

    @builtins.property
    @jsii.member(jsii_name="deploymentRole")
    def deployment_role(self) -> _aws_cdk_aws_iam_940a1ce0.IRole:
        '''
        :stability: deprecated
        '''
        return typing.cast(_aws_cdk_aws_iam_940a1ce0.IRole, jsii.get(self, "deploymentRole"))


@jsii.data_type(
    jsii_type="@aws-cdk/app-delivery.PipelineDeployStackActionProps",
    jsii_struct_bases=[],
    name_mapping={
        "admin_permissions": "adminPermissions",
        "input": "input",
        "stack": "stack",
        "capabilities": "capabilities",
        "change_set_name": "changeSetName",
        "create_change_set_action_name": "createChangeSetActionName",
        "create_change_set_run_order": "createChangeSetRunOrder",
        "execute_change_set_action_name": "executeChangeSetActionName",
        "execute_change_set_run_order": "executeChangeSetRunOrder",
        "role": "role",
    },
)
class PipelineDeployStackActionProps:
    def __init__(
        self,
        *,
        admin_permissions: builtins.bool,
        input: _aws_cdk_aws_codepipeline_0063e444.Artifact,
        stack: _aws_cdk_core_f4b25747.Stack,
        capabilities: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudformation_6e482e6f.CloudFormationCapabilities]] = None,
        change_set_name: typing.Optional[builtins.str] = None,
        create_change_set_action_name: typing.Optional[builtins.str] = None,
        create_change_set_run_order: typing.Optional[jsii.Number] = None,
        execute_change_set_action_name: typing.Optional[builtins.str] = None,
        execute_change_set_run_order: typing.Optional[jsii.Number] = None,
        role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
    ) -> None:
        '''
        :param admin_permissions: (deprecated) Whether to grant admin permissions to CloudFormation while deploying this template. Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you don't specify any alternatives. The default role that will be created for you will have admin (i.e., ``*``) permissions on all resources, and the deployment will have named IAM capabilities (i.e., able to create all IAM resources). This is a shorthand that you can use if you fully trust the templates that are deployed in this pipeline. If you want more fine-grained permissions, use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation deployment is allowed to do.
        :param input: (deprecated) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.
        :param stack: (deprecated) The CDK stack to be deployed.
        :param capabilities: (deprecated) Acknowledge certain changes made as part of deployment. For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation might create or update those resources. For example, you must specify AnonymousIAM if your stack template contains AWS Identity and Access Management (IAM) resources. For more information Default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true
        :param change_set_name: (deprecated) The name to use when creating a ChangeSet for the stack. Default: CDK-CodePipeline-ChangeSet
        :param create_change_set_action_name: (deprecated) The name of the CodePipeline action creating the ChangeSet. Default: 'ChangeSet'
        :param create_change_set_run_order: (deprecated) The runOrder for the CodePipeline action creating the ChangeSet. Default: 1
        :param execute_change_set_action_name: (deprecated) The name of the CodePipeline action creating the ChangeSet. Default: 'Execute'
        :param execute_change_set_run_order: (deprecated) The runOrder for the CodePipeline action executing the ChangeSet. Default: ``createChangeSetRunOrder + 1``
        :param role: (deprecated) IAM role to assume when deploying changes. If not specified, a fresh role is created. The role is created with zero permissions unless ``adminPermissions`` is true, in which case the role will have admin permissions. Default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: deprecated
        :exampleMetadata: infused

        Example::

            import aws_cdk.aws_codebuild as codebuild
            import aws_cdk.aws_codepipeline as codepipeline
            import aws_cdk.aws_codepipeline_actions as codepipeline_actions
            import aws_cdk.core as cdk
            import aws_cdk.app_delivery as cicd
            import aws_cdk.aws_iam as iam
            
            class MyServiceStackA(cdk.Stack):
                pass
            class MyServiceStackB(cdk.Stack):
                pass
            
            app = cdk.App()
            
            # We define a stack that contains the CodePipeline
            pipeline_stack = cdk.Stack(app, "PipelineStack")
            pipeline = codepipeline.Pipeline(pipeline_stack, "CodePipeline",
                # Mutating a CodePipeline can cause the currently propagating state to be
                # "lost". Ensure we re-run the latest change through the pipeline after it's
                # been mutated so we're sure the latest state is fully deployed through.
                restart_execution_on_update=True
            )
            
            # Configure the CodePipeline source - where your CDK App's source code is hosted
            source_output = codepipeline.Artifact()
            source = codepipeline_actions.GitHubSourceAction(
                action_name="GitHub",
                output=source_output,
                owner="myName",
                repo="myRepo",
                oauth_token=cdk.SecretValue.unsafe_plain_text("secret")
            )
            pipeline.add_stage(
                stage_name="source",
                actions=[source]
            )
            
            project = codebuild.PipelineProject(pipeline_stack, "CodeBuild")
            synthesized_app = codepipeline.Artifact()
            build_action = codepipeline_actions.CodeBuildAction(
                action_name="CodeBuild",
                project=project,
                input=source_output,
                outputs=[synthesized_app]
            )
            pipeline.add_stage(
                stage_name="build",
                actions=[build_action]
            )
            
            # Optionally, self-update the pipeline stack
            self_update_stage = pipeline.add_stage(stage_name="SelfUpdate")
            self_update_stage.add_action(cicd.PipelineDeployStackAction(
                stack=pipeline_stack,
                input=synthesized_app,
                admin_permissions=True
            ))
            
            # Now add our service stacks
            deploy_stage = pipeline.add_stage(stage_name="Deploy")
            service_stack_a = MyServiceStackA(app, "ServiceStackA")
            # Add actions to deploy the stacks in the deploy stage:
            deploy_service_aAction = cicd.PipelineDeployStackAction(
                stack=service_stack_a,
                input=synthesized_app,
                # See the note below for details about this option.
                admin_permissions=False
            )
            deploy_stage.add_action(deploy_service_aAction)
            # Add the necessary permissions for you service deploy action. This role is
            # is passed to CloudFormation and needs the permissions necessary to deploy
            # stack. Alternatively you can enable [Administrator](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_job-functions.html#jf_administrator) permissions above,
            # users should understand the privileged nature of this role.
            my_resource_arn = "arn:partition:service:region:account-id:resource-id"
            deploy_service_aAction.add_to_deployment_role_policy(iam.PolicyStatement(
                actions=["service:SomeAction"],
                resources=[my_resource_arn]
            ))
            
            service_stack_b = MyServiceStackB(app, "ServiceStackB")
            deploy_stage.add_action(cicd.PipelineDeployStackAction(
                stack=service_stack_b,
                input=synthesized_app,
                create_change_set_run_order=998,
                admin_permissions=True
            ))
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__c3b1fa10779593ce89fb572f766e71e388de454d1438b483dc820e6da700cd4f)
            check_type(argname="argument admin_permissions", value=admin_permissions, expected_type=type_hints["admin_permissions"])
            check_type(argname="argument input", value=input, expected_type=type_hints["input"])
            check_type(argname="argument stack", value=stack, expected_type=type_hints["stack"])
            check_type(argname="argument capabilities", value=capabilities, expected_type=type_hints["capabilities"])
            check_type(argname="argument change_set_name", value=change_set_name, expected_type=type_hints["change_set_name"])
            check_type(argname="argument create_change_set_action_name", value=create_change_set_action_name, expected_type=type_hints["create_change_set_action_name"])
            check_type(argname="argument create_change_set_run_order", value=create_change_set_run_order, expected_type=type_hints["create_change_set_run_order"])
            check_type(argname="argument execute_change_set_action_name", value=execute_change_set_action_name, expected_type=type_hints["execute_change_set_action_name"])
            check_type(argname="argument execute_change_set_run_order", value=execute_change_set_run_order, expected_type=type_hints["execute_change_set_run_order"])
            check_type(argname="argument role", value=role, expected_type=type_hints["role"])
        self._values: typing.Dict[builtins.str, typing.Any] = {
            "admin_permissions": admin_permissions,
            "input": input,
            "stack": stack,
        }
        if capabilities is not None:
            self._values["capabilities"] = capabilities
        if change_set_name is not None:
            self._values["change_set_name"] = change_set_name
        if create_change_set_action_name is not None:
            self._values["create_change_set_action_name"] = create_change_set_action_name
        if create_change_set_run_order is not None:
            self._values["create_change_set_run_order"] = create_change_set_run_order
        if execute_change_set_action_name is not None:
            self._values["execute_change_set_action_name"] = execute_change_set_action_name
        if execute_change_set_run_order is not None:
            self._values["execute_change_set_run_order"] = execute_change_set_run_order
        if role is not None:
            self._values["role"] = role

    @builtins.property
    def admin_permissions(self) -> builtins.bool:
        '''(deprecated) Whether to grant admin permissions to CloudFormation while deploying this template.

        Setting this to ``true`` affects the defaults for ``role`` and ``capabilities``, if you
        don't specify any alternatives.

        The default role that will be created for you will have admin (i.e., ``*``)
        permissions on all resources, and the deployment will have named IAM
        capabilities (i.e., able to create all IAM resources).

        This is a shorthand that you can use if you fully trust the templates that
        are deployed in this pipeline. If you want more fine-grained permissions,
        use ``addToRolePolicy`` and ``capabilities`` to control what the CloudFormation
        deployment is allowed to do.

        :stability: deprecated
        '''
        result = self._values.get("admin_permissions")
        assert result is not None, "Required property 'admin_permissions' is missing"
        return typing.cast(builtins.bool, result)

    @builtins.property
    def input(self) -> _aws_cdk_aws_codepipeline_0063e444.Artifact:
        '''(deprecated) The CodePipeline artifact that holds the synthesized app, which is the contents of the ``<directory>`` when running ``cdk synth -o <directory>``.

        :stability: deprecated
        '''
        result = self._values.get("input")
        assert result is not None, "Required property 'input' is missing"
        return typing.cast(_aws_cdk_aws_codepipeline_0063e444.Artifact, result)

    @builtins.property
    def stack(self) -> _aws_cdk_core_f4b25747.Stack:
        '''(deprecated) The CDK stack to be deployed.

        :stability: deprecated
        '''
        result = self._values.get("stack")
        assert result is not None, "Required property 'stack' is missing"
        return typing.cast(_aws_cdk_core_f4b25747.Stack, result)

    @builtins.property
    def capabilities(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_cloudformation_6e482e6f.CloudFormationCapabilities]]:
        '''(deprecated) Acknowledge certain changes made as part of deployment.

        For stacks that contain certain resources, explicit acknowledgement that AWS CloudFormation
        might create or update those resources. For example, you must specify AnonymousIAM if your
        stack template contains AWS Identity and Access Management (IAM) resources. For more
        information

        :default: [AnonymousIAM, AutoExpand], unless ``adminPermissions`` is true

        :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#using-iam-capabilities
        :stability: deprecated
        '''
        result = self._values.get("capabilities")
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_cloudformation_6e482e6f.CloudFormationCapabilities]], result)

    @builtins.property
    def change_set_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name to use when creating a ChangeSet for the stack.

        :default: CDK-CodePipeline-ChangeSet

        :stability: deprecated
        '''
        result = self._values.get("change_set_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_change_set_action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the CodePipeline action creating the ChangeSet.

        :default: 'ChangeSet'

        :stability: deprecated
        '''
        result = self._values.get("create_change_set_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def create_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The runOrder for the CodePipeline action creating the ChangeSet.

        :default: 1

        :stability: deprecated
        '''
        result = self._values.get("create_change_set_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def execute_change_set_action_name(self) -> typing.Optional[builtins.str]:
        '''(deprecated) The name of the CodePipeline action creating the ChangeSet.

        :default: 'Execute'

        :stability: deprecated
        '''
        result = self._values.get("execute_change_set_action_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def execute_change_set_run_order(self) -> typing.Optional[jsii.Number]:
        '''(deprecated) The runOrder for the CodePipeline action executing the ChangeSet.

        :default: ``createChangeSetRunOrder + 1``

        :stability: deprecated
        '''
        result = self._values.get("execute_change_set_run_order")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def role(self) -> typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole]:
        '''(deprecated) IAM role to assume when deploying changes.

        If not specified, a fresh role is created. The role is created with zero
        permissions unless ``adminPermissions`` is true, in which case the role will have
        admin permissions.

        :default: A fresh role with admin or no permissions (depending on the value of ``adminPermissions``).

        :stability: deprecated
        '''
        result = self._values.get("role")
        return typing.cast(typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PipelineDeployStackActionProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "PipelineDeployStackAction",
    "PipelineDeployStackActionProps",
]

publication.publish()

def _typecheckingstub__551c6548b8015c43ee6bc945fc69bce7f6b5c1044d362d3d6c49904ca23c689c(
    statement: _aws_cdk_aws_iam_940a1ce0.PolicyStatement,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__a2bc0ce9e9abe819af4024e04338eb87c9b17f7f0aae3705e68980e8dda4ff9e(
    scope: _aws_cdk_core_f4b25747.Construct,
    stage: _aws_cdk_aws_codepipeline_0063e444.IStage,
    *,
    bucket: _aws_cdk_aws_s3_55f001a5.IBucket,
    role: _aws_cdk_aws_iam_940a1ce0.IRole,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__40d8fec746009ffcf86a8fb3903691ce859ed2719a6c414f7c9fd1991fb103f8(
    name: builtins.str,
    target: typing.Optional[_aws_cdk_aws_events_efcdfa54.IRuleTarget] = None,
    *,
    description: typing.Optional[builtins.str] = None,
    enabled: typing.Optional[builtins.bool] = None,
    event_bus: typing.Optional[_aws_cdk_aws_events_efcdfa54.IEventBus] = None,
    event_pattern: typing.Optional[typing.Union[_aws_cdk_aws_events_efcdfa54.EventPattern, typing.Dict[builtins.str, typing.Any]]] = None,
    rule_name: typing.Optional[builtins.str] = None,
    schedule: typing.Optional[_aws_cdk_aws_events_efcdfa54.Schedule] = None,
    targets: typing.Optional[typing.Sequence[_aws_cdk_aws_events_efcdfa54.IRuleTarget]] = None,
) -> None:
    """Type checking stubs"""
    pass

def _typecheckingstub__c3b1fa10779593ce89fb572f766e71e388de454d1438b483dc820e6da700cd4f(
    *,
    admin_permissions: builtins.bool,
    input: _aws_cdk_aws_codepipeline_0063e444.Artifact,
    stack: _aws_cdk_core_f4b25747.Stack,
    capabilities: typing.Optional[typing.Sequence[_aws_cdk_aws_cloudformation_6e482e6f.CloudFormationCapabilities]] = None,
    change_set_name: typing.Optional[builtins.str] = None,
    create_change_set_action_name: typing.Optional[builtins.str] = None,
    create_change_set_run_order: typing.Optional[jsii.Number] = None,
    execute_change_set_action_name: typing.Optional[builtins.str] = None,
    execute_change_set_run_order: typing.Optional[jsii.Number] = None,
    role: typing.Optional[_aws_cdk_aws_iam_940a1ce0.IRole] = None,
) -> None:
    """Type checking stubs"""
    pass
