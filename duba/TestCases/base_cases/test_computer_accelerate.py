import allure
import pytest

from common import utils
from common.tools.duba_tools import find_dubapath_by_reg
from duba.PageObjects.computer_accelerate_page import defend_pop_operation, ComputerAcceleratePage
from common.samba import Samba
from duba.config import config
import os
from common.log import log
from common.utils import remove_path, process_start, set_reg_value, query_reg_value, is_reg_exist, remove_reg_key, \
    is_process_exists
import time
from common.tools.duba_tools import deal_mainpage_close_pop
from duba.utils import close_duba_self_protecting, kill_duba_page_process


@allure.epic(f'毒霸电脑加速基础用例验证（{config.ENV.value}）')
@allure.feature('场景：电脑加速基础核心用例验证')
class TestComputerAccelerate(object):
    @allure.story('1.毒霸电脑加速基础用例验证')
    def test_computer_accelerate(self, kill_exited_process):
        allure.dynamic.description(
            '\tstep1: 从远端获取文件并存在本地\n'
            '\tstep2: 关闭若干推广泡泡开关"\n'
            '\tstep3：在注册表中添加启动项配置\n'
            '\tstep4：调起毒霸进行电脑加速\n'
            '\tstep5: 检测扫描结果是否符合预期\n'
            '\tstep6: 点击一键加速并判断结果\n'
            '\tstep7: 构造验证运行加速环境\n'
            '\tstep8: 验证运行加速扫描结果中是否存在检测项\n'
            '\tstep9: 验证加速后进程状态\n'

        )
        allure.dynamic.title('毒霸电脑加速基础用例验证')

        with allure.step("step1: 从远端获取文件并存在本地"):
            speed_tool_path = os.path.join(os.getcwd(), "SpeedTool")
            if os.path.exists(speed_tool_path):
                remove_path(speed_tool_path)
            samba_o = Samba("10.12.36.203", "duba","duba123")
            samba_o.download_dir("TcSpace", os.path.join('autotest','duba_fast_speed'), speed_tool_path)
            test1_path = os.path.join(speed_tool_path, 'test1.exe')
            bctester_ch_path = os.path.join(speed_tool_path, 'bctester-ch.exe')
            bctester_zh_path = os.path.join(speed_tool_path, 'bctester-zh.exe')
            log.log_pass("从远端拉取文件完成")
            if not os.path.exists(test1_path) and os.path.exists(bctester_zh_path) and os.path.exists(bctester_ch_path):
                log.log_error("从远端拉取文件存在本地失败--本地未找到对应文件")
            log.log_pass("从远端拉取文件存在本地成功--本地已找到对应文件")

        with allure.step("step2: 关闭若干推广泡泡开关"):
            close_duba_self_protecting()
            log.log_info("通过修改相关配置文件关闭若干主功能使用后界面关闭推广泡泡")
            deal_mainpage_close_pop()
            log.log_info("关闭推广泡配置已完成")

        with allure.step("step3：在注册表中添加启动项配置"):
            log.log_info("规避环境添加自启动项被毒霸本身规避的因素")
            kill_duba_page_process(excludeKislive=False)
            file_path = os.path.join(find_dubapath_by_reg(), 'data', 'bksq.dat')
            time.sleep(3)
            remove_path(file_path)
            log.log_pass("删除bksg.dat文件成功")
            log.log_info("往注册表中增加测试启动项配置")
            run_reg_path = r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run'
            set_result = set_reg_value(regpath=run_reg_path, keyname='test1', value=test1_path)
            # 由于毒霸服务存在会导致在添加启动项验证时出现防御弹窗，故采用点击弹窗的形式规避
            defend_pop_operation()
            if not query_reg_value(regpath=run_reg_path, keyname='test1'):
                log.log_error("添加启动项注册表项配置失败")
            log.log_pass("添加启动注册表项配置成功")

        with allure.step("step4：调起毒霸进行电脑加速"):
            log.log_info("调起毒霸并点击进入电脑加速界面，执行电脑加速")
            accelerate_page = ComputerAcceleratePage()
            while not accelerate_page.check_accelerate_scan_status():
                log.log_info("电脑加速扫描进行中")
            log.log_pass("电脑加速扫描已完成")

        with allure.step("step5: 检测扫描结果是否符合预期"):
            log.log_info("在扫描结果列表中查找指定项")
            kjjs_module_result = accelerate_page.is_module_exists(module_name='KJJS')
            if not kjjs_module_result[0]:
                log.log_error("未在开机加速中查找到对应项")
            log.log_pass("在开机加速项中查找到对应的测试项")
            utils.perform_sleep(1)
            accelerate_page.click_bcTester_select(kjjs_module_result[1])
            log.log_info("已操作勾选bcTester勾选框为选中状态")


        with allure.step("step6: 点击一键加速并判断结果"):
            accelerate_page.click_accelerate_button()
            log.log_pass("点击一键加速完成")
            while not accelerate_page.is_accelerate_finished():
                log.log_info("电脑加速进行中")
            log.log_pass("电脑加速已完成")
            log.log_info("判断注册表中是否还存在对应测试项")
            if query_reg_value(regpath=run_reg_path, keyname='test1'):
                log.log_error("注册表中仍存在测试项，未处理")
            log.log_pass("注册表中不存在测试项，加速处理成功")

        with allure.step("step7: 构造验证运行加速环境"):
            # 恢复环境是为了避免先前验证点开机加速扫描结果列表中存在测试图标影响验证结果
            accelerate_page.click_return_mainpage_button(reclick=True)
            accelerate_page.click_return_mainpage_button()
            close_duba_self_protecting()
            kill_duba_page_process(excludeKislive=False)
            file_path = os.path.join(find_dubapath_by_reg(), 'data', 'bksq.dat')
            time.sleep(3)
            remove_path(file_path)
            log.log_pass("删除bksg.dat文件成功")
            reg_path = r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Run\test1'
            if is_reg_exist(regpath=reg_path):
                remove_reg_key(regpath=reg_path)
            process_start(process_path=bctester_ch_path, async_start=True)
            os.environ['process_name'] = "bctester-ch.exe"
            time.sleep(2)
            log.log_pass("构造验证运行加速环境完成")

        with allure.step("step8: 验证运行加速扫描结果中是否存在检测项"):
            accelerate_page_new = ComputerAcceleratePage()
            while not accelerate_page_new.check_accelerate_scan_status:
                log.log_info("电脑加速扫描进行中")
            log.log_pass("电脑加速扫描已完成")
            yxjs_module_result = accelerate_page_new.is_module_exists(module_name='YXJS')
            if not yxjs_module_result[0]:
                log.log_error("运行加速列表中不存在指定检测项---检测不通过")
                utils.kill_process_by_name(process_name="bctester-ch.exe")
            log.log_pass("运行加速列表中存在指定检测项---检测通过")

        with allure.step("step9: 验证加速后进程状态"):
            accelerate_page_new.click_accelerate_button()
            while not accelerate_page_new.is_accelerate_finished():
                log.log_info("电脑加速进行中")
            log.log_pass("电脑加速已完成")
            log.log_info("判断测试进程是否存在")
            if is_process_exists("bctester-ch.exe"):
                log.log_error("测试进程仍存在---检测不通过")
                utils.kill_process_by_name(process_name="bctester-ch.exe")
            log.log_pass("测试进程不存在---检测通过")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])





















