#!/usr/bin/evn python
# --coding = 'utf-8' --
# 垃圾清理页
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from duba.PageObjects.main_page import main_page
from duba.PageObjects.setting_page import SettingPage
import random


class RubbishCleanPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0, is_monitor_perf=True, close_protect=False):
        self.close_protect = close_protect
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec, is_monitor_perf=is_monitor_perf)
    def pre_open(self):
        # TODO：执行打开动作
        # 关闭自保护
        if self.close_protect:
            self.sp = SettingPage()
            self.sp.self_protecting_close()
            self.sp.page_del()
            utils.click_element_by_pic(self.get_page_shot("entry_rubbish_clean.png"), retry=2, sim=0.85)
        else:
            self.mp = main_page()
            self.mp.cleaner_click()

    @page_method_record("点击回首页按钮")
    def entry_homepage_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("return_homepage_button.png"), sim=0.8, retry=3)

    @page_method_record("点击界面返回按钮")
    def return_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("page_return_button.png"), sim=0.7, retry=3)

    @page_method_record("判断放弃清理按钮是否存在")
    def is_giveup_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("giveup_clean_button.png"), sim=0.8, retry=3)[0]

    @page_method_record("点击放弃清理按钮")
    def giveup_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("giveup_clean.png"), sim=0.7, retry=3)

    @page_method_record("点击重新扫描按钮")
    def rescan_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("rescan_button.png"), sim=0.8, retry=3)

    @page_method_record("点击一键清理按钮")
    def clean_up_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("clean_up_button.png"), sim=0.8, retry=3)

    @page_method_record("判断取消扫描是否成功")
    def is_scan_canceled_success(self):
        return utils.find_element_by_pic(
            self.get_page_shot("scan_canceled_word.png"), sim=0.8, retry=3)[0]

    @page_method_record("点击深度清理tab")
    def deep_clean_tab_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("deep_clean_tab.png"), sim=0.8, retry=3)

    @page_method_record("查找页面中的可勾选框并随机进行勾选")
    def select_checkbox_operation(self):
        checkbox_result, checkbox_list = utils.find_elements_by_pic(self.get_page_shot("select_checkbox.png"), sim=0.8, retry=2)
        if not checkbox_result:
            return False
        click_pos = checkbox_list[random.randint(0, len(checkbox_list)-1)]
        utils.mouse_click(click_pos)
        utils.perform_sleep(2)
        return True

    @page_method_record("判断选择清理项弹窗是否存在")
    def is_selected_window_exist(self):
        return utils.find_element_by_pic(self.get_page_shot("selected_window_tab.png"), sim=0.8, retry=3)

    @page_method_record("点击选择深度清理项弹窗确认按钮")
    def sure_button_click(self):
        utils.click_element_by_pic(self.get_page_shot("sure_button.png"), sim=0.7, retry=3)

    @page_method_record("点击取消按钮")
    def cancel_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("cancel_button.png"), sim=0.8, retry=3)

    @page_method_record("点击暂不清理按钮")
    def refuse_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("refuse_button.png"), sim=0.8, retry=3)

    @page_method_record("判断是否存在清理风险提示窗")
    def is_warning_page_exist(self):
        if not (utils.find_element_by_pic(
            self.get_page_shot("warning_page_tab_logo.png"), sim=0.8, retry=3)[0] and utils.find_element_by_pic(
            self.get_page_shot("warning_page_logo.png"), sim=0.8, retry=3)[0]):
            return False
        return True

    @page_method_record("点击风险提示泡确认按钮")
    def warning_pop_sure_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("warning_pop_sure_button.png"), sim=0.7, retry=3)

    @page_method_record("判断是否存在风险提示泡")
    def is_warning_pop_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("warning_pop_logo.png"), sim=0.8, retry=3)[0]

    @page_method_record("判断垃圾清理扫描状态")
    def check_scan_status(self):
        if not utils.find_element_by_pic(
            self.get_page_shot("cancel_button.png"), sim=0.8, retry=3)[0]:
            return True
        return False

    @page_method_record("判断垃圾清理扫描是否完成")
    def is_clean_scan_finish(self):
        if not (utils.find_element_by_pic(
                self.get_page_shot("scan_finish_word.png"), sim=0.8, retry=3)[0] or utils.find_element_by_pic(
            self.get_page_shot("clean_up_button.png"), sim=0.8, retry=3)[0]):
            return False
        return True

    @page_method_record("判断一键清理是否完成")
    def is_clean_finish(self):
        if not (utils.find_element_by_pic(
                self.get_page_shot("return_homepage_button.png"), sim=0.8, retry=3)[0] or utils.find_element_by_pic(
            self.get_page_shot("clean_finished_word.png"), sim=0.8, retry=3)[0]):
            return False
        return True

    @page_method_record("判断垃圾清理tab是否存在")
    def is_rubbish_clean_tab_exist(self):
        return utils.find_element_by_pic(
                self.get_page_shot("entry_rubbish_clean.png"), sim=0.8, retry=3)[0]

    @page_method_record("判断回首页按钮是否存在")
    def is_return_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("return_homepage_button.png"), sim=0.8, retry=3)[0]

    @page_method_record("判断深度清理按钮是否存在")
    def is_deep_clean_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("deep_clean_button.png"), sim=0.85, retry=3)[0]

    @page_method_record("点击深度清理按钮")
    def deep_clean_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("deep_clean_button.png"), sim=0.85, retry=3)

    @page_method_record("判断重新扫描按钮是否存在")
    def is_rescan_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("rescan_button.png"), sim=0.8, retry=2)[0]

    @page_method_record("判断暂不处理按钮是否存在")
    def is_refuse_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("refuse_button.png"), sim=0.7, retry=2)[0]

    @page_method_record("等待垃圾清理扫描完成")
    def wait_scan_finish(self):
        while not self.check_scan_status():
            if self.is_deep_clean_button_exist():
                log.log_info("垃圾清理扫描已完成---很干净")
                break
            log.log_info("垃圾清理扫描进行中")
            utils.perform_sleep(2)
        if not self.is_clean_scan_finish():
            return False
        return True

    @page_method_record("等待垃圾清理完成")
    def wait_clean_finish(self):
        while not self.is_clean_finish():
            log.log_info("垃圾清理进行中")
            if self.is_refuse_button_exist():
                self.refuse_button_click()
            utils.perform_sleep(2)
            if self.is_deep_clean_button_exist():
                if not self.deal_deep_clean():
                    log.log_info("处理深度清理场景异常")
                    return False
                self.deep_clean_button_click()
                utils.perform_sleep(1)
        if not self.is_return_button_exist():
            return False
        return True

    @page_method_record("处理深度清理场景")
    def deal_deep_clean(self):
        if not self.select_checkbox_operation():
            log.log_info("未查找到可勾选的checkbox")
            return False
        if not self.is_selected_window_exist():
            log.log_info("未查找到深度清理确认框")
            return False
        if not self.select_checkbox_operation():
            log.log_info("未查找到深度清理确认框中可勾选的checkbox")
            return False
        if not self.sure_button_click():
            log.log_info("点击确认按钮失败")
            return False
        return True

    @page_method_record("判断清理结果页进程占用提示是否存在")
    def is_result_tips_exists(self):
        return utils.find_element_by_pic(
            self.get_page_shot("result_warning_logo.png"), sim=0.7, retry=3)

    @page_method_record("判断清理结果页chrome进程是否存在")
    def is_chrome_logo_exist(self):
        judge_num = 1
        judge_result = False
        while judge_num <= 10:
            result = utils.find_element_by_pic(
            self.get_page_shot("chrome_logo.png"), sim=0.8, retry=2)
            if result[0]:
                judge_result = True
                break
            utils.mouse_scroll(300)
            utils.perform_sleep(1)
            judge_num += 1
        return judge_result

    @page_method_record("点击清理结果页进程占用提示")
    def result_tips_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("result_warning_logo.png"), sim=0.8, retry=3)
