from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
from common.unexpectwin_system import UnExpectWin_System
from common.utils import perform_sleep, Location
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.vip_page import vip_page

"""系统碎片清理王"""


class DefragPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        perform_sleep(10)

        log.log_info("查找新手指引弹窗")
        if utils.find_element_by_pic(self.get_page_shot("guide_tab_logo.png"), sim=0.9, retry=5, sim_no_reduce=True,
                                     hwnd=self.hwnd)[0]:
            log.log_info("关闭新手指引弹窗")
            assert utils.click_element_by_pic(self.get_page_shot("guide_exit_button.png"), retry=2,
                                              hwnd=self.hwnd), "点击新手指引弹窗关闭按钮失败"
        else:
            log.log_info("未找到新手指引弹窗")

        # 查找并关闭升级会员弹窗
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.EXIT_VIP_UPDATE, find_retry=2, hwnd=self.hwnd):
            perform_sleep(1)
        # 查找快速登录弹窗（游客状态下弹出）
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.QUICK_LOGIN, hwnd=self.hwnd):
            perform_sleep(1)

    def pre_open(self):
        # 从会员页进入系统碎片清理王页
        self.vp = vip_page()
        self.vp.system_defrag_click()

    def page_confirm_close(self):
        perform_sleep(2)

        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        # # 关闭升级VIP提示弹窗
        # log.log_info("正在检测升级VIP提示弹窗")
        # find_result, position = utils.find_element_by_pic(self.get_page_shot("tab_update_vip.png"),
        #                                                   location=Location.LEFT_UP.value,
        #                                                   sim=0.8, retry=3, sim_no_reduce=True, hwnd=self.hwnd)
        # if find_result:
        #     utils.mouse_click(position[0] + 379, position[1] + 15)
        #
        # # 关闭温馨提示弹窗
        # log.log_info("正在检测温馨提示弹窗")
        # if utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"), sim=0.8, retry=3, sim_no_reduce=True,
        #                              hwnd=self.hwnd)[0]:
        #     self.click_prompt_confirm_button(hwnd=self.hwnd)
        UnExpectWin_System().unexpectwin_detect_beta()

    @page_method_record("点击确定按钮（退出弹窗）")
    def click_prompt_confirm_button(self, hwnd=None):
        return utils.click_element_by_pic(self.get_page_shot("prompt_confirm_button.png"), hwnd=hwnd,
                                          sim_no_reduce=True)

    @page_method_record("点击取消按钮（退出弹窗）")
    def click_prompt_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_cancel_button.png"), sim_no_reduce=True)

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        # # 关闭升级VIP提示弹窗
        # find_result, position = utils.find_element_by_pic(self.get_page_shot("tab_update_vip.png"),
        #                                                   location=Location.LEFT_UP.value,
        #                                                   sim=0.8, retry=3, sim_no_reduce=True, hwnd=self.hwnd)
        # if find_result:
        #     utils.mouse_click(position[0] + 379, position[1] + 15)
        UnExpectWin_System().unexpectwin_detect_beta()
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"), sim_no_reduce=True)


if __name__ == '__main__':
    page = DefragPage()
    # page.click_login_button()
    # perform_sleep(1)
