import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.privacy_cleaner_page import PrivacyCleanerPage
from duba.config import config
from duba.utils import login_normal_user, check_vip_block


@pytest.fixture(scope="class", autouse=True)
def switch_host():
    """
    切换到毒霸服务端测试服
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸隐私清理基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开隐私清理界面')
class TestKsysslimBase(object):
    @allure.story('1.非会员场景测试')
    def test_privacy_cleaner_vip_block(self):
        allure.dynamic.description(
            '\t1.会员卡点检查\n'
        )
        allure.dynamic.title('隐私清理非会员场景测试')

        with allure.step("step1：登录非会员，检查会员卡点"):
            privacy = PrivacyCleanerPage()
            login_normal_user(privacy)
            privacy.click_start_scanning_button()
            privacy.check_scaning()
            privacy.close_high_rish_remind_tab()
            utils.perform_sleep(2)
            privacy.click_clean()
            log.log_info("点击""一键清理""之后截图", screenshot=True)
            ret = check_vip_block(privacy)
            assert ret, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，使用隐私清理，弹出会员卡点")
            log.log_pass("非会员使用功能弹出会员卡点")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
