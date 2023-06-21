import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.driver_manager_page import DriverManagerPage
from duba.config import config
from duba.utils import login_normal_user, check_vip_block


@pytest.fixture(scope="class", autouse=True)
def b_switch_host():
    """
    切换到毒霸服务端测试服
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸驱动管理测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开驱动管理界面')
class TestDriverManagerNormal(object):
    @allure.story('驱动管理非会员场景')
    def test_driver_manager_scan_check(self):
        allure.dynamic.title('驱动管理扫描功能测试')
        allure.dynamic.description(
            '\t1.打开驱动管理页面'
            '\t2.登录非会员'
            '\t3.进行扫描'
            '\t4.使用功能，检查卡点'
        )

        with allure.step("step1：打开驱动管理，进行扫描"):
            driver1 = DriverManagerPage()
            login_normal_user(driver1)
            driver1.click_scan_btn()
            res = driver1.check_scan_driver(close_box=False)
            assert res, log.log_error("扫描功能异常", need_assert=False)
            log.log_pass("驱动管理扫描结束")

        with allure.step("step2：点击修复按钮, 检查会员卡点"):
            driver1.click_remind_fix_btn()
            log.log_info("已执行点击修复按钮操作", screenshot=True)
            utils.perform_sleep(2)
            res = check_vip_block(driver1)
            assert res, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，使用驱动管理功能，弹出会员卡点")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
