import os
import allure
import pytest

from common import utils
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep, Location
from common.tools.duba_tools import find_dubapath_by_reg
import shutil

from duba.PageObjects.ksthlp_tool_page import KsthlpToolPage
from duba.utils import close_duba_self_protecting



@allure.epic(f'毒霸ksapi驱动功能测试')
@allure.feature('场景：关闭毒霸自保护->测试前准备->打开毒霸自保护->执行测试->分析测试结果')
class TestKsthlp(object):
    @allure.story('1.毒霸ksapi驱动功能测试')
    def test_ksthlp(self):
        allure.dynamic.description(
            '\t1.关闭毒霸自保护\n'
            '\t2.测试前准备\n'
            '\t3.打开毒霸自保护\n'
            '\t4.执行测试\n'
            '\t5.分析测试结果\n'
        )
        allure.dynamic.title('毒霸ksthlp功能测试')

        with allure.step("step1：关闭毒霸自保护"):
            close_duba_self_protecting()
            perform_sleep(1)

        with allure.step("step2：下拉测试相关文件到毒霸log目录"):
            defend_tool_path = os.path.join(os.getcwd(), "defendtool")
            # defend_tool_path = r'E:\dubatestpro\dubatestpro\defendtool'
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "dubadefend")
            samba_o.download_dir("TcSpace", demo_path, defend_tool_path)
            TestDlg_self_sign_path = os.path.join(defend_tool_path, "TestDlg_self_sign.exe")
            WriteMemoryTest_path = os.path.join(defend_tool_path, "WriteMemoryTest.exe")
            vcredist2005_x86_sp1_path = os.path.join(defend_tool_path, "vcredist2005_x86_sp1.exe")
            if os.path.exists(TestDlg_self_sign_path) and os.path.exists(WriteMemoryTest_path) and os.path.exists(vcredist2005_x86_sp1_path):
                log.log_info("下拉验证ksthlp工具成功", attach=False)
            else:
                log.log_error("下拉验证ksthlp工具失败", attach=False)

        with allure.step("step3:测试前准备"):
            utils.process_start(vcredist2005_x86_sp1_path, async_start=True)
            utils.perform_sleep(2)
            vcred = utils.find_element_by_pic(pic=os.path.join(os.getcwd(), "duba", "PageShot", 'ksthlp_tool_page', 'vcredist2005_x86_sp1.png'), location=Location.RIGHT_BOTTOM.value)
            if vcred[0] is True:
                utils.mouse_click(vcred[1][0] - 123, vcred[1][1] + 27)
                while True:
                    if not utils.is_process_exists('vcredist2005_x86_sp1.exe'):
                        log.log_info('vcredist200安装完成', attach=False)
                        break
            else:
                log.log_info('vcredist2005打开失败', attach=False)
        with allure.step("step4:执行测试"):
            duba_path = find_dubapath_by_reg()
            if os.path.exists(duba_path):
                TestDlg_self_sign_dubapath = shutil.copy(TestDlg_self_sign_path, duba_path)
                log.log_info("拷贝文件到毒霸目录成功")
                ksthlpToolPage = KsthlpToolPage(TestDlg_self_sign_dubapath)
                ksthlpToolPage.get_TestDlg_positions()
                ksthlpToolPage.click_init_button()
                utils.perform_sleep(2)
                ksthlpToolPage.click_all_proc_shellcode()
                ksthlpToolPage.click_proc_shellcode()
                ksthlpToolPage.click_get_proc_handle()
                ksthlpToolPage.click_open_proc()
                ksthlpToolPage.click_close_proc()
                ksthlpToolPage.click_read()
                ksthlpToolPage.click_write()
                ksthlpToolPage.check_bufeng(duba_path)


            else:
                log.log_error("未找到毒霸安装路径", attach=False)



if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
