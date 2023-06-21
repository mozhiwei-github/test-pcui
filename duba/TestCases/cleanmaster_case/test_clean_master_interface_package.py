import allure
import pytest

from common import utils
from common.log import log
from common.utils import perform_sleep
from duba.PageObjects.clean_master_install_page import DownloadPackage, \
    KcleanMasterInstall, InstallCheck, print_tid_tod
from duba.PageObjects.clean_master_uninstall_page import KcleanMasterUnInstall
from duba.config import config


@allure.epic(f'清理大师非静默安装包验证测试（{config.ENV.value}）')
class TestduliKsysslimInterfacePackage(object):
    @allure.story('1.清理大师非静默安装包验证测试')
    def test_ksysslim_base(self):
        allure.dynamic.description(
            '\t0.下拉安装包\n'
            '\t1.检查安装包签名\n'
            '\t2.安装包命名检查 tod\n'
            '\t3.安装过程检查\n'
            '\t4.进程启动检查\n'
            '\t5.开始菜单项检查\n'
            '\t6.桌面快捷方式检查\n'
            '\t7.tid/tod信息核对\n'
            '\t8.控制面板卸载项\n'
            '\t9.执行卸载\n'
            '\t10.卸载检查\n'
        )
        allure.dynamic.title('清理大师非静默安装包安装卸载流程测试')

        inscheck = InstallCheck()

        with allure.step("step0：下拉安装包"):
            package = DownloadPackage()
            retpa = package.download_package()
            assert retpa, "下拉文件失败！！"
            log.log_pass("下拉文件成功")
            perform_sleep(1)

        with allure.step("step1：检查安装包签名"):
            ...

        with allure.step("step2：安装包命名检查 tod"):
            ...

        with allure.step("step3：安装过程检查"):
            kcleanInstall = KcleanMasterInstall()
            res = kcleanInstall.check_package_interface_installing()
            assert res, "安装过程异常"
            log.log_pass("安装过程正常")
            perform_sleep(1)

        with allure.step("step4：进程启动检查"):
            package_exists = inscheck.check_clean_master_process()
            assert package_exists, "安装后进程无启动！！"
            log.log_pass("安装后进程成功启动")

        with allure.step("step5：开始菜单项检查"):
            start_menu_exists = inscheck.check_start_menu()
            assert start_menu_exists, "没找到开始菜单快捷方式"
            log.log_pass("开始菜单快捷方式存在")

        with allure.step("step6：桌面快捷方式检查"):
            desktop_lnk_exists = inscheck.check_desktop_lnk()
            assert desktop_lnk_exists, "没找到桌面快捷方式"
            log.log_pass("桌面快捷方式存在")

        with allure.step("step7：tid/tod信息核对"):
            print_tid_tod()
            log.log_pass("已输出tid_tod")

        with allure.step("step8：控制面板卸载项核对"):
            control_panel_exists = inscheck.check_control_panel()
            assert control_panel_exists, "没找到控制面板卸载项"
            log.log_pass("控制面板卸载项存在")

        with allure.step("step9：执行卸载"):
            unins = KcleanMasterUnInstall()
            unins_res = unins.uninstall()
            assert unins_res, "卸载流程异常"
            log.log_pass("卸载流程结束，卸载成功")

        with allure.step("step10：卸载检查"):
            utils.perform_sleep(5)
            package_exists = inscheck.check_clean_master_process()
            assert not package_exists, "卸载后5秒，进程仍然存在"
            log.log_pass("cmtray.exe进程已关闭")

            start_menu_exists = inscheck.check_start_menu()
            assert not start_menu_exists, "卸载后，开始菜单快捷方式依然存在"
            log.log_pass("卸载后，开始菜单快捷方式不存在")

            desktop_lnk_exists = inscheck.check_desktop_lnk()
            assert not desktop_lnk_exists, "卸载后，桌面快捷方式依然存在"
            log.log_pass("卸载后，桌面快捷方式不存在")

            control_panel_exists = inscheck.check_control_panel()
            assert not control_panel_exists, "卸载后，控制面板卸载项依然存在"
            log.log_pass("卸载后，控制面板卸载项不存在")

            check_file = inscheck.check_file()
            assert check_file, "卸载后，相关文件没有删除"
            log.log_pass("卸载后，相关文件已被删除")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
