import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from duba.config import config
from duba.PageObjects.c_slimming_page import CSlimmingPage, CreateGarbage
from duba.utils import login_normal_user, check_vip_block


@pytest.fixture(scope="class", autouse=True)
def d_error_to_kill_kxetray():
    yield 1
    # utils.kill_process_by_name("kxetray.exe")
    utils.kill_process_by_name("ksysslim.exe")


@pytest.fixture(scope="class", autouse=True)
def b_switch_host():
    """
    切换到毒霸服务端测试服
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@pytest.fixture(scope="class", autouse=True)
def c_pull_file():
    """
    拉下模拟文件，并打开c盘瘦身界面
    """
    grab = CreateGarbage()
    retgb = grab.create_garbage()
    assert retgb, log.log_error("下拉用于模拟的搬家文件失败！！", need_assert=False)
    log.log_pass("下拉用于模拟的搬家文件成功")


@allure.epic(f'毒霸C盘瘦身基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开C盘瘦身界面')
class TestKsysslimBase(object):
    @allure.story('1.C盘瘦身非会员卡点场景')
    def test_ksysslim_vip_block(self):
        allure.dynamic.description(
            '\t1.检查c盘瘦身会员卡点\n'
        )
        allure.dynamic.title('C盘瘦身会员卡点功能测试')

        with allure.step("step1：登录非会员，检查会员卡点"):
            ksysslim = CSlimmingPage()
            login_normal_user(ksysslim)
            ksysslim.click_to_slimming(check_user=False)
            log.log_info("点击""一键瘦身""之后截图", screenshot=True)
            ret = check_vip_block(ksysslim)
            assert ret, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，使用c盘瘦身功能，弹出会员卡点")
            pass


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
