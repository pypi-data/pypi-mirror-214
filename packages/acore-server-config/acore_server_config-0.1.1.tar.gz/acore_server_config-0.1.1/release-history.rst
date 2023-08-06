.. _release_history:

Release and Version History
==============================================================================


x.y.z (Backlog)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

**Minor Improvements**

**Bugfixes**

**Miscellaneous**


0.1.1 (2023-06-17)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
**Features and Improvements**

- First release
- Allow developer to deploy server configurations in batch to AWS parameter store.
- Allow EC2 instance to auto-discover its configuration from AWS parameter store.
- Add the following public api:
    - ``acore_server_config.api.IS_LOCAL``
    - ``acore_server_config.api.IS_GITHUB_CI``
    - ``acore_server_config.api.IS_EC2``
    - ``acore_server_config.api.IS_CODEBUILD_CI``
    - ``acore_server_config.api.EnvEnum``
    - ``acore_server_config.api.Env``
    - ``acore_server_config.api.Config``
    - ``acore_server_config.api.Server``
    - ``acore_server_config.api.get_server``
