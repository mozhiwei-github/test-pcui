#!/usr/bin/evn python
# --coding = 'utf-8' --
import time
from common import utils
from common.basepage import BasePage, page_method_record
from duba.PageObjects.vip_page import vip_page

"""网络测速"""


class NetworkSpeedPage(BasePage):
    def pre_open(self):
        # 从会员页进入网络测速页
        self.vp = vip_page()
        self.vp.network_speed_click()

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = NetworkSpeedPage()
    page.click_login_button()
    time.sleep(1)
