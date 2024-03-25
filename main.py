from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance
from cdktf_cdktf_provider_aws.security_group import SecurityGroup
from cdktf_cdktf_provider_aws.vpc import Vpc
from cdktf_cdktf_provider_aws.subnet import Subnet  # Import the Subnet class

class WebsiteStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        # Define the AWS provider
        AwsProvider(self, 'aws', region='us-west-2')

        # Define the VPC
        vpc = Vpc(self, 'MyVpc',
                  cidr_block='10.0.0.0/16',
                  enable_dns_support=True,
                  enable_dns_hostnames=True)

        # Define the public subnet
        subnet = Subnet(self, 'PublicSubnet',
                        vpc_id=vpc.id,
                        cidr_block='10.0.1.0/24')  # Adjust the CIDR block as needed

        # Define the Security Group without ingress and egress rules
       # Define the Security Group with specific ingress and egress rules
security_group = SecurityGroup(self, 'WebServerSecurityGroup',
                               vpc_id=vpc.id,
                               ingress=[{
                                   'from_port': 80,
                                   'to_port': 80,
                                   'protocol': 'tcp',
                                   'cidr_blocks': ['0.0.0.0/0']
                               }, {
                                   'from_port': 443,
                                   'to_port': 443,
                                   'protocol': 'tcp',
                                   'cidr_blocks': ['0.0.0.0/0']
                               }],
                               egress=[{
                                   'from_port': 0,
                                   'to_port': 0,
                                   'protocol': '-1',
                                   'cidr_blocks': ['0.0.0.0/0']
                               }])

        # Define the EC2 instance
        instance = Instance(self, 'WebServer',
                            ami='ami-0a911ace2794b9c40',  # Use the ID of the Amazon Linux 2023 AMI (64-bit, Arm)
                            instance_type='t4g.micro',  # Use an instance type compatible with the arm64 architecture
                            tags={'Name': 'WebServer'},
                            user_data="""
                            #!/bin/bash
                            sudo yum update -y
                            sudo yum install httpd -y
                            sudo service httpd start
                            echo "<h1>Welcome to my website!</h1>" > /var/www/html/index.html
                            """,
                            security_groups=[security_group.id],
                            subnet_id=subnet.id)  # Use the ID of the subnet you created

        # Output the public IP of the instance
        public_ip_output = TerraformOutput(self, 'public_ip', value=instance.public_ip)

# Instantiate the app
app = App()

# Instantiate the stack
WebsiteStack(app, "bobo")

# Synthesize the app
app.synth()
