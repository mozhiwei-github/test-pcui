# --coding = 'utf-8' --
import os
from common import utils
from common.log import log
from common.utils import perform_sleep, Location
from common.basepage import page_method_record
from common.tools.duli_tools import find_duli_c_slimming_by_reg
from duba.PageObjects.c_slimming_page import CSlimmingPage
from duba.PageObjects.defrag_page import DefragPage
from duba.PageObjects.file_shredding_page import FileShreddingPage
from duba.PageObjects.login_page import LoginPage
from duba.PageObjects.popup_intercept_page import PopupInterceptPage

"""c盘清理大师（c盘瘦身独立版）"""

duba_reg = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus"
dg_reg = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"


def set_duba_reg(value):
    utils.set_reg_value(regpath=duba_reg, keyname="ProgramPath", value=value)


def set_dg_reg(value):
    utils.set_reg_value(regpath=dg_reg, keyname="AppPath", value=value)


def get_path():
    product_path = find_duli_c_slimming_by_reg()
    return product_path


class CleanMasterPage(CSlimmingPage):
    def pre_open(self):
        # TODO：执行打开动作
        product_path = find_duli_c_slimming_by_reg()
        scriptpath = os.getcwd()
        for i in range(1, 3, 1):
            os.chdir(product_path)
            utils.process_start(self.process_name, True)
            os.chdir(scriptpath)
            perform_sleep(2)
            find_result, tab_position = self.get_resourse_pic(self.tab_pic, 10, sim_no_reduce=False,
                                                              location=Location.LEFT_UP.value)
            if find_result:
                log.log_info("检测到C盘独立瘦身主界面tab")
                # 读取C盘瘦身TryNo号
                with open(os.path.join(product_path, "ressrc", "chs", "uplive.svr"), "r") as fr:
                    while True:
                        row_data = fr.readline()
                        if row_data.find("TryNo") >= 0:
                            log.log_info(row_data)
                            break
                        if not row_data:
                            break
                break
        os.chdir(scriptpath)

    def page_confirm_close(self):
        self.check_close_tip_windows()

    def check_close_tip_windows(self):
        find_r, _ = utils.find_element_by_pic(self.get_page_shot("tip_trush_clean.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭垃圾清理提示框")
            utils.click_element_by_pic(self.get_page_shot("button_giveup_trush.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("tip_speed.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭电脑加速提示框")
            utils.click_element_by_pic(self.get_page_shot("button_giveup_speed.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("tip_c_slimming.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭C盘瘦身提示框")
            utils.click_element_by_pic(self.get_page_shot("button_cancel.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("tip_privacy.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭隐私清理提示框")
            utils.click_element_by_pic(self.get_page_shot("button_privacy_tip_cancle.png"))

    def check_close_pop(self):
        """垃圾清理，电脑加速，使用功能后退弹泡"""
        find_r, _ = utils.find_element_by_pic(self.get_page_shot("defrag_pop.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭碎片清理推广泡")
            utils.click_element_by_pic(self.get_page_shot("pop_exit.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("privacy_pop.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭隐私清理推广")
            utils.click_element_by_pic(self.get_page_shot("pop_exit.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("sysslim_pop.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭C盘瘦身推广泡")
            utils.click_element_by_pic(self.get_page_shot("pop_exit.png"))

        find_r, _ = utils.find_element_by_pic(self.get_page_shot("filedestroy_pop.png"), retry=2, sim_no_reduce=True,
                                              hwnd=self.hwnd)
        if find_r:
            log.log_info("关闭文件粉碎推广泡")
            utils.click_element_by_pic(self.get_page_shot("pop_exit.png"))

    @page_method_record("点击C盘瘦身tab")
    def tab_click_c_slimming(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 103)
        if not utils.find_element_by_pic(self.get_page_shot("tab_c_slimming.png"), sim_no_reduce=True)[0]:
            log.log_error("点击C盘瘦身tab失败")
            return False
        else:
            return True

    @page_method_record("点击垃圾清理tab")
    def tab_click_trash_clean(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 163)
        if not utils.find_element_by_pic(self.get_page_shot("tab_laji_qingli.png"), sim_no_reduce=True)[0]:
            log.log_error("点击垃圾清理tab失败")
            return False
        else:
            return True

    @page_method_record("点击电脑加速tab")
    def tab_click_diannao_jiasu(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 223)
        if not utils.find_element_by_pic(self.get_page_shot("tab_diannao_jiasu.png"), sim_no_reduce=True)[0]:
            log.log_error("点击电脑加速tab失败")
            return False
        else:
            return True

    @page_method_record("点击隐私清理tab")
    def tab_click_privacy_clean(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 293)
        if not utils.find_element_by_pic(self.get_page_shot("tab_privacy_clean_finish_scan.png"), sim_no_reduce=True)[
            0]:
            log.log_error("点击隐私清理tab失败")
            return False
        else:
            return True

    @page_method_record("点击碎片清理王tab")
    def tab_click_defrag(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 343)
        DefragPage_o = DefragPage(do_pre_open=False)
        perform_sleep(3)
        result = utils.compare_cmdline("kdefrag.exe", "Clean Master")
        if result:
            log.log_info("确认从清理大师打开碎片清理")
            if DefragPage_o.page_close():
                return True
            else:
                return False
        else:
            log.log_error("打开的不是清理大师的碎片清理")
            return False

    @page_method_record("利用命令行弹出预扫泡")
    def scan_pop(self, exe_name, param):
        product_path = find_duli_c_slimming_by_reg()
        exe_demo_file = os.path.join(product_path, exe_name)
        a = utils.process_start(process_path=exe_demo_file, param=param, async_start=True, )
        print(a)

    @page_method_record("碎片清理预扫泡检查")
    def check_defage_scan_pop(self):
        if not utils.find_element_by_pic(self.get_page_shot("defage_scan_pop_title.png"), sim_no_reduce=True)[0]:
            log.log_error("碎片清理预扫泡没调起")
            return False
        else:
            log.log_info("碎片清理预扫泡已调起")
        utils.click_element_by_pic(self.get_page_shot("defage_scan_pop_clean_button.png"))
        log.log_info("点击预扫泡中的立即清理碎片按钮")
        DefragPage_o = DefragPage(do_pre_open=False)
        perform_sleep(3)
        result = utils.compare_cmdline("kdefrag.exe", "Clean Master")
        if result:
            log.log_info("确认从清理大师打开碎片清理")
            if DefragPage_o.page_close():
                return True
            else:
                return False
        else:
            log.log_error("打开的不是清理大师的碎片清理")
            return False

    @page_method_record("点击弹窗拦截tab")
    def tab_click_pop_intercept(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 405)
        PopupInterceptPage_o = PopupInterceptPage(do_pre_open=False, delay_sec=3)
        perform_sleep(3)
        result = utils.compare_cmdline("ksoftpurifier.exe", "Clean Master")
        if result:
            log.log_info("确认从清理大师打开弹窗拦截")
            if PopupInterceptPage_o.page_close():
                return True
            else:
                return False
        else:
            log.log_error("打开的不是清理大师的弹窗拦截")
            return False

    @page_method_record("点击文件粉碎tab")
    def tab_click_file_destroy(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 467)
        FileShreddingPage_o = FileShreddingPage(do_pre_open=False, delay_sec=3)
        perform_sleep(3)
        result1 = utils.compare_cmdline("kfiledestroy64.exe", "Clean Master")
        result2 = utils.compare_cmdline("kfiledestroy.exe", "Clean Master")
        if result1 or result2:
            log.log_info("确认从清理大师打开文件粉碎")
            if FileShreddingPage_o.page_close():
                return True
            else:
                return False
        else:
            log.log_error("打开的不是清理大师的弹窗拦截")
            return False

    @page_method_record("点击软件卸载tab")
    def tab_click_software_manage(self):
        utils.mouse_click(self.position[0] + 83, self.position[1] + 529)
        perform_sleep(3)
        result = utils.compare_cmdline("assoftmgr.exe", "Clean Master")
        if result:
            log.log_info("确认从清理大师打开软件卸载（管理）")
        else:
            log.log_error("打开的不是清理大师的软件卸载（管理）")
            return False
        utils.click_element_by_pic(self.get_page_shot("software_manage_close.png"))

    @page_method_record("点击登录按钮")
    def click_login_entry(self):
        if utils.click_element_by_pic(self.get_page_shot("button_login_entry.png"), retry=2, sim_no_reduce=True):
            duba_login_page_o = LoginPage(do_pre_open=False)
            duba_login_page_o.qq_user_login()
            return True
        else:
            return False

    @page_method_record("检查加速中或者扫描中")
    def check_scanning_or_cleaning(self, state_log_info, waiting_pic, end_log_info):
        for i in range(0, 100, 1):
            perform_sleep(1)
            log.log_info(state_log_info)
            # 检查取消按钮还在则意味还在扫描则进行等待
            if not utils.find_element_by_pic(
                    self.get_page_shot(waiting_pic),
                    retry=1, sim_no_reduce=True, hwnd=self.hwnd)[0]:
                log.log_info(end_log_info)
                break

    @page_method_record("检查垃圾清理tab")
    def check_clean_trash_tab(self):
        self.tab_click_trash_clean()
        perform_sleep(1)
        ret = False
        # 点击快速扫描
        if utils.click_element_by_pic(self.get_page_shot("button_kuaisu_saomiao.png")):
            log.log_info("点击快速扫描成功")

        self.check_scanning_or_cleaning("垃圾扫描中", "button_trush_clean_cancel.png", "扫描完成")

        # 点击清理按钮
        if utils.click_element_by_pic(self.get_page_shot("button_qingli.png"), retry=10,
                                      sim_no_reduce=True):
            log.log_info("点击清理")
            # 检查是否弹出风险提示窗
            log.log_info("检查是否有风险提示窗")
            if utils.find_element_by_pic(self.get_page_shot("tip_fengxian.png"), retry=10,
                                         sim_no_reduce=True, hwnd=self.hwnd)[0]:
                log.log_info("检查有风险提示窗")
                # 关闭风险提示窗
                utils.click_element_by_pic(self.get_page_shot("tip_fengxian_close.png"),
                                           retry=3, sim_no_reduce=True, hwnd=self.hwnd)
                log.log_info("关闭风险提示窗")

        self.check_scanning_or_cleaning("垃圾清理中", "tip_cleannig.png", "清理完成")

        # 检查是否有弹出更多提示窗
        self.check_close_tip_windows()

        # 点击完成按钮
        if utils.click_element_by_pics([self.get_page_shot("button_finish.png"),
                                        self.get_page_shot("button_finish_2.png"),
                                        self.get_page_shot("button_finish_3.png")],
                                       retry=10, sim_no_reduce=True):
            self.check_close_pop()
            log.log_info("点击完成")
            ret = True
        if ret:
            log.log_pass("垃圾清理tab检查成功")
        else:
            log.log_error("垃圾清理tab检查失败")

    @page_method_record("检查电脑加速tab")
    def check_accelerate_tab(self):
        self.tab_click_diannao_jiasu()
        ret = 0
        # 点击快速扫描
        if utils.click_element_by_pic(self.get_page_shot("button_kuaisu_saomiao.png")):
            log.log_info("点击快速扫描成功")

        self.check_scanning_or_cleaning("垃圾扫描中", "tip_scanning.png", "扫描完成")

        # 点击加速按钮
        if utils.click_element_by_pic(self.get_page_shot("button_one_key_jiasu.png")):
            log.log_info("点击一键加速成功")
            ret = 1

        self.check_scanning_or_cleaning("电脑加速中", "tip_accelerating.png", "加速扫描完成")

        if ret > 0:
            # 检查是否有弹出更多提示窗
            self.check_close_tip_windows()

            if utils.click_element_by_pics([self.get_page_shot("button_finish.png"),
                                            self.get_page_shot("button_finish_2.png"),
                                            self.get_page_shot("button_finish_3.png")],
                                           retry=10, sim_no_reduce=True):
                self.check_close_pop()
                log.log_info("加速完成")
                ret = 2
            log.log_pass("电脑加速tab检查成功")
        else:
            log.log_error("电脑加速tab检查失败")

    @page_method_record("检查隐私清理tab")
    def check_privacy_clean_tab(self):
        ret = self.tab_click_privacy_clean()
        if ret:
            log.log_info("点击隐私清理tab成功")
            log.log_pass("隐私清理tab检查成功")
        # 点击快速扫描
        # if utils.click_element_by_pic(self.get_page_shot("button_privacy_scan.png")):
        #     log.log_info("点击扫描成功")
        #     log.log_pass("隐私清理tab检查成功")
        #     if utils.click_element_by_pic(duli_c_slimming_page_o.get_page_shot("button_privacy_clean.png")):
        #         log.log_info("点击立即清理成功")
        #         ret = 1
        #
        #         for i in range(0, 10, 1):
        #             perform_sleep(10)
        #             log.log_info("隐私清理中")
        #             # 检查加速标志还在则意味还在加速则进行等待
        #             if not utils.find_element_by_pic(
        #                     duli_c_slimming_page_o.get_page_shot("tip_privacy_cleaning.png"),
        #                     retry=1, sim_no_reduce=True, hwnd=duli_c_slimming_page_o.hwnd)[0]:
        #                 log.log_info("加速扫描完成")
        #                 break
        #
        #         # 检查是否有弹出更多提示窗
        #         duli_c_slimming_page_o.check_close_tip_windows()
        #         if utils.click_element_by_pics([duli_c_slimming_page_o.get_page_shot("button_finish.png"),
        #                                         duli_c_slimming_page_o.get_page_shot("button_finish_2.png"),
        #                                         duli_c_slimming_page_o.get_page_shot("button_finish_3.png")],
        #                                        retry=10, sim_no_reduce=True):
        #             log.log_info("加速完成")
        #             ret = 2
        # if ret > 0:
        #     log.log_pass("隐私清理tab检查成功")
        # else:
        #     log.log_error("隐私清理tab检查失败")


if __name__ == '__main__':
    ...
