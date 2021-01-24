#!/usr/bin/env python3

from aws_cdk import core
from cdkiac.pipeline_stack import PipelineStack
from cdkiac.lambda_stack import LambdaStack


CODECOMMIT_REPO_NAME = "UnitsConversion"

app = core.App()

lambda_stack = LambdaStack(app, "LambdaStack", env={'region': 'us-east-2'})

PipelineStack(app, "PipelineDeployingLambdaStack",
              lambda_code=lambda_stack.lambda_code,
              repo_name=CODECOMMIT_REPO_NAME, env={'region': 'us-east-2'})

app.synth()
