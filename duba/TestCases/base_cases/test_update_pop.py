import os

import win32gui

import common.utils
import pytest
import allure
from common import utils
from common.log import log
from common.samba import Samba
from common.tools.base_tools import get_page_shot
from duba.PageObjects.UpdatePop_Tool_Page import UpdatePopToolPage
from duba.PageObjects.main_page import main_page
from duba.PageObjects.update_pop_page import delete_pophistory, block_popcenter, update_reg_operation, UpdatePopPage
from duba.config import config
from duba.utils import close_duba_self_protecting,kill_duba_page_process


@allure.epic(f'毒霸升级完成泡功能测试（{config.ENV.value}）')
@allure.feature('场景：打开毒霸并关闭毒霸自保护->构建升级完成泡弹出环境->下拉升级完成泡调起工具->调用弹泡工具进行弹泡->分确认升级泡存在')
class TestUpdatePop(object):
    @allure.story('1.毒霸升级完成泡功能测试')
    def test_update_pop(self):
        allure.dynamic.description(
            '\t1.打开毒霸并关闭毒霸自保护\n'
            '\t2.构建升级完成泡弹出环境\n'
            '\t3.下拉升级完成泡调起工具\n'
            '\t4.调用弹泡工具进行弹泡\n'
            '\t5.确认升级泡存在\n'
        )
        allure.dynamic.title('毒霸升级完成泡功能测试')

        with allure.step("step1:打开毒霸并关闭毒霸自保护"):
            close_duba_self_protecting()
            utils.perform_sleep(1)
            log.log_pass("毒霸自保护已关闭")

        with allure.step("step2:构建升级完成泡弹出环境"):
            log.log_info("关闭毒霸服务以删除pophistory")
            kill_duba_page_process(excludeKislive=True)
            try:
                delete_pophistory()
                block_popcenter()
                # update_reg_operation()
            except:
                log.log_error("屏蔽泡泡中心失败", attach=False)
            log.log_pass("屏蔽泡泡中心成功", attach=False)
            log.log_info("重启毒霸")
            duba_main_page = main_page()
            close_duba_self_protecting()
            update_reg_operation()
            log.log_info("删除相关注册表项完成")


        with allure.step("step3:下拉升级完成泡调起工具"):
            updatepop_tool_path = os.path.join(os.getcwd(), "UpdatepopTool")
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            samba_o.download_dir("TcSpace", os.path.join('autotest', 'business'), updatepop_tool_path)
            tool_path = os.path.join(updatepop_tool_path, "tttttttttttttttttttttttttttttt.exe")
            if not os.path.exists(tool_path):
                log.log_error("下拉升级完成泡调起工具失败", attach=False)
            log.log_pass("下拉升级完成泡调起工具成功", attach=False)

        with allure.step("step4:调用弹泡工具进行弹泡"):
            # utils.process_start(tool_path)
            os.popen(tool_path)
            judge_num = 0
            page_exist = False
            while judge_num < 4:
                if not win32gui.FindWindow("#32770","tttttttttttttttttttttttttttttt") == 0:
                    log.log_info("弹泡工具界面存在")
                    page_exist = True
                    break
                utils.perform_sleep(2)
                judge_num += 1
            if page_exist:
                ToolPage = UpdatePopToolPage()
                if not ToolPage.click_show_updatepop_button():
                    log.log_error("点击升级泡弹出按钮异常")
                log.log_pass("已点击弹泡工具调起升级泡完成按钮")
            else:
                log.log_error("工具界面不存在")


        with allure.step("step5:确认升级泡存在"):
            UpdatePop_tab_null_path = get_page_shot("UpdatePop_Page","updatepop_tab_null.png")
            UpdatePop_tab_old_path = get_page_shot("UpdatePop_Page", "updatepop_tab_old.png")
            UpdatePop_tab_new_path = get_page_shot("UpdatePop_Page", "updatepop_tab_new.png")
            res1, pos1 = utils.find_element_by_pic(UpdatePop_tab_null_path,sim=0.9)
            res2, pos2 = utils.find_element_by_pic(UpdatePop_tab_old_path,sim=0.9)
            res3, pos3 = utils.find_element_by_pic(UpdatePop_tab_new_path, sim=0.9)
            if res2 or res3:
                log.log_pass("检测到升级完成泡")
            elif res1:
                log.log_error("检测到升级泡但展示异常")
            else:
                log.log_error("未检测到升级完成泡")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])





