# -*- coding: utf-8 -*-

"""
**"Runtime" Definition**

Runtime is where you execute your code. For example, if this code is running
in a CI build environment, then the runtime is "ci". If this code is running
on your local laptop, then the runtime is "local". If this code is running on
AWS Lambda, then the runtime is "lambda"

This module automatically detect what is the current runtime.

.. note::

    This module is "ZERO-DEPENDENCY".
"""

import os
import enum

IS_LOCAL = False
IS_GITHUB_CI = False
IS_EC2 = False
IS_CODEBUILD_CI = False


class RunTimeEnum(str, enum.Enum):
    local = "loc"
    github_ci = "github_ci"
    ec2 = "ec2"
    codebuild_ci = "codebuild_ci"
    unknown = "unknown"


CURRENT_RUNTIME: str = RunTimeEnum.unknown.value

if os.environ.get("HOME", "NA") == "/home/ubuntu":  # pragma: no cover
    IS_EC2 = True
    CURRENT_RUNTIME = RunTimeEnum.ec2.value
# if you use AWS CodeBuild for CI/CD
# ref: https://docs.aws.amazon.com/codebuild/latest/userguide/build-env-ref-env-vars.html
elif "CODEBUILD_CI" in os.environ:  # pragma: no cover
    IS_CODEBUILD_CI = True
    CURRENT_RUNTIME = RunTimeEnum.codebuild_ci.value
# if you use GitHub CI for CI/CD
# ref: https://docs.github.com/en/actions/learn-github-actions/variables
elif "CI" in os.environ:  # pragma: no cover
    IS_GITHUB_CI = True
    CURRENT_RUNTIME = RunTimeEnum.github_ci.value
else:  # pragma: no cover
    IS_LOCAL = True
    CURRENT_RUNTIME = RunTimeEnum.local.value
