import os

import allure

from common.samba import Samba
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.main_page import main_page
from common.basepage import BasePage, page_method_record
from common import utils
from common.utils import Location, perform_sleep, find_element_by_pic
from common.log import log

"""
弹窗拦截页面
"""


class PopupInterceptPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        # 查找并关闭用户体验改进弹窗
        log.log_info("查找并关闭用户体验改进弹窗")
        prompt_result, prompt_position = utils.find_element_by_pic(
            self.get_page_shot("improve_user_experience_tab_logo.png"), sim=0.9, hwnd=self.hwnd, sim_no_reduce=True,
            location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭用户体验改进弹窗")
            utils.mouse_click(prompt_position[0] + 465, prompt_position[1] + 15)
        else:
            log.log_info("未查找用户体验改进弹窗")

    def pre_open(self):
        self.mp = main_page()
        self.mp.popup_intercept_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        # 查找并关闭退出确认弹窗
        log.log_info("检测自动拦截功能弹窗")
        prompt_result, prompt_position = utils.find_element_by_pic(self.get_page_shot("prompt_tab_logo.png"),
                                                                   location=Location.LEFT_UP.value, sim=0.9, retry=2,
                                                                   sim_no_reduce=True, hwnd=self.hwnd)
        if prompt_result:
            log.log_info("关闭自动拦截功能弹窗")
            utils.mouse_click(prompt_position[0] + 338, prompt_position[1] + 15)

    # 点击扫描
    @page_method_record("点击扫描")
    def scan_click(self):
        return utils.mouse_click(self.position[0] + 777, self.position[1] + 185)

    # 弹窗拦截会员中心
    @page_method_record("点击会员中心")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("nor_center.png"), self.get_page_shot("vip_center.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击升级会员按钮")
    def click_upgrade_vip_button(self):
        return utils.click_element_by_pic(self.get_page_shot("upgrade_vip_button.png"), retry=3)

    @page_method_record("执行拦截样本")
    def execute_demo_exe(self, exe_name):
        yangben_path = os.path.join(os.getenv("temp"), "yangben")
        exe_demo_file = yangben_path + os.path.sep + exe_name

        if not os.path.exists(exe_demo_file):
            samba_o = Samba("10.12.36.203", "duba", "duba123")
            demo_path = os.path.join("autotest", "popintercept")
            samba_o.download_dir("TcSpace", demo_path, yangben_path)

        if os.path.exists(exe_demo_file):
            if "winrar.exe" == exe_name:
                param = " /posx:710 /posy:320 /width:500 /height:400 /popclass:\"RarReminder\" /poptitle:\"1\" /popstyle:0 /closesleep:0 /hide:0"
            if "ucalendar.exe" == exe_name:
                param = " /posx:1620 /posy:770 /width:300 /height:270 /popclass:\"1\" /poptitle:\"1\" /popstyle:0 /closesleep:0 /hide:0"
            cmdstr = exe_demo_file + param
            utils.process_start(cmdstr, async_start=True)
            if utils.find_element_by_pic(self.get_page_shot("pop_system_block.png"), retry=2, sim_no_reduce=True)[0]:
                if utils.click_element_by_pic(self.get_page_shot("button_add_trust.png"), retry=3):
                    utils.process_start(cmdstr, async_start=True)
            return True
        return False

    @page_method_record("点击盖帽泡泡拦截弹窗")
    def click_block_hat_pop(self):
        if utils.find_element_by_pic(self.get_page_shot("tab_pop_hat.png"), retry=2, sim_no_reduce=True)[0]:
            if utils.click_element_by_pic(self.get_page_shot("button_block.png"), retry=2, sim_no_reduce=True):
                return True
        return False

    @page_method_record("点击盖帽泡泡不拦截弹窗")
    def click_no_block_hat_pop(self):
        if utils.find_element_by_pic(self.get_page_shot("tab_pop_hat.png"), retry=2, sim_no_reduce=True)[0]:
            if utils.click_element_by_pic(self.get_page_shot("button_no_block.png"), retry=2, sim_no_reduce=True):
                return True
        return False

    @page_method_record("清空不拦截软件记录")
    def clear_no_block_mark(self):
        if utils.click_element_by_pic(self.get_page_shot("button_no_block_mark.png"), retry=2, sim_no_reduce=True):
            if utils.find_element_by_pic(self.get_page_shot("tip_have_no_no_block.png"), retry=2,
                                         sim_no_reduce=True)[0]:
                utils.click_element_by_pic(self.get_page_shot("exit_mark_win.png"), retry=2, sim_no_reduce=True)
                return True
            elif utils.click_element_by_pic(self.get_page_shot("button_all_cancel.png"), retry=2, sim_no_reduce=True):
                return True
        return False

    @page_method_record("清空拦截软件记录")
    def clear_block_mark(self):
        if utils.click_element_by_pic(self.get_page_shot("button_block_mark.png"), retry=2, sim_no_reduce=True):
            if utils.find_element_by_pic(self.get_page_shot("tip_have_no_block.png"), retry=2,
                                         sim_no_reduce=True)[0]:
                utils.click_element_by_pic(self.get_page_shot("exit_mark_win.png"), retry=2, sim_no_reduce=True)
                return True
            elif utils.click_element_by_pic(self.get_page_shot("button_all_cancel.png"), retry=2, sim_no_reduce=True):
                return True
        return False

    @page_method_record("点击扫描按钮")
    def click_scan(self):
        if utils.click_element_by_pic(self.get_page_shot("button_scan.png"), retry=2, sim_no_reduce=True):
            utils.perform_sleep(5)
            if utils.find_element_by_pic(self.get_page_shot("button_scan_back.png"), retry=10, sim_no_reduce=True)[0]:
                return True
        return False

    @page_method_record("点击扫描返回按钮")
    def click_scan_back(self):
        if utils.click_element_by_pic(self.get_page_shot("button_scan_back.png"), retry=10, sim_no_reduce=True):
            return True
        return False


if __name__ == '__main__':
    from duba.PageObjects.vip_page import vip_kaitong_page, vip_page, VipPageShot

    # vp = vip_page()
    # vp.tanchuang_lanjie_click()
    test = PopupInterceptPage()
    test.execute_demo_exe("winrar.exe")
    # re = test.click_block_hat_pop()
    # print(re)
    utils.perform_sleep(3)
    re = test.click_no_block_hat_pop()
    print(re)
    # test.vip_center_click()
    # print(test.position)
    # print(test.rect_pos)
    # print(test.hwnd)

    # print("vip_center_click")
    # perform_sleep(3)
    # vp = vip_kaitong_page(False)
    # paycodes_price_list = vp.get_each_paycodes_price(tool="弹窗拦截")
    # screen_price_list = vp.get_price_on_screen()
    # log.log_info("paycodes_price_list {}".format(paycodes_price_list))
    # log.log_info("screen_price_list {}".format(screen_price_list))
    # if paycodes_price_list == screen_price_list:
    #     log.log_pass("对比价格一致")
    # else:
    #     log.log_error("对比价格不一致")
    # perform_sleep(3)
    # test.page_close()
