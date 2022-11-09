from aws_cdk import (
    # Duration,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs,
    Duration, NestedStack,
)
from aws_cdk.aws_ecs import EfsVolumeConfiguration, AuthorizationConfig, ContainerImage, LogDriver, ContainerDefinition, \
    PortMapping, MountPoint
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService

from constructs import Construct


class AgentStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, app_name: str, jenkins_home: str, cluster: ecs.Cluster,
                 file_system: efs.FileSystem, access_point: efs.AccessPoint,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
                                                            family=app_name,
                                                            memory_limit_mib=2048,
                                                            cpu=1024,
                                                            )

        container_def = ContainerDefinition(self, 'ContainerDefinition',
                                            task_definition=fargate_task_definition,
                                            image=ContainerImage.from_registry("jenkins/ssh-agent:alpine"),
                                            logging=LogDriver.aws_logs(
                                                stream_prefix='jenkins',
                                            ),
                                            port_mappings=[PortMapping(container_port=22)],
                                            start_timeout=Duration.minutes(2),
                                            stop_timeout=Duration.seconds(30),
                                            )

        service = ApplicationLoadBalancedFargateService(
            self, "JenkinsAgentService",
            service_name='JenkinsAgent',
            cluster=cluster,
            task_definition=fargate_task_definition,
            memory_limit_mib=2048,
            cpu=1024,
            max_healthy_percent=100,
            min_healthy_percent=0,
            health_check_grace_period=Duration.minutes(15),
            desired_count=1,
        )
        # service.service.connections.allow_to(file_system, ec2.Port.tcp(2049))

        # Configure Health-check
        # service.target_group.configure_health_check(
        #     enabled=True,
        #     port='8080',
        #     path='/login',
        #     interval=Duration.seconds(30),
        # )
