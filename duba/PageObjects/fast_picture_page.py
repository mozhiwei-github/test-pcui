from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location, perform_sleep
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.vip_page import vip_page

"""毒霸看图"""


class FastPicturePage(BasePage):
    """毒霸看图页"""

    def pre_open(self):
        # 从会员页进入毒霸看图页
        self.vp = vip_page()
        self.vp.duba_see_pic_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        log.log_info("检测二次确认窗（默认工具）")
        find_result, tab_close_position = utils.find_element_by_pic(self.get_page_shot("tab_close_confirm.png"),
                                                                    location=Location.LEFT_UP.value, retry=2,
                                                                    hwnd=self.hwnd)
        if find_result:
            log.log_info("关闭二次确认窗（默认工具）")
            utils.mouse_click(tab_close_position[0] + 377, tab_close_position[1] + 16)  # 点击关闭
            return

        log.log_info("检测二次确认窗（桌面图标）")
        find_result_2, tab_close_position_2 = utils.find_element_by_pic(self.get_page_shot("tab_close_confirm_2.png"),
                                                                        location=Location.LEFT_UP.value, retry=2,
                                                                        hwnd=self.hwnd)
        if find_result_2:
            log.log_info("关闭二次确认窗（桌面图标）")
            utils.mouse_click(tab_close_position_2[0] + 361, tab_close_position_2[1] + 18)  # 点击关闭
            return

    @page_method_record("点击打开图片按钮")
    def click_open_image_button(self):
        return utils.click_element_by_pic(self.get_page_shot("open_image_button.png"))

    @page_method_record("点击打开按钮（添加图片窗口）")
    def click_add_image_open_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_image_open_button.png"))

    @page_method_record("点击取消按钮（添加图片窗口）")
    def click_add_image_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_image_cancel_button.png"))

    @page_method_record("打开图片美化")
    def open_picture_beautification(self):
        return utils.click_element_by_pic(self.get_page_shot("picture_beautification_button.png"))


class PictureBeautificationPage(BasePage):
    """毒霸看图页 —— 图片美化页"""

    def pre_open(self):
        self.fp = FastPicturePage()
        self.fp.open_picture_beautification()

    @page_method_record("点击会员中心按钮")
    def click_vip_center_button(self):
        return utils.click_element_by_pic(self.get_page_shot("vip_center_button.png"))


if __name__ == '__main__':
    # page = FastPicturePage()
    # page.open_picture_beautification()
    # perform_sleep(1)
    # picture_beautification_page = PictureBeautificationPage(False)

    picture_beautification_page = PictureBeautificationPage()
    perform_sleep(1)
