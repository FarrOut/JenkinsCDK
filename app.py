#!/usr/bin/env python3
import os

import aws_cdk as cdk

from jenkins.jenkins_stack import JenkinsStack

app = cdk.App()

jenkins_home = 'jenkins-home'
app_name = 'jenkins-cdk'

default_env = cdk.Environment(account=os.getenv('CDK_DEFAULT_ACCOUNT'),
                              region=os.getenv('CDK_DEFAULT_REGION'))

JenkinsStack(app, "JenkinsStack",
             app_name=app_name,
             jenkins_home=jenkins_home,
             env=default_env,
             )

app.synth()
