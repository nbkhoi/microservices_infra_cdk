import os

from aws_cdk import Environment

class ProdEnv:
    def __init__(self):
        self.env_name = "prod"
        self.project_name = "gotik"
        self.vpc_cidr = "10.0.0.0/16"
        self.vpc_max_azs = 2
        self.vpc_nat_gateways = 0
        self.eureka_image = "eureka:latest"
        self.eureka_cpu = "256"
        self.eureka_memory = "512"
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