import aws_cdk as core
import aws_cdk.assertions as assertions

# example test. To run these test, uncomment this file along with the example
# resource in stack/microservies_infra_cdk_stack.py
def test_sqs_queue_created():
    app = core.App()