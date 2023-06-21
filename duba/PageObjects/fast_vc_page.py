# !/usr/bin/evn python
# --coding = 'utf-8' --
import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location
from duba.PageObjects.vip_page import vip_page

"""毒霸视频格式专家"""


class FastVcPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 不使用窗口右上角坐标关闭
        self.enable_rect_pos_close = False

    def pre_open(self):
        # 从会员页进入毒霸视频格式专家页
        self.vp = vip_page()
        self.vp.fast_vc_click()

    def page_confirm_close(self):
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("desktop_icon_prompt_tab_logo.png"),
                                                              sim=0.9, retry=2, sim_no_reduce=True, hwnd=self.hwnd,
                                                              location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 423, prompt_pos[1] + 17)
        else:
            log.log_info("未找到添加桌面图标弹窗")

    @page_method_record("点击会员中心按钮")
    def click_vip_center_button(self):
        return utils.mouse_click(self.position[0] + 646, self.position[1] + 26)


if __name__ == '__main__':
    page = FastVcPage()
    page.click_vip_center_button()
    time.sleep(1)
