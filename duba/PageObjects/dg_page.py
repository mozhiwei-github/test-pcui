from common.log import log
from common.utils import perform_sleep
from common import utils
from common.basepage import BasePage, page_method_record
from common.tools.duba_tools import find_dgpath_by_reg


class DgPage(BasePage):
    def pre_open(self):
        # TODO：执行打开动作
        dgpath = find_dgpath_by_reg()
        utils.process_start(dgpath, async_start=True)

    @page_method_record("点击设置页")
    def open_setting(self):
        utils.mouse_click(self.position[0] + 845, self.position[1] + 10)
        return utils.click_element_by_pic(self.get_page_shot("button_setting.png"), sim=0.9, retry=3)

    @page_method_record("点击安全设置页")
    def safe_setting(self):
        return utils.click_element_by_pic(self.get_page_shot("safe_setting.png"), sim=0.9, retry=3)

    @page_method_record("关闭自保护")
    def self_protecting_close(self):
        self.open_setting()
        self.safe_setting()
        self_protecting_result, position = utils.find_element_by_pic(
            self.get_page_shot("button_self_protecting_close.png"),
            sim=0.9, sim_no_reduce=True, retry=4,
            location="left_upper_corner")
        if self_protecting_result:
            perform_sleep(1)
            utils.mouse_click(position)
            utils.mouse_move(10, 10)
            self_protecting_result = \
            utils.find_element_by_pic(self.get_page_shot("check_self_protecting_status.png"), sim=0.9, retry=5,
                                      sim_no_reduce=False)[0]
            perform_sleep(3)
            utils.keyboardInputAltF4()
            return self_protecting_result
        return False

    @page_method_record("执行电脑体检")
    def click_to_examination(self):
        result = utils.click_element_by_pic(self.get_page_shot("button_examination.png"))
        if result:
            log.log_pass("点击立即检测成功")
            return True
        else:
            log.log_error("点击立即检测失败")
            return False

    @page_method_record("判断是否在体检中")
    def check_examing(self):
        find, pos = utils.find_element_by_pic(self.get_page_shot("check_examing.png"))
        while find:
            perform_sleep(0.5)
            log.log_info("正在体检中...")
            find1, pos = utils.find_element_by_pic(self.get_page_shot("examination_done.png"), sim=0.9,
                                                   sim_no_reduce=True, retry=3)
            if find1:
                log.log_pass("体检完成")
                break
        return False

    @page_method_record("点击返回按钮")
    def click_back_button(self):
        return utils.click_element_by_pic(self.get_page_shot("button_back.png"), sim=0.9,
                                          sim_no_reduce=True, retry=3)

    @page_method_record("执行垃圾清理")
    def click_to_clean(self):
        result = utils.click_element_by_pic(self.get_page_shot("button_clean.png"))
        if result:
            log.log_pass("点击垃圾清理成功")
            return True
        else:
            log.log_error("点击垃圾清理失败")
            return False

    @page_method_record("判断是否在垃圾扫描中")
    def check_clean_scanning(self):
        find, pos = utils.find_element_by_pic(self.get_page_shot("check_scanning.png"))
        while find:
            perform_sleep(0.5)
            log.log_info("正在扫描中...")
            find1, pos = utils.find_element_by_pic(self.get_page_shot("button_start_clean.png"))
            if find1:
                log.log_pass("垃圾扫描完成")
                break
        return False

    @page_method_record("点击一键清理按钮")
    def click_start_clean_button(self):
        return utils.click_element_by_pic(self.get_page_shot("button_start_clean.png"))

    @page_method_record("检查风险提醒弹窗")
    def check_warning(self):
        perform_sleep(1)
        if utils.find_element_by_pic(self.get_page_shot("warning_logo.png")):
            log.log_info("存在风险提醒弹窗")
            utils.click_element_by_pic(self.get_page_shot("not_clean_now.png"))
        else:
            log.log_info("无风险提醒弹窗")

    @page_method_record("判断是否在垃圾清理中")
    def check_cleaning(self):
        find, pos = utils.find_element_by_pic(self.get_page_shot("check_cleaning.png"))
        while find:
            perform_sleep(0.5)
            log.log_info("正在清理中...")
            find1, pos = utils.find_element_by_pic(self.get_page_shot("clean_done.png"))
            if find1:
                log.log_pass("垃圾清理完成")
                break
        return False

    @page_method_record("关闭垃圾清理功能")
    def click_close_button(self):
        print(utils.find_element_by_pic(self.get_page_shot("clean_exit.png"), sim=0.9,
                                        sim_no_reduce=True, retry=3))
