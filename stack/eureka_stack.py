from aws_cdk import Stack
from constructs import Construct
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs

from construct.ecs_service import CustomEcsServiceConstruct


class EurekaStack(Stack):
    def __init__(self, scope: Construct, id: str, env_config, cluster: ecs.Cluster, **kwargs):
        super().__init__(scope, id, **kwargs)
        
        # Security Group for Eureka
        self.eureka_security_group = ec2.SecurityGroup(
            self, "EurekaSecurityGroup",
            vpc=cluster.vpc,
            security_group_name=f"{env_config.env_name}-{env_config.project_name}-eureka-sg",
            description="Allow traffic to Eureka on port 8761",
            allow_all_outbound=True
        )

        # Add ingress rule to Eureka Security Group
        self.eureka_security_group.add_ingress_rule(
            peer=self.eureka_security_group,
            connection=ec2.Port.tcp(8761),
            description="Allow Eureka to communicate with itself"
        )

        # ECS Service for Eureka
        self.eureka_service = CustomEcsServiceConstruct(
            self, "EurekaService",
            service_name=f"{env_config.env_name}-{env_config.project_name}-eureka-service",
            cluster=cluster,
            image=env_config.eureka_image,
            cpu=env_config.eureka_cpu,
            memory=env_config.eureka_memory,
            desired_count=env_config.eureka_desired_count,
            security_group=self.eureka_security_group,
            subnet_selection=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS),
            container_env=env_config.eureka_container_env
        )