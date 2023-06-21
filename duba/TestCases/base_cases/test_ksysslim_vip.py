import os

import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.c_slimming_page import CSlimmingPage, CreateGarbage, Occupy_process_Path
from duba.utils import login_super_vip


@pytest.fixture(scope="class", autouse=True)
def error_to_kill_kxetray():
    yield 1
    # utils.kill_process_by_name("kxetray.exe")
    utils.kill_process_by_name("ksysslim.exe")
    utils.kill_process_by_name("npp.7.6.3.Installer.exe")


@pytest.fixture(scope="class", autouse=True)
def b_pull_file():
    """
    拉下模拟文件，并打开c盘瘦身界面
    """
    grab = CreateGarbage()
    retgb = grab.create_garbage()
    assert retgb, log.log_error("下拉用于模拟的搬家文件失败！！", need_assert=False)
    log.log_pass("下拉用于模拟的搬家文件成功")


@pytest.fixture(scope="class", autouse=True)
def c_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")

#
@pytest.fixture(scope="class", autouse=True)
def d_login():
    """
    登录超级会员
    """
    ksysslim = CSlimmingPage()
    login_super_vip(ksysslim, username="golanger030", password="kingsoft")


@allure.epic(f'毒霸C盘瘦身基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开C盘瘦身界面')
class TestKsysslimBase(object):

    @allure.story('1.c盘瘦身会员场景--垃圾清理')
    def test_ksysslim_base_vip1(self):
        allure.dynamic.description(
            '\t1.执行C盘瘦身垃圾清理功能\n'
        )
        allure.dynamic.title('C盘瘦身垃圾清理功能测试')

        with allure.step("step1：执行C盘瘦身垃圾清理功能"):
            ksysslim = CSlimmingPage()
            ksysslim.click_to_slimming()
            ret = ksysslim.ksysslim_check_clean()
            assert ret, log.log_error("C盘瘦身基本功能异常！！", need_assert=False)
            log.log_pass("C盘瘦身基本功能正常")
            perform_sleep(1)

    @allure.story('1.c盘瘦身会员场景--大文件搬家')
    def test_ksysslim_base_vip2(self):
        allure.dynamic.description(
            '\t1.执行大文件搬家功能\n'
        )
        allure.dynamic.title('C盘瘦身大文件搬家功能测试')

        with allure.step("step1：执行大文件搬家功能"):
            utils.process_start(os.path.join(Occupy_process_Path, "npp.7.6.3.Installer.exe"), async_start=True)
            ksysslim = CSlimmingPage()
            ret = ksysslim.click_to_slimming_bigfilemoving()
            assert ret, log.log_error("大文件搬家执行失败", need_assert=False)
            utils.perform_sleep(1)
            ksysslim.click_occupy_btn()
            res2 = utils.is_process_exists("npp.7.6.3.Installer.exe")
            assert res2, log.log_error("占用进程关闭失败", need_assert=False)
            ret3 = ksysslim.big_file_moving_check_clean()
            assert ret3, log.log_error("大文件搬家还原失败", need_assert=False)
            log.log_pass("大文件搬家功能正常")

    @allure.story('1.c盘瘦身会员场景--软件搬家')
    def test_ksysslim_base_vip3(self):
        allure.dynamic.description(
            '\t1.执行软件搬家功能\n'
        )
        allure.dynamic.title('C盘瘦身软件搬家功能测试')

        with allure.step("step1：执行软件搬家功能"):
            ksysslim = CSlimmingPage()
            ret = ksysslim.click_to_software_moving()
            assert ret, log.log_error("软件搬家执行失败", need_assert=False)
            ret3 = ksysslim.software_moving_check_clean()
            assert ret3, log.log_error("软件搬家还原失败", need_assert=False)
            log.log_pass("软件搬家功能正常")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
