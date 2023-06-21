import time
from common import utils
from common.basepage import BasePage, page_method_record
from duba.PageObjects.vip_page import vip_page

"""孩子守护王"""


class TeenModePage(BasePage):
    def pre_open(self):
        # 从会员页进入孩子守护王页
        self.vp = vip_page()
        self.vp.teen_mode_click()

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = TeenModePage()
    page.click_login_button()
    time.sleep(1)
