import datetime

from aws_cdk import (
    core,
    aws_lambda as lambda_,
    aws_apigateway as apigateway
)


class LambdaStack(core.Stack):
    def __init__(self, app: core.App, id: str, **kwargs):
        super().__init__(app, id, **kwargs)

        self.lambda_code = lambda_.Code.from_cfn_parameters()

        # Configuring for Lambda function creation now
        lambda_function_handler = lambda_.Function(self, "UnitsValidationLambda",
                                                   code=self.lambda_code,
                                                   handler="lambda_function.lambda_handler",
                                                   runtime=lambda_.Runtime.PYTHON_3_8,
                                                   description="Function generated on {}".format(
                                                       datetime.datetime.now()),
                                                   )

        # Configuring api using API gateway for Lambda function now
        api = apigateway.LambdaRestApi(
            self, 'UnitsValidationEndpoint',
            handler=lambda_function_handler,
            proxy=False
        )

        # Attaching resource 'units' to api now
        units = api.root.add_resource("units")
        # Attaching 'GET' method to 'units' resource now
        units.add_method("GET")



