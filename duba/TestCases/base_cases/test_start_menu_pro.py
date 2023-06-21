import os
import random
import allure
import pytest
from common import utils
from common.log import log
from common.tools.duba_tools import find_dubapath_by_reg
from duba.PageObjects.feedback_page import FeedbackPage
from duba.PageObjects.screen_capture_page import ScreenCapturePage
from duba.PageObjects.screen_record_page import ScreenRecordPage
from duba.config import config
from duba.PageObjects.start_menu_pro_page import StartMenuProPage, HotkeyType


@allure.epic(f'毒霸开始菜单Pro 业务流程测试（{config.ENV.value}）')
@allure.feature('场景：开始菜单Pro常规功能检查')
class TestStartMenuPro(object):
    @allure.story('用例：开始菜单Pro常规功能检查 预期成功')
    @allure.description("""
        step1：打开开始菜单Pro
        step2：设置快捷键
        step3：任务栏图标校验
        step4：升级与还原开始菜单
        step5：搜索软件和文件
        step6：删除软件
        step7：添加软件
        step8：添加文件、文件夹
        step9：查看更多实用工具
        step10：电源菜单检查
        step11：录屏按钮检查
        step12：截图按钮检查
        step13：系统设置按钮检查
        step14：反馈建议检查
        step15：功能介绍检查
        step16：从任务栏取消固定检查
    """)
    @allure.title('开始菜单Pro常规功能检查')
    def test_start_menu_pro_success(self):
        with allure.step("step1：打开开始菜单Pro"):
            start_menu_page = StartMenuProPage()
            log.log_pass("打开开始菜单Pro成功")

        with allure.step("step2：设置快捷键"):
            # 打开快捷键设置界面
            start_menu_page.open_hotkey_setting_prompt()
            # 启用使用快捷键打开开始菜单Pro
            start_menu_page.enable_start_menu_hotkey()
            # 设置快捷键
            hotkey_type = random.choice(list(HotkeyType._value2member_map_.values()))
            start_menu_page.set_hotkey(hotkey_type)
            # 关闭快捷键设置界面
            start_menu_page.close_hotkey_setting_prompt()

            # 使用快捷键关闭开始菜单Pro界面
            start_menu_page.input_hotkey(hotkey_type)

            utils.perform_sleep(2)

            if start_menu_page.get_tab_logo()[0]:
                log.log_error("使用快捷键关闭开始菜单Pro失败")

            # 使用快捷键打开开始菜单Pro界面
            start_menu_page.input_hotkey(hotkey_type)

            utils.perform_sleep(2)

            if not start_menu_page.get_tab_logo()[0]:
                log.log_error("使用快捷键打开开始菜单Pro失败")

            log.log_pass("设置快捷键检查通过")

        with allure.step("step3：任务栏图标校验"):
            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()

            utils.perform_sleep(2)

            if start_menu_page.get_tab_logo()[0]:
                log.log_error("点击任务栏图标关闭开始菜单Pro失败")

            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()

            utils.perform_sleep(2)

            if not start_menu_page.get_tab_logo()[0]:
                log.log_error("点击任务栏图标打开开始菜单Pro失败")

            log.log_pass("任务栏图标检查通过")

        with allure.step("step4：升级与还原开始菜单"):
            # 升级开始菜单
            start_menu_page.update_start_menu()
            utils.perform_sleep(2)

            # 还原开始菜单
            start_menu_page.reset_start_menu()
            utils.perform_sleep(2)

            log.log_pass("升级与还原开始菜单检查通过")

        with allure.step("step5：搜索软件和文件"):
            # 搜索软件和文件
            start_menu_page.search_file(start_menu_page.process_name)
            utils.perform_sleep(2)

            find_result = utils.find_element_by_pic(start_menu_page.get_page_shot("launchpad_search_result.png"),
                                                    retry=3, sim_no_reduce=True)
            assert find_result, log.log_error("搜索结果校验失败", need_assert=False)

            # 关闭搜索结果
            assert start_menu_page.close_search_result(), log.log_error("关闭搜索结果失败", need_assert=False)

            log.log_pass("搜索软件和文件检查通过")

        with allure.step("step6：删除软件"):
            # 删除软件
            start_menu_page.remove_software()

            log.log_pass("删除软件检查通过")

        with allure.step("step7：添加软件"):
            # 添加软件
            start_menu_page.add_software()

            log.log_pass("添加软件检查通过")

        with allure.step("step8：添加文件、文件夹"):
            # 获取毒霸安装路径
            duba_path = find_dubapath_by_reg()
            kismain_path = os.path.join(duba_path, "ksoftlaunchpad.exe")

            # 添加文件
            start_menu_page.add_file(kismain_path)

            # 添加文件夹
            start_menu_page.add_folder(duba_path)

            log.log_pass("添加文件、文件夹检查通过")

        with allure.step("step9：查看更多实用工具"):
            # 查看更多实用工具
            start_menu_page.enter_more_practical_tools()
            # 退出实用工具更多界面
            assert start_menu_page.exit_more_practical_tools(), log.log_error("退出实用工具更多界面失败", need_assert=False)

            log.log_pass("查看更多实用工具检查通过")

        with allure.step("step10：电源菜单检查"):
            # 查看电源菜单
            start_menu_page.show_power_menu()

            assert utils.find_element_by_pic(start_menu_page.get_page_shot("power_menu.png"), retry=3,
                                             sim_no_reduce=True)[0], log.log_error("电源菜单校验失败")
            # 关闭电源菜单
            start_menu_page.close_power_menu()

            log.log_pass("电源菜单检查通过")

        with allure.step("step11：录屏按钮检查"):
            # 点击录屏按钮
            start_menu_page.click_record_button()
            utils.perform_sleep(3)

            screen_record_page = ScreenRecordPage(do_pre_open=False)
            log.log_info("打开录屏大师成功", screenshot=True)

            screen_record_page.page_del()
            log.log_info("关闭录屏大师")

            log.log_pass("录屏按钮检查通过")

        with allure.step("step12：截图按钮检查"):
            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()
            utils.perform_sleep(1)

            # 点击截图按钮
            start_menu_page.click_screenshot_button()
            utils.perform_sleep(2)
            # 在鼠标点击一下，触发显示截图工具栏
            utils.mouse_click(0, 0)
            utils.perform_sleep(2)

            screen_capture_page = ScreenCapturePage(do_pre_open=False)
            log.log_info("打开毒霸截图王成功", screenshot=True)

            screen_capture_page.page_del()
            log.log_info("关闭毒霸截图王")

            log.log_pass("截图按钮检查通过")

        with allure.step("step13：系统设置按钮检查"):
            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()
            utils.perform_sleep(1)

            # 点击系统设置按钮
            start_menu_page.click_system_setting_button()
            utils.perform_sleep(2)

            assert utils.find_element_by_pic(start_menu_page.get_page_shot("system_setting_tab_logo.png"), retry=3,
                                             sim_no_reduce=True)[0], log.log_error("查找系统设置页面标识失败")
            log.log_info("打开系统设置页面成功", screenshot=True)

            assert utils.click_element_by_pic(start_menu_page.get_page_shot("system_setting_exit_button.png"), retry=3,
                                              sim_no_reduce=True), log.log_error("关闭系统设置界面失败")

            log.log_pass("系统设置按钮检查通过")

        with allure.step("step14：反馈建议检查"):
            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()
            utils.perform_sleep(1)
            # 点击反馈建议按钮
            start_menu_page.click_feedback_button()
            utils.perform_sleep(2)

            feedback_page = FeedbackPage(do_pre_open=False)
            log.log_info("打开反馈建议成功", screenshot=True)

            feedback_page.page_del()
            log.log_info("关闭反馈建议")

            log.log_pass("反馈建议检查通过")

        with allure.step("step15：功能介绍检查"):
            # 点击任务栏图标
            start_menu_page.click_task_bar_start_button()
            utils.perform_sleep(1)
            # 打开功能介绍界面
            start_menu_page.open_function_introduction()
            utils.perform_sleep(2)

            # 功能介绍翻页
            start_menu_page.function_introduction_next_page()

            # 关闭功能介绍界面
            assert start_menu_page.close_function_introduction(), log.log_error("关闭功能介绍界面失败", need_assert=False)

            log.log_pass("功能介绍检查通过")

        with allure.step("step16：从任务栏取消固定检查"):
            start_menu_page.cancel_task_bar_lock()

            log.log_pass("从任务栏取消固定检查通过")


if __name__ == '__main__':
    pytest.main(["-v", "-s", __file__])
