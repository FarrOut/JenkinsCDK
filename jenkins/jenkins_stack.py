import os

from aws_cdk import (
    # Duration,
    Stack, Environment,
)
from constructs import Construct

from jenkins.network_stack import NetworkStack
from jenkins.service_stack import ServiceStack
from jenkins.storage_stack import StorageStack


class JenkinsStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, app_name: str, jenkins_home: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        networking = NetworkStack(self, "NetworkStack", )

        storage = StorageStack(self, "StorageStack",
                               jenkins_home=jenkins_home,
                               vpc=networking.vpc,
                               )

        ServiceStack(self, "ServiceStack",
                     jenkins_home=jenkins_home,
                     app_name=app_name,
                     vpc=networking.vpc,
                     file_system=storage.file_system,
                     access_point=storage.access_point,
                     )
