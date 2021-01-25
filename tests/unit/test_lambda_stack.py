import json

from aws_cdk import core
from cdkiac.lambda_stack import LambdaStack


def get_template():
    app = core.App()
    LambdaStack(app, "lambdastack")
    return json.dumps(app.synth().get_stack("lambdastack").template)


def test_lambda_function_created():
    assert("AWS::Lambda::Function" in get_template())


def test_sns_topic_created():
    assert("AWS::ApiGateway::RestApi" in get_template())
