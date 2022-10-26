from aws_cdk import (
    # Duration,
    Stack,
    aws_ecs as ecs,
    aws_ecs_patterns as patterns,
)

from constructs import Construct


class ServiceStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
