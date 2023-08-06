
.. image:: https://readthedocs.org/projects/acore-server-config/badge/?version=latest
    :target: https://acore-server-config.readthedocs.io/en/latest/
    :alt: Documentation Status

.. image:: https://github.com/MacHu-GWU/acore_server_config-project/workflows/CI/badge.svg
    :target: https://github.com/MacHu-GWU/acore_server_config-project/actions?query=workflow:CI

.. image:: https://codecov.io/gh/MacHu-GWU/acore_server_config-project/branch/main/graph/badge.svg
    :target: https://codecov.io/gh/MacHu-GWU/acore_server_config-project

.. image:: https://img.shields.io/pypi/v/acore-server-config.svg
    :target: https://pypi.python.org/pypi/acore-server-config

.. image:: https://img.shields.io/pypi/l/acore-server-config.svg
    :target: https://pypi.python.org/pypi/acore-server-config

.. image:: https://img.shields.io/pypi/pyversions/acore-server-config.svg
    :target: https://pypi.python.org/pypi/acore-server-config

.. image:: https://img.shields.io/badge/Release_History!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_server_config-project/blob/main/release-history.rst

.. image:: https://img.shields.io/badge/STAR_Me_on_GitHub!--None.svg?style=social
    :target: https://github.com/MacHu-GWU/acore_server_config-project

------

.. image:: https://img.shields.io/badge/Link-Document-blue.svg
    :target: https://acore-server-config.readthedocs.io/en/latest/

.. image:: https://img.shields.io/badge/Link-API-blue.svg
    :target: https://acore-server-config.readthedocs.io/en/latest/py-modindex.html

.. image:: https://img.shields.io/badge/Link-GitHub-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_config-project

.. image:: https://img.shields.io/badge/Link-Submit_Issue-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_config-project/issues

.. image:: https://img.shields.io/badge/Link-Request_Feature-blue.svg
    :target: https://github.com/MacHu-GWU/acore_server_config-project/issues

.. image:: https://img.shields.io/badge/Link-Download-blue.svg
    :target: https://pypi.org/pypi/acore-server-config#files


Welcome to ``acore_server_config`` Documentation
==============================================================================
**项目背景**

在生产环境中一个 "魔兽世界服务器" 通常有多个 "大区", 亚洲, 北美, 美国西部, 美国东部等. 每个 "大区" 下有多组服务器, 一个服务器也就是我们在选择服务器见面看到的 Realm, 比如国服著名的 "山丘之王", "洛萨" 等. 每个服务器都有自己的配置, 例如数据库账号密码等. 那么如何对这么多服务器的配置进行管理呢? 本项目就是为了解决这个问题而生的.

下面我们来看看具体需求.

1. **从开发者的角度看, 我们需要对服务器集群配置进行批量管理和部署. 而我们希望将服务器本身和配置数据分离, 以便于在不重新部署服务器的情况下更新配置**. 根据上一段提到的服务器层级架构, 我们需要一个树状的数据结构来定义这些服务器的配置. 例如一个大区有它默认设置. 在这个大区下的所有服务器如果没有特别说明, 则沿用大区默认设置. 如果有特别说明则用特别说明的设置. 所以我们这个项目需要解决批量管理的功能. 幸运的是, 我以前为企业做的一个项目中有一个按树状结构, 批量管理多个环境的配置的模块 `config_patterns <https://github.com/MacHu-GWU/config_patterns-project>`_ 刚好可以解决这一问题.

2. **而从服务器的角度看, 出于安全考虑, 每个服务器只要知道自己的配置即可, 不需要知道其他服务器的配置. 所以我们需要一个脚本用于** "自省" **(自己判断自己是谁, 去哪里读取配置数据) 并读取属于自己这个服务器的配置数据**. 这个脚本只需要能在服务器上运行即可.

为了解决以上两个需求, 我创建了这一项目. 请阅读完整文档 (点击 Document 标签) 做进一步了解.
