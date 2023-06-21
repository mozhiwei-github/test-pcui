import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location
from duba.PageObjects.vip_page import vip_page

"""隐私护盾"""


class PrivacyShieldPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0):
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec)

        log.log_info("查找升级会员提示弹窗")
        vip_prompt_result, vip_prompt_position = utils.find_element_by_pic(
            self.get_page_shot("upgrade_vip_prompt_tab_logo.png"),
            sim=0.9, retry=2, hwnd=self.hwnd,
            location=Location.LEFT_UP.value)
        if vip_prompt_result:
            log.log_info("关闭升级会员提示弹窗")
            utils.mouse_click(vip_prompt_position[0] + 339, vip_prompt_position[1] + 15)
        else:
            log.log_info("未找到升级会员提示弹窗")

    def pre_open(self):
        # 从会员页进入隐私护盾页
        self.vp = vip_page()
        self.vp.privacy_shield_click()

    def page_confirm_close(self):
        # 查找并关闭添加桌面图标弹窗
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(
            self.get_page_shot("desktop_icon_prompt_tab_logo.png"), sim=0.9, retry=2, sim_no_reduce=True,
            hwnd=self.hwnd,
            location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 485, prompt_pos[1] + 15)
        else:
            log.log_info("未找到添加桌面图标弹窗")

    @page_method_record("点击登录按钮")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("login_button1.png"),
                                            self.get_page_shot("login_button2.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("开启基础防护总开关")
    def open_basic_protection(self):
        ret1 = utils.find_element_by_pic(self.get_page_shot("base_open.png"), retry=3,
                                         sim_no_reduce=True)[0]
        if ret1:
            log.log_info("基础防护总开关已开启, 无需再次开启")
            return
        ret = utils.find_element_by_pic(self.get_page_shot("basic_protection_close_btn.png"))[1]
        utils.mouse_click(ret[0] + 132, ret[1])

    @page_method_record("开启增强防护总开关")
    def open_enhanced_protection(self):
        ret1 = utils.find_element_by_pic(self.get_page_shot("all_open_sign.png"), retry=3,
                                         sim_no_reduce=True)[0]
        if ret1:
            log.log_info("增强防护总开关已开启, 无需再次开启")
            return
        ret = utils.find_element_by_pic(self.get_page_shot("enhanced_protection_close_btn.png"))[1]
        utils.mouse_click(ret[0] + 132, ret[1])

    def click_i_know_btn(self):
        """
        判断是否弹出风险预制窗口，有则关闭
        :return:
        """
        ret = utils.find_element_by_pic(self.get_page_shot("risk_prediction_window.png"),
                                        retry=10, sim_no_reduce=True)[0]
        if not ret:
            log.log_info("无弹出风险预知窗口")
            return
        return utils.click_element_by_pic(self.get_page_shot("i_know_btn.png"))

    def check_basic_protection_open(self):
        """
        检查基础防护是否开启成功
        :return:
        """
        ret1 = utils.find_element_by_pic(self.get_page_shot("base_open.png"), retry=3,
                                         sim_no_reduce=True)[0]
        if ret1:
            log.log_info("基础防护总开关已开启")
            return True
        else:
            log.log_info("基础防护未开启")
            return False

    def check_enhanced_protection_open(self):
        """
        检查增强防护是否开启成功
        :return:
        """
        ret1 = utils.find_element_by_pic(self.get_page_shot("all_open_sign.png"), retry=3,
                                         sim_no_reduce=True)[0]
        if ret1:
            log.log_info("增强防护总开关已开启")
            return True
        else:
            log.log_info("增强防护未开启")
            return False


if __name__ == '__main__':
    page = PrivacyShieldPage()
    page.open_basic_protection()
    page.open_enhanced_protection()
    time.sleep(1)
