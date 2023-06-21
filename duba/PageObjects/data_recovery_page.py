#!/usr/bin/evn python
# --coding = 'utf-8' --
from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
from common.utils import perform_sleep
from duba.PageObjects.vip_page import vip_page

"""数据恢复页"""


class DataRecoveryPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 查找并关闭建议事项弹窗
        if self.exit_suggestions():
            perform_sleep(1)

    def pre_open(self):
        # 从会员页进入数据恢复页
        self.vp = vip_page()
        self.vp.data_recovery_click()

    def page_confirm_close(self):
        perform_sleep(5)

        # 关闭页面的二次确认
        close_result = self.close_confirm_modal()
        if not close_result:
            log.log_error("点击关闭数据恢复页二次确认按钮失败")
            return

        utils.mouse_move(0, 0)

        log.log_info("关闭数据恢复页成功")

    @page_method_record("关闭确认弹窗")
    def close_confirm_modal(self):
        if not utils.find_element_by_pic(self.get_page_shot("exit_confirm_tab_logo.png"), 0.8, hwnd=self.hwnd)[0]:
            return False

        return utils.click_element_by_pic(self.get_page_shot("exit_confirm_button.png"))

    @page_method_record("点击万能恢复功能")
    def open_all_powerful_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 155)

    @page_method_record("点击删除文件恢复功能")
    def open_delete_file_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 220)

    @page_method_record("点击误格式化恢复功能")
    def open_heedless_format_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 285)

    @page_method_record("点击U盘/手机相机卡功能")
    def open_usb_flash_drive_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 347)

    @page_method_record("点击误清空回收站功能")
    def open_computer_recycle_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 413)

    @page_method_record("点击磁盘分区丢失功能")
    def open_disk_partition_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 476)

    @page_method_record("点击手机内置卡恢复功能")
    def open_phone_builtin_card_recovery(self):
        utils.mouse_click(self.position[0] + 100, self.position[1] + 540)

    @page_method_record("点击开始恢复按钮")
    def click_start_recovery_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_recovery_button.png"))

    @page_method_record("点击一键开启按钮")  # 手机内置卡恢复
    def click_one_touch_start_button(self):
        return utils.click_element_by_pic(self.get_page_shot("one_touch_start_button.png"))

    @page_method_record("点击返回上一步按钮")
    def click_previous_step_button(self):
        return utils.click_element_by_pic(self.get_page_shot("previous_step_button.png"))

    @page_method_record("点击开始扫描按钮")
    def click_start_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_scanning_button.png"))

    @page_method_record("点击中断扫描按钮")
    def click_stop_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("stop_scanning_button.png"))

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))

    @page_method_record("打开使用帮助")
    def open_using_help(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("using_help_button.png"))
        if click_result and utils.find_element_by_pic(self.get_page_shot("using_help_tab_logo.png"), sim=0.8)[0]:
            return True
        return False

    @page_method_record("关闭使用帮助")
    def exit_using_help(self):
        return utils.click_element_by_pic(self.get_page_shot("exit_using_help_button.png"))

    @page_method_record("打开建议事项")
    def open_suggestions(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("suggestions_button.png"))
        if click_result and utils.find_element_by_pic(self.get_page_shot("suggestions_tab_logo.png"), sim=0.8)[0]:
            return True
        return False

    @page_method_record("查找并关闭建议事项")
    def exit_suggestions(self):
        if utils.find_element_by_pic(self.get_page_shot("suggestions_tab_logo.png"), sim=0.9, retry=2)[0]:
            return utils.click_element_by_pic(self.get_page_shot("exit_suggestions_button.png"))
        log.log_info("未找到建议事项弹窗")
        return False

    @page_method_record("点击我知道了按钮")
    def click_i_know_button(self):
        return utils.click_element_by_pic(self.get_page_shot("i_know_button.png"))

    @page_method_record("点击用户信息按钮")
    def click_user_info_button(self):
        btn_result, btn_position = utils.find_element_by_pic(self.get_page_shot("user_info_button.png"), 0.9, retry=2)
        if not btn_result:
            return False

        utils.mouse_click(btn_position)
        utils.mouse_move(btn_position[0], btn_position[1] + 20)
        return True

    @page_method_record("点击立刻充值按钮")
    def click_recharge_now_button(self):
        return utils.click_element_by_pic(self.get_page_shot("recharge_now_button.png"))

    @page_method_record("打开数据恢复支付页")
    def open_recharge_page(self):
        # 点击用户信息按钮
        assert self.click_user_info_button(), "点击用户信息按钮失败"
        # 点击立刻充值按钮
        assert self.click_recharge_now_button(), "点击立刻充值按钮失败"


if __name__ == '__main__':
    page = DataRecoveryPage()
    # 误删恢复
    page.open_computer_recycle_recovery()
    perform_sleep(1)
    page.click_start_recovery_button()
    perform_sleep(1)
    # 中止扫描
    page.click_stop_scanning_button()
    perform_sleep(1)
    page.close_confirm_modal()
    perform_sleep(1)
    # 返回上一步
    page.click_previous_step_button()
    perform_sleep(1)
    page.close_confirm_modal()
    perform_sleep(5)
