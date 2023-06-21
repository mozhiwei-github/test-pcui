import os
import shutil

import allure
import pytest

from common import utils
from common.contants import Host
from common.log import log
from common.tools import duba_tools
from common.tools.duba_tools import find_dubapath_by_reg, rename_kpopcenter, recover_kpopcenter
from duba.PageObjects.main_page import main_page
from duba.PageObjects.trash_auto_clean_page import delete_popcfg, delete_ktrashud, delete_popdata, \
    modify_kvipapp_setting, set_xml_attribute_value, TrashAutoCleanPage
from duba.config import config
from duba.utils import login_super_vip, login_normal_user, check_vip_block, close_duba_self_protecting


@pytest.fixture(scope="function")
def login_vip():
    """
    登录超级会员并打开开关
    """
    close_duba_self_protecting()
    trashauto = TrashAutoCleanPage()
    login_super_vip(trashauto, username="golanger030", password="kingsoft")
    trashauto.open_auto_clean()  # 打开自动清理开关


@pytest.fixture(scope="class", autouse=True)
def a_switch_host():
    """
    切换测试服host
    """
    utils.modify_host(Host.DUBA_SERVER_TEST.value)
    log.log_info("切换到毒霸服务端测试服")


@pytest.fixture(scope="function")
def a_rename_kpopcenter():
    """
    重命名kpopcenter.dll
    """
    close_duba_self_protecting()
    rename_kpopcenter()
    yield 1
    recover_kpopcenter()


@allure.epic(f'毒霸垃圾自动清理基础场景测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸界面->打开会员中心->打开垃圾自动清理界面')
class TestTrashAutoClean(object):

    @allure.story('1.垃圾自动清理---会员卡点测试')
    def test_trash_auto_clean_vip_block(self, a_rename_kpopcenter):
        allure.dynamic.description(
            '\t1.检查会员卡点\n'
        )
        allure.dynamic.title('会员卡点测试')

        with allure.step("step1：登录非会员触发卡点"):
            trashauto = TrashAutoCleanPage()
            login_normal_user(trashauto)
            trashauto.open_auto_clean()
            log.log_info("点击""一键开启""之后截图", screenshot=True)
            ret = check_vip_block(trashauto)
            assert ret, log.log_error("非会员使用功能无弹出会员卡点", need_assert=False)
            log.log_pass("非会员，点击一键开启，弹出会员卡点")

        with allure.step("step2：模拟弹出自动清理泡泡"):
            trashauto = TrashAutoCleanPage()
            login_super_vip(trashauto, username="golanger030", password="kingsoft")
            trashauto.open_auto_clean()  # 打开自动清理开关

            delete_popcfg()
            delete_ktrashud()
            delete_popdata()
            modify_kvipapp_setting()

            Datmaker_local = os.path.join("c:", "datmaker", "datmaker.exe")
            file_local = os.path.join("c:", "datmaker", "ktaskcfg.dat")
            file_local2 = os.path.join("c:", "datmaker")
            duba_file = os.path.join(find_dubapath_by_reg(), "data", "ktaskcfg.dat")
            duba_file2 = os.path.join(find_dubapath_by_reg(), "data")

            utils.pull_datmaker()  # 下拉解密工具
            shutil.copy(duba_file, file_local2)  # 复制毒霸的文件到file_local2目录下
            utils.decrypt_dat(Datmaker_local, file_local, op="-d")  # 解密ktaskcfg.dat
            set_xml_attribute_value(file_local)
            utils.decrypt_dat(Datmaker_local, file_local, op="-e")  # 加密ktaskcfg.dat
            shutil.copy(file_local, duba_file2)

            duba_tools.restart_kxetray()
            dubapage = main_page()  # 打开毒霸主界面，以便刷新会员信息
            # dubapage.minimize_click()

            trashauto = TrashAutoCleanPage(do_pre_open=False, check_open_result=False)
            res = trashauto.check_auto_trash_clean_pop()
            assert res, log.log_error("垃圾自动清理泡泡弹出失败，请查看日志：ktrashmon.dll.log（详情请看wiki:《自动清理垃圾》）", need_assert=False)
            log.log_pass("垃圾自动清理泡泡弹出成功")




if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
