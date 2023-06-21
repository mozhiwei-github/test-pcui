import os
from common.tools.duba_tools import find_dubapath_by_reg
import allure
import pytest
from common.log import log
from common.utils import win32gui, win32con
from duba.PageObjects.rubbish_clean_page import RubbishCleanPage
from duba.PageObjects.setting_page import SettingPage
from duba import config
from common import utils
from common.webpage import WebPage
from duba.conftest import kill_exited_process
from duba.contants import ChromeCachePath
from common.samba import Samba
from common.tools.duba_tools import deal_mainpage_close_pop

@allure.epic(f"垃圾清理功能测试（{config.ENV.value}）")
@allure.feature('场景：垃圾清理功能用例验证')
class TestRubbishClean(object):
    @allure.story('垃圾清理功能用例验证')
    def test_rubbish_clean(self, kill_exited_process):
        allure.dynamic.description(
            '\tstep1: 构造测试环境\n'
            '\tstep2: 修改配置文件规避会员弹泡\n'
            '\tstep3: 调起毒霸并打开垃圾清理\n'
            '\tstep4: 验证垃圾清理重新扫描\n'
            '\tstep5: 验证深度清理项\n'
            '\tstep6: 验证进程存在时浏览器垃圾清理场景\n'
            '\tstep7: 验证取消垃圾清理扫描\n'
        )
        allure.dynamic.title('垃圾清理功能验证')

        with allure.step("step1: 构造测试环境"):
            chrome_exists = True

            # 构建chrome浏览器垃圾缓存文件
            if utils.is_process_exists("chrome.exe"):
                utils.kill_process_by_name("chrome.exe")
            chrome_cache_path = ChromeCachePath.CHROMECACHEPATH.value
            if os.path.exists(os.path.join(chrome_cache_path, "GPUCache")):
                utils.remove_path(os.path.join(chrome_cache_path, "GPUCache"))
            sambo_o = Samba("10.12.36.203", "duba", "duba123")
            sambo_o.download_dir("TcSpace", os.path.join('autotest', 'kcleaner'), chrome_cache_path)
            log.log_info("从共享获取测试文件完成")
            if not os.path.exists(os.path.join(chrome_cache_path, "GPUCache")):
                log.log_error("从远端拉取文件存在本地失败--本地未找到对应文件")
            log.log_pass("从远端拉取文件存在本地成功--本地已找到对应文件")

            # 调起谷歌浏览器（获取chrome路径->启动chrome.exe）
            chrome_path = utils.query_reg_value(
                regpath=r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome", keyname="InstallLocation")
            if not chrome_path:
                chrome_path = utils.query_reg_value(
                    regroot=win32con.HKEY_CURRENT_USER, regpath=r"Software\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome", keyname="InstallLocation")
            if not chrome_path:
                log.log_pass("验证环境找不到chrome，请确认已安装chrome")
                chrome_exists = False
            else:
                chrome_exepath = os.path.join(chrome_path, "chrome.exe")
                os.environ['process_name'] = "chrome.exe"
                utils.process_start(chrome_exepath, async_start=True)
                utils.perform_sleep(3)
                if not utils.is_process_exists("chrome.exe"):
                    log.log_error("chrome未正常启动")
                else:
                    log.log_pass("chrome已正常启动")
            log.log_info("测试前先返回桌面防止界面被挡")
            utils.keyboardInput2Key(utils.VK_CODE.get("left_win"), utils.VK_CODE.get("d"))

            sp = SettingPage()
            sp.self_protecting_close()
            sp.page_del()
            utils.perform_sleep(2)

            # 删除本地扫描及清理记录
            ktrashud_path_old = os.path.join(find_dubapath_by_reg(), 'ktrashud_old.dat')
            if os.path.exists(ktrashud_path_old):
                utils.remove_path(ktrashud_path_old)
            ktrashud_path = os.path.join(find_dubapath_by_reg(), 'ktrashud.dat')
            os.rename(ktrashud_path, os.path.join(find_dubapath_by_reg(), 'ktrashud_old.dat'))
            log.log_info("删除本地扫描及清理记录完成")

        with allure.step("step2: 修改配置文件规避会员弹泡"):
            deal_mainpage_close_pop()
            log.log_pass("修改推广泡泡配置文件已完成")

        with allure.step("step3: 调起毒霸并打开垃圾清理"):
            rcp = RubbishCleanPage()
            if not rcp.wait_scan_finish():
                log.log_error("垃圾清理扫描出现异常，未正常完成")
            log.log_pass("垃圾清理扫描正常完成")
            # # TODO：垃圾清理扫描完成，很干净
            # if rcp.is_deep_clean_button_exist():
            #     log.log_pass("垃圾清理扫描已完成---很干净")

        with allure.step("step4: 验证垃圾清理重新扫描"):
            rcp.rescan_button_click()
            utils.mouse_move(0,0)
            if not rcp.wait_scan_finish():
                log.log_error("垃圾清理重新扫描出现异常，未正常完成")
            log.log_pass("垃圾清理重新扫描正常完成")
            # # TODO：垃圾清理扫描完成，很干净
            # if rcp.is_deep_clean_button_exist():
            #     log.log_pass("垃圾清理扫描已完成---很干净")

        with allure.step("step5: 验证深度清理项"):
            utils.perform_sleep(1)
            rcp.deep_clean_tab_click()
            utils.mouse_move(0, 0)
            if not rcp.select_checkbox_operation():
                log.log_pass("未查找到可勾选的checkbox")
            else:
                if not rcp.is_selected_window_exist():
                    log.log_error("未匹配到选择清理项弹窗")
                log.log_pass("匹配到选择清理项弹窗")
                rcp.select_checkbox_operation()
                utils.perform_sleep(1)
                rcp.sure_button_click()
                utils.mouse_move(0, 0)
                utils.perform_sleep(1)
                if rcp.is_warning_pop_exist():
                    log.log_info("识别到风险提示泡")
                    rcp.warning_pop_sure_button_click()
                    utils.perform_sleep(1)
            rcp.clean_up_button_click()
            utils.mouse_move(0, 0)
            utils.perform_sleep(1)
            if rcp.is_warning_page_exist():
                log.log_info("识别到清理风险提示窗")
                rcp.refuse_button_click()
                utils.mouse_move(0, 0)
                utils.perform_sleep(1)
                if rcp.is_warning_page_exist():
                    log.log_error("清理风险提示窗未正常关闭")
                log.log_pass("清理风险提示窗已正常关闭")
            if not rcp.wait_clean_finish():
                log.log_error("垃圾清理过程出现异常")
            log.log_pass("垃圾清理已完成")

        with allure.step("step6: 验证进程存在时浏览器垃圾清理场景"):
            if chrome_exists:
                # 判断chrome进程是否存在
                process_status = utils.is_process_exists("chrome.exe")
                result = rcp.is_result_tips_exists()
                if not result[0]:
                    log.log_error("未出现进程占用暂缓处理提示")
                rcp.result_tips_click()
                utils.perform_sleep(2)
                utils.mouse_move(result[1][0] + 70, result[1][1] + 70)
                if rcp.is_chrome_logo_exist() and process_status:
                    log.log_pass("chrome进程存在时，暂缓处理chrome垃圾文件")
                    # utils.kill_process_by_name("chrome.exe")
                else:
                    # utils.kill_process_by_name("chrome.exe")
                    log.log_error("chrome进程存在时，未暂缓处理chrome垃圾文件")
            else:
                log.log_pass("测试环境未安装chrome.exe，请手动验证该场景")

        with allure.step("step7: 验证取消垃圾清理扫描"):
            utils.perform_sleep(3)
            if not rcp.is_rescan_button_exist():
                rcp = RubbishCleanPage()
            else:
                rcp.rescan_button_click()
                utils.perform_sleep(1)
                # 暂缓处理tips会导致首次重新扫描点击用来关闭tips
                if rcp.is_rescan_button_exist():
                    rcp.rescan_button_click()
                utils.mouse_move(0, 0)
            rcp.cancel_button_click()
            utils.mouse_move(0, 0)
            utils.perform_sleep(2)
            if not rcp.is_rescan_button_exist():
                log.log_error("扫描未正常取消")
            # if not rcp.is_scan_canceled_success():
            #     log.log_error("扫描未正常取消")
            log.log_pass("扫描已被正常取消")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])