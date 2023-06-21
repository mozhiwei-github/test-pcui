import os
import pytest
from selenium.webdriver import DesiredCapabilities
from office.config import config
from selenium import webdriver
from common.browsermob_proxy import terminate_browsermob_processes, start_browsermob_proxy, get_browsermob_proxy_client
from common.log import log
from common.utils import get_domain_ip
from common.webdriver import get_chrome_options
from office.contants import TaskRunMode, ChromeDownloadPath

# 配置chrome启动参数--默认下载路径
prefs_options = {'download.default_directory': r"C:\Users\admin\Downloads"}


def pytest_generate_tests(metafunc):
    """获取命令行中的指定参数"""
    env_param = metafunc.config.getoption("--env")
    try:
        metafunc.parametrize("get_environment", [env_param])
    except Exception as e:
        log.log_error("get_environment parametrize error")
        raise e

@pytest.fixture(scope='function')
def get_environment(request):
    env = request.param
    return env

@pytest.fixture(scope='session', autouse=False)
def chrome_driver_init(request):
    """Chrome驱动初始化"""

    log.log_info(f"当前任务运行方式：{config.RUN_MODE.value}")

    if config.RUN_MODE == TaskRunMode.LOCAL:  # 本地运行 browsermob-proxy 与 chrome webdriver
        os.system('taskkill /im chromedriver.exe /F')
        terminate_browsermob_processes()

        proxy, server = start_browsermob_proxy(config.BROWSERMOB_PROXY_PATH, port=config.BROWSERMOB_PROXY_LOCAL_PORT)
        # 获取 chrome webdriver 运行配置
        chrome_options = get_chrome_options(proxy.proxy,prefs=prefs_options)
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

