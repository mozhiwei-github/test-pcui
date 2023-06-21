#!/usr/bin/evn python
# --coding = 'utf-8' --
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import Location, perform_sleep
from duba.PageObjects.vip_page import vip_page
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo

"""超级隐私清理"""


class PrivacyCleanerPage(BasePage):
    def pre_open(self):
        # 从会员页进入超级隐私清理页
        self.vp = vip_page()
        self.vp.privacy_clean_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        # 查找并关闭添加桌面图标弹窗
        log.log_info("查找添加桌面图标弹窗")
        prompt_result, prompt_pos = utils.find_element_by_pic(
            self.get_page_shot("desktop_icon_tab_logo.png"), sim=0.9, retry=3, location=Location.LEFT_UP.value)
        if prompt_result:
            log.log_info("关闭添加桌面图标弹窗")
            utils.mouse_click(prompt_pos[0] + 471, prompt_pos[1] + 20)
        else:
            log.log_info("未找到添加桌面图标弹窗")

        log.log_info("查找垃圾清理弹窗")
        self.click_give_up_trash_clean()


    @page_method_record("点击开始扫描按钮")
    def click_start_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_scanning.png"))

    @page_method_record("点击会员中心")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("upgrade_vip_button.png"),
                                            self.get_page_shot("vip_center.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击一键清理")
    def click_clean(self):
        return utils.click_element_by_pic(self.get_page_shot("clean_button.png"))

    def check_cleaning(self):
        """
        检查是否正在清理中
        :return:
        """
        for i in range(40):
            utils.perform_sleep(1)
            res, pos = utils.find_element_by_pic(self.get_page_shot("finish_button.png"), retry=2, sim_no_reduce=True)
            if res:
                log.log_info("清理结束")
                return True
            log.log_info("清理中......")
        log.log_info("清理时间超过40s")
        return False

    def check_scaning(self):
        """
        检查是否正在扫描中
        :return:
        """
        for i in range(60):
            utils.perform_sleep(1)
            res, pos = utils.find_element_by_pic(self.get_page_shot("clean_button.png"), retry=2,
                                                 sim_no_reduce=True)
            if res:
                log.log_info("扫描结束")
                return True
            log.log_info("扫描中......")
        log.log_error("扫描超时", need_assert=False)
        return False

    @page_method_record("点击其他敏感隐私的勾选框")
    def click_sensitive_privacy_item(self):
        ret, pos = utils.find_element_by_pic(self.get_page_shot("sensitive_privacy_item.png"))
        utils.mouse_click_int(pos[0] + 20, pos[1] + 20)

    def check_clipboard(self):
        if utils.get_clipboard_text() is None:
            log.log_info("剪切板为空")
            return True
        log.log_info("注意：剪切板不为空")
        return False

    @page_method_record("关闭高危隐私提醒窗")
    def close_high_rish_remind_tab(self):
        """
        关闭高危隐私提醒窗
        """

        utils.perform_sleep(1)
        res, pos = utils.find_element_by_pic(self.get_page_shot("high_risk_remind_tab.png"))
        if not res:
            return False
        return utils.mouse_click_int(pos[0] + 588, pos[1] - 23)

    @page_method_record("点击关闭隐私清理界面时出现的暂不设置按钮")
    def click_no_setting(self):
        return utils.click_element_by_pic(self.get_page_shot("no_setting_button.png"))

    @page_method_record("点击放弃垃圾清理")
    def click_give_up_trash_clean(self):
        res, pos = utils.find_element_by_pic(self.get_page_shot("trash_clean_tab.png"))
        if not res:
            return
        utils.click_element_by_pic(self.get_page_shot("no_setting_button.png"))
        log.log_info("已点击放弃垃圾清理")

    @page_method_record("点击被占用窗口的提示")
    def click_close_occupy(self):
        res, pos = utils.find_element_by_pic(self.get_page_shot("occupy_tab.png"), retry=2)
        if not res:
            return
        utils.click_element_by_pic(self.get_page_shot("not_clean_temporarily.png"))
        log.log_info("已点击关闭被占用窗口的提示")

    @page_method_record("检查并关闭设置密码蒙层弹窗")
    def close_password_tips(self):
        res, pos = utils.find_element_by_pic(self.get_page_shot("password_tips_confirm.png"), retry=2)
        if not res:
            return
        utils.click_element_by_pic(self.get_page_shot("password_tips_confirm.png"))
        log.log_info("关闭密码设置提示蒙层")


if __name__ == '__main__':
    test = PrivacyCleanerPage()
