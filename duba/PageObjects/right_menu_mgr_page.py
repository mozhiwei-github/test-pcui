#!/usr/bin/evn python
# --coding = 'utf-8' --
import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location
from duba.PageObjects.vip_page import vip_page

"""右键菜单管理"""


class RightMenuMgrPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 不使用窗口右上角坐标关闭
        self.enable_rect_pos_close = False

    def pre_open(self):
        # 从会员页进入右键菜单管理页
        self.vp = vip_page()
        self.vp.right_mouse_menu_click()

    def page_confirm_close(self):
        # 在扫描中点击关闭会有提示框，自动点击放弃扫描
        if utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"), sim=0.9, retry=2, hwnd=self.hwnd,
                                     sim_no_reduce=True)[0]:
            return self.click_prompt_giveup_scanning_button(hwnd=self.hwnd)

        # 查找并关闭满意评价弹窗
        log.log_info("查找满意评价弹窗A")
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("satisfaction_prompt_tab_logo_1.png"),
                                                              sim=0.8, retry=3, sim_no_reduce=True, hwnd=self.hwnd,
                                                              location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭满意评价弹窗A")
            utils.mouse_click(prompt_pos[0] + 435, prompt_pos[1] + 15)
        else:
            log.log_info("未找到满意评价弹窗A")

        log.log_info("查找满意评价弹窗B")
        prompt_result, prompt_pos = utils.find_element_by_pic(self.get_page_shot("satisfaction_prompt_tab_logo_2.png"),
                                                              sim=0.8, retry=3, sim_no_reduce=True, hwnd=self.hwnd,
                                                              location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭满意评价弹窗B")
            utils.mouse_click(prompt_pos[0] + 381, prompt_pos[1] + 18)
        else:
            log.log_info("未找到满意评价弹窗B")

        # 查找并关闭添加桌面图标弹窗
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(
            self.get_page_shot("desktop_icon_prompt_tab_logo.png"), sim=0.9, retry=2, sim_no_reduce=True,
            hwnd=self.hwnd, location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 485, prompt_pos[1] + 15)
        else:
            log.log_info("未找到添加桌面图标弹窗")

    @page_method_record("点击放弃扫描按钮")
    def click_prompt_giveup_scanning_button(self, hwnd=None):
        return utils.click_element_by_pic(self.get_page_shot("prompt_giveup_scanning_button.png"), hwnd=hwnd)

    @page_method_record("点击继续扫描按钮")
    def click_prompt_continue_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("prompt_continue_scanning_button.png"))

    @page_method_record("点击登录按钮")
    def vip_center_click(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))

    @page_method_record("点击开始扫描按钮")
    def click_start_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_scanning.png"))

    @page_method_record("点击文件右键菜单tab")
    def click_file_tab(self):
        return utils.click_element_by_pic(self.get_page_shot("file_tab.png"))

    @page_method_record("点击文件夹右键菜单tab")
    def click_folder_tab(self):
        return utils.click_element_by_pic(self.get_page_shot("folder_tab.png"))

    @page_method_record("点击桌面右键菜单tab")
    def click_desktop_tab(self):
        return utils.click_element_by_pic(self.get_page_shot("desktop_tab.png"))

    @page_method_record("勾选文件右键菜单tab")
    def choose_file_tab(self):
        ret = utils.find_element_by_pic(self.get_page_shot("file_tab.png"), retry=3,
                                        sim_no_reduce=True)[1]
        utils.mouse_click(ret[0] - 94, ret[1])

    @page_method_record("勾选文件夹右键菜单tab")
    def choose_folder_tab(self):
        ret = utils.find_element_by_pic(self.get_page_shot("folder_tab.png"), retry=3,
                                        sim_no_reduce=True)[1]
        utils.mouse_click(ret[0] - 94, ret[1])

    @page_method_record("勾选桌面右键菜单tab")
    def choose_desktop_tab(self):
        ret = utils.find_element_by_pic(self.get_page_shot("desktop_tab.png"), retry=3,
                                        sim_no_reduce=True)[1]
        utils.mouse_click(ret[0] - 94, ret[1])

    @page_method_record("点击一键清理")
    def click_start_clean(self):
        return utils.click_element_by_pic(self.get_page_shot("start_cleanning.png"))

    @page_method_record("点击恢复删除记录")
    def click_recovery_btn(self):
        return utils.click_element_by_pic(self.get_page_shot("recovery_btn.png"))

    @page_method_record("全选删除记录")
    def choose_all_delete(self):
        ret = utils.find_element_by_pic(self.get_page_shot("recover_choose_all.png"), retry=3,
                                        sim_no_reduce=True)[1]
        utils.mouse_click(ret[0] - 19, ret[1])

    @page_method_record("点击恢复按钮")
    def click_recover_btn(self):
        return utils.click_element_by_pic(self.get_page_shot("recover_btn.png"))

    @page_method_record("点击恢复界面的关闭按钮")
    def click_recovery_close_btn(self):
        return utils.click_element_by_pic(self.get_page_shot("recovery_close_btn.png"))

    def stow_all_tab(self):
        """
        收起所有tab项
        :return:
        """
        if self.check_scan_finished():
            self.click_file_tab()
            self.click_folder_tab()
            self.click_desktop_tab()

    def choose_all_tab(self):
        """
        勾选所有tab项
        :return:
        """
        if self.check_scan_finished():
            self.choose_file_tab()
            self.choose_folder_tab()
            self.choose_desktop_tab()

    @page_method_record("检查是否扫描结束")
    def check_scan_finished(self):
        for i in range(60):
            utils.perform_sleep(1)
            ret = utils.find_element_by_pic(self.get_page_shot("start_cleanning.png"), retry=3,
                                            sim_no_reduce=True)[0]
            if ret:
                log.log_info("扫描结束")
                return True
        log.log_info("扫描一分钟后仍未结束")
        return False

    @page_method_record("检查是否清理结束")
    def check_clean_finished(self):
        for i in range(60):
            utils.perform_sleep(1)
            ret = utils.find_element_by_pic(self.get_page_shot("finished_sign.png"), retry=3,
                                            sim_no_reduce=True)[0]
            if ret:
                log.log_info("清理结束")
                return True
        log.log_info("清理一分钟后仍未结束")
        return False

    @page_method_record("检查是否恢复结束")
    def check_recover_finished(self):
        for i in range(60):
            utils.perform_sleep(1)
            ret = utils.find_element_by_pic(self.get_page_shot("recovered_sign.png"), retry=3,
                                            sim_no_reduce=True)[0]
            if ret:
                log.log_info("恢复结束")
                self.click_recovery_close_btn()
                return True
        log.log_info("恢复一分钟后仍未结束")
        return False


if __name__ == '__main__':
    page = RightMenuMgrPage()
    page.click_start_scanning_button()

    page.stow_all_tab()
    page.choose_all_tab()
    page.click_start_clean()
    page.check_clean_finished()
