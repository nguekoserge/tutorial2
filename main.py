from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.instance import Instance

class WebsiteStack(TerraformStack):
    def __init__(self, scope: Construct, ns: str):
        super().__init__(scope, ns)

        AwsProvider(self, 'aws', region='us-east-2')

        instance = Instance(self, 'WebServer',
            ami='ami-0492f9e8743eb62eb',  # Utilisez l'ID de l'AMI Amazon Linux 2023 (64-bit, Arm)
            instance_type='t4g.micro',  # Utilisez un type d'instance compatible avec l'architecture arm64
            tags={'Name': 'WebServer'}
        )

        TerraformOutput(self, 'public_ip', value=instance.public_ip)

app = App()
WebsiteStack(app, "website-stack")
app.synth()
