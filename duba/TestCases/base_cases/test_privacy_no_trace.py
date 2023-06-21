import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.privacy_no_trace_page import PrivacyNoTracePage
from duba.config import config
from duba.utils import login_normal_user, check_vip_block, login_super_vip


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸隐私无痕模式基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开隐私无痕模式界面')
class TestTrashAutoClean(object):

    @allure.story('1.隐私无痕模式---基础用例测试')
    def test_trash_auto_clean_vip_block(self):
        allure.dynamic.description(
            '\t1.检查基础用例\n'
        )
        allure.dynamic.title('基础用例测试')

        with allure.step("step1：登录非会员触发卡点"):
            priNo = PrivacyNoTracePage()
            login_normal_user(priNo)
            priNo.click_all_open()
            utils.perform_sleep(1)
            log.log_info("点击""一键开启""之后截图", screenshot=True)
            res = check_vip_block(priNo)
            assert res, log.log_error("点击一键开启，无弹出会员卡点", need_assert=False)
            log.log_pass("会员卡点弹出成功")

        with allure.step("step2：登录会员开启开关"):
            login_super_vip(priNo, username="golanger030", password="kingsoft")
            priNo.click_all_open()
            res1 = priNo.check_all_open()
            assert res1, log.log_error("开关开启失败", need_assert=False)
            log.log_pass("开关开启成功")

            priNo.click_all_close()
            res2 = priNo.check_all_close()
            assert res2, log.log_error("开关关闭失败", need_assert=False)
            log.log_pass("开关关闭成功")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
