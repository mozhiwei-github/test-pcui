# !/usr/bin/evn python
# --coding = 'utf-8' --
import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location
from duba.PageObjects.vip_page import vip_page

"""文字转语音"""


class TextToVoicePage(BasePage):
    def pre_open(self):
        # 从会员页进入文字转语音页
        self.vp = vip_page()
        self.vp.font_to_voice_click()

    def page_confirm_close(self):
        find_result, tab_close_position = utils.find_element_by_pic(self.get_page_shot("tip_create_icon.png"),
                                                                    location=Location.LEFT_UP.value, retry=2)
        if find_result:
            log.log_info("关闭二次确认弹窗")
            utils.mouse_click(tab_close_position[0] + 106, tab_close_position[1] + 134)  # 点击退出程序

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = TextToVoicePage()
    page.click_login_button()
    time.sleep(1)
