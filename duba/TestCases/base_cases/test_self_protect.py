import json
import os

import allure
import pytest
from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from duba.PageObjects.setting_page import SettingPage


@allure.epic(f'毒霸自保护功能测试')
@allure.feature('场景：打开毒霸自保护->下拉防御自保护测试工具->执行测试->分析测试结果')
class TestSelfProtect(object):
    @allure.story('1.毒霸自保护功能测试')
    def test_self_protect(self):
        allure.dynamic.description(
            '\t1.打开毒霸自保护\n'
            '\t2.下拉防御自保护测试工具\n'
            '\t3.执行测试\n'
            '\t4.分析测试结果\n'
        )
        allure.dynamic.title('毒霸自保护功能测试')

        with allure.step("step1：打开毒霸自保护"):
            setting_page_o = SettingPage()
            if setting_page_o.self_protecting_open():
                log.log_pass("打开毒霸自保护成功", attach=False)
            perform_sleep(1)

        with allure.step("step2：下拉毒霸自保护测试工具成功"):
            defend_tool_path = os.path.join(os.getcwd(), "defendtool")
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "dubadefend")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            self_protect_tool_path = os.path.join(defend_tool_path, "DubaDefendTest.exe")
            if os.path.exists(self_protect_tool_path):
                log.log_pass("下拉毒霸自保护测试工具成功", attach=False)
                utils.perform_sleep(5)
            else:
                log.log_error("下拉毒霸自保护测试工具失败", attach=False)

        with allure.step("step3：执行测试"):
            utils.process_start(self_protect_tool_path, async_start=True)
            defend_report_path = os.path.join(os.getcwd(), "defend_report.json")
            for i in range(5):
                if not os.path.exists(defend_report_path):
                    utils.perform_sleep(10)
                else:
                    log.log_pass("执行完毕报告已生成", attach=False)
                    break

            if os.path.exists(defend_report_path):
                with open(defend_report_path, "r", encoding="utf-8") as fr:
                    report_data = json.loads(fr.read())
                    for test_case in report_data:
                        if report_data[test_case]:
                            log.log_pass(test_case + str(report_data[test_case]), attach=False)
                        else:
                            log.log_error(test_case + str(report_data[test_case]), attach=False, need_assert=False)
            else:
                log.log_error("执行测试失败", attach=False)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
