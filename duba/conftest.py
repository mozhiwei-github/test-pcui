import os
import re
import shutil
import tempfile
import pytest
from selenium.webdriver import DesiredCapabilities

from common import utils
from selenium import webdriver
from common.browsermob_proxy import terminate_browsermob_processes, start_browsermob_proxy, get_browsermob_proxy_client
from common.log import log
from common.samba import Samba
from common.utils import copytree, kill_process_by_name, get_domain_ip
from common.webdriver import get_chrome_options
from common.yaml_reader import YamlReader
from common.tools.duba_tools import find_dubapath_by_reg
from conftest import SMB_DUBA_FILEPATH
from duba import config
from duba.contants import TaskRunMode
from duba.utils import close_duba_self_protecting, kill_duba_page_process, DubaFilePath

# 配置chrome启动参数--默认下载路径
prefs_options = {'download.default_directory': r"C:\Users\admin\Downloads"}


@pytest.fixture(scope="session", autouse=True)
def turnoff_duba_self_protecting(request):
    """关闭毒霸自保护"""
    autosession = request.param
    if not autosession:
        return

    import time
    time.sleep(5)
    close_duba_self_protecting()
    return


@pytest.fixture()
def kill_exited_process():
    yield 1
    kill_process_by_name(os.getenv("process_name"))


@pytest.fixture(scope="session", autouse=True)
def a_retrun_desktop():
    log.log_info("测试前先返回桌面防止界面被挡")
    utils.keyboardInput2Key(utils.VK_CODE.get("left_win"), utils.VK_CODE.get("d"))


@pytest.fixture(scope="function", autouse=True)
def reset_duba_page(request):
    """重置毒霸页面"""
    autosession = request.param
    if not autosession:
        return

    kill_duba_page_process()
    return


# @pytest.fixture(scope="session", autouse=True)
# def z_delete_user_cache():
#     """
#     删除毒霸的前端用户信息缓存
#     :return:
#     """
#     utils.kill_process_by_name("knewvip.exe")
#     appdata = os.getenv("APPDATA")
#     userpath = os.path.dirname(
#         os.path.dirname(appdata))  # 回到上一级目录。。。因为os.getenv("APPDATA")打开的是C:\Users\CF\AppData\Roaming
#     path1 = os.path.join(userpath, "AppData", "Roaming", "Kingsoft", "kvip")
#     path2 = os.path.join(userpath, "AppData", "Local", "Kingsoft", "kvip")
#     shutil.rmtree(path1)
#     shutil.rmtree(path2)
#     utils.process_start(DubaFilePath.knewvip_exe_file_path)
#     utils.kill_process_by_name("knewvip.exe")
#

@pytest.fixture(scope="session", autouse=True)
def replace_duba_file_with_smb(request, turnoff_duba_self_protecting):
    """使用smb中文件替换毒霸相应文件"""
    autosession = request.param
    if not autosession:
        return

    smb_path_join = request.config.getoption("--smb")
    if smb_path_join is None:
        return

    # 先杀掉毒霸页面进程再做后续操作
    kill_duba_page_process()
    utils.perform_sleep(5)
    for smb_path in smb_path_join.split(","):
        match = re.match(r'\\\\([\w\.]+)\\(.*)', smb_path)
        if not match:
            log.log_error(f"smb path error, path: {smb_path}", attach=False)
            return

        host = match.group(1)
        full_smb_path = match.group(2)

        service_name = full_smb_path.split('\\')[0]
        dir_path = full_smb_path[full_smb_path.index(service_name) + len(service_name) + 1:]

        # 根据smb地址获取相应配置信息
        reader = YamlReader()
        root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        yaml_result = reader.read_yaml(os.path.join(root_path, "common", "config", "common.yml"))
        smb_config = yaml_result.get("smb")
        if not smb_config:
            log.log_error("smb config not found", attach=False)
            return

        host_config = smb_config.get(host)
        if not host_config:
            log.log_error(f"smb host not found, host: {host}", attach=False)
            return

        # 将smb共享目录文件下载到本地temp目录下
        target_path = os.path.join(tempfile.gettempdir(), "samba_test")
        samba = Samba(host, host_config.get("username"), host_config.get("password"), host_config.get("port"))
        download_result, file_info_list = samba.download_dir(service_name, os.path.join(dir_path, SMB_DUBA_FILEPATH),
                                                             target_path)

        if download_result:
            copytree_result = True
            duba_path = find_dubapath_by_reg()
            try:
                copytree(target_path, duba_path)
            except Exception as e:
                log.log_error(f"replace duba file failed, err: {e}", attach=False, need_assert=False)
                copytree_result = False

        # 删除temp下载缓存目录
        shutil.rmtree(target_path)

        assert download_result, "smb download error"
        assert copytree_result, "smb copytree error"

    log.log_info(f"使用smb中文件替换毒霸相应文件完成, 共复制文件 {len(file_info_list)} 个")
    return


@pytest.fixture(scope='session', autouse=False)
def chrome_driver_init(request):
    """Chrome驱动初始化"""

    log.log_info(f"当前任务运行方式：{config.RUN_MODE.value}")

    if config.RUN_MODE == TaskRunMode.LOCAL:  # 本地运行 browsermob-proxy 与 chrome webdriver
        os.system('taskkill /im chromedriver.exe /F')
        terminate_browsermob_processes()

        proxy, server = start_browsermob_proxy(config.BROWSERMOB_PROXY_PATH, port=config.BROWSERMOB_PROXY_LOCAL_PORT)
        # 获取 chrome webdriver 运行配置
        chrome_options = get_chrome_options(proxy.proxy, prefs=prefs_options)
        # 本地运行 chrome webdriver
        driver = webdriver.Chrome(options=chrome_options)

        def teardown():
            # 停止 chrome webdriver
            driver.quit()
            # 停止 browsermob-proxy 服务
            proxy.close()
            server.stop()

        request.addfinalizer(teardown)

        yield proxy, driver
    else:  # 远程运行 browsermob-proxy 与 chrome webdriver
        proxy_server_ip = get_domain_ip(config.BROWSERMOB_PROXY_SERVER_HOST)
        proxy = get_browsermob_proxy_client(f'{proxy_server_ip}:{config.BROWSERMOB_PROXY_SERVER_PORT}')
        proxy_server = f'{proxy_server_ip}:{config.BROWSERMOB_PROXY_SERVER_PORT_PREFIX}{proxy.port}'
        # 获取 chrome webdriver 运行配置
        chrome_options = get_chrome_options(proxy_server)
        # 远程运行 chrome webdriver
        driver = webdriver.Remote(command_executor=config.DRIVER_REMOTE_HUB,
                                  desired_capabilities=DesiredCapabilities.CHROME, options=chrome_options)

        yield proxy, driver

        # 停止 chrome webdriver
        driver.quit()

        # 关闭 browsermob-proxy 连接
        assert proxy.close() == 200
