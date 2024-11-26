from constructs import Construct
from aws_cdk import aws_iam as iam
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_logs as logs

class CustomEcsServiceConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            id: str,
            cluster: ecs.Cluster,
            image: str,
            cpu: str,
            memory: str,
            security_group: ec2.SecurityGroup = None,
            subnet_selection: ec2.SubnetSelection = None,
            desired_count: int = None,
            container_env: dict = None,
            service_name: str = None,
            **kwargs
    ):
        super().__init__(scope, id, **kwargs)

        # Retrieve keywork arguments or set default values
        container_env = container_env or {}
        desired_count = desired_count if desired_count is not None else 2
        # ECS Task Role
        task_role = iam.Role(
            self, "EcsTaskRole",
            assumed_by=iam.ServicePrincipal("ecs-tasks.amazonaws.com")
        )
        # Add default and custom permissions
        task_role.add_managed_policy(
            iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AmazonECSTaskExecutionRolePolicy")
        )

        # ECS Task Definition
        task_definition = ecs.TaskDefinition(
            self, "TaskDef",
            compatibility=ecs.Compatibility.FARGATE,
            cpu=cpu,
            memory_mib=memory,
            task_role=task_role
        )

        # Add container to task definition
        container = task_definition.add_container(
            "Container",
            image=ecs.ContainerImage.from_registry(image),
            environment=container_env,
            logging=ecs.LogDriver.aws_logs(
                stream_prefix=service_name or self.node.default_child.logical_id,
                log_group=logs.LogGroup(self, "LogGroup")
            )
        )
        container.add_port_mappings(ecs.PortMapping(container_port=80))

        # ECS Service
        self.service = ecs.FargateService(
            self, "Service",
            service_name=service_name or self.node.default_child.logical_id,
            cluster=cluster,
            task_definition=task_definition,
            security_groups=[security_group],
            desired_count=desired_count,
            vpc_subnets=subnet_selection
        )