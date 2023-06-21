# --coding = 'utf-8' --
from common.basepage import BasePage, page_method_record
from common import utils
from common.log import log
from common.utils import perform_sleep, Location
from duba.PageObjects.main_page import main_page

"""主界面设置页"""


class SettingPage(BasePage):
    def pre_open(self):
        # TODO：执行打开动作
        self.mp = main_page()
        self.mp.setting_center_menu_click()
        utils.click_element_by_pic(self.get_page_shot("button_setting_center.png"), sim=0.8, retry=3)

    @page_method_record("点击其他设置页")
    def other_setting(self):
        return utils.click_element_by_pic(self.get_page_shot("button_other_setting.png"), sim=0.9, retry=3)

    @page_method_record("关闭自保护")
    def self_protecting_close(self):
        self.other_setting()
        self_protecting_result, position = utils.find_element_by_pic(
            self.get_page_shot("button_self_protecting_close.png"),
            sim=0.9, sim_no_reduce=True, retry=3,
            location="left_upper_corner")
        if self_protecting_result:
            perform_sleep(1)
            utils.mouse_click(position)
            return utils.find_element_by_pic(self.get_page_shot("check_self_protecting_status.png"), sim=0.9, retry=2,
                                             sim_no_reduce=True)[0]
        return False

    @page_method_record("打开自保护")
    def self_protecting_open(self):
        self.other_setting()
        self_protecting_result, position = utils.find_element_by_pic(
            self.get_page_shot("button_self_protecting_open.png"),
            sim=0.9, sim_no_reduce=True, retry=3,
            location="left_upper_corner")
        if self_protecting_result:
            perform_sleep(1)
            utils.mouse_click(position)
            return utils.find_element_by_pic(self.get_page_shot("check_self_protecting_status_open.png"), sim=0.9, retry=2,
                                             sim_no_reduce=True)[0]
        return False

    # 判断自保护状态
    @page_method_record("判断当前自保护状态")
    def get_protect_status(self):
        self.other_setting()
        return utils.find_element_by_pic(self.get_page_shot("protect_open.png"),retry=2)[0]

    @page_method_record("开启截图快捷键")
    def screen_capture_hotkey_enable(self):
        find_result, find_pos = utils.find_element_by_pic(self.get_page_shot("hotkey_switch_disable.png"), sim=0.9,
                                                          retry=2, sim_no_reduce=True, location=Location.RIGHT_UP.value)
        if find_result:
            log.log_info("点击截图快捷键开关")
            switch_pos = (find_pos[0] - 20, find_pos[1] + 10)
            utils.mouse_click(switch_pos)

    @page_method_record("关闭截图快捷键")
    def screen_capture_hotkey_disable(self):
        find_result, find_pos = utils.find_element_by_pic(self.get_page_shot("hotkey_switch_enable.png"), sim=0.9,
                                                          retry=2, sim_no_reduce=True, location=Location.RIGHT_UP.value)
        if find_result:
            log.log_info("点击截图快捷键开关")
            switch_pos = (find_pos[0] - 20, find_pos[1] + 10)
            utils.mouse_click(switch_pos)

    @page_method_record("修改截图快捷键")
    def change_screen_capture_hotkey(self, hotkey_pic_name="screen_capture_hotkey_alt_a_close.png"):
        # 开启截图快捷键
        self.screen_capture_hotkey_enable()
        perform_sleep(1)
        # 修改截图快捷键
        find_result, find_pos = utils.find_element_by_pic(self.get_page_shot(hotkey_pic_name), sim=0.95, retry=2,
                                                          sim_no_reduce=True, location=Location.LEFT_UP.value)
        if find_result:
            log.log_info("点击快捷键前的选项框")
            utils.mouse_click(find_pos[0] + 3, find_pos[1] + 3)
        else:
            log.log_info("当前快捷键已和要设置的快捷键一致")


if __name__ == '__main__':
    sp = SettingPage()
    log.log_debug(sp.self_protecting_close())
    perform_sleep(5)
