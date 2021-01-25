
# UnitsConversion Validation project!

## About
Application is to Validate Unit Conversions and return correct/incorrect/invalid response in json format based on the input params. Input is passed as Querystring parameters.
[Note: supports units Fahrenheit, Celsius and Kelvin]
- Both Application and Application Infrastructure code is written in Python.

## Prerequisites
Install
 - Python (Python 3.6 or later including pip and virtualenv)
 - AWS CLI (https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html)
 - Nodejs (Node.js 10.3.0 or later (Note: not 13.0.0 through 13.6.0)),
 - aws-cdk
 ```
 npm install -g aws-cdk

 ```
- Create IAM user and configure using awscli as a default profile or with a named profile, attach proper devops policy's or attach Administrator policy for now)
```
You can follow document to configure 'IAM user for accessing CodeCommit'
https://docs.aws.amazon.com/codecommit/latest/userguide/setting-up-gc.html?icmpid=docs_acc_console_connect
```

## Steps to set up the environment and deploy Application and Application infrastructure
- Go to AWS console and create a CodeCommit project with name 'UnitsConversion' in region 'us-east-2' (Note: us-east-2 region has been hard coded in cdk project so please use the same).
- Get 'clone url' from CodeCommit/UnitsConversion project and keep
- In terminal window cd to an intended project directory and Clone repository from location, https://github.com/SKCodeGen/UnitsConversion.git
```
git clone https://github.com/SKCodeGen/UnitsConversion.git
```
- Change the git remote url to the CodeCommit/UnitsConversion project to below, replacing '{git-user}' and '{git-password}' with your IAM user git credentials created from the step in Prerequisites
```
git remote set-url origin https://{git-user}:{git-password}git-codecommit.us-east-2.amazonaws.com/v1/repos/UnitsConversion
```
- Do git push to push code to CodeCommit/UnitsConversion project
```
git push
```
- Deploy 'PipelineDeployingLambdaStack' to deploy infrastructure for 'pipeline' to build 'lambda code' and 'lambda/apigateway infrastructure code'. Replace {profile-name} with your programmatic user profile or '--profile' tag when using default profile
```
cdk deploy PipelineDeployingLambdaStack --profile {profile-name}
```
- Above command would create apigateway url to call the service, use url with 'units' path and proper querystring parameters. Replace '{UUIDByAPIGateway}' below with the UUID created for your apigateway url
```
Example for 'incorrect' response
https://{UUIDByAPIGateway}.execute-api.us-east-2.amazonaws.com/prod/units?source_unit=Kelvin&source_value=84.2&target_unit=Celsius&target_value=112.70
Example for 'correct' response
https://{UUIDByAPIGateway}.execute-api.us-east-2.amazonaws.com/prod/units?source_unit=Kelvin&source_value=84.2&target_unit=Celsius&target_value=-188.95
Example for 'invalid' response
https://{UUIDByAPIGateway}.execute-api.us-east-2.amazonaws.com/prod/units?source_unit=Kelvin&source_value=Kelvin&target_unit=Celsius&target_value=-188.95
```

## For doing modifications in local and commit code
- Execute below commands to set up local env. Make sure you are in Project directory
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements-cdk.txt
```
- Do modifications as required and commit changes. Every commit triggers 'code pipeline' deploy
```
git add .
git commit -m "modifications"
git push
```
- In case of recreating the all the infrastructure, execute below commands. Replace {profile-name} with your programmatic user profile or '--profile' tag when using default profile
```
cdk destroy PipelineDeployingLambdaStack --profile {profile-name}
cdk deploy PipelineDeployingLambdaStack --profile {profile-name}
```
- Execute below if just to see diff after modifications
```
cdk diff PipelineDeployingLambdaStack --profile {profile-name}
```
Execute below if just to synthesize the cloud formation template
```
cdk synth PipelineDeployingLambdaStack --profile {profile-name}
```

## Backlog

	Application:
		- query parameters validation
		- improve unit tests coverage
		- specific error handling
		- enhance to support other units too, not it supports only Fahrenheit, Celsius and Kelvin

	IaC:
		- Lambda should be deployed inside VPC
		- Specific 'Service Roles' were not required so not created, but practice is to create one
		- API gateway has been implemented with most default’s
		- region, code repo name, environment name, etc. values parameterization is not done
		```
