from aws_cdk import (
    # Duration,
    Stack,
    aws_efs as efs,
    aws_ec2 as ec2, RemovalPolicy,
)
from aws_cdk.aws_efs import PosixUser
from constructs import Construct


class StorageStack(Stack):

    def __init__(self, scope: Construct, vpc: ec2.Vpc, construct_id: str, jenkins_home: str, props: dict,
                 **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        self.file_system = efs.FileSystem(self, "MyEfsFileSystem",
                                          vpc=vpc,
                                          lifecycle_policy=efs.LifecyclePolicy.AFTER_14_DAYS,
                                          # files are not transitioned to infrequent access (IA) storage by default
                                          performance_mode=efs.PerformanceMode.GENERAL_PURPOSE,  # default
                                          out_of_infrequent_access_policy=efs.OutOfInfrequentAccessPolicy.AFTER_1_ACCESS,
                                          removal_policy=RemovalPolicy.DESTROY,
                                          )

        self.file_system.add_access_point(self.stack_name,
                                          path=jenkins_home,
                                          posix_user=PosixUser(
                                              uid="1000",
                                              gid="1000"
                                          ),
                                          create_acl=efs.Acl(
                                              owner_uid="1000",
                                              owner_gid="1000",
                                              permissions="755"
                                          ),
                                          )