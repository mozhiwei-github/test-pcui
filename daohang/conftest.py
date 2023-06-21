import os
import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
from common.browsermob_proxy import start_browsermob_proxy, terminate_browsermob_processes, get_browsermob_proxy_client
from common.log import log
from common.utils import get_domain_ip
from common.webdriver import get_chrome_options
from daohang.config import config
from daohang.contants import TaskRunMode, NavigationChannel, NavigationEnv

"""导航fixture"""


def pytest_generate_tests(metafunc):
    # 获取命令行参数中测试用例配置
    channel_param = metafunc.config.getoption("--channel")
    env_param = metafunc.config.getoption("--env")
    if not channel_param:
        channel_list = list(NavigationChannel._value2member_map_.keys())
    else:
        channel_list = []
        for channel in channel_param.split(","):
            try:
                channel_list.append(NavigationChannel[channel].value)
            except:
                channel_list.append(channel)

    if not env_param:
        env_list = list(NavigationEnv._value2member_map_.keys())
    else:
        env_list = []
        for env in env_param.split(","):
            try:
                env_list.append(NavigationEnv[env].value)
            except:
                env_list.append(env)

    # 遍历用例涉及的fixture函数，使用配置信息中的参数值替换fixture的入参
    fixture_names = metafunc.fixturenames
    for fixture in fixture_names:
        if fixture == "get_env_and_channel":
            env_and_channel_list = []
            for env in env_list:
                for channel in channel_list:
                    env_and_channel_list.append((env, channel))

            try:
                metafunc.parametrize("get_env_and_channel", env_and_channel_list, indirect=True)
            except Exception as e:
                log.log_error("get_env_and_channel parametrize error")
                raise e


@pytest.fixture(scope="function")
def get_base_url(request):
    """获取导航不同渠道主页地址"""
    base_url = request.param
    return base_url.value


@pytest.fixture(scope="function")
def get_env_and_channel(request):
    """获取导航环境与渠道信息"""
    env, channel = request.param
    return env, channel


@pytest.fixture(scope="function")
def chrome_driver_init():
    """Chrome驱动初始化"""

    log.log_info(f"当前任务运行方式：{config.RUN_MODE.value}")

    if config.RUN_MODE == TaskRunMode.LOCAL:  # 本地运行 browsermob-proxy 与 chrome webdriver
        os.system('taskkill /im chromedriver.exe /F')
        terminate_browsermob_processes()

        proxy, server = start_browsermob_proxy(config.BROWSERMOB_PROXY_PATH, port=config.BROWSERMOB_PROXY_LOCAL_PORT)
        # 获取 chrome webdriver 运行配置
        chrome_options = get_chrome_options(proxy.proxy)
        # 本地运行 chrome webdriver
        driver = webdriver.Chrome(options=chrome_options)

        yield proxy, driver

        # 停止 chrome webdriver
        driver.quit()
        # 停止 browsermob-proxy 服务
        server.stop()
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
