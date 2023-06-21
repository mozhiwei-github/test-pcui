#!/usr/bin/evn python
# --coding = 'utf-8' --
# 全面扫描页
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.utils import find_element_by_pic
from duba.PageObjects.main_page import main_page
from duba.PageObjects.setting_page import SettingPage
from common.unexpectwin_system import UnExpectWin_System
from duba.utils import while_operation


class overall_scan_page(BasePage):
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
            self.mp = main_page()
            self.mp.overall_scan_click()
        else:
            self.mp = main_page()
            self.mp.overall_scan_click()

    # 判断全面扫描结果状态
    @page_method_record("检测全面扫描状态")
    def check_scan_status(self):
        scan_status = False
        if utils.find_element_by_pic(self.get_page_shot("button_cancel.png"),retry=1,sim=0.9)[0]:
            scan_status = True
        return scan_status

    # 等待全面扫描完成并展示一键修复按钮
    @page_method_record("等待全面扫描完成并展示一键修复按钮")
    def wait_scan_finish(self):
        while self.check_scan_status():
            log.log_info("全面扫描中")
            utils.perform_sleep(2)
        if utils.find_element_by_pic(self.get_page_shot("button_fix.png"), retry=2, sim=0.8):
            log.log_info("匹配到一键修复按钮")
            return True
        log.log_info("未匹配到一键修复按钮")
        return False

    # 点击一键修复
    @page_method_record("点击一键修复")
    def overall_fix_click(self):
        return utils.click_element_by_pic(self.get_page_shot("button_fix.png"), sim=0.8, retry=2)

    # 判断当前修复进度和结果
    @page_method_record("判断当前修复状态和结果")
    def check_fix_result(self):
        fix_result = False
        if utils.find_element_by_pic(self.get_page_shot("fix_success.png"),retry=2)[0]:
            fix_result = True
        return fix_result

    # 等待并判断一键修复完成
    @page_method_record("等待并判断一键修复完成")
    def wait_fix_finish(self):
        while not self.check_fix_result():
            log.log_info("一键修复进行中")
        if utils.find_element_by_pic(self.get_page_shot("button_open.png"), retry=2)[0] or utils.find_element_by_pic(
            self.get_page_shot("ignore_button.png"), retry=3)[0]:
            return True
        elif utils.find_element_by_pic(self.get_page_shot("button_return_homepage.png"), retry=2)[0]:
            return True
        return False

    @page_method_record("判断修复结果是否完全健康")
    def is_fully_recovered(self):
        if utils.find_element_by_pic(self.get_page_shot("fully_recovered.png"), retry=2, sim=0.8)[0]:
            return True
        elif utils.find_element_by_pic(self.get_page_shot("not_fully_recovered.png"), retry=2, sim=0.8)[0]:
            return False

    @page_method_record("判断修复结果页推荐项展示")
    def check_fix_result_recommend(self):
        check_result = False
        if self.is_fully_recovered():
            log.log_info("环境完全健康,不存在推荐项")
            check_result = True
        if utils.find_element_by_pic(self.get_page_shot("homepage_protect_warning.png"), retry=2, sim=0.8)[0]:
            log.log_info("存在主页保护项未开启")
            check_result = True
        if utils.find_element_by_pic(self.get_page_shot("default_software_protect_warning.png"), retry=2, sim=0.8)[0]:
            log.log_info("存在默认软件保护项未开启")
            check_result = True
        return check_result

    # 点击返回按钮返回首页
    @page_method_record("点击返回按钮返回首页")
    def return_homepage(self):
        if not utils.find_element_by_pic(self.get_page_shot("button_return_homepage.png"), retry=2)[0]:
            utils.click_element_by_pic(self.get_page_shot("exit_button.png"),retry=2,sim=0.8)
        else:
            self.return_homepage_click()
        UnExpectWin_System().unexpectwin_detect()

    # 点击回主页按钮返回首页
    @page_method_record("点击回主页按钮返回首页")
    def return_homepage_click(self):
        utils.click_element_by_pic(self.get_page_shot("button_return_homepage.png"), retry=2)
        self.deal_satisfied_vippop()

    # 点击全部忽略按钮
    @page_method_record("点击全部忽略按钮")
    def ignore_button_click(self):
        return utils.click_element_by_pic(self.get_page_shot("ignore_button.png"), retry=2)

    # 判断系统保护是否为未开启
    @page_method_record("判断系统保护是否为未开启")
    def check_protect_status(self):
        protect_status = False
        if find_element_by_pic(self.get_page_shot("scan_protect_status.png"), retry=2, sim=0.95)[0]:
            protect_status = True
        return protect_status

    @page_method_record("判断自保护状态")
    def check_self_protect_status(self):
        self_protect_status = True
        utils.perform_sleep(2)
        # utils.mouse_click(self.position[0] + 690, self.position[1] + 15)
        utils.click_element_by_pic(self.get_page_shot("setting_menu.png"), retry=2, sim=0.85)
        log.log_info("点击更多菜单")
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("setting_center_button.png"), retry=2, sim=0.85)
        log.log_info("点击设置中心")
        utils.perform_sleep(1)
        if utils.find_element_by_pic(self.get_page_shot("settingpage_logo.png"), sim=0.8, retry=2)[0]:
            log.log_info("设置中心页面已打开")
            utils.click_element_by_pic(self.get_page_shot("other_setting_button.png"), retry=2, sim=0.8)
            if not utils.find_element_by_pic(self.get_page_shot("self_protect_on.png"), retry=2, sim=0.9)[0]:
                if utils.find_element_by_pic(self.get_page_shot("self_protect_off.png"), retry=2, sim=0.9)[0]:
                    self_protect_status = False
            return self_protect_status
        else:
            log.log_error("设置中心页面未打开")

    @page_method_record("点击设置页面关闭按钮")
    def setting_page_close_button_click(self):
        return utils.click_element_by_pic(self.get_page_shot("setting_page_close.png"), retry=2, sim=0.8)

    @page_method_record("点击全面扫描按钮")
    def click_overall_button(self):
        return utils.click_element_by_pic(self.get_page_shot("entry_overall_scan.png"), retry=2, sim=0.8)

    @page_method_record("点击取消按钮")
    def click_cancel_button(self):
        return utils.click_element_by_pic(self.get_page_shot("button_cancel.png"), retry=2, sim=0.85)

    @page_method_record("判断退出确认框是否存在")
    def is_exitpop_exist(self):
        return utils.find_element_by_pic(self.get_page_shot("overall_exit_besure.png"), retry=2, sim=0.85)[0]

    @page_method_record("点击确认框中的退出扫描按钮")
    def click_exitoverscan_button(self):
        return utils.click_element_by_pic(self.get_page_shot("exit_overscan_button.png"), retry=2, sim=0.85)

    @page_method_record("判断全面扫描按钮是否存在")
    def is_overscan_button_exist(self):
        return utils.find_element_by_pic(self.get_page_shot("entry_overall_scan.png"), retry=2, sim=0.8)[0]

    @page_method_record("处理碎片清理vip弹窗")
    def deal_suipian_vippop(self):
        if utils.find_element_by_pic(self.get_page_shot("suipian_vippop_logo.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("giveup_clean_button.png"), retry=2, sim=0.85)
        else:
            log.log_info("未发现碎片清理vip弹窗")

    @page_method_record("处理C盘瘦身vip弹窗")
    def deal_c_slim_vippop(self):
        if utils.find_element_by_pic(self.get_page_shot("c_slim_vippop.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("c_slim_pop_refuse_button.png"), retry=2, sim=0.85)
        else:
            log.log_info("未发现c盘瘦身vip弹窗")

    @page_method_record("处理驱动管理王vip弹窗")
    def deal_qudong_vippop(self):
        if utils.find_element_by_pic(self.get_page_shot("qudong_vippop_tab.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("giveup_fix_button.png"), retry=2, sim=0.85)
        else:
            log.log_info("未发现驱动管理王vip弹窗")

    @page_method_record("处理会员满意度调查弹窗")
    def deal_satisfied_vippop(self):
        # 该弹窗是前端弹窗，存在加载时间
        utils.perform_sleep(5)
        if utils.find_element_by_pic(self.get_page_shot("recommend_pop_logo.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("recommend_pop_agree_button.png"), retry=2, sim=0.7)
            utils.perform_sleep(1)
            utils.click_element_by_pic(self.get_page_shot("recommend_pop_submit_button.png"), retry=2, sim=0.7)
            # 该弹窗会自动消失
            utils.perform_sleep(4)

        else:
            log.log_info("未发现会员满意度调查弹窗")

    @page_method_record("判断是否存在电脑医生弹窗")
    def is_computer_doct_vippop_exist(self):
        utils.perform_sleep(2)
        computer_doct_vippop_exist = utils.find_element_by_pic(self.get_page_shot("computer_doct_vippop.png"), retry=2,
                                                               sim=0.8)
        return computer_doct_vippop_exist[0]

    @page_method_record("处理会员电脑医生弹窗")
    def deal_computer_doct_vippop(self):
        if self.is_computer_doct_vippop_exist():
            log.log_info("存在电脑医生弹窗")
            deal_result = utils.click_element_by_pic(self.get_page_shot("computer_doct_vippop_cancel_button.png"), retry=2, sim=0.8)
            if deal_result and not self.is_computer_doct_vippop_exist():
                log.log_pass("电脑医生弹窗已关闭")
            else:
                log.log_error("电脑医生弹窗未正常关闭")
        else:
            log.log_info("不存在电脑医生弹窗")

    @page_method_record("处理所有功能使用后退出界面弹窗")
    def deal_all_vippop(self):
        utils.perform_sleep(3)
        self.deal_c_slim_vippop()
        self.deal_computer_doct_vippop()
        self.deal_suipian_vippop()
        self.deal_satisfied_vippop()
        self.deal_qudong_vippop()

    @page_method_record("判断回首页按钮是否存在")
    def is_return_button_exist(self):
        result = utils.find_element_by_pic(self.get_page_shot("button_return_homepage.png"), retry=2, sim=0.8)[0]
        return result

    @page_method_record("判断修复一键修复按钮是否存在")
    def is_recovery_once_button_exist(self):
        result = utils.find_element_by_pic(self.get_page_shot("button_fix.png"), retry=2, sim=0.8)[0]
        return result







# if __name__ == '__main__':
#     osp = overall_scan_page()
#     while True:
#         status, pos = osp.check_scan_status()
#         if status == "scanning":
#             import time
#
#             time.sleep(5)
#         else:
#             # 尝试点击一键修复
#             osp.one_key_fix_click()
#             time.sleep(5)
#             osp.return_homepage_click()
#             time.sleep(5)
#             break
