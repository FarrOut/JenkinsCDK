#!/usr/bin/env python3
import os

import aws_cdk as cdk

from jenkins.jenkins_stack import JenkinsStack
from jenkins.storage_stack import StorageStack
from jenkins.network_stack import NetworkStack
from jenkins.service_stack import ServiceStack

app = cdk.App()

jenkins_home = 'jenkins-home'
app_name = 'jenkins-cdk'

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                              region=os.getenv('CDK_DEFAULT_REGION'))

networking = NetworkStack(app, "NetworkStack",
                          env=default_env,
                          )

storage = StorageStack(app, "StorageStack",
                       jenkins_home=jenkins_home,
                       env=default_env,
                       )

ServiceStack(app, "ServiceStack",
             jenkins_home=jenkins_home,
             app_name=app_name,
             vpc=networking.vpc,
             file_system=storage.file_system,
             access_point=storage.access_point,
             env=default_env,
             )

JenkinsStack(app, "JenkinsStack",
             env=default_env,
             )

app.synth()
