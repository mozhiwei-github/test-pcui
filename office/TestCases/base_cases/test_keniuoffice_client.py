import allure
import pytest
import os
from common import utils
from common.log import log
from common.samba import Samba
from office.config import config
from office.contants import keniuofficePath
from office.PageObjects.keniuoffice_install_page import KeniuOfficeInstallPage
from office.PageObjects.keniuoffice_client_page import is_keniuOfficePage_exist, close_keniuOfficePage, KeniuOfficeClientPage
from office.PageObjects.keniuoffice_uninstall_page import KeniuOfficeUninstallPage

@allure.epic(f"可牛办公独立版基础用例测试({config.ENV.value})")
@allure.feature('可牛办公独立版基础用例测试---安装测试')
class TestKeniuOfficeInstall(object):
    @allure.story('可牛办公独立版基础用例测试---安装测试')
    def test_keniuoffice_install(self, get_environment):
        allure.dynamic.description(
            '\tstep1: 从云端下拉安装包至本地\n'
            '\tstep2: 可牛办公安装验证\n'
            '\tstep3: 安装完成后主自动调起可牛办公界面\n'
        )
        allure.dynamic.title("可牛办公独立版基础用例测试")

        with allure.step("step1: 从云端下拉安装包至本地"):
            debug_package_path = os.path.join(os.getcwd(), "KeniuOffice")
            if os.path.exists(debug_package_path):
                utils.remove_path(debug_package_path)
            sambo_o = Samba("10.12.36.203", "duba", "duba123")
            sambo_o.download_dir("TcSpace", os.path.join('autotest', 'KeniuOfficeClient'), debug_package_path)
            keniuoffice_install_package_path = os.path.join(debug_package_path, "keniuoffice_debug_package.exe")
            if not os.path.exists(keniuoffice_install_package_path):
                log.log_error("从远端拉取安装包文件失败")
            log.log_pass("从远端获取安装包文件成功")

        with allure.step("step2: 可牛办公安装验证"):
            # 判断本地是否已经安装可牛办公独立版
            if os.path.exists(os.path.join(keniuofficePath.DEFAULTINSTALLPATH.value, "ktemplate.exe")):
                uninstall_page = KeniuOfficeUninstallPage()
                if not uninstall_page.is_uninstall_page_exist():
                    log.log_error("卸载界面展示异常")
                log.log_pass("卸载界面展示正常")
                uninstall_page.click_uninstall_button()
                utils.perform_sleep(1)
                if not uninstall_page.is_uninstall_finished():
                    log.log_error("60s内未卸载完成")
                log.log_pass("卸载完成")
                utils.perform_sleep(1)
                uninstall_page.click_uninstall_finished_button()
                utils.perform_sleep(3)
                if not uninstall_page.is_keniuoffice_path_exist():
                    log.log_error("可牛办公ktemplate.exe文件仍存在")
                log.log_pass("可牛办公ktemplate.exe文件不存在")
            install_page = KeniuOfficeInstallPage(keniuoffice_install_package_path)
            if not install_page.install_keniuoffice():
                log.log_error("可牛办公安装失败")
            log.log_pass("可牛办公独立版安装成功")

        with allure.step("step3: 安装完成后主动调起可牛办公界面"):
            if is_keniuOfficePage_exist():
                log.log_pass("安装完成后自动调起了可牛办公主界面")
                if not close_keniuOfficePage():
                    log.log_error("可牛办公主界面关闭异常")
                else:
                    log.log_pass("可牛办公主界面已关闭")
            else:
                log.log_error("安装完成后未自动调起可牛办公主界面")

@allure.epic(f"可牛办公独立版基础用例测试({config.ENV.value})")
@allure.feature('可牛办公独立版基础用例测试---基础用例')
class TestKeniuOfficeClient(object):
    @allure.story('可牛办公独立版基础用例测试---基础用例')
    def test_keniuoffice_client(self,get_environment):
        allure.dynamic.description(
            '\tstep1: 打开可牛办公主界面并查看界面是否展示异常\n'
            '\tstep2: 验证qq登录\n'
            '\tstep3: 验证首页展示\n'
            '\tstep4: 验证点击下载\n'
            '\tstep5: 验证点击收藏\n'
            '\tstep5: 验证点击收藏\n'
        )

        with allure.step("step1: 打开可牛办公主界面并查看界面是否展示异常"):
            keniuoffice_page = KeniuOfficeClientPage()
            if keniuoffice_page.is_page_show_normal():
                log.log_pass("可牛办公主界面展示正常")
            else:
                log.log_error("可牛办公主界面未正常展示")

        with allure.step("step2: 验证qq登录"):
            if not keniuoffice_page.is_main_page_with_login():
                keniuoffice_page.login_by_qq()
                utils.perform_sleep(3)
                log.log_pass("QQ登陆正常")
            else:
                log.log_info("当前为已登录状态")

        with allure.step("step3: 验证首页展示"):
            if not keniuoffice_page.is_main_page_with_login():
                log.log_error("首页展示异常/登录状态异常")
            keniuoffice_page.click_leftnav_word()
            if not keniuoffice_page.is_tab_page_normal():
                log.log_error("word-tab展示异常")
            log.log_pass("word-tab展示正常")
            keniuoffice_page.click_leftnav_ppt()
            if not keniuoffice_page.is_tab_page_normal():
                log.log_error("ppt-tab展示异常")
            log.log_pass("ppt-tab展示正常")
            keniuoffice_page.click_leftnav_excel()
            if not keniuoffice_page.is_tab_page_normal():
                log.log_error("excel-tab展示异常")
            log.log_pass("excel-tab展示正常")
            keniuoffice_page.click_leftnav_design()
            if not keniuoffice_page.is_tab_page_normal():
                log.log_error("design-tab展示异常")
            log.log_pass("design-tab展示正常")
            keniuoffice_page.click_leftnav_sucai()
            if not keniuoffice_page.is_tab_page_normal():
                log.log_error("sucai-tab展示异常")
            log.log_pass("sucai-tab展示正常")
            keniuoffice_page.click_user_center()
            utils.perform_sleep(1)
            keniuoffice_page.click_leftnav_mydownload()
            if not keniuoffice_page.is_my_page_normal():
                log.log_error("我的下载-tab展示异常")
            log.log_pass("我的下载-tab展示正常")
            keniuoffice_page.click_leftnav_mycollection()
            if not keniuoffice_page.is_my_page_normal():
                log.log_error("我的收藏-tab展示异常")
            log.log_pass("我的收藏-tab展示正常")

        with allure.step("step4: 验证点击下载"):
            keniuoffice_page.click_leftnav_ppt()
            utils.perform_sleep(1)
            keniuoffice_page.click_download_button()
            if not keniuoffice_page.is_more_download():
                log.log_error("点击立即下载后没有新增下载记录标记")
            log.log_pass("点击立即下载后存在新增下载记录标记")

        with allure.step("step5: 验证点击收藏"):
            result_old, poslist_old = keniuoffice_page.is_collected_button_exist()
            if result_old:
                collected_num_old = len(poslist_old)
            else:
                collected_num_old = 0
            keniuoffice_page.click_collection_button()
            result_new, poslist_new = keniuoffice_page.is_collected_button_exist()
            if not result_new or len(poslist_new)<collected_num_old:
                log.log_error("点击收藏按钮后没有新增收藏记录标记")
            log.log_pass("点击收藏按钮后存在新增收藏记录标记")

        with allure.step("step6: 验证搜索页面"):
            keniuoffice_page.click_search_button()
            utils.perform_sleep(3)
            if not keniuoffice_page.is_page_show_normal():
                log.log_error("搜索页面展示异常")
            log.log_pass("搜索页面展示正常")
            keniuoffice_page.click_mainpage_tab()


@allure.epic(f"可牛办公独立版基础用例测试({config.ENV.value})")
@allure.feature('可牛办公独立版基础用例测试---卸载验证')
class TestKeniuOfficeUninstall(object):
    @allure.story('可牛办公独立版基础用例测试---卸载验证')
    def test_keniuoffice_uninstall(self,get_environment):
        allure.dynamic.description(
            '\tstep1: 调起卸载程序\n'
            '\tstep2: 卸载可牛办公\n'
            '\tstep3: 从文件路径判断是否卸载成功\n'
        )

        with allure.step('step1: 调起卸载程序'):
            uninstall_page = KeniuOfficeUninstallPage()
            if not uninstall_page.is_uninstall_page_exist():
                log.log_error("卸载界面展示异常")
            log.log_pass("卸载界面展示正常")
            uninstall_page.click_uninstall_button()

        with allure.step("step2: 卸载可牛办公"):
            uninstall_page.click_uninstall_button()
            if not uninstall_page.is_uninstall_finished():
                log.log_error("60s内未卸载完成")
            log.log_pass("卸载完成")
            utils.perform_sleep(1)
            uninstall_page.click_uninstall_finished_button()
            utils.perform_sleep(3)

        with allure.step("step3: 从文件路径判断是否卸载成功"):
            if not uninstall_page.is_keniuoffice_path_exist():
                log.log_error("可牛办公ktemplate.exe文件仍存在")
            log.log_pass("可牛办公ktemplate.exe文件不存在")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])