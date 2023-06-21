#!/usr/bin/evn python
# --coding = 'utf-8' --
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location, perform_sleep
from common.tools.base_tools import get_page_shot
from duba.PageObjects.vip_page import vip_page

"""录屏大师"""


class ScreenRecordPage(BasePage):
    def pre_open(self):
        # 从会员页进入录屏大师页
        self.vp = vip_page()
        self.vp.screen_record_click()

    def page_confirm_close(self):
        find_result, tab_close_position = utils.find_element_by_pic(self.get_page_shot("tab_close_confirm.png"),
                                                                    location=Location.LEFT_UP.value, retry=2)
        if find_result:
            log.log_info("关闭二次确认弹窗")
            utils.mouse_click(tab_close_position[0] + 146, tab_close_position[1] + 160)  # 点击退出程序
            perform_sleep(1)
            utils.mouse_click(tab_close_position[0] + 271, tab_close_position[1] + 241)  # 点击确定

        # 查找并关闭添加桌面图标弹窗
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(
            self.get_page_shot("desktop_icon_prompt_tab_logo.png"), sim=0.9, retry=2, sim_no_reduce=True,
            hwnd=self.hwnd,
            location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 380, prompt_pos[1] + 15)
        else:
            log.log_info("未找到添加桌面图标弹窗")

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    find_result, tab_close_position = utils.find_element_by_pic(
        get_page_shot("screen_record_page", "tab_close_confirm.png"), location=Location.LEFT_UP.value, retry=2)
    if find_result:
        log.log_info("关闭二次确认窗")
        utils.mouse_click(tab_close_position[0] + 146, tab_close_position[1] + 160)  # 点击退出程序
        perform_sleep(1)
        utils.mouse_click(tab_close_position[0] + 271, tab_close_position[1] + 241)  # 点击确定
    perform_sleep(1)
