#!/usr/bin/evn python
# --coding = 'utf-8' --
import allure
import pytest

from common import utils
from common.log import log
from common.unexpectwin_system import UnExpectWin_System
from common.utils import perform_sleep
from duba.PageObjects.fast_vc_page import FastVcPage
from duba.config import config
from duba.contants import UserType
from duba.PageObjects.driver_manager_page import DriverManagerPage
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.vip_page import vip_kaitong_page, VipKaitongPageShot
from duba.PageObjects.data_recovery_page import DataRecoveryPage
from duba.PageObjects.file_shredding_page import FileShreddingPage
from duba.PageObjects.pdf_convert_page import PDFConvertPage
from duba.PageObjects.popup_intercept_page import PopupInterceptPage
from duba.PageObjects.privacy_cleaner_page import PrivacyCleanerPage
from duba.PageObjects.c_slimming_page import CSlimmingPage
from duba.PageObjects.document_repair_page import DocumentRepairPage
from duba.PageObjects.fast_picture_page import FastPicturePage, PictureBeautificationPage
from duba.PageObjects.screen_record_page import ScreenRecordPage
from duba.PageObjects.text_to_voice_page import TextToVoicePage
from duba.PageObjects.defrag_page import DefragPage


@allure.epic(f"毒霸VIP会员页，打开独立支付页检查（{config.ENV.value}）")
@allure.feature("场景：打开VIP会员页->打开各种独立支付页")
class TestVipCenterOpenOperation(object):
    @allure.story('登录会员状态下，检查工具打开独立支付页情况')
    @pytest.mark.parametrize("user_type", [UserType.NON_VIP], indirect=True)
    def test_logout_open_tools(self, user_type):
        allure.dynamic.description(
            '\t1.打开会员中心\n'
            '\t2.登录普通用户账号\n'
            '\t3.逐个打开各工具的独立支付页\n'
        )
        allure.dynamic.title(f"检查各工具独立支付页情况，用户类型：{user_type.value}")

        with allure.step("step1：打开主界面的会员中心，登录账号"):
            log.log_info("测试前先返回桌面防止界面被挡")
            utils.keyboardInput2Key(utils.VK_CODE.get("left_win"), utils.VK_CODE.get("d"))
            login_page = LoginPage()

            # 如果登录失败就进行一次弹窗系统检测，若检测成功则再初始化一次登录界面
            if not login_page.do_user_login(user_type):
                if UnExpectWin_System().unexpectwin_detect():
                    login_page = LoginPage()
                    assert login_page.do_user_login(user_type), log.log_error("登录失败", need_assert=False)
            vp = login_page.vp
            log.log_pass(f"{user_type.value} 账号登录成功")

        with allure.step("step2：打开PDF转换独立支付页"):
            vp.pdfconvert_click()
            pdf_convert_page = PDFConvertPage(False, delay_sec=1)
            pdf_convert_page.click_login_button()
            pdf_convert_vip_page = vip_kaitong_page(page_desc="PDF转换支付")
            assert pdf_convert_vip_page.check_page_tag(VipKaitongPageShot.PDF_CONVERT.value), \
                log.log_error("PDF转换独立支付页检查失败", need_assert=False)

            log.log_info("关闭PDF转换独立支付页")
            pdf_convert_vip_page.page_del()
            log.log_info("关闭PDF转换页")
            pdf_convert_page.page_del()
            perform_sleep(1)
            log.log_pass("PDF转换独立支付页检测通过")

        with allure.step("step3: 打开C盘瘦身独立支付页"):
            vp.c_slimming_click()
            c_slimming_page = CSlimmingPage(False, delay_sec=2)
            c_slimming_page.click_upgrade_vip_button()
            c_slimming_vip_page = vip_kaitong_page(page_desc="C盘瘦身支付")
            assert c_slimming_vip_page.check_page_tag(VipKaitongPageShot.C_SLIMMING.value), \
                log.log_error("C盘瘦身独立支付页检查失败", need_assert=False)

            log.log_info("关闭C盘瘦身独立支付页")
            c_slimming_vip_page.page_del()
            log.log_info("关闭C盘瘦身页")
            c_slimming_page.page_del()
            perform_sleep(1)
            log.log_pass("C盘瘦身独立支付页检测通过")

        with allure.step("step4: 打开系统碎片清理王独立支付页"):
            vp.system_defrag_click()
            defrag_page = DefragPage(False, delay_sec=2)
            perform_sleep(5)
            defrag_page.click_login_button()
            defrag_vip_page = vip_kaitong_page(page_desc="系统碎片清理王支付", delay_sec=5)
            assert defrag_vip_page.check_page_tag(VipKaitongPageShot.DEFRAG.value), \
                log.log_error("系统碎片清理王独立支付页检查失败", need_assert=False)

            log.log_info("关闭系统碎片清理王独立支付页")
            defrag_vip_page.page_del()
            log.log_info("关闭系统碎片清理王页")
            defrag_page.page_del()
            perform_sleep(1)
            log.log_pass("系统碎片清理王独立支付页检测通过")

        with allure.step("step5: 打开文档修复独立支付页"):
            vp.file_fix_click()
            document_repair_page = DocumentRepairPage(False, delay_sec=1)
            document_repair_page.open_recharge_page()
            document_repair_vip_page = vip_kaitong_page(page_desc="文档修复支付", delay_sec=2)
            assert document_repair_vip_page.check_page_tag(VipKaitongPageShot.DOCUMENT_REPAIR.value), \
                log.log_error("文档修复独立支付页检查失败", need_assert=False)

            log.log_info("关闭文档修复独立支付页")
            document_repair_vip_page.page_del()
            log.log_info("关闭文档修复页")
            document_repair_page.page_del()
            perform_sleep(1)
            log.log_pass("文档修复独立支付页检测成功")

        with allure.step("step6: 打开文件粉碎独立支付页"):
            vp.file_shredding_click()
            file_shredding_page = FileShreddingPage(False, delay_sec=2)
            file_shredding_page.vip_center_click()
            file_shredding_vip_page = vip_kaitong_page(page_desc="文件粉碎支付", delay_sec=2)
            assert file_shredding_vip_page.check_page_tag(VipKaitongPageShot.FILE_SHREDDING.value), \
                log.log_error("文件粉碎独立支付页检查失败", need_assert=False)

            log.log_info("关闭文件粉碎独立支付页")
            file_shredding_vip_page.page_del()
            log.log_info("关闭文件粉碎页")
            file_shredding_page.page_del()
            perform_sleep(1)
            log.log_pass("文件粉碎独立支付页检测成功")

        with allure.step("step7: 打开弹窗拦截独立支付页"):
            vp.tanchuang_lanjie_click()
            popup_intercept_page = PopupInterceptPage(False, delay_sec=2)
            popup_intercept_page.click_upgrade_vip_button()
            popup_intercept_vip_page = vip_kaitong_page(page_desc="弹窗拦截支付", delay_sec=2)
            assert popup_intercept_vip_page.check_page_tag(VipKaitongPageShot.POPUP_INTERCEPT.value), \
                log.log_error("弹窗拦截独立支付页检查失败", need_assert=False)

            log.log_info("关闭弹窗拦截独立支付页")
            popup_intercept_vip_page.page_del()
            log.log_info("关闭弹窗拦截页")
            popup_intercept_page.page_del()
            perform_sleep(1)
            log.log_pass("弹窗拦截独立支付页检测成功")

        with allure.step("step8: 打开录屏大师独立支付页"):
            vp.screen_record_click()
            screen_record_page = ScreenRecordPage(False, delay_sec=5)
            screen_record_page.click_login_button()
            screen_record_vip_page = vip_kaitong_page(page_desc="录屏大师支付", delay_sec=2)
            assert screen_record_vip_page.check_page_tag(VipKaitongPageShot.SCREEN_RECORD.value), \
                log.log_error("录屏大师独立支付页检查失败", need_assert=False)

            log.log_info("关闭录屏大师独立支付页")
            screen_record_vip_page.page_del()
            log.log_info("关闭录屏大师页")
            screen_record_page.page_del()
            perform_sleep(1)
            log.log_pass("录屏大师独立支付页检测成功")

        with allure.step("step9: 打开文字转语音独立支付页"):
            vp.font_to_voice_click()
            text_to_voice_page = TextToVoicePage(False, delay_sec=3)
            text_to_voice_page.click_login_button()
            text_to_voice_vip_page = vip_kaitong_page(page_desc="文字转语音支付", delay_sec=2)
            assert text_to_voice_vip_page.check_page_tag(VipKaitongPageShot.TEXT_TO_VOICE.value), \
                log.log_error("文字转语音独立支付页检查失败", need_assert=False)

            log.log_info("关闭文字转语音独立支付页")
            text_to_voice_vip_page.page_del()
            log.log_info("关闭文字转语音页")
            text_to_voice_page.page_del()
            perform_sleep(1)
            log.log_pass("文字转语音独立支付页检测成功")

        with allure.step("step10: 打开超级隐私清理独立支付页"):
            vp.privacy_clean_click()
            privacy_cleaner_page = PrivacyCleanerPage(False, delay_sec=2)
            privacy_cleaner_page.vip_center_click()
            privacy_cleaner_vip_page = vip_kaitong_page(page_desc="超级隐私清理支付", delay_sec=2)
            assert privacy_cleaner_vip_page.check_page_tag(VipKaitongPageShot.PRIVACY_CLEANUP.value), \
                log.log_error("超级隐私清理独立支付页检查失败", need_assert=False)

            log.log_info("关闭超级隐私清理独立支付页")
            privacy_cleaner_vip_page.page_del()
            log.log_info("关闭超级隐私清理页")
            privacy_cleaner_page.page_del()
            perform_sleep(1)
            log.log_pass("超级隐私清理独立支付页检测成功")

        with allure.step("step11: 打开数据恢复独立支付页"):
            vp.data_recovery_click()
            data_recovery_page = DataRecoveryPage(False, delay_sec=2)
            data_recovery_page.open_recharge_page()
            data_recovery_vip_page = vip_kaitong_page(page_desc="数据恢复支付", delay_sec=2)
            assert data_recovery_vip_page.check_page_tag(VipKaitongPageShot.DATA_RECOVERY.value), \
                log.log_error("数据恢复独立支付页检查失败", need_assert=False)

            log.log_info("关闭数据恢复独立支付页")
            data_recovery_vip_page.page_del()
            log.log_info("关闭数据恢复页")
            data_recovery_page.page_del()
            perform_sleep(1)
            log.log_pass("数据恢复独立支付页检测成功")

        with allure.step("step12: 打开毒霸看图独立支付页"):
            vp.duba_see_pic_click()
            fast_picture_page = FastPicturePage(False, delay_sec=2)
            # 打开图片美化
            fast_picture_page.open_picture_beautification()
            picture_beautification_page = PictureBeautificationPage(False, delay_sec=2)
            # 点击会员中心
            picture_beautification_page.click_vip_center_button()
            fast_picture_vip_page = vip_kaitong_page(page_desc="毒霸看图支付", delay_sec=2)
            assert fast_picture_vip_page.check_page_tag(VipKaitongPageShot.FAST_PICTURE.value), \
                log.log_error("毒霸看图独立支付页检查失败", need_assert=False)

            log.log_info("关闭毒霸看图独立支付页")
            fast_picture_vip_page.page_del()

            log.log_info("关闭图片美化页（毒霸看图）")
            picture_beautification_page.page_del()

            log.log_info("关闭毒霸看图页")
            fast_picture_page.page_del()
            perform_sleep(1)
            log.log_pass("毒霸看图独立支付页检测成功")

        with allure.step("step13: 打开驱动管理王独立支付页"):
            vp.drive_download_click()
            driver_manager_page = DriverManagerPage(False, delay_sec=2)
            driver_manager_page.vip_center_click()
            driver_manager_vip_page = vip_kaitong_page(page_desc="驱动管理王支付", delay_sec=2)
            assert driver_manager_vip_page.check_page_tag(VipKaitongPageShot.DRIVER_MANAGER.value), \
                log.log_error("驱动管理王独立支付页检查失败", need_assert=False)

            log.log_info("关闭驱动管理王独立支付页")
            driver_manager_vip_page.page_del()
            log.log_info("关闭驱动管理王页")
            driver_manager_page.page_del()
            perform_sleep(1)
            log.log_pass("驱动管理王独立支付页检测成功")

        with allure.step("step14: 打开毒霸视频格式专家独立支付页"):
            vp.fast_vc_click()
            fast_vc_page = FastVcPage(False, delay_sec=2)
            fast_vc_page.click_vip_center_button()
            pdf_convert_vip_page = vip_kaitong_page(page_desc="PDF转换支付")
            assert pdf_convert_vip_page.check_page_tag(VipKaitongPageShot.PDF_CONVERT.value), \
                log.log_error("PDF转换独立支付页检查失败", need_assert=False)

            log.log_info("关闭毒霸视频格式专家独立支付页")
            pdf_convert_vip_page.page_del()
            log.log_info("关闭毒霸视频格式专家页")
            fast_vc_page.page_del()
            perform_sleep(1)
            log.log_pass("毒霸视频格式专家独立支付页检测通过")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
