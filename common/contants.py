import os
from common import file_process
from enum import unique, Enum
from selenium.webdriver.common.by import By

base_dir = os.path.dirname(os.path.dirname(__file__))

# 日志目录
make_dir = file_process.DirOperation()
make_dir.makedir(os.path.join(base_dir, 'logs'))
logs_file = os.path.join(base_dir, "logs")

# 进程监控文件路径
PROCESS_MONITOR_CACHE = os.path.join(base_dir, ".proc_monitor_cache")


@unique
class ServerHost(Enum):
    """服务器地址"""
    CDS = "http://10.12.36.155:8080"  # 容器调度服务地址
    AUTO_TEST_CF = "http://autotest.cf.com"  # 移动构建集成平台地址


@unique
class InputLan(Enum):
    """
    输入法语言
    https://msdn.microsoft.com/en-us/library/cc233982.aspx
    """
    EN = 0x4090409
    ZH = 0x8040804


@unique
class EnvVar(Enum):
    """环境变量"""
    UITEST_LOG_LEVEL = "UITEST_LOG_LEVEL"  # UI自动化测试日志等级
    KVM_ENV = "kvm_env"  # KVM虚拟机环境
    CASE_ID = "caseid"  # 用例ID
    CASE_NAME = "casename"  # 用例名称
    USERNAME = "username"  # 触发用户
    AUTO_TEST_ENV = "autotestenv"  # 自动化测试环境

@unique
class Host(Enum):
    """测试环境host"""
    # 毒霸服务端测试服
    DUBA_SERVER_TEST = ['193.112.115.162 pay-cloud.duba.net',
                        '193.112.115.162 account-cloud.duba.net',
                        '193.112.115.162 newvip.zhhainiao.com',
                        '193.112.115.162 newvip.duba.net'
                        ]

    # 毒霸前端测试服
    DUBA_WEB_TEST = ['49.233.120.205 newvip.ijinshan.com']

    # 毒霸前端预发布
    DUBA_WEB_PRE = ['211.159.144.247 newvip.ijinshan.com']


@unique
class RogueSoftWareInformation(Enum):
    """流氓软件的一些信息。如：注册表位置，安装路径（默认）"""
    appdata = os.getenv("APPDATA")

    # 云上PDF
    IPDF_UNINSTALL_REGISTRY_64 = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\iPDF"  # 64位卸载注册表
    IPDF_UNINSTALL_REGISTRY_32 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\iPDF"  # 32位卸载注册表
    IPDF_INSTALL_REGISTRY_64 = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\iPDF"  # 64位软件信息注册表
    IPDF_INSTALL_REGISTRY_32 = r"HKEY_LOCAL_MACHINE\SOFTWARE\iPDF"  # 64位软件信息注册表
    IPDF_INSTALL_PATH = os.path.join(appdata, "Local", "iPDF")  # 默认安装路径

    # 小黑笔记本
    HEINOTE_UNINSTALL_REGISTRY_64 = r"HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Heinote"  # 64位卸载注册表
    HEINOTE_UNINSTALL_REGISTRY_32 = r"HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\Heinote"  # 32位卸载注册表
    HEINOTE_INSTALL_PATH = os.path.join(appdata, "Roaming", "Heinote")  # 默认安装路径