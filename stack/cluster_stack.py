from aws_cdk import Stack, Tags
from aws_cdk.aws_ec2 import Vpc
from aws_cdk.aws_ecs import Cluster
from constructs import Construct


class SharedClusterStack(Stack):
    def __init__(self, scope: Construct, id: str, env_config, vpc: Vpc, **kwargs):
        super().__init__(scope, id, **kwargs)

        # ECS Cluster
        self.cluster = Cluster(
            self, "SharedCluster",
            vpc=vpc,
            cluster_name=f"{env_config.env_name}-{env_config.project_name}-cluster"
        )

        # Add tags to the cluster
        Tags.of(self.cluster).add("env", env_config.env_name)
        Tags.of(self.cluster).add("project", env_config.project_name)
        Tags.of(self.cluster).add("name", f"{env_config.env_name}-{env_config.project_name}-cluster")