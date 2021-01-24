import json
import pytest

from aws_cdk import core
from cdkiac.lambda_stack import LambdaStack


def get_template():
    app = core.App()
    LambdaStack(app, "lambdastack")
    return json.dumps(app.synth().get_stack("lambdastack").template)


def test_sqs_queue_created():
    assert("AWS::SQS::Queue" in get_template())


def test_sns_topic_created():
    assert("AWS::SNS::Topic" in get_template())
