#!/usr/bin/env python3
import os

import aws_cdk as cdk
import aws_cdk.aws_ec2 as ec2
from environment.dev_env import DevEnv
from environment.prod_env import ProdEnv
from environment.staging_env import StagingEnv
from stack.network_stack import NetworkStack
from stack.cluster_stack import SharedClusterStack
from stack.eureka_stack import EurekaStack
from stack.gateway_stack import GatewayStack

app = cdk.App()
environment = app.node.try_get_context("env") or "dev"
env_config = {
    "dev": DevEnv,
    "staging": StagingEnv,
    "prod": ProdEnv
}[environment]()
network_stack = NetworkStack(app, f"{ env_config.env_name.capitalize() }{ env_config.project_name.capitalize() }NetworkStack", env_config=env_config)
cluster_stack = SharedClusterStack(app, f"{ env_config.env_name.capitalize() }{ env_config.project_name.capitalize() }ClusterStack", env_config=env_config, vpc=network_stack.vpc)
eureka_security_groups = [network_stack.eureka_security_group]
gateway_security_groups = [network_stack.gateway_security_group, network_stack.microservices_security_group]
eureka_stack = EurekaStack(app, f"{ env_config.env_name.capitalize() }{ env_config.project_name.capitalize() }EurekaStack", env_config=env_config, cluster=cluster_stack.cluster, security_groups=eureka_security_groups)
gateway_stack = GatewayStack(app, f"{ env_config.env_name.capitalize() }{ env_config.project_name.capitalize() }GatewayStack", env_config=env_config, cluster=cluster_stack.cluster, security_groups=gateway_security_groups)

app.synth()
