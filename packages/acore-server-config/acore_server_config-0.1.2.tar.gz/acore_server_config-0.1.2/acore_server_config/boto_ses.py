# -*- coding: utf-8 -*-

from boto_session_manager import BotoSesManager

from .runtime import IS_LOCAL, IS_GITHUB_CI, IS_EC2, IS_CODEBUILD_CI

aws_region = "us-east-1"
# environment aware boto session manager
if IS_LOCAL:  # put production first
    bsm = BotoSesManager(
        profile_name="bmt_app_dev_us_east_1",
        region_name=aws_region,
    )
elif IS_GITHUB_CI:
    bsm = BotoSesManager(
        region_name=aws_region,
    )
elif IS_EC2 or IS_CODEBUILD_CI:
    bsm = BotoSesManager(
        region_name=aws_region,
    )
else:  # pragma: no cover
    raise NotImplementedError
