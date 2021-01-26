from aws_cdk import (core, aws_codebuild as codebuild,
                     aws_codecommit as codecommit,
                     aws_codepipeline as codepipeline,
                     aws_codepipeline_actions as codepipeline_actions,
                     aws_lambda as lambda_)


class PipelineStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, *, repo_name: str = None,
                 lambda_code: lambda_.CfnParametersCode = None, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Creating repository object now from the repository we have created through console (repo_name)
        code = codecommit.Repository.from_repository_name(self, "UnitConversionCodeCommitRepo",
                                                          repo_name)

        # Creating CodeBuild project for Lambda/Apigateway infrastructure build now
        cdk_build = codebuild.PipelineProject(self, "UnitConversionCdkBuild",
                                              build_spec=codebuild.BuildSpec.from_source_filename('cdkbuildspec.yml'))

        # Creating CodeBuild project for Lambda/Apigateway application build now
        lambda_build = codebuild.PipelineProject(self, 'UnitConversionLambdaBuild',
                                                 build_spec=codebuild.BuildSpec.from_source_filename('lambdabuildspec'
                                                                                                     '.yml'))

        # Providing Artifacts locations for pipeline's source and build output's
        source_output = codepipeline.Artifact()
        cdk_build_output = codepipeline.Artifact("UnitConversionCdkBuildOutput")
        lambda_build_output = codepipeline.Artifact("UnitConversionLambdaBuildOutput")

        # Reading s3 location from lambda function build artifact to provide in Deploy stage of pipeline
        lambda_location = lambda_build_output.s3_location

        # Creating pipeline now with stages for CodeCommit, CodeBuild's and Deploy actions
        codepipeline.Pipeline(self, "UnitConversionPipeline",
                              stages=[
                                  codepipeline.StageProps(stage_name="Source",
                                                          actions=[
                                                              codepipeline_actions.CodeCommitSourceAction(
                                                                  action_name="CodeCommit_Source",
                                                                  repository=code,
                                                                  output=source_output)]),
                                  codepipeline.StageProps(stage_name="Build",
                                                          actions=[
                                                              codepipeline_actions.CodeBuildAction(
                                                                  action_name="Lambda_Build",
                                                                  project=lambda_build,
                                                                  input=source_output,
                                                                  outputs=[lambda_build_output]),
                                                              codepipeline_actions.CodeBuildAction(
                                                                  action_name="CDK_Build",
                                                                  project=cdk_build,
                                                                  input=source_output,
                                                                  outputs=[cdk_build_output])]),
                                  codepipeline.StageProps(stage_name="Deploy",
                                                          actions=[
                                                              codepipeline_actions.CloudFormationCreateUpdateStackAction(
                                                                  action_name="Lambda_CFN_Deploy",
                                                                  template_path=cdk_build_output.at_path(
                                                                      "LambdaStack.template.json"),
                                                                  stack_name="UnitConversionLambdaDeploymentStack",
                                                                  admin_permissions=True,
                                                                  parameter_overrides=dict(
                                                                      lambda_code.assign(
                                                                          bucket_name=lambda_location.bucket_name,
                                                                          object_key=lambda_location.object_key,
                                                                          object_version=lambda_location.object_version)),
                                                                  extra_inputs=[lambda_build_output])])
                              ]
                              )
