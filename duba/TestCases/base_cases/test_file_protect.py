import allure
import pytest
from common import utils
from common.contants import Host
from common.log import log
from duba.PageObjects.file_protect_page import FileProtectPage
from duba.config import config
from duba.utils import login_normal_user


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@allure.epic(f'毒霸文件夹加密基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开文件夹加密界面')
class TestTrashAutoClean(object):

    @allure.story('1.文件夹加密---会员卡点测试')
    def test_trash_auto_clean_vip_block(self):
        allure.dynamic.description(
            '\t1.检查会员卡点\n'
        )
        allure.dynamic.title('会员卡点测试')

        with allure.step("step1：登录非会员触发卡点"):
            file_protect = FileProtectPage()
            login_normal_user(file_protect)
            ret = file_protect.check_vip_block()
            assert ret, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，点击添加文件夹，弹出会员卡点")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
