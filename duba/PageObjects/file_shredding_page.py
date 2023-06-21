#!/usr/bin/evn python
# --coding = 'utf-8' --
import os
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.samba import Samba
from common.utils import perform_sleep
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page

"""文件粉碎页"""

file_share_path = os.path.join("autotest", "FileShredding")  # 粉碎的文件的共享目录
file_local_path = os.path.join("C:\\", "FileShredding")  # 粉碎的文件的本地目录


def pull_file():
    cr = Samba("10.12.36.203", "duba", "duba123")
    cr.download_dir("TcSpace", file_share_path,
                    file_local_path)


class FileShreddingPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0, is_monitor_perf=True, from_bbx=False):
        self.from_bbx = from_bbx
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec,
                         is_monitor_perf=is_monitor_perf)

    def pre_open(self):
        if not self.from_bbx:
            # 从会员页进入文件粉碎页
            self.vp = vip_page()
            self.vp.file_shredding_click()
        else:
            self.bbxp = baibaoxiang_page()
            self.bbxp.filedestroy_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))

    @page_method_record("打开会员中心")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("upgrade_vip_button.png")])

    @page_method_record("点击添加文件图标")
    def click_add_file_icon(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_icon.png"))

    @page_method_record("点击添加文件按钮")
    def click_add_file_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_button.png"))

    @page_method_record("点击添加文件夹按钮")
    def click_add_folder_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_folder_button.png"))

    @page_method_record("点击添加文件窗口打开按钮")
    def click_add_file_open_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_open_button.png"))

    @page_method_record("点击添加文件窗口取消按钮")
    def click_add_file_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_file_cancel_button.png"))

    @page_method_record("点击新建文件夹按钮（添加文件夹窗口）")
    def click_add_folder_create_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_folder_create_button.png"))

    @page_method_record("点击确定按钮（添加文件夹窗口）")
    def click_add_folder_confirm_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_folder_confirm_button.png"))

    @page_method_record("点击取消按钮（添加文件夹窗口）")
    def click_add_folder_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("add_folder_cancel_button.png"))

    @page_method_record("查看粉碎历史")
    def open_shredding_history(self):
        click_result = utils.click_element_by_pic(self.get_page_shot("shredding_history_button.png"))
        if click_result and utils.find_element_by_pic(self.get_page_shot("shredding_history_tab_logo.png"), sim=0.8)[0]:
            return True
        return False

    @page_method_record("清空粉碎历史")
    def clear_shredding_history(self):
        return utils.click_element_by_pic(self.get_page_shot("clear_shredding_history_button.png"))

    @page_method_record("关闭粉碎历史")
    def exit_shredding_history(self):
        return utils.click_element_by_pic(self.get_page_shot("exit_shredding_history_button.png"))

    @page_method_record("点击一键粉碎按钮")
    def click_start_shredding_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_shredding_button.png"))

    @page_method_record("点击全选按钮")
    def click_select_add_button(self):
        return utils.click_element_by_pic(self.get_page_shot("select_all_button.png"))

    @page_method_record("点击确认按钮")
    def click_confirm_btn(self):
        return utils.click_element_by_pic(self.get_page_shot("confirm_btn.png"))

    @page_method_record("检查是否清理结束")
    def check_clean_finished(self):
        res = utils.find_element_by_pic(self.get_page_shot("clean_finished_tab.png"), sim_no_reduce=True, retry=3)
        for i in range(35):
            if res:
                self.click_confirm_btn()
                log.log_info("清理结束")
                return True
            res = utils.find_element_by_pic(self.get_page_shot("clean_finished_tab.png"), sim_no_reduce=True, retry=3)
            utils.perform_sleep(1)
        log.log_info("清理超时，超过35s")
        return False


if __name__ == '__main__':
    pull_file()


