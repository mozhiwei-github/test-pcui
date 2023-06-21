import os
import pytest
from common import utils
import allure
from common.samba import Samba
from duba.config import config
from duba.PageObjects.software_manage_page import SoftWareManagePage
from common.log import log


@allure.epic(f"软件管家功能用例测试({config.ENV.value})")
@allure.feature('软件管家功能用例测试')
class TestSoftwareManage(object):
    @allure.story('软件管家功能用例验证')
    def test_software_manage(self):
        allure.dynamic.description(
            '\t1. 软件管家首页展示及刷新正常\n'
            '\t2. 验证首页轮播banner轮播是否正常\n'
            '\t3. 软件安装验证-一键安装及安装\n'
            '\t4. 查看全部tab界面展示\n'
            '\t5. 在全部tab安装软件\n'
            '\t6. 在详情页安装软件\n'
            '\t7. 在卸载页面卸载软件\n'
            '\t8. 验证软件升级\n'
        )
        allure.dynamic.title('软件管家功能用例测试')

        with allure.step("step1: 软件管家首页展示及刷新正常"):
            smp = SoftWareManagePage()
            utils.perform_sleep(3)
            # 若存在推荐泡泡需要先关闭
            if not smp.close_recommend_pop():
                log.log_error("推荐弹窗关闭异常")
            log.log_pass("推荐弹窗关闭成功")
            if not smp.is_page_show_normal():
                log.log_error("软件管家首页界面展示异常")
            log.log_pass("软件管家首页界面展示正常")
            # TODO:需要将界面显示错误后点击刷新按钮刷新界面
            # TODO:存在像素点color为白色的时候---结果为存在轮播图片展示空白---fail
            smp.click_reload_button()
            utils.perform_sleep(2)
            if not smp.is_page_show_normal():
                log.log_error("点击刷新-软件管家首页界面展示异常")
            log.log_pass("点击刷新-软件管家首页界面展示正常")

        with allure.step("step2: 验证首页轮播banner轮播是否正常"):
            result = smp.is_shlidshow_normal()
            if not result:
                log.log_error("首页轮播banner轮播异常")
            log.log_pass("首页轮播banner轮播正常")


        with allure.step("step3: 首页软件安装验证-一键安装及安装"):
            log.log_info("点击安装可牛办公验证 安装-非静默")
            if not smp.install_keniuoffice_from_mainpage():
                log.log_error("在首页点击安装可牛办公验证 安装-非静默---安装异常")
            log.log_pass("在首页点击安装可牛办公验证 安装-非静默---安装成功")
            log.log_info("在首页点击安装腾讯视频验证 一键安装---静默")
            if not smp.install_tencent_video_from_mainpage():
                log.log_error("在首页点击安装腾讯视频验证 一键安装-静默---安装异常")
            log.log_pass("在首页点击安装腾讯视频验证 一键安装-静默---安装成功")

        with allure.step("step4: 查看全部tab界面展示"):
            smp.click_all_tab()
            utils.perform_sleep(1)
            if not smp.is_page_show_normal():
                log.log_error("全部tab界面未正常展示")
            log.log_pass("全部tab界面展示正常")

        with allure.step("step5: 在全部tab安装软件"):
            # Uninstall the software firstly
            smp.uninstall_keniuoffice_and_tencentvideo()
            utils.perform_sleep(3)
            smp.click_logo()
            log.log_info("在全部tab点击安装可牛办公验证 安装---非静默")
            if not smp.install_keniuoffice_from_alltab():
                log.log_error("在全部tab点击安装可牛办公验证 安装-非静默---安装异常")
            log.log_pass("在全部tab点击安装可牛办公验证 安装-非静默---安装成功")
            smp.click_logo()
            log.log_info("在全部tab点击安装腾讯视频验证 一键安装---静默")
            if not smp.install_tencentvideo_from_alltab():
                log.log_error("在全部tab点击安装腾讯视频验证 一键安装-静默---安装异常")
            log.log_pass("在全部tab点击安装腾讯视频验证 一键安装-静默---安装成功")

        with allure.step("step6: 在详情页安装软件"):
            utils.perform_sleep(3)
            # Uninstall the software firstly
            smp.uninstall_keniuoffice_and_tencentvideo()
            utils.perform_sleep(3)
            smp.click_logo()
            log.log_info("在详情页点击安装可牛办公验证 安装---非静默")
            if not smp.install_keniuoffice_from_detail():
                log.log_error("在详情页点击安装可牛办公验证 安装-非静默---安装异常")
            log.log_pass("在详情页点击安装可牛办公验证 安装-非静默---安装成功")
            smp.click_logo()
            log.log_info("在详情页点击安装腾讯视频验证 一键安装---静默")
            if not smp.install_tencentvideo_from_detail():
                log.log_error("在详情页点击安装腾讯视频验证 一键安装-静默---安装异常")
            log.log_pass("在详情页点击安装腾讯视频验证 一键安装-静默---安装成功")

        with allure.step("step7: 在卸载页面卸载软件"):
            utils.perform_sleep(3)
            smp.uninstall_keniuoffice_and_tencentvideo()

        with allure.step("step8: 验证软件升级"):
            winrar_regpath = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\WinRAR archiver"
            # 远端拉取低版本winrar安装包
            old_winrar_path = os.path.join(os.getcwd(), "OldWinrar")
            if os.path.exists(old_winrar_path):
                utils.remove_path(old_winrar_path)
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            samba_o.download_dir("TcSpace", os.path.join('autotest','duba_software_manage'), old_winrar_path)
            winrar_path = os.path.join(old_winrar_path, 'winrar_6.1.0.0.exe')
            log.log_pass("远端拉取安装包完成")
            if not os.path.exists(winrar_path):
                log.log_error("从远端拉取文件存在本地失败--本地未找到对应文件")
            log.log_pass("从远端拉取文件存在本地成功--本地已找到对应文件")
            # 安装低版本winrar
            winrar_path_new = os.path.join(old_winrar_path, '60040196_6.11.0.0.exe')
            os.rename(winrar_path, winrar_path_new)
            if not smp.install_old_winrar(winrar_path_new):
                log.log_error("旧版winrar安装失败")
            log.log_pass("旧版winrar安装成功")
            old_version = utils.query_reg_value(regpath=winrar_regpath, keyname="DisplayVersion")
            utils.perform_sleep(3)
            smp.click_update_tab()
            if smp.update_winrar_from_update():
                utils.perform_sleep(5)
                new_version = utils.query_reg_value(regpath=winrar_regpath, keyname="DisplayVersion")
                if not new_version == old_version:
                    log.log_pass("旧版winrar升级成功")
                else:
                    log.log_info(f"old_version:{old_version}")
                    log.log_info(f"new_version:{new_version}")
                    log.log_error("旧版winrar升级失败")
            else:
                log.log_error("旧版winrar升级失败")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])