import os

from aws_cdk import Environment

class DevEnv:
    def __init__(self):
        self.env_name = "dev"
        self.project_name = "gotik"
        self.vpc_cidr = "11.11.0.0/16"
        self.vpc_max_azs = 2
        self.vpc_nat_gateways = 0
        self.eureka_image = "eureka-server:latest"
        self.eureka_cpu = "256"
        self.eureka_memory = "512"
        self.eureka_desired_count = 0
        self.eureka_container_env = {
            "SPRING_PROFILES_ACTIVE": self.env_name
        }
        self.gateway_image = "api-gateway:latest"
        self.gateway_cpu = "256"
        self.gateway_memory = "512"
        self.gateway_desired_count = 0
        self.gateway_container_env = {
            "SPRING_PROFILES_ACTIVE": self.env_name
        }