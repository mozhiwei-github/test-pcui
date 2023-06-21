import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.browser_home_protect_page import BrowserHomeProtectPage
from duba.PageObjects.right_menu_mgr_page import RightMenuMgrPage
from duba.config import config
from duba.utils import login_normal_user, check_vip_block


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸浏览器主页修复基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开浏览器主页修复界面')
class TestTrashAutoClean(object):

    @allure.story('1.浏览器主页修复---基础用例测试')
    def test_trash_auto_clean_vip_block(self):
        allure.dynamic.description(
            '\t1.检查基础用例\n'
        )
        allure.dynamic.title('基础用例测试')

        with allure.step("step1：扫描"):
            bro = BrowserHomeProtectPage()
            login_normal_user(bro)
            bro.click_start_scanning_button()
            res = bro.check_sacn()
            assert res, log.log_error("扫描功能异常", need_assert=False)
            log.log_pass("扫描功能正常")

        with allure.step("step2：检查会员卡点"):
            bro.click_unlock_button()
            utils.perform_sleep(1)
            log.log_info("点击""一键解锁""之后截图", screenshot=True)
            res = check_vip_block(bro)
            assert res, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，使用一键解锁，弹出会员卡点")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
