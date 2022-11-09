import os

from aws_cdk import (
    Duration,
    Stack, Environment,
    aws_ecs as ecs,
)
from constructs import Construct

from jenkins.agent_stack import AgentStack
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

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=networking.vpc
                              )

        ServiceStack(self, "ServiceStack",
                     jenkins_home=jenkins_home,
                     app_name=app_name,
                     cluster=cluster,
                     file_system=storage.file_system,
                     access_point=storage.access_point,
                     timeout=Duration.minutes(10),
                     )

        AgentStack(self, "AgentStack",
                   jenkins_home=jenkins_home,
                   app_name=app_name,
                   cluster=cluster,
                   timeout=Duration.minutes(10),
                   )
