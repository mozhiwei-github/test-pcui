import allure
import pytest

from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.c_slimming_page import CSlimmingPage, CreateGarbage
from duba.utils import check_ksysslim_exist_loop


@pytest.fixture()
def c_error_to_kill():
    yield 1
    utils.kill_process_by_name("ksysslim.exe")


@pytest.fixture(scope="class", autouse=True)
def b_pull_file():
    """
    拉下模拟文件，并打开c盘瘦身界面
    """
    grab = CreateGarbage()
    retgb = grab.create_garbage()
    assert retgb, log.log_error("下拉用于模拟的搬家文件失败！！", need_assert=False)
    log.log_pass("下拉用于模拟的搬家文件成功")


@allure.epic(f'毒霸C盘瘦身基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开C盘瘦身界面')
class TestKsysslimScanOut(object):
    @allure.story('1.C盘瘦身打开退出场景')
    def test_ksysslim_scan_click_out(self, c_error_to_kill):
        allure.dynamic.description(
            '\t1.执行C盘瘦身反复扫描,点击按钮退出\n'
        )
        allure.dynamic.title('C盘瘦身反复扫描，退出，检查ksysslim.exe是否退出')
        scan_num = 20  # 反复扫描次数+1，需要减1使用

        with allure.step("step1：执行C盘瘦身反复扫描退出20次"):
            ksysslim = CSlimmingPage()
            log.log_info("-----------第{1}次扫描-----------")
            ksysslim.scan_check()
            res = check_ksysslim_exist_loop()
            assert res, log.log_error("第1次扫描退出，ksysslim.exe无退出")

            # 第二次之后的扫描
            for i in range(scan_num - 1):
                log.log_info("-----------第{x}次扫描-----------".format(x=i + 2))
                ksysslim.scan_check(manual_scanning=True)
                res = check_ksysslim_exist_loop()
                assert res, log.log_error("第{x}次扫描退出，ksysslim.exe无退出".format(x=i + 2))
            log.log_pass("C盘瘦身反复扫描退出功能正常")

    @allure.story('1.C盘瘦身打开，强制杀进程场景')
    def test_ksysslim_scan_kill_exe_out(self, c_error_to_kill):
        allure.dynamic.description(
            '\t1.执行C盘瘦身反复扫描,扫描未结束强制杀进程退出\n'
        )
        allure.dynamic.title('C盘瘦身反复扫描，并强制杀进程退出，检查ksyshelper64.exe或者ksyshelper.exe是否退出')
        scan_num = 20  # 反复扫描次数+1，需要减1使用

        with allure.step("step1：c盘瘦身点击扫描后杀进程，重复20次"):
            ksysslim = CSlimmingPage()  # 此处无法手动点击扫描
            log.log_info("-----------第{1}次扫描-----------")
            ksysslim.scan_check_forced_exit()
            utils.perform_sleep(3)
            res = ksysslim.check_ksyshelper_exit()
            assert res, log.log_error("第1次扫描退出，ksyshelper64.exe或者ksyshelper.exe无退出")

            # 第二次之后的扫描
            for i in range(scan_num - 1):
                log.log_info("-----------第{x}次扫描-----------".format(x=i + 2))
                ksysslim.scan_check_forced_exit(click_scan=True)
                utils.perform_sleep(3)
                res = ksysslim.check_ksyshelper_exit()
                assert res, log.log_error(
                    "第{x}次扫描, ksysslim.exe关闭后3s后，ksyshelper64.exe或者ksyshelper.exe无退出".format(x=i + 2))
            log.log_pass("c盘瘦身点击扫描后杀进程，ksyshelper64.exe或者ksyshelper.exe退出正常")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
