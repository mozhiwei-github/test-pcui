import os

import allure
import pytest
from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from common.tools.pop_tools import BasePop
from duba.PageObjects.setting_page import SettingPage


@allure.epic(f'毒霸防御基础功能测试')
@allure.feature('场景：打开毒霸自保护->下拉防御基础功能测试工具->依次执行测试工具->操作弹出泡泡')
class TestSelfProtect(object):
    @allure.story('1.毒霸防御基础功能测试')
    def test_self_protect(self):
        allure.dynamic.description(
            '\t1.打开毒霸自保护\n'
            '\t2.下拉防御基础功能测试工具\n'
            '\t3.依次执行测试工具\n'
            '\t4.双后缀名拦截样本测试\n'
        )
        allure.dynamic.title('毒霸防御基础功能测试')

        with allure.step("step1：打开毒霸自保护"):
            setting_page_o = SettingPage()
            # 先关闭毒霸自保护，删除自动拦截不弹泡泡的键值
            if setting_page_o.self_protecting_close():
                if utils.query_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                    if utils.remove_reg_value(None, r"SOFTWARE\WOW6432Node\kingsoft\antivirus", "DenyAuto"):
                        log.log_pass("删除自动拦截不弹泡泡的键值", attach=False)
            perform_sleep(1)
            if setting_page_o.self_protecting_open():
                log.log_pass("打开毒霸自保护成功", attach=False)
            perform_sleep(1)

        with allure.step("step2：下拉防御基础功能测试工具/样本"):
            defend_tool_path = os.path.join(os.getcwd(), "defendtool")
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "dubadefend")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            # 双后缀名拦截样本
            tool_path_1 = os.path.join(defend_tool_path, "1.jpg.exe")

            if os.path.exists(tool_path_1):
                log.log_pass("下拉所有毒霸防御测试工具成功", attach=False)
                utils.perform_sleep(5)
            else:
                log.log_error("下拉毒霸防御测试工具失败", attach=False)

        with allure.step("step3：双后缀名拦截样本测试"):
            for i in range(0, 80, 1):
                utils.process_start(tool_path_1, async_start=True)
                utils.perform_sleep(5)
                defendpop = BasePop()
                if defendpop.pop_init:
                    log.log_pass("双后缀名拦截泡泡正常")
                    defendpop.click_defend_stop()
                else:
                    log.log_error("泡泡没有弹出来", need_assert=False, attach=False)
                utils.perform_sleep(8 * 60)


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
