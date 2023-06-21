import allure
import pytest
import time
from duba.config import config
from common import utils
from common.log import log
from duba.PageObjects.overall_scan_page import overall_scan_page
from common.unexpectwin_system import UnExpectWin_System
from common.tools.duba_tools import deal_mainpage_close_pop
from duba.utils import close_duba_self_protecting



@allure.epic(f"全面扫描功能测试（{config.ENV.value}）")
@allure.feature('场景：判断关闭自保护后检测结果及修复后的自保护状态')
class TestOverAllScan(object):
    @allure.story('全面扫描基础功能验证')
    def test_overall_scan(self):
        allure.dynamic.description(
            '\t1.修改相关配置文件以屏蔽一些推广泡泡\n'
            '\t2.打开全面扫描界面并进行扫描至扫描完成\n'
            '\t3.判断扫描结果与自保护状态是否一致\n'
            '\t4.点击修复并返回主界面\n'
            '\t5.判断修复后自保护是否恢复\n'
            '\t6.检测扫描中断情况\n'
        )
        allure.dynamic.title('全面扫描功能测试')

        with allure.step("step1:修改相关配置文件以屏蔽一些推广泡泡"):
            close_duba_self_protecting()
            deal_mainpage_close_pop()
            log.log_pass("推广泡泡配置修改已完成")

        with allure.step("step2:打开全面扫描界面并进行扫描至扫描完成"):
            protect_status = False
            scan_page = overall_scan_page(close_protect=True)
            while scan_page.check_scan_status():
                #log.log_info("全面扫描进行中")
                time.sleep(3)
            log.log_pass("全面扫描已完成")

        with allure.step("step3:判断扫描结果与自保护状态是否一致"):
            scan_result_status = False # 扫描结果：系统防护未开启
            if not scan_page.check_protect_status():
                scan_result_status = True # 扫描结果：系统防护已开启
            if scan_result_status == protect_status:
                log.log_pass("全面扫描功能正常--自保护状态和扫描状态一致")
            else:
                log.log_error("全面扫描功能正常--自保护状态和扫描状态不一致")

        with allure.step("step4:点击修复并返回主界面"):
            scan_page.overall_fix_click()
            while not scan_page.check_fix_result():
                # 一键修复进行中
                time.sleep(3)
            log.log_info("一键修复已完成")
            #scan_page.return_homepage()

        with allure.step("step5:判断修复后自保护是否恢复"):
            if not scan_page.check_self_protect_status():
                log.log_error("修复后自保护尚未开启")
            log.log_pass("修复后自保护已开启")
            scan_page.setting_page_close_button_click()
            log.log_info("点击关闭设置页")
            scan_page.return_homepage()
            utils.perform_sleep(3)
            UnExpectWin_System().unexpectwin_detect()

        with allure.step("step6:检测扫描中断情况"):
            scan_page.click_overall_button()
            scan_page.click_cancel_button()
            utils.perform_sleep(2)
            if scan_page.is_exitpop_exist():
                log.log_pass("中断扫描过程后存在确认框")
                log.log_info("等待30s以判断是否维持在中断状态")
                utils.perform_sleep(30)
                if not scan_page.is_exitpop_exist():
                    log.log_error("中断30s过程中出现异常，未维持在中断状态")
                log.log_pass("中断30s过程中，依旧处于中断状态")
                if scan_page.click_exitoverscan_button():
                    UnExpectWin_System().unexpectwin_detect()
                    if not scan_page.is_overscan_button_exist():
                        if scan_page.is_recovery_once_button_exist():
                            scan_page.overall_fix_click()
                            if scan_page.wait_fix_finish():
                                scan_page.ignore_button_click()
                                if not scan_page.is_overscan_button_exist():
                                    log.log_error("未检测到全面扫描按钮---未返回主页")
                    log.log_pass("检测到全面扫描按钮---已返回主页")
                else:
                    log.log_error("关闭中断扫描确认框失败")
            elif scan_page.is_return_button_exist() or scan_page.is_recovery_once_button_exist():
                log.log_pass("扫描过程较短，无法验证中断扫描场景，请手动检查此项")
            else:
                log.log_error("中断扫描过程后未出现确认框")



if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])




