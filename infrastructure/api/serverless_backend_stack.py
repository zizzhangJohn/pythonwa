from aws_cdk import (
    Stack,
    CfnParameter as cfnParameter,
    aws_cognito,
    aws_s3,
    aws_dynamodb,
    aws_lambda,
    aws_apigateway,
    RemovalPolicy,
    aws_iam,
    aws_route53,
    aws_route53_targets,
    aws_certificatemanager,
)
from constructs import Construct
from pathlib import Path

THIS_DIR = Path(__file__).resolve().parent
LAMBDA_DIR = THIS_DIR.parent.parent / "apis"
LAMBDA_LAYERS_DIR = THIS_DIR.parent / "lambda_layers"


class ServerlessBackendStack(Stack):
    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        domain_certificate_arn: str = None,
        hosted_zone_name: str = None,
        hosted_zone_id: str = None,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        requests_pydantic_layer = aws_lambda.LayerVersion(
            self,
            "requests_pydantic_layer",
            code=aws_lambda.Code.from_asset(
                str(LAMBDA_LAYERS_DIR / "layer_requests_pydantic.zip")
            ),
            description="Requests and Pydantic",
            compatible_runtimes=[aws_lambda.Runtime.PYTHON_3_9],
            removal_policy=RemovalPolicy.DESTROY,
        )

        pythonwa_slack_invite_lambda = aws_lambda.Function(
            self,
            id="lambdafunction",
            function_name="pythonwa_slack_invite_lambda",
            description="PythonWA Slack Invite API handler",
            runtime=aws_lambda.Runtime.PYTHON_3_9,
            handler="lambda_handler.handler",
            code=aws_lambda.Code.from_asset(str(LAMBDA_DIR / "slack_invite")),
            environment={
                "key": "value",
            },
            layers=[requests_pydantic_layer],
        )

        lambda_allow_ssm_policy = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            actions=["ssm:GetParameters", "ssm:GetParameter"],
            resources=["*"],
        )
        pythonwa_slack_invite_lambda.add_to_role_policy(lambda_allow_ssm_policy)

        certificate = aws_certificatemanager.Certificate.from_certificate_arn(
            self,
            "site_certificate",
            certificate_arn=domain_certificate_arn,
        )

        domain_name_options = aws_apigateway.DomainNameOptions(
            domain_name="api.pythonwa.com",
            certificate=certificate,
            security_policy=aws_apigateway.SecurityPolicy.TLS_1_2,
            endpoint_type=aws_apigateway.EndpointType.EDGE,
        )

        pythonwa_api = aws_apigateway.LambdaRestApi(
            self,
            id="lambdaapi",
            rest_api_name="pythonwa_api",
            handler=pythonwa_slack_invite_lambda,
            proxy=True,
            domain_name=domain_name_options,
        )
        post_data = pythonwa_api.root.add_resource("form")
        post_data.add_method("POST")  # POST images/files & metadata

        hosted_zone = aws_route53.HostedZone.from_hosted_zone_attributes(
            self,
            "hosted_zone",
            zone_name=hosted_zone_name,
            hosted_zone_id=hosted_zone_id,
        )

        aws_route53.ARecord(
            self,
            "ApiRecord",
            record_name="api",
            zone=hosted_zone,
            target=aws_route53.RecordTarget.from_alias(aws_route53_targets.ApiGateway(pythonwa_api)),
        )
