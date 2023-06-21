import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.right_menu_mgr_page import RightMenuMgrPage
from duba.config import config
from duba.utils import login_normal_user


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸右键菜单管理基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开右键菜单管理界面')
class TestTrashAutoClean(object):

    @allure.story('1.右键菜单管理---基础用例测试')
    def test_trash_auto_clean_vip_block(self):
        allure.dynamic.description(
            '\t1.检查基础用例\n'
        )
        allure.dynamic.title('基础用例测试')

        with allure.step("step1：扫描"):
            rightMe = RightMenuMgrPage()
            login_normal_user(rightMe)
            rightMe.click_start_scanning_button()
            res = rightMe.check_scan_finished()
            assert res, log.log_error("扫描功能异常", need_assert=False)
            log.log_pass("扫描功能正常")

        with allure.step("step2：清理"):
            rightMe.stow_all_tab()
            rightMe.choose_all_tab()
            rightMe.click_start_clean()
            res = rightMe.check_clean_finished()
            assert res, log.log_error("清理功能异常", need_assert=False)
            log.log_pass("清理功能正常")

        with allure.step("step3：恢复"):
            rightMe.click_recovery_btn()
            rightMe.choose_all_delete()
            rightMe.click_recover_btn()
            res = rightMe.check_recover_finished()
            assert res, log.log_error("恢复功能异常", need_assert=False)
            log.log_pass("恢复功能正常")




if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
