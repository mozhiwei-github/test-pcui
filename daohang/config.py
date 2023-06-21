import os
from daohang.contants import TaskRunMode

"""导航项目配置"""

USER_HOME_PATH = os.path.expanduser("~")
assert USER_HOME_PATH, "获取用户目录失败"

class DefaultConfig:
    # 运行方式
    RUN_MODE = TaskRunMode.LOCAL
    # browsermob-proxy 本地路径
    BROWSERMOB_PROXY_PATH = os.path.join(USER_HOME_PATH, r'Downloads\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    BROWSERMOB_PROXY_LOCAL_PORT = 8081
    # browsermob-proxy 远程服务配置
    BROWSERMOB_PROXY_SERVER_HOST = "host.docker.internal"
    BROWSERMOB_PROXY_SERVER_PORT = "58080"
    BROWSERMOB_PROXY_SERVER_PORT_PREFIX = "5"
    # selenium grid hub 地址
    DRIVER_REMOTE_HUB = "http://host.docker.internal:4444/wd/hub"

# # 采用远程机器调试方法：
# class DefaultConfig:
#     # 运行方式
#     RUN_MODE = TaskRunMode.REMOTE
#     # browsermob-proxy 本地路径
#     BROWSERMOB_PROXY_PATH = os.path.join(USER_HOME_PATH, r'Downloads\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
#     BROWSERMOB_PROXY_LOCAL_PORT = 8081
#     # browsermob-proxy 远程服务配置
#     BROWSERMOB_PROXY_SERVER_HOST = "10.12.36.155"
#     BROWSERMOB_PROXY_SERVER_PORT = "58080"
#     BROWSERMOB_PROXY_SERVER_PORT_PREFIX = "5"
#     # selenium grid hub 地址
#     DRIVER_REMOTE_HUB = "http://10.12.36.155:4444/wd/hub"


config = DefaultConfig()

# 当运行环境为docker时，将运行模式改为远程运行
case_id = os.environ.get("caseid")
docker_env = os.environ.get("docker_env", None)
if case_id and docker_env:
    config.RUN_MODE = TaskRunMode.REMOTE
