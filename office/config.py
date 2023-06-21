import os
from socket import gethostbyname
from urllib.parse import urlparse

from office.contants import TaskRunMode
from office.contants import Env

"""办公模板项目配置"""


USER_HOME_PATH = os.path.expanduser("~" )
assert USER_HOME_PATH, "获取用户目录失败"

class AccountInfo:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class DefaultConfig:
    """配置基类"""
    ENV = Env.TEST
    CDS_HOST = "http://10.12.36.155:8080"  # 容器调度服务地址
    GATEWAY_HOST = "http://newvip-dev-gw.duba.net"  # 网关地址
    DEV1_HOST = None
    NON_VIP_ACCOUNT = None
    COMMON_VIP_ACCOUNT = None
    DIAMOND_VIP_ACCOUNT = None
    SUPER_VIP_ACCOUNT = None
    HONOR_VIP_ACCOUNT = None

    # 运行方式
    RUN_MODE = TaskRunMode.LOCAL
    # RUN_MODE = TaskRunMode.REMOTE
    # browsermob-proxy 本地路径
    BROWSERMOB_PROXY_PATH = os.path.join(USER_HOME_PATH, r'Downloads\browsermob-proxy-2.1.4\bin\browsermob-proxy.bat')
    BROWSERMOB_PROXY_LOCAL_PORT = 8081
    # browsermob-proxy 远程服务配置
    BROWSERMOB_PROXY_SERVER_HOST = "10.12.36.155"
    BROWSERMOB_PROXY_SERVER_PORT = "58080"
    BROWSERMOB_PROXY_SERVER_PORT_PREFIX = "5"
    # selenium grid hub 地址
    DRIVER_REMOTE_HUB = "http://10.12.36.155:4444/wd/hub"


class TestEnvConfig(DefaultConfig):
    """测试环境配置"""
    ENV = Env.TEST
    GATEWAY_HOST = "http://newvip-dev-gw.duba.net"
    DEV1_HOST = "http://newvip-dev1.duba.net"  # 193.112.115.162
    NON_VIP_ACCOUNT = AccountInfo(username="golanger027", password="kingsoft")
    COMMON_VIP_ACCOUNT = AccountInfo(username="golanger025", password="kingsoft")
    DIAMOND_VIP_ACCOUNT = AccountInfo(username="golanger045", password="kingsoft")
    SUPER_VIP_ACCOUNT = AccountInfo(username="golanger030", password="kingsoft")
    HONOR_VIP_ACCOUNT = AccountInfo(username="golanger026", password="kingsoft")
    QQ_ACCOUNT = AccountInfo(username="3445347241", password="liebao123liebao")


class ProductionEnvConfig(DefaultConfig):
    """线上生产环境配置"""
    ENV = Env.PRODUCTION
    GATEWAY_HOST = "https://newvip.duba.net"
    NON_VIP_ACCOUNT = AccountInfo(username="jj4747", password="47474747")
    QQ_ACCOUNT = AccountInfo(username="3445347241", password="liebao123liebao")

config = DefaultConfig()

# 当运行环境为kvm时，将运行模式改为远程运行
case_id = os.environ.get("caseid")
kvm_env = os.environ.get("kvm_env", None)
if case_id and kvm_env:
    config.RUN_MODE = TaskRunMode.REMOTE

# 取host中毒霸会员域名对应ip
host_ip = gethostbyname("newvip.duba.net")

# 取测试服配置中DEV1域名对应ip
test_host = urlparse(TestEnvConfig.DEV1_HOST).netloc
test_host_ip = gethostbyname(test_host)

# 比较host中毒霸会员ip与测试服配置一致时，选择测试服配置
if host_ip == test_host_ip:
    config = TestEnvConfig()
else:
    config = ProductionEnvConfig()