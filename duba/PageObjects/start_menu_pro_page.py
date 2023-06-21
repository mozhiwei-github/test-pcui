from enum import unique, Enum
from common.contants import InputLan
from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
from common.utils import perform_sleep, Location
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page

"""开始菜单Pro"""


@unique
class HotkeyType(Enum):
    ALT_WIN = "Alt + Win"
    CTRL_WIN = "Ctrl + Win"


class StartMenuProPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 不使用窗口右上角坐标关闭
        self.enable_rect_pos_close = False
        # 快捷键设置窗口坐标
        self.hotkey_setting_prompt_pos = None
        # 添加窗口坐标
        self.add_prompt_pos = None

    def pre_open(self):
        # 从百宝箱进入
        chest_page = baibaoxiang_page()
        chest_page.tools_button_click(chest_page.get_page_shot("button_start_menu_pro.png"))
        utils.perform_sleep(3)

        # 关闭新手指引
        next_step_count = 4
        for i in range(next_step_count):
            log.log_info("查找新手指引下一步按钮")
            click_result = utils.click_element_by_pic(self.get_page_shot("next_step_button.png"), retry=3,
                                                      sim_no_reduce=True)
            # 首次未找到下一步按钮说明已经关闭新手指引了
            if i == 0 and not click_result:
                log.log_info("未发现新手指引界面", screenshot=True)
                break

            assert click_result, log.log_error("点击新手指引下一步按钮失败", need_assert=False)
            utils.perform_sleep(1)

            # 完成所有下一步后，点击我知道了按钮结束新手指引
            if i == (next_step_count - 1):
                log.log_info("点击新手指引我知道了按钮", screenshot=True)
                utils.click_element_by_pic(self.get_page_shot("i_known_button.png"), retry=3, sim_no_reduce=True)
                utils.perform_sleep(3)

    def page_confirm_close(self):
        # 查找并关闭满意评价弹窗
        log.log_info("查找满意评价弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("satisfaction_prompt_tab_logo.png"),
                                                              retry=3, sim_no_reduce=True,
                                                              location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭满意评价弹窗")
            utils.mouse_click(prompt_pos[0] + 456, prompt_pos[1] + 20)
        else:
            log.log_info("未找到满意评价弹窗")

    @page_method_record("点击菜单按钮")
    def click_menu_button(self):
        return utils.click_element_by_pic(self.get_page_shot("menu_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("打开快捷键设置界面")
    def open_hotkey_setting_prompt(self):
        assert self.click_menu_button(), log.log_error("点击菜单按钮失败", need_assert=False)
        if not utils.click_element_by_pic(self.get_page_shot("hotkey_setting_menu.png"), retry=3, sim_no_reduce=True):
            log.log_error("打开快捷键设置界面失败")

        utils.perform_sleep(1)

        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("hotkey_setting_tab_logo.png"),
                                                              retry=3, sim_no_reduce=True,
                                                              location=Location.LEFT_UP.value)
        if not prompt_result:
            log.log_error("查找快捷键设置界面标识失败")

        self.hotkey_setting_prompt_pos = prompt_pos

    @page_method_record("关闭快捷键设置界面")
    def close_hotkey_setting_prompt(self):
        assert self.hotkey_setting_prompt_pos, log.log_error("获取快捷键设置界面坐标失败", need_assert=False)
        utils.mouse_click(self.hotkey_setting_prompt_pos[0] + 376, self.hotkey_setting_prompt_pos[1] + 18)

    @page_method_record("启用使用快捷键打开开始菜单Pro")
    def enable_start_menu_hotkey(self):
        checkbox_prompt, checkbox_pos = utils.find_element_by_pic(self.get_page_shot("start_menu_hotkey_disabled.png"),
                                                                  sim=0.98, retry=3, sim_no_reduce=True,
                                                                  location=Location.LEFT_UP.value)
        if checkbox_prompt:
            log.log_info("勾选使用快捷键打开开始菜单Pro")
            utils.mouse_click(checkbox_pos[0] + 10, checkbox_pos[1] + 10)
        else:
            log.log_info("已勾选使用快捷键打开开始菜单Pro")

    @page_method_record("设置快捷键")
    def set_hotkey(self, hotkey_type):
        """
        设置快捷键
        @param hotkey_type: 快捷键类型枚举值 HotkeyType
        @return:
        """
        if hotkey_type == HotkeyType.ALT_WIN:
            hotkey_shot = "alt_hotkey_radio.png"
        elif hotkey_type == HotkeyType.CTRL_WIN:
            hotkey_shot = "ctrl_hotkey_radio.png"
        else:
            log.log_error(f"设置快捷键 hotkey_type 参数错误: {hotkey_type}")

        hotkey_result, hotkey_pos = utils.find_element_by_pic(self.get_page_shot(hotkey_shot), retry=3, sim=0.98,
                                                              sim_no_reduce=True, location=Location.LEFT_UP.value)
        if hotkey_result:
            log.log_info(f"设置快捷键为 {hotkey_type.value}")
            utils.mouse_click(hotkey_pos[0] + 8, hotkey_pos[1] + 8)
        else:
            log.log_info(f"快捷键已设置为 {hotkey_type.value}")

    @page_method_record("调用快捷键")
    def input_hotkey(self, hotkey_type):
        if hotkey_type == HotkeyType.ALT_WIN:
            hotkey_list = ['alt', 'left_win']
        elif hotkey_type == HotkeyType.CTRL_WIN:
            hotkey_list = ['ctrl', 'left_win']
        else:
            log.log_error(f"调用快捷键 hotkey_type 参数错误: {hotkey_type}")

        return utils.keyboardInputHotkey(*hotkey_list)

    @page_method_record("校验开始菜单Pro界面打开状态")
    def get_tab_logo(self):
        return utils.find_element_by_pic(self.get_page_shot("tab_logo.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击任务栏图标")
    def click_task_bar_start_button(self):
        return utils.click_element_by_pic(self.get_page_shot("task_bar_start_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("升级开始菜单")
    def update_start_menu(self):
        # TODO: 目前只会替换主屏幕的开始菜单，所以双屏情况下会运行失败
        if not utils.find_element_by_pic(self.get_page_shot("windows_start_menu.png"), sim=0.9, retry=3,
                                         sim_no_reduce=True)[0]:
            log.log_info("开始菜单已升级", screenshot=True)
            return

        log.log_info("点击升级开始菜单按钮")
        assert utils.click_element_by_pic(self.get_page_shot("upgrade_start_menu_button.png"), retry=3,
                                          sim_no_reduce=True), log.log_error("点击升级开始菜单按钮失败", need_assert=False)

        utils.perform_sleep(3)

        if utils.click_element_by_pic(self.get_page_shot("i_known_button.png"), retry=3, sim_no_reduce=True):
            log.log_info("点击我知道了按钮关闭指引")
        else:
            log.log_info("未找到指引界面，继续后续流程")

        update_result = not utils.find_element_by_pic(self.get_page_shot("windows_start_menu.png"), sim=0.9, retry=5,
                                                      sim_no_reduce=True)[0]
        assert update_result, log.log_error("升级开始菜单失败", need_assert=False)

    @page_method_record("还原开始菜单")
    def reset_start_menu(self):
        # TODO: 目前只会替换主屏幕的开始菜单，所以双屏情况下会运行失败
        if utils.find_element_by_pic(self.get_page_shot("windows_start_menu.png"), sim=0.9, retry=3,
                                     sim_no_reduce=True)[0]:
            log.log_info("开始菜单已还原", screenshot=True)
            return

        log.log_info("点击还原开始菜单按钮")
        assert utils.click_element_by_pic(self.get_page_shot("reset_start_menu_button.png"), retry=3,
                                          sim_no_reduce=True), log.log_error("点击还原开始菜单按钮失败", need_assert=False)

        utils.perform_sleep(3)

        if utils.click_element_by_pic(self.get_page_shot("i_known_button.png"), retry=3, sim_no_reduce=True):
            log.log_info("点击我知道了按钮关闭指引")
        else:
            log.log_info("未找到指引界面，继续后续流程")

        reset_result = utils.find_element_by_pic(self.get_page_shot("windows_start_menu.png"), sim=0.9, retry=5,
                                                 sim_no_reduce=True)[0]
        assert reset_result, log.log_error("还原开始菜单失败", need_assert=False)

    @page_method_record("搜索软件和文件")
    def search_file(self, filename):
        """
        搜索软件和文件
        @param filename: 文件名（目前仅支持英文输入）
        @return:
        """
        click_result = utils.click_element_by_pic(self.get_page_shot("search_file_placeholder.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击搜索框失败", need_assert=False)
        # 设置为英文输入法
        utils.change_input_lan(InputLan.EN)
        utils.perform_sleep(1)
        # 输入文件名
        utils.key_input(filename)

    @page_method_record("关闭搜索结果")
    def close_search_result(self):
        return utils.click_element_by_pic(self.get_page_shot("search_bar_exit_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击编辑按钮")
    def click_edit_button(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("edit_button.png"), retry=3, sim_no_reduce=True)
        if not click_result:
            return False

        # 查找并关闭编辑指引界面
        step_result = utils.click_element_by_pic(self.get_page_shot("next_step_button.png"), retry=3,
                                                 sim_no_reduce=True)
        if step_result:
            log.log_info("点击下一步按钮成功")
            utils.perform_sleep(1)

            know_result = utils.click_element_by_pic(self.get_page_shot("i_known_button.png"), retry=3,
                                                     sim_no_reduce=True)
            assert know_result, log.log_error("点击我知道了按钮失败", need_assert=False)
            log.log_info("点击我知道了按钮成功")
        else:
            log.log_info("未找到编辑指引界面")

        return True

    @page_method_record("删除软件")
    def remove_software(self):
        # 点击编辑按钮
        assert self.click_edit_button(), log.log_error("点击编辑按钮失败", need_assert=False)
        log.log_info("进入编辑状态成功", screenshot=True, shot_delay=1)

        find_result, button_pos = utils.find_element_by_pic(self.get_page_shot("remove_software_button.png"), retry=3,
                                                            sim_no_reduce=True)
        assert find_result, log.log_error("查找软件删除按钮失败", need_assert=False)

        utils.mouse_click(button_pos)
        log.log_info("点击软件删除按钮", screenshot=True, shot_delay=1)

        # 点击确认删除按钮
        confirm_result = utils.click_element_by_pic(self.get_page_shot("confirm_button.png"), retry=3,
                                                    sim_no_reduce=True)
        assert confirm_result, log.log_error("点击确认删除按钮失败", need_assert=False)
        utils.perform_sleep(1)

        finish_result = utils.click_element_by_pic(self.get_page_shot("finish_button.png"), retry=3, sim_no_reduce=True)
        assert finish_result, log.log_error("点击完成按钮失败", need_assert=False)

        log.log_info("删除软件成功")

    @page_method_record("点击添加按钮")
    def click_add_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("打开添加界面")
    def open_add_prompt(self):
        assert self.click_add_button(), log.log_error("点击添加按钮失败", need_assert=False)

        utils.perform_sleep(1)

        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("add_prompt_tab_logo.png"),
                                                              retry=3, sim_no_reduce=True,
                                                              location=Location.LEFT_UP.value)
        if not prompt_result:
            log.log_error("查找添加界面标识失败")

        self.add_prompt_pos = prompt_pos

    @page_method_record("关闭添加界面")
    def close_add_prompt(self):
        assert self.add_prompt_pos, log.log_error("获取添加界面坐标失败", need_assert=False)
        utils.mouse_click(self.add_prompt_pos[0] + 314, self.add_prompt_pos[1] + 22)

    @page_method_record("添加软件")
    def add_software(self):
        # 打开添加界面
        self.open_add_prompt()

        # 点击添加软件按钮
        click_result = utils.click_element_by_pic(self.get_page_shot("add_software_button.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击添加软件按钮失败", need_assert=False)
        utils.perform_sleep(1)

        # 查找添加软件界面标识
        find_result, find_pos = utils.find_element_by_pic(self.get_page_shot("add_software_prompt_tab_logo.png"),
                                                          retry=3, sim_no_reduce=True)
        assert find_result, log.log_error("查找添加软件界面标识失败", need_assert=False)
        log.log_info("打开添加软件界面成功", screenshot=True)

        # 点击软件添加按钮
        add_result = utils.click_element_by_pic(self.get_page_shot("software_add_button.png"), retry=3,
                                                sim_no_reduce=True)
        assert add_result, log.log_error("点击软件添加按钮失败", need_assert=False)
        log.log_info("点击软件添加按钮成功", screenshot=True, shot_delay=1)

        finish_result = utils.click_element_by_pic(self.get_page_shot("finish_button.png"), retry=3, sim_no_reduce=True)
        assert finish_result, log.log_error("点击完成按钮失败", need_assert=False)

        log.log_info("添加软件成功")

    @page_method_record("添加文件")
    def add_file(self, filepath):
        # 打开添加界面
        self.open_add_prompt()

        # 点击添加文件按钮
        click_result = utils.click_element_by_pic(self.get_page_shot("add_file_button.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击添加文件按钮失败", need_assert=False)
        utils.perform_sleep(1)

        # 查找添加文件窗口标识
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("add_file_prompt_tab_logo.png"),
                                                              retry=3, sim_no_reduce=True,
                                                              location=Location.LEFT_UP.value)
        assert prompt_result, log.log_error("查找添加文件窗口标识失败", need_assert=False)

        # 输入文件路径
        utils.copy_to_clipboard(filepath)
        utils.key_paste()

        # 点击添加文件窗口左上角位置，关闭文件路径下拉列表
        utils.mouse_click(prompt_pos[0] + 5, prompt_pos[1] + 5)

        open_result = utils.click_element_by_pic(self.get_page_shot("add_prompt_open_button.png"), retry=3,
                                                 sim_no_reduce=True)
        assert open_result, log.log_error("点击打开按钮失败", need_assert=False)
        log.log_info("点击打开按钮成功", screenshot=True, shot_delay=0.5)

        finish_result = utils.click_element_by_pic(self.get_page_shot("finish_button.png"), retry=3, sim_no_reduce=True)
        assert finish_result, log.log_error("点击完成按钮失败", need_assert=False)

        log.log_info("添加文件成功")

    @page_method_record("添加文件夹")
    def add_folder(self, folder_path):
        # 打开添加界面
        self.open_add_prompt()

        # 点击添加文件夹按钮
        click_result = utils.click_element_by_pic(self.get_page_shot("add_folder_button.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击添加文件夹按钮失败", need_assert=False)
        utils.perform_sleep(1)

        # 查找添加文件夹窗口标识
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("add_folder_prompt_tab_logo.png"),
                                                              retry=3, sim_no_reduce=True,
                                                              location=Location.LEFT_UP.value)
        assert prompt_result, log.log_error("查找添加文件夹窗口标识失败", need_assert=False)

        # 输入文件夹路径
        utils.copy_to_clipboard(folder_path)
        utils.key_paste()

        # 点击添加文件夹窗口左上角位置，关闭文件夹路径下拉列表
        utils.mouse_click(prompt_pos[0] + 5, prompt_pos[1] + 5)

        open_result = utils.click_element_by_pic(self.get_page_shot("add_prompt_select_folder_button.png"), retry=3,
                                                 sim_no_reduce=True)
        assert open_result, log.log_error("点击选择文件夹按钮失败", need_assert=False)
        log.log_info("点击选择文件夹按钮成功", screenshot=True, shot_delay=0.5)

        finish_result = utils.click_element_by_pic(self.get_page_shot("finish_button.png"), retry=3, sim_no_reduce=True)
        assert finish_result, log.log_error("点击完成按钮失败", need_assert=False)

        log.log_info("添加文件夹成功")

    @page_method_record("查看更多实用工具")
    def enter_more_practical_tools(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("more_button.png"), retry=3, sim_no_reduce=True)
        assert click_result, log.log_error("点击实用工具更多按钮失败", need_assert=False)

        if not utils.find_element_by_pic(self.get_page_shot("practical_tools_tab_logo.png"))[0]:
            log.log_error("实用工具更多界面打开失败")
            return

        log.log_info("实用工具更多界面打开成功")

    @page_method_record("退出实用工具更多界面")
    def exit_more_practical_tools(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("practical_tools_exit_button.png"), retry=3,
                                                  sim_no_reduce=True)
        if click_result:
            # 鼠标归位
            utils.mouse_move(self.position[0], self.position[1])
        return click_result

    @page_method_record("查看电源菜单")
    def show_power_menu(self):
        result, pos = utils.find_element_by_pic(self.get_page_shot("power_button.png"), retry=3, sim_no_reduce=True)
        assert result, log.log_error("查找电源按钮失败", need_assert=False)
        # 移动鼠标到按钮位置
        utils.mouse_move(pos[0], pos[1])

    @page_method_record("关闭电源菜单")
    def close_power_menu(self):
        utils.mouse_move(self.position[0] + 5, self.position[1] + 5)

    @page_method_record("点击录屏按钮")
    def click_record_button(self):
        return utils.click_element_by_pic(self.get_page_shot("record_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击截图按钮")
    def click_screenshot_button(self):
        return utils.click_element_by_pic(self.get_page_shot("screenshot_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击系统设置按钮")
    def click_system_setting_button(self):
        return utils.click_element_by_pic(self.get_page_shot("system_setting_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("点击反馈建议按钮")
    def click_feedback_button(self):
        return utils.click_element_by_pic(self.get_page_shot("feedback_button.png"), retry=3, sim_no_reduce=True)

    @page_method_record("打开功能介绍界面")
    def open_function_introduction(self):
        assert self.click_menu_button(), log.log_error("点击菜单按钮失败", need_assert=False)

        click_result = utils.click_element_by_pic(self.get_page_shot("function_infroduction_menu.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击功能介绍菜单失败", need_assert=False)

        assert utils.find_element_by_pic(self.get_page_shot("function_introduction_tab_logo.png"), retry=5,
                                         sim_no_reduce=True), log.log_error("打开功能介绍界面失败")

    @page_method_record("关闭功能介绍界面")
    def close_function_introduction(self):
        return utils.click_element_by_pic(self.get_page_shot("function_introduction_exit_button.png"), retry=3,
                                          sim_no_reduce=True)

    @page_method_record("功能介绍翻页")
    def function_introduction_next_page(self):
        while True:
            result, pos = utils.find_element_by_pic(self.get_page_shot("function_introduction_next_button.png"),
                                                    sim=0.9, retry=2, sim_no_reduce=True)
            if not result:
                log.log_info("找不到下一页按钮，结束翻页")
                break

            log.log_info("点击下一页按钮")
            utils.mouse_click(pos)
            # 点击后鼠标归位
            utils.mouse_move(self.position[0] + 5, self.position[1] + 5)
            utils.perform_sleep(1)

    @page_method_record("从任务栏取消固定")
    def cancel_task_bar_lock(self):
        assert self.click_menu_button(), log.log_error("点击菜单按钮失败", need_assert=False)

        click_result = utils.click_element_by_pic(self.get_page_shot("cancel_taskbar_lock_menu.png"), retry=3,
                                                  sim_no_reduce=True)
        assert click_result, log.log_error("点击从任务栏取消固定菜单失败", need_assert=False)

        utils.perform_sleep(1)

        confirm_result = utils.click_element_by_pic(self.get_page_shot("confirm_button.png"), retry=3,
                                                    sim_no_reduce=True)
        assert confirm_result, log.log_error("点击从任务栏取消固定二次确认按钮失败", need_assert=False)

        utils.perform_sleep(2)

        find_result = utils.find_element_by_pic(self.get_page_shot("task_bar_start_button.png"), retry=3,
                                                sim_no_reduce=True)[0]
        assert not find_result, log.log_error("校验任务栏图标失败", need_assert=False)


if __name__ == '__main__':
    page = StartMenuProPage()
    page.click_menu_button()
    perform_sleep(5)
