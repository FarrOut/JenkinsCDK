from aws_cdk import (
    # Duration,
    Stack,
    aws_ec2 as ec2,
    aws_efs as efs,
    aws_ecs as ecs,
    aws_ecs_patterns as patterns, Duration, NestedStack,
)
from aws_cdk.aws_ecs import EfsVolumeConfiguration, AuthorizationConfig, ContainerImage, LogDriver, ContainerDefinition, \
    PortMapping, MountPoint
from aws_cdk.aws_ecs_patterns import ApplicationLoadBalancedFargateService, ApplicationLoadBalancedTaskImageOptions

from constructs import Construct


class ServiceStack(NestedStack):

    def __init__(self, scope: Construct, construct_id: str, app_name: str, jenkins_home: str, vpc: ec2.Vpc,
                 file_system: efs.FileSystem, access_point: efs.AccessPoint,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Create an ECS cluster
        cluster = ecs.Cluster(self, "Cluster",
                              vpc=vpc
                              )

        volume = ecs.Volume(
            name=jenkins_home,
            efs_volume_configuration=EfsVolumeConfiguration(
                file_system_id=file_system.file_system_id,
                transit_encryption='ENABLED',
                authorization_config=AuthorizationConfig(
                    access_point_id=access_point.access_point_id,
                    iam='ENABLED'
                ),
            )
        )

        fargate_task_definition = ecs.FargateTaskDefinition(self, "TaskDef",
                                                            family=app_name,
                                                            memory_limit_mib=2048,
                                                            cpu=1024,
                                                            volumes=[volume],
                                                            )

        container_def = ContainerDefinition(self, 'ContainerDefinition',
                                            task_definition=fargate_task_definition,
                                            image=ContainerImage.from_registry("jenkins/jenkins:lts"),
                                            logging=LogDriver.aws_logs(
                                                stream_prefix='jenkins',
                                            ),
                                            port_mappings=[PortMapping(container_port=8080)],
                                            )
        container_def.add_mount_points(MountPoint(
            container_path='/var/jenkins_home',
            read_only=False,
            source_volume=jenkins_home,
        ))

        load_balanced_fargate_service = ApplicationLoadBalancedFargateService(
            self, "Service",
            cluster=cluster,
            task_definition=fargate_task_definition,
            memory_limit_mib=2048,
            cpu=1024,
            max_healthy_percent=100,
            min_healthy_percent=0,
            health_check_grace_period=Duration.minutes(15),
            desired_count=1,
        )
        load_balanced_fargate_service.listener.connections.allow_to(
            file_system, ec2.Port.tcp(2049)
        )
