import time
from common.log import log
from common.utils import Location
from common import utils
from common.basepage import BasePage, page_method_record
from duba.PageObjects.vip_page import vip_page

"""文档保护"""


class DocumentProtectPage(BasePage):
    def pre_open(self):
        # 从会员页进入文档保护页
        self.vp = vip_page()
        self.vp.file_guard_click()

    def page_confirm_close(self):
        # 查找并关闭添加桌面图标弹窗
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("desktop_icon_prompt_tab_logo.png"),
                                                              sim=0.9, retry=2, sim_no_reduce=True, hwnd=self.hwnd,
                                                              location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 485, prompt_pos[1] + 15)
        else:
            log.log_info("未找到添加桌面图标弹窗")

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))


if __name__ == '__main__':
    page = DocumentProtectPage()
    page.click_login_button()
    time.sleep(1)
