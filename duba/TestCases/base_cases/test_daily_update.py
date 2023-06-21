import os
from duba.contants import DubaVersion
import allure
import pytest
from common.tools.duba_tools import find_dubapath_by_reg
from common import utils
from common.log import log
from common.samba import Samba
from common.tools.duba_tools import deal_mainpage_close_pop
from duba.PageObjects.main_page import main_page
from duba.PageObjects.overall_scan_page import overall_scan_page
from duba.PageObjects.rubbish_clean_page import RubbishCleanPage
from duba.PageObjects.computer_accelerate_page import ComputerAcceleratePage
from duba.PageObjects.software_manage_page import SoftWareManagePage
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.setting_page import SettingPage
from duba.PageObjects.update_page import update_page
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page
from duba.PageObjects.file_shredding_page import FileShreddingPage
from duba.PageObjects.c_slimming_page import CSlimmingPage
from duba import config


@allure.epic(f'毒霸日常平滑用例验证（{config.ENV.value}）')
@allure.feature('场景：#待补充')
class TestDailyUpdate(object):
    @allure.story('1.毒霸日常平滑-毒霸主界面验证')
    def test_duba_mainpage(self):
        allure.dynamic.description(
            '\tstep1: 启动毒霸打开主界面\n'
        )
        allure.dynamic.title('毒霸日常平滑-毒霸主界面验证')

        with allure.step("step1: 启动毒霸并打开主界面,修改配置文件规避会员弹泡"):
            sp = SettingPage()
            sp.self_protecting_close()
            # 将源文件重命名
            deal_mainpage_close_pop()
            sp.page_del()
            log.log_pass("修改主界面会员弹泡配置文件已完成")

        with allure.step("step2: hover百宝箱验证"):
            mp = main_page()
            mp.hover_to_baibaoxiang()
            utils.perform_sleep(1)
            if not mp.is_baibaoxiang_pop_exist():
                if not mp.is_mainpage_version_new(DubaVersion.EXCEPTVERSION.value):
                    log.log_error("不存在百宝箱hover框")
                log.log_pass("当前为新版本界面内，不存在百宝箱hover框")
            else:
                log.log_pass("存在百宝箱hover框")

    @allure.story('2.毒霸日常平滑-全面扫描验证')
    def test_overscan(self):
        allure.dynamic.description(
            '\tstep1: 从主界面调起全面扫描进行扫描\n'
            '\tstep2: 全面扫描后进行修复\n'
            '\tstep3: 判断修复结果页是否符合预期\n'
            '\tstep4: 从扫描结果页返回首页\n'
        )
        allure.dynamic.title('毒霸日常平滑-全面扫描验证')

        with allure.step("step1: 从主界面调起全面扫描进行扫描"):
            # 关闭自保护确保存在修复项
            osp = overall_scan_page(close_protect=True)
            if not osp.wait_scan_finish():
                log.log_error("全面扫描未正常完成")
            log.log_pass("全面扫描正常完成")

        with allure.step("step2: 全面扫描后进行修复"):
            utils.perform_sleep(2)
            osp.overall_fix_click()
            if not osp.wait_fix_finish():
                log.log_error("一键修复未正常完成")
            log.log_pass("一键修复正常完成")

        with allure.step("step3: 判断修复结果页是否符合预期"):
            # 推荐项在自动滚动后出现
            utils.perform_sleep(3)
            if not osp.is_fully_recovered():
                if not osp.check_fix_result_recommend():
                    log.log_error("未完全修复但未存在及展示推荐开启项")
                log.log_pass("修复结果页符合预期")
            elif osp.check_fix_result_recommend():
                log.log_error("完全修复但存在推荐项")
            else:
                log.log_pass("修复结果页符合预期")

        with allure.step("step4: 从扫描结果页返回首页"):
            osp.ignore_button_click()
            utils.perform_sleep(1)
            osp.return_homepage_click()
            utils.perform_sleep(1)
            if not osp.is_overscan_button_exist():
                log.log_error("未正常返回至首页")
            log.log_pass("已正确返回首页")

    @allure.story("3.毒霸日常平滑-垃圾清理验证")
    def test_rubbish_clean(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸并打开垃圾清理\n'
            '\tstep2: 在垃圾清理结果页进行垃圾清理\n'
            '\tstep3: 退出垃圾清理返回首页\n'
        )
        allure.dynamic.title('毒霸日常平滑-垃圾清理验证')

        with allure.step("step1: 调起毒霸并打开垃圾清理"):
            rcp = RubbishCleanPage()
            if not rcp.wait_scan_finish():
                log.log_error("垃圾清理扫描未正常完成")
            log.log_pass("垃圾清理扫描已完成")

        with allure.step("step2: 在垃圾清理结果页进行垃圾清理"):
            rcp.clean_up_button_click()
            if rcp.is_warning_page_exist():
                log.log_info("识别到清理风险提示窗")
                utils.perform_sleep(1)
                rcp.refuse_button_click()
                utils.perform_sleep(1)
                if rcp.is_warning_page_exist():
                    log.log_error("清理风险提示窗关闭失败")
                log.log_pass("清理风险提示窗关闭成功")
            else:
                log.log_info("未弹出清理风险提示窗")
            utils.perform_sleep(1)
            if not rcp.wait_clean_finish():
                log.log_error("垃圾清理未正常完成")
            log.log_pass("垃圾清理已完成")

        with allure.step("step3: 退出垃圾清理返回首页"):
            if not rcp.is_deep_clean_button_exist():
                rcp.entry_homepage_button_click()
            else:
                rcp.return_button_click()
            utils.perform_sleep(2)
            if not rcp.is_rubbish_clean_tab_exist():
                log.log_error("未正常返回首页")
            log.log_pass("已返回首页")


    @allure.story("4.毒霸日常平滑-电脑加速验证")
    def test_computer_accelerate(self, kill_exited_process):
        allure.dynamic.description(
            '\tstep1: 从云端下拉测试文件并启动\n'
            '\tstep2: 调起毒霸并打开电脑加速\n'
            '\tstep3: 在电脑加速扫描结果页进行加速\n'
            '\tstep4: 加速完成后返回首页\n'
        )
        allure.dynamic.title('毒霸日常平滑-电脑加速验证')

        with allure.step("step1: 从云端下拉测试文件并启动"):
            # 确保存在默认的加速项
            speed_tool_path = os.path.join(os.getcwd(), "SpeedTool")
            if os.path.exists(speed_tool_path):
                utils.remove_path(speed_tool_path)
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            samba_o.download_dir("TcSpace", os.path.join('autotest', 'duba_fast_speed'), speed_tool_path)
            test1_path = os.path.join(speed_tool_path, 'test1.exe')
            bctester_ch_path = os.path.join(speed_tool_path, 'bctester-ch.exe')
            bctester_zh_path = os.path.join(speed_tool_path, 'bctester-zh.exe')
            log.log_pass("从远端拉取文件完成")
            if not os.path.exists(test1_path) and os.path.exists(bctester_zh_path) and os.path.exists(bctester_ch_path):
                log.log_error("从远端拉取文件存在本地失败--本地未找到对应文件")
            log.log_pass("从远端拉取文件存在本地成功--本地已找到对应文件")

            utils.process_start(process_path=bctester_ch_path, async_start=True)
            os.environ['process_name'] = "bctester-ch.exe"
            utils.perform_sleep(2)

        with allure.step("step2: 调起毒霸并打开电脑加速"):
            cap = ComputerAcceleratePage()
            if not cap.wait_accelerate_scan_finish():
                log.log_error("电脑加速扫描未正常完成")
            log.log_pass("电脑加速扫描正常完成")

        with allure.step("step3: 在电脑加速扫描结果页进行加速"):
            cap.click_accelerate_button()
            if not cap.wait_accelerate_finish():
                log.log_error("电脑加速未正常完成")
            log.log_pass("电脑加速正常完成")

        with allure.step("step4: 加速完成后返回首页"):
            cap.click_return_mainpage_button()
            utils.perform_sleep(1)
            if not cap.is_accelerate_tab_exist():
                log.log_error("未正常返回首页")
            log.log_pass("已正常返回首页")

    @allure.story("5.毒霸日常平滑-软件管家验证")
    def test_software_manage(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸并打开软件管家\n'
        )
        allure.dynamic.title('毒霸日常平滑-软件管家验证')

        with allure.step("step1: 调起毒霸并打开软件管家"):
            smp = SoftWareManagePage()
            utils.perform_sleep(1)
            if not smp.close_recommend_pop():
                log.log_error("软管推荐分发泡泡未正常关闭")
            log.log_pass("软管推荐分发泡泡已关闭")

    @allure.story("6.毒霸日常平滑-会员中心验证")
    def test_vip_center(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸并打开会员中心\n'
        )
        allure.dynamic.title('毒霸日常平滑-会员中心验证')

        with allure.step("step1: 调起毒霸并打开会员中心"):
            vipp = vip_page()
            utils.perform_sleep(1)
            vipp.page_confirm_close()

    @allure.story("7.毒霸日常平滑-设置中心验证")
    def test_setting_menu(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸并打开设置中心\n'
        )
        allure.dynamic.title('毒霸日常平滑-设置中心验证')

        with allure.step("step1: 调起毒霸并打开设置中心"):
            sp = SettingPage()

    @allure.story("8.毒霸日常平滑-升级程序验证")
    def test_update_program(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸并打开升级程序\n'
        )
        allure.dynamic.title('毒霸日常平滑-升级程序验证')

        with allure.step("step1: 调起毒霸并打开升级程序"):
            up = update_page()

    @allure.story("9.毒霸日常平滑-百宝箱文件粉碎验证")
    def test_baibaoxiang_filedestroy(self):
        allure.dynamic.description(
            '\tstep1: 调起毒霸设置页并关闭毒霸自保护\n'
            '\tstep2: 构造测试环境\n'
            '\tstep3: 在百宝箱中打开文件粉碎功能\n'
        )
        allure.dynamic.title('毒霸日常平滑-百宝箱文件粉碎验证')

        with allure.step("step1: 调起毒霸设置页并关闭毒霸自保护"):
            sp = SettingPage()
            sp.self_protecting_close()
            sp.page_del()

        with allure.step("step2: 构造测试环境"):
            build_result = False
            duba_path = find_dubapath_by_reg()
            update_path = os.path.join(duba_path, "update")
            kfiledestroy_path = os.path.join(duba_path, "kfiledestroy.exe")
            kfiledestroy64_path = os.path.join(duba_path, "kfiledestroy.exe")
            utils.remove_path(update_path)
            utils.perform_sleep(1)
            if not os.path.exists(update_path):
                build_result = True
                log.log_info("update目录删除成功")
            utils.remove_path(kfiledestroy_path)
            utils.perform_sleep(1)
            if not os.path.exists(kfiledestroy_path):
                build_result = True
                log.log_info("kfiledestroy.exe删除成功")
            utils.remove_path(kfiledestroy64_path)
            utils.perform_sleep(1)
            if not os.path.exists(kfiledestroy64_path):
                build_result = True
                log.log_info("kfiledestroy64.exe删除成功")
            if not build_result:
                log.log_error("测试环境构造异常")
            log.log_pass("测试环境构造成功")

        with allure.step("step3: 在百宝箱中打开文件粉碎功能"):
            fdp = FileShreddingPage(from_bbx=True)

    @allure.story("10.毒霸日常平滑-百宝箱C盘瘦身验证")
    def test_baibaoxiang_C(self):
        allure.dynamic.description(
            '\tstep1: 从百宝箱调起C盘瘦身\n'
        )
        allure.dynamic.title('毒霸日常平滑-百宝箱C盘瘦身验证')

        with allure.step("step1: 从百宝箱调起C盘瘦身"):
            csp = CSlimmingPage(from_bbx=True)
            utils.perform_sleep(2)
            if not csp.is_C_slimming_main_page():
                log.log_error("C盘瘦身界面未正常展示主界面")
            log.log_pass("C盘瘦身界面展示正常")
            csp.exit_button_click()
            utils.perform_sleep(1)
            if csp.is_exit_sure_pop_exist():
                if not csp.close_exit_sure_pop():
                    log.log_error("退出确认框没有正常关闭")
                log.log_pass("退出确认框已正常关闭")


    @allure.story("11.毒霸日常平滑-百宝箱快捷工具设置验证")
    def test_tools_set(self):
        allure.dynamic.description(
            '\tstep1: 配置快捷工具\n'
            '\tstep2: 验证首页快捷工具配置生效\n'
        )
        allure.dynamic.title('毒霸日常平滑-百宝箱快捷工具设置验证')
        with allure.step("step1: 配置快捷工具"):
            bbxp = baibaoxiang_page()
            bbxp.tools_update_button_click()
            utils.perform_sleep(1)
            bbxp.delete_setted_tools()
            log.log_pass("删除已存在配置完成")

        with allure.step("step2: 验证添加工具至常用工具栏操作"):
            utils.perform_sleep(1)
            if not bbxp.set_tools():
                log.log_error("添加工具至常用工具栏操作验证失败")
            log.log_pass("添加工具至常用工具栏操作验证成功")
            utils.perform_sleep(1)
            bbxp.return_homepage()


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])



















