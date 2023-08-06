# -*- coding: utf-8 -*-

"""
该模块用于在 EC2 实例中被调用, 并 "自省" 发现自己的服务器 ID 并在 AWS Parameter Store
找到对应的配置数据并读取.

注: 该模块只应在 EC2 内被运行, 它需要调用 AWS EC2 metadata API 获得自己的 instance id
从而继续发现自己的服务器 ID, 然后到 AWS Parameter Store 读取配置数据.

Usage:

.. code-block:: python

    >>> from acore_server_config.api import get_server
    >>> server = get_server()
    >>> server
    Server(id='sbx-blue', db_admin_password='sbx*dummy4test', db_username='myuser', db_password='sbx*dummy4test')
"""


import typing as T

from simple_aws_ec2.api import Ec2Instance
from acore_server_metadata.api import settings

from .boto_ses import bsm
from .config.define import EnvEnum, Env, Config, Server

if T.TYPE_CHECKING:
    from boto_session_manager import BotoSesManager


def get_server(
    bsm: "BotoSesManager" = bsm,
    parameter_name_prefix: str = "acore_server_config-",
) -> Server:
    """
    在 EC2 上通过 "自省", 获得属于这个服务器的配置数据.

    配置数据的详细数据结构请参考 :class:`acore_server_config.config.define.server.Server`.

    :param bsm:
    :param parameter_name_prefix: AWS parameter name prefix, the full name will
        be ${parameter_name_prefix}-${server_id}.
    """
    ec2_inst = Ec2Instance.from_ec2_inside(bsm.ec2_client)
    server_id = ec2_inst.tags[settings.ID_TAG_KEY]

    env_name, server_name = server_id.split("-", 1)
    parameter_name = f"{parameter_name_prefix}{env_name}"

    config = Config.read(
        env_class=Env,
        env_enum_class=EnvEnum,
        bsm=bsm,
        parameter_name=parameter_name,
        parameter_with_encryption=True,
    )
    env = config.get_env(env_name=env_name)
    server = env.servers[server_name]
    return server
