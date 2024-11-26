from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from construct.ecs_service import CustomEcsServiceConstruct

class GatewayStack(Stack):
    def __init__(self, scope: Construct, id: str, env_config, cluster: ecs.Cluster, security_groups: list[ec2.SecurityGroup], **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # ECS Service for API Gateway
        self.gateway_service = CustomEcsServiceConstruct(
            self, "GatewayService",
            service_name=f"{env_config.env_name}-{env_config.project_name}-gateway-service",
            cluster=cluster,
            image=env_config.gateway_image,
            cpu=env_config.gateway_cpu,
            memory=env_config.gateway_memory,
            desired_count=env_config.gateway_desired_count,
            security_groups=security_groups,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            container_env=env_config.gateway_container_env
        )
