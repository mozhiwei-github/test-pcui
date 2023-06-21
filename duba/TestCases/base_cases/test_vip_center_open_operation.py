#!/usr/bin/evn python
# --coding = 'utf-8' --
import allure
import pytest

from common import utils
from duba.contants import UserType, Env
from common.log import log
from common.utils import perform_sleep
from duba.config import config
from duba.PageObjects.fast_vc_page import FastVcPage
from duba.PageObjects.driver_manager_page import DriverManagerPage
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.data_recovery_page import DataRecoveryPage
from duba.PageObjects.file_shredding_page import FileShreddingPage
from duba.PageObjects.pdf_convert_page import PDFConvertPage
from duba.PageObjects.popup_intercept_page import PopupInterceptPage
from duba.PageObjects.pure_no_ad_page import PureNoADPage
from duba.PageObjects.privacy_cleaner_page import PrivacyCleanerPage
from duba.PageObjects.file_protect_page import FileProtectPage
from duba.PageObjects.c_slimming_page import CSlimmingPage
from duba.PageObjects.browser_home_protect_page import BrowserHomeProtectPage
from duba.PageObjects.document_repair_page import DocumentRepairPage
from duba.PageObjects.document_protect_page import DocumentProtectPage
from duba.PageObjects.privacy_shield_page import PrivacyShieldPage
from duba.PageObjects.privacy_no_trace_page import PrivacyNoTracePage
from duba.PageObjects.right_menu_mgr_page import RightMenuMgrPage
from duba.PageObjects.fast_picture_page import FastPicturePage
from duba.PageObjects.screen_record_page import ScreenRecordPage
from duba.PageObjects.network_speed_page import NetworkSpeedPage
from duba.PageObjects.text_to_voice_page import TextToVoicePage
from duba.PageObjects.trash_auto_clean_page import TrashAutoCleanPage
from duba.PageObjects.defrag_page import DefragPage
from duba.PageObjects.teen_mode_page import TeenModePage

# 目前正式服只有游客和非会员账号
USER_TYPE_LIST = UserType if config.ENV == Env.TEST else [UserType.NON_VIP]


@allure.epic(f"毒霸VIP会员页，打开工具检查（{config.ENV.value}）")
@allure.feature("场景：打开VIP会员页->打开各种工具")
class TestVipCenterOpenOperation(object):
    @allure.story('各种账号状态下检查工具打开情况')
    @pytest.mark.parametrize("user_type", USER_TYPE_LIST, indirect=True)
    def test_user_open_tools(self, user_type):
        allure.dynamic.description(
            '\t1.打开会员中心\n'
            f'\t2.切换为{user_type.value}账号\n'
            '\t3.逐个打开关闭各工具\n'
        )
        allure.dynamic.title(f'检查各工具打开情况，用户类型：{user_type.value}')
        log.log_info("测试前先返回桌面防止界面被挡")
        utils.keyboardInput2Key(utils.VK_CODE.get("left_win"), utils.VK_CODE.get("d"))

        if user_type == UserType.GUEST:
            with allure.step("step1：打开主界面的会员中心，退出登录状态"):
                vp = vip_page()
                logout_result = True
                if not vp.is_guest_user():
                    logout_result = vp.logout()
                assert logout_result, log.log_error("退出登录失败", need_assert=False)
                perform_sleep(2)
                # 检查限时福利的弹窗，如果有就直接关闭
                if UnexpectedPopup.popup_process(UnexpectedPopupInfo.TIME_LIMITED_BENEFITS, hwnd=vp.hwnd):
                    perform_sleep(1)
                log.log_pass("切换为游客状态成功")
        else:
            with allure.step("step1：打开主界面的会员中心，登录账号"):
                login_page = LoginPage()
                assert login_page.do_user_login(user_type), log.log_error("登录失败", need_assert=False)
                vp = login_page.vp
                log.log_pass(f"{user_type.value} 账号登录成功")

        with allure.step("step2：打开数据恢复"):
            vp.data_recovery_click()
            data_recovery_page = DataRecoveryPage(False)
            data_recovery_page.page_del()
            log.log_pass("数据恢复页检测通过")
            perform_sleep(2)

        with allure.step("step3：打开文件粉碎"):
            vp.file_shredding_click()
            file_shredding_page = FileShreddingPage(False)
            file_shredding_page.page_del()
            log.log_pass("文件粉碎页检测通过")
            perform_sleep(2)

        with allure.step("step4：打开广告拦截"):
            vp.tanchuang_lanjie_click()
            popup_intercept_page = PopupInterceptPage(False)
            popup_intercept_page.page_del()
            log.log_pass("广告拦截页检测通过")
            perform_sleep(2)

        with allure.step("step5：打开PDF转换"):
            vp.pdfconvert_click()
            pdf_convert_page = PDFConvertPage(False, delay_sec=1)
            pdf_convert_page.page_del()
            log.log_pass("PDF转换页检测通过")
            perform_sleep(2)

        # with allure.step("step6：打开纯净无广告"):
        #     vp.pure_no_ad_click()
        #     pure_no_ad_page = PureNoADPage(False)
        #     pure_no_ad_page.page_del()
        #     log.log_pass("纯净无广告页检测通过")
        #     perform_sleep(2)

        with allure.step("step7：打开超级隐私清理"):
            vp.privacy_clean_click()
            privacy_cleaner_page = PrivacyCleanerPage(False)
            privacy_cleaner_page.page_del()
            log.log_pass("超级隐私清理页检测通过")
            perform_sleep(2)

        with allure.step("step8：打开文件夹加密"):
            vp.file_encode_click()
            file_protect_page = FileProtectPage(False)
            file_protect_page.page_del()
            log.log_pass("文件夹加密页检测通过")
            perform_sleep(2)

        with allure.step("step9：打开C盘瘦身专家"):
            vp.c_slimming_click()
            c_slimming_page = CSlimmingPage(False, delay_sec=5)
            c_slimming_page.page_del()
            log.log_pass("C盘瘦身专家页检测通过")
            perform_sleep(2)

        with allure.step("step10：打开浏览器主页修复"):
            vp.browser_mainpage_fix_click()
            browser_home_protect_page = BrowserHomeProtectPage(False)
            browser_home_protect_page.page_del()
            log.log_pass("浏览器主页修复页检测通过")
            perform_sleep(2)

        with allure.step("step11：打开文档修复"):
            vp.file_fix_click()
            document_repair_page = DocumentRepairPage(False, delay_sec=5)
            document_repair_page.page_del()
            log.log_pass("文档修复页检测通过")
            perform_sleep(2)

        with allure.step("step12：打开文档保护"):
            vp.file_guard_click()
            document_protect_page = DocumentProtectPage(False, delay_sec=2)
            document_protect_page.page_del()
            log.log_pass("文档保护页检测通过")
            perform_sleep(2)

        with allure.step("step13：打开隐私护盾"):
            vp.privacy_shield_click()
            perform_sleep(2)
            privacy_shield_page = PrivacyShieldPage(False)
            privacy_shield_page.page_del()
            log.log_pass("隐私护盾页检测通过")
            perform_sleep(2)

        with allure.step("step14：打开隐私无痕模式"):
            vp.privacy_notrace_click()
            privacy_no_trace_page = PrivacyNoTracePage(False)
            privacy_no_trace_page.page_del()
            log.log_pass("隐私无痕模式页检测通过")
            perform_sleep(2)

        with allure.step("step15：打开右键菜单管理"):
            vp.right_mouse_menu_click()
            right_menu_mgr_page = RightMenuMgrPage(False)
            right_menu_mgr_page.page_del()
            log.log_pass("右键菜单管理页检测通过")
            perform_sleep(2)

        with allure.step("step16：打开毒霸看图"):
            vp.duba_see_pic_click()
            fast_picture_page = FastPicturePage(False)
            fast_picture_page.page_del()
            log.log_pass("毒霸看图页检测通过")
            perform_sleep(2)

        with allure.step("step17：打开录屏大师"):
            vp.screen_record_click()
            screen_record_page = ScreenRecordPage(False, delay_sec=5)  # 录屏大师工具打开较慢
            screen_record_page.page_del()
            log.log_pass("录屏大师页检测通过")
            perform_sleep(2)

        with allure.step("step18：打开网络优化"):
            vp.network_speed_click()
            network_speed_page = NetworkSpeedPage(False)
            network_speed_page.page_del()
            log.log_pass("网络优化页检测通过")
            perform_sleep(2)

        with allure.step("step19：打开文字转语音"):
            vp.font_to_voice_click()
            text_to_voice_page = TextToVoicePage(False, delay_sec=3)  # 文字转语音工具打开较慢
            text_to_voice_page.page_del()
            log.log_pass("文字转语音页检测通过")
            perform_sleep(2)

        with allure.step("step20：打开自动清理垃圾"):
            vp.auto_clean_crash_click()
            trash_auto_clean_page = TrashAutoCleanPage(False, delay_sec=1)
            trash_auto_clean_page.page_del()
            log.log_pass("自动清理垃圾页检测通过")
            perform_sleep(2)

        with allure.step("step21：打开系统碎片清理王"):
            vp.system_defrag_click()
            defrag_page = DefragPage(False, delay_sec=5)
            defrag_page.page_del()
            log.log_pass("系统碎片清理王页检测通过")
            perform_sleep(2)

        with allure.step("step22：打开孩子守护王"):
            vp.teen_mode_click()
            teen_mode_page = TeenModePage(False)
            teen_mode_page.page_del()
            log.log_pass("孩子守护王页检测通过")
            perform_sleep(2)

        with allure.step("step23：打开驱动管理王"):
            vp.drive_download_click()
            driver_manager_page = DriverManagerPage(False)
            driver_manager_page.page_del()
            log.log_pass("驱动管理王页检测通过")
            perform_sleep(2)

        with allure.step("step24：打开毒霸视频格式专家"):
            vp.fast_vc_click()
            fast_vc_page = FastVcPage(False)
            fast_vc_page.page_del()
            log.log_pass("毒霸视频格式专家页检测通过")
            perform_sleep(2)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
