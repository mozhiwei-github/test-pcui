from common import utils
from common.basepage import BasePage, page_method_record
from common.utils import perform_sleep
from duba.PageObjects.data_recovery_page import DataRecoveryPage

"""手机数据恢复"""


class PhoneRecoveryPage(BasePage):
    def pre_open(self):
        # 从数据恢复进入手机数据恢复页
        self.dp = DataRecoveryPage()
        self.dp.open_phone_builtin_card_recovery()
        perform_sleep(1)
        self.dp.click_one_touch_start_button()

    def page_confirm_close(self):
        # 关闭退出确认弹窗
        if utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"), sim=0.8, sim_no_reduce=True,
                                     hwnd=self.hwnd)[0]:
            return self.click_prompt_confirm_button(hwnd=self.hwnd)

    @page_method_record("点击确定按钮（退出弹窗）")
    def click_prompt_confirm_button(self, hwnd=None):
        return utils.click_element_by_pic(self.get_page_shot("prompt_confirm_button.png"), hwnd=hwnd)

    @page_method_record("点击取消按钮（退出弹窗）")
    def click_prompt_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_cancel_button.png"))

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = PhoneRecoveryPage()
    # page.click_login_button()
    perform_sleep(1)
