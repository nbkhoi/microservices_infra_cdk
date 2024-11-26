from aws_cdk import Stack, Tags
from aws_cdk import aws_ec2 as ec2
from constructs import Construct
class NetworkStack(Stack):
    def __init__(self, scope: Construct, id: str, env_config, **kwargs):
        super().__init__(scope, id, **kwargs)

        self.vpc = ec2.Vpc(
            self, "VPC",
            ip_addresses=ec2.IpAddresses.cidr(env_config.vpc_cidr),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="Public",
                    subnet_type=ec2.SubnetType.PUBLIC,
                    cidr_mask=24,
                    reserved=False
                ),
                ec2.SubnetConfiguration(
                    name="Private",
                    subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS,
                    cidr_mask=24,
                    reserved=False
                ),
            ],
            max_azs=env_config.vpc_max_azs,
            nat_gateways=env_config.vpc_nat_gateways
        )
        
        # Security Group for Eureka
        self.eureka_security_group = ec2.SecurityGroup(
            self, "EurekaSecurityGroup",
            vpc=self.vpc,
            security_group_name=f"{env_config.env_name}-{env_config.project_name}-eureka-sg",
            description="Allow traffic to Eureka on port 8761",
            allow_all_outbound=True
        )
        
        # Security Group for API Gateway
        self.gateway_security_group = ec2.SecurityGroup(
            self, "GatewaySecurityGroup",
            vpc=self.vpc,
            security_group_name=f"{env_config.env_name}-{env_config.project_name}-gateway-sg",
            description="Allow traffic to Gateway on port 8080",
            allow_all_outbound=True
        )
        
        # Security Group for Application Load Balancer
        self.alb_security_group = ec2.SecurityGroup(
            self, "AlbSecurityGroup",
            vpc=self.vpc,
            security_group_name=f"{env_config.env_name}-{env_config.project_name}-alb-sg",
            description="Allow traffic to ALB on port 80",
            allow_all_outbound=True
        )
        
        # Security Group for Microservices
        self.microservices_security_group = ec2.SecurityGroup(
            self, "MicroservicesSecurityGroup",
            vpc=self.vpc,
            security_group_name=f"{env_config.env_name}-{env_config.project_name}-microservices-sg",
            description="Allow traffic to Microservices on port 8080",
            allow_all_outbound=True
        )
        
        # Add Ingress rules to Security Groups
        # Allow Eureka to communicate with itself
        self.eureka_security_group.add_ingress_rule(
            peer=self.eureka_security_group,
            connection=ec2.Port.tcp(8761),
            description="Allow Eureka to communicate with itself on port 8761"
        )
        # Allow Gateway to communicate with itself
        self.gateway_security_group.add_ingress_rule(
            peer=self.gateway_security_group,
            connection=ec2.Port.tcp(8080),
            description="Allow Gateway to communicate with itself on port 8080"
        )
        # Allow Internet to communicate with ALB on port 80
        self.alb_security_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80),
            description="Allow Internet to communicate with ALB on port 80"
        )
        # Allow Microservices to communicate with itself
        self.microservices_security_group.add_ingress_rule(
            peer=self.microservices_security_group,
            connection=ec2.Port.tcp(8080),
            description="Allow Microservices to communicate with itself on port 8080"
        )

        # Add a tag to specify the VPC name
        Tags.of(self.vpc).add("env", env_config.env_name)
        Tags.of(self.vpc).add("project", env_config.project_name)
        Tags.of(self.vpc).add("Name", f"{env_config.env_name}-{env_config.project_name}-vpc")
        # Add tags to each subnet
        for index, subnet in enumerate(self.vpc.public_subnets, start=1):
            Tags.of(self.vpc).add("env", env_config.env_name)
            Tags.of(self.vpc).add("project", env_config.project_name)
            Tags.of(subnet).add("Name", f"{env_config.env_name}-{env_config.project_name}-public-subnet-{index}")
        for index, subnet in enumerate(self.vpc.private_subnets, start=1):
            Tags.of(self.vpc).add("env", env_config.env_name)
            Tags.of(self.vpc).add("project", env_config.project_name)
            Tags.of(subnet).add("Name", f"{env_config.env_name}-{env_config.project_name}-private-subnet-{index}")
        # Add tags to NAT Gateways
        for index, nat_gateway in enumerate(self.vpc.node.find_all(), start=1):
            if isinstance(nat_gateway, ec2.CfnNatGateway):
                Tags.of(self.vpc).add("env", env_config.env_name)
                Tags.of(self.vpc).add("project", env_config.project_name)
                Tags.of(nat_gateway).add("Name", f"{env_config.env_name}-{env_config.project_name}-nat-gateway-{index}")
