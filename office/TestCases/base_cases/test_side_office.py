import os
import re
import time
import allure
import pytest
from common import utils
from common.contants import InputLan
from common.log import log
from common.wadlib import wadlib
global office_path
@allure.epic(f'office模板插件ppt场景测试')
@allure.feature('ppt模板插件功能测试')
class TestKeniuOfficeSide(object):
    front_mark = False

    def setup_class(self):
        global office_path
        allure.dynamic.description(
            '\t初始化环境\n'
        )
        allure.dynamic.title("初始化电脑环境")

        with allure.step("初始化环境"):
            if utils.is_process_exists("POWERPNT.EXE"):
                # 需要关闭毒霸自保护
                os.system('taskkill /im POWERPNT.EXE')
                log.log_info("关掉ppt进程")
            office_path = r"D:\Program Files (x86)\Microsoft Office\Office12\POWERPNT.EXE"
            utils.change_input_lan(InputLan.EN)

    def teardown_class(self):
        utils.change_input_lan(InputLan.ZH)
        allure.dynamic.description(
            '\t执行结束后\n'
        )
        allure.dynamic.title("执行结束")
        with allure.step("执行结束"):
            if utils.is_process_exists("POWERPNT.EXE"):
                # 需要关闭毒霸自保护
                os.system('taskkill /im POWERPNT.EXE')
                log.log_info("用例运行结束，发现ppt进程未关闭，执行命令行关闭ppt")

    @pytest.fixture(scope='function', autouse=True)
    def kill_process(self):
        if utils.is_process_exists("POWERPNT.EXE"):
            # 每次执行用例或重跑用例时，检测进程是否存在，存在则调用命令行干掉
            os.system('taskkill /im POWERPNT.EXE')
            log.log_info("杀掉ppt进程")

    @allure.story('顶部栏操作')
    @pytest.mark.flaky(reruns=1)
    def test_side_office(self):
        allure.dynamic.description(
            '\t1.打开界面\n'
            '\t2.刷新\n'
        )
        allure.dynamic.title('office侧边栏测试')
        with allure.step("step-1:刷新、收起、关闭、展开测试"):
            global front_mark

            top_task = wadlib(app_path=office_path)
            utils.perform_sleep(1)

            top_task.click_find_by_name("页面重载")
            assert top_task.isElementPresent("name", "总结"), "刷新页面失败！"
            log.log_pass("成功刷新")
            utils.perform_sleep(1)

            top_task.click_find_by_name("收起")
            assert top_task.isElementPresent("name", "收起"), "收起侧边栏失败！"
            log.log_pass("成功收起侧边栏")
            utils.perform_sleep(1)

            top_task.click_find_by_name("总结")
            assert top_task.isElementPresent("name", "收起"), "展开侧边栏失败！"
            log.log_pass("成功展开侧边栏")
            utils.perform_sleep(1)

        with allure.step("step-2:搜索功能测试"):

            search_task = wadlib(app_path=office_path)
            utils.perform_sleep(1)
            search_task.click_find_by_name("搜索...")
            utils.perform_sleep(1)
            search_task.click_find_by_name("总结汇报")
            utils.perform_sleep(1)
            search_task.input_find_by_name("搜索...","免费")
            search_task.send_keys_enter("搜索...")
            log.log_pass("成功搜索")

        #with allure.step("step-3:模板详情页测试"):

        with allure.step("step-4:切换tab测试"):

            tab_task = wadlib(app_path=office_path)
            utils.perform_sleep(1)

            tab_task.click_find_by_name("总结")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '总结汇报'):
                log.log_pass("成功切换总结tab")

            tab_task.click_find_by_name("教育")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '教学模板'):
                log.log_pass("成功切换教育tab")

            tab_task.click_find_by_name("党政")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '党政报告'):
                log.log_pass("成功切换党政tab")

            tab_task.click_find_by_name("策划")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '策划方案'):
                log.log_pass("成功切换策划tab")

            tab_task.click_find_by_name("答辩")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '论文答辩'):
                log.log_pass("成功切换答辩tab")

            tab_task.click_find_by_name("图示")
            tab_task.click_find_by_name("所有分类")
            if tab_task.isElementPresent("name", '目录'):
                log.log_pass("成功切换目录tab")



if __name__ == '__main__':
    allure_attach_path = os.path.join("Outputs", "allure")
    pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    os.system("allure serve %s" % allure_attach_path)