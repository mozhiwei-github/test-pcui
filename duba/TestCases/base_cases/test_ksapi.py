import os
import allure
import pytest
from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from common.tools.duba_tools import find_dubapath_by_reg
import shutil
from duba.utils import close_duba_self_protecting
from duba.PageObjects.ksapi_tool_page import KsapiToolPage


@allure.epic(f'毒霸ksapi驱动功能测试')
@allure.feature('场景：关闭毒霸自保护->下拉测试相关文件到毒霸log目录->打开毒霸自保护->执行测试->分析测试结果')
class TestKsapi(object):
    @allure.story('1.毒霸ksapi驱动功能测试')
    def test_ksapi(self):
        allure.dynamic.description(
            '\t1.关闭毒霸自保护\n'
            '\t2.下拉测试相关文件到毒霸log目录\n'
            '\t3.打开毒霸自保护\n'
            '\t4.执行测试\n'
            '\t5.分析测试结果\n'
        )
        allure.dynamic.title('毒霸ksapi功能测试')

        with allure.step("step1：关闭毒霸自保护"):
            close_duba_self_protecting()
            perform_sleep(1)

        with allure.step("step2：下拉测试相关文件到毒霸log目录"):
            defend_tool_path = os.path.join(os.getcwd(), "defendtool")
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "dubadefend")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            fantasy_ksapi_path = os.path.join(defend_tool_path, "fantasy_ksapi.exe")
            if os.path.exists(fantasy_ksapi_path):
                log.log_info("下拉验证ksapi工具成功", attach=False)
            else:
                log.log_error("下拉验证ksapi工具失败", attach=False)

        with allure.step("step3:将相关测试文件拷贝到毒霸log目录下"):
            if utils.is_process_exists("fantasy_ksapi.exe"):
                os.system("taskkill /f /im fantasy_ksapi.exe")
                utils.perform_sleep(3)
            duba_path = find_dubapath_by_reg()
            if os.path.exists(duba_path):
                duba_log_path = os.path.join(duba_path, 'log')
                fantasy_ksapi_dubapath = shutil.copy(fantasy_ksapi_path, duba_log_path)
                if os.path.exists(r"C:\Program Files (x86)"):
                    ksapi_dll_path = os.path.join(duba_path, "ksapi64.dll")
                else:
                    ksapi_dll_path = os.path.join(duba_path, "ksapi.dll")
                shutil.copy(ksapi_dll_path, duba_log_path)
                log.log_info("拷贝文件到毒霸log目录成功")
            else:
                log.log_error("未找到毒霸安装路径", attach=False)

        with allure.step("step4:执行测试"):
            ksapi_tool_page = KsapiToolPage(fantasy_ksapi_dubapath)
            utils.perform_sleep(1)
            ksapi_tool_page.click_kill_process()
            ksapi_tool_page.click_delete_file1()
            ksapi_tool_page.click_delete_file2()
            ksapi_tool_page.click_write_file()
            ksapi_tool_page.click_read_file()
            ksapi_tool_page.click_delete_key()
            ksapi_tool_page.click_eum_value()
            ksapi_tool_page.click_create_key()
            ksapi_tool_page.click_create_key_Ex()
            ksapi_tool_page.click_delete_value()
            ksapi_tool_page.click_set_value()
            ksapi_tool_page.click_query_value()


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
