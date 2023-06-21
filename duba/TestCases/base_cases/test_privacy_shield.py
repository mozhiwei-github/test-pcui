import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.privacy_shield_page import PrivacyShieldPage
from duba.config import config
from duba.utils import login_normal_user, check_vip_block, login_super_vip


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸隐私护盾基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开隐私护盾界面')
class TestTrashAutoClean(object):

    @allure.story('1.隐私护盾---基础用例测试')
    def test_trash_auto_clean_vip_block(self):
        allure.dynamic.description(
            '\t1.检查基础用例\n'
        )
        allure.dynamic.title('基础用例测试')

        with allure.step("step1：登录非会员触发卡点"):
            prish = PrivacyShieldPage()
            login_normal_user(prish)
            prish.open_enhanced_protection()
            utils.perform_sleep(1)
            log.log_info("点击""增强防护总开关""之后截图", screenshot=True)
            res = check_vip_block(prish)
            assert res, log.log_error("点击增强防护总开关无弹出会员卡点", need_assert=False)
            log.log_pass("会员卡点弹出成功")

        with allure.step("step2：登录会员开启开关"):
            login_super_vip(prish, username="golanger030", password="kingsoft")
            prish.open_basic_protection()
            prish.open_enhanced_protection()
            prish.click_i_know_btn()
            res1 = prish.check_basic_protection_open()
            res2 = prish.check_enhanced_protection_open()
            assert (res1 and res2), log.log_error("开关开启失败", need_assert=False)
            log.log_pass("开关开启成功")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
