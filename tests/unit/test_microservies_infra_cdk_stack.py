import aws_cdk as core
import aws_cdk.assertions as assertions

from microservies_infra_cdk.microservies_infra_cdk_stack import MicroserviesInfraCdkStack

# example tests. To run these tests, uncomment this file along with the example
# resource in microservies_infra_cdk/microservies_infra_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = MicroserviesInfraCdkStack(app, "microservies-infra-cdk")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
