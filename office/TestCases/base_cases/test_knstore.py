import os

from common.utils import win32gui, win32con
from office.PageObjects.knstore_install_page import KnstoreInstallPage
from office.PageObjects.knstore_uninstall_page import KnstoreUninstallPage
import allure
from office.contants import knstorePath
from common import utils
from common.log import log
from common.samba import Samba
from office.config import config


@allure.epic(f"可牛应用市场基础用例测试({config.ENV.value})")
@allure.feature('可牛应用市场基础用例测试---安装测试')
class TestKnstoreInstall(object):
    @allure.story('可牛应用市场基础用例测试---安装测试')
    def test_keniuoffice_install(self):
        allure.dynamic.description(
            '\tstep1: 从云端下拉安装包至本地\n'
            '\tstep2: 可牛应用市场安装验证\n'
            '\tstep3: 安装完成后主动调起可牛应用市场界面\n'
        )
        allure.dynamic.title("可牛应用市场基础用例测试")

        with allure.step("step1: 从云端下拉安装包至本地"):
            debug_package_path = os.path.join(os.getcwd(), "Knstore")
            if os.path.exists(debug_package_path):
                utils.remove_path(debug_package_path)
            sambo_o = Samba("10.12.36.203", "duba", "duba123")
            sambo_o.download_dir("TcSpace", os.path.join('autotest', 'Knstore'), debug_package_path)
            knstore_install_package_path = os.path.join(debug_package_path, "knstore_debug_package.exe")
            if not os.path.exists(knstore_install_package_path):
                log.log_error("从远端拉取安装包文件失败")
            log.log_pass("从远端获取安装包文件成功")

        with allure.step("step2: 可牛应用市场安装验证"):
            # 判断本地是否已经安装了可牛应用市场

            if os.path.exists(os.path.join(knstorePath.DEFAULTINSTALLPATH.value, "knstore.exe")):
                uninstall_page = KnstoreUninstallPage()
                if not uninstall_page.uninstall_knstore():
                    log.log_error("卸载过程出现异常")
                log.log_pass("已正常完成可牛应用市场卸载")
                utils.perform_sleep(3)

            install_page = KnstoreInstallPage(knstore_install_package_path)
            if not install_page.install_knstore():
                log.log_error("安装过程出现异常--安装失败")
            log.log_pass("安装正常完成---安装成功")

        with allure.step("step3: 安装后主动调起主界面"):
            if not install_page.is_mainpage_exist():
                log.log_error("安装完成后未调起应用市场主界面")
            log.log_pass("安装完成后调起了应用市场主界面")
            # 关闭可牛应用市场主界面
            knstore_class_name = "store dialog class"
            knstore_hwnd = utils.get_hwnd_class_name(knstore_class_name)
            win32gui.PostMessage(knstore_hwnd, win32con.WM_CLOSE, 0, 0)
            if install_page.is_mainpage_exist():
                log.log_error("应用市场主界面未关闭")
            log.log_pass("应用市场主界面已关闭")


class TestKnstoreUninstall(object):
    @allure.story('可牛应用市场基础用例测试---卸载测试')
    def test_keniuoffice_install(self):
        allure.dynamic.description(
            '\tstep1: 调起应用市场卸载程序\n'
            '\tstep2: 判断本地环境是都卸载成功\n'
        )
        allure.dynamic.title("可牛应用市场基础用例测试---卸载测试")

        with allure.step("step1: 调起应用市场卸载程序"):
            uninstall_page = KnstoreUninstallPage()
            if not uninstall_page.uninstall_knstore():
                log.log_error("卸载过程出现异常")
            log.log_pass("已正常完成可牛应用市场卸载")

        with allure.step("step2: 判断本地环境是都卸载成功"):
            utils.perform_sleep(3)
            if os.path.exists(os.path.join(knstorePath.DEFAULTINSTALLPATH.value, "knstore.exe")):
                log.log_error("本地存在主程序，卸载失败")
            log.log_pass("本地不存在主程序，卸载成功")








