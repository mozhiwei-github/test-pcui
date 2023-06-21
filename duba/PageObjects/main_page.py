#!/usr/bin/evn python
# --coding = 'utf-8' --
import os
from common import utils
from common.log import log
from common.utils import Location, perform_sleep
from common.basepage import BasePage, page_method_record
from common.tools.duba_tools import find_dubapath_by_reg, get_duba_tryno
from common.file_process import FileOperation


class main_page(BasePage):
    def pre_open(self):
        # TODO：执行打开动作
        dubapath = find_dubapath_by_reg()
        scriptpath = os.getcwd()
        for i in range(1, 3, 1):
            os.chdir(dubapath)
            utils.process_start("kismain.exe", True)
            os.chdir(scriptpath)
            perform_sleep(2)
            find_result, tab_position = self.get_resourse_pic(self.tab_pic, 2, location=Location.LEFT_UP.value)
            if find_result:
                log.log_info("检测到毒霸主界面tab")
                # 读取毒霸TryNo号
                log.log_info("TryNo=" + get_duba_tryno())
                break
        os.chdir(scriptpath)

    # 点击会员中心
    @page_method_record("点击会员中心界面")
    def vip_click(self):
        utils.mouse_click(self.position[0] + 488, self.position[1] + 28)

    # 点击皮肤中心
    # @page_method_record("点击皮肤中心界面")
    # def skin_center_click(self):
    #     utils.mouse_click(self.position[0] + 686, self.position[1] + 13)

    # 点击设置菜单
    @page_method_record("点击设置菜单界面")
    def menu_click(self, button_pos=1):
        """
        param: button_pos 1-设置中心 2-检查更新 3-新版特性 4-日志管理 5-恢复区 6-帮助中心 7-反馈意见 8-服务播报 9-关于
        """
        self.setting_menu_click()
        perform_sleep(1)
        utils.mouse_click(self.position[0] + 706, self.position[1] + 30 + button_pos * 35)

    @page_method_record("点击设置菜单")
    def setting_menu_click(self):
        utils.mouse_click(self.position[0] + 691, self.position[1] + 29)

    @page_method_record("点击设置中心")
    def setting_center_menu_click(self):
        self.setting_menu_click()
        perform_sleep(1)
        return utils.click_element_by_pic(self.get_page_shot("button_setting_center.png"), sim_no_reduce=True)

    @page_method_record("点击检查更新")
    def check_update_menu_click(self):
        self.setting_menu_click()
        perform_sleep(1)
        return utils.click_element_by_pic(self.get_page_shot("check_update_btn.png"), sim_no_reduce=True)

    @page_method_record("点击反馈建议")
    def feedback_click(self):
        self.setting_menu_click()
        perform_sleep(1)
        return utils.click_element_by_pic(self.get_page_shot("feedback_btn.png"), sim_no_reduce=True)

    # 点击最小化
    @page_method_record("点击最小化")
    def minimize_click(self):
        utils.mouse_click(self.position[0] + 731, self.position[1] + 30)

    # 点击全面扫描
    @page_method_record("点击全面扫描")
    def overall_scan_click(self):
        utils.mouse_click(self.position[0] + 525, self.position[1] + 320)

    # 点击弹窗拦截
    @page_method_record("点击弹窗拦截")
    def popup_intercept_click(self):
        utils.mouse_click(self.position[0] + 450, self.position[1] + 485)

    # 点击闪电查杀
    @page_method_record("点击闪电查杀")
    def fast_killing_click(self):
        utils.mouse_click(self.position[0] + 65, self.position[1] + 490)

    # 点击垃圾清理
    @page_method_record("点击垃圾清理")
    def cleaner_click(self):
        utils.mouse_click(self.position[0] + 165, self.position[1] + 485)

    # 点击电脑加速
    @page_method_record("点击电脑加速")
    def computer_accelerate_click(self):
        utils.mouse_click(self.position[0] + 260, self.position[1] + 485)

    # 点击软件管家
    @page_method_record("点击软件管家")
    def software_manager_click(self):
        utils.mouse_click(self.position[0] + 355, self.position[1] + 485)

    # 点击实时保护
    @page_method_record("点击实时保护")
    def realtime_protect_click(self):
        utils.mouse_click(self.position[0] + 180, self.position[1] + 412)

    # 点击电脑医生
    @page_method_record("点击电脑医生")
    def computer_doctor_click(self):
        # utils.click_element_by_pic(self.get_page_shot("computer_doctor.png"), sim=0.9, retry=3)
        utils.mouse_click(self.position[0] + 805, self.position[1] + 610)
    # 点击百宝箱入口
    @page_method_record("点击百宝箱入口")
    def baibaoxiang_click(self):
        utils.mouse_click(self.position[0] + 740, self.position[1] + 480)

    @page_method_record("鼠标hover至百宝箱处")
    def hover_to_baibaoxiang(self):
        utils.mouse_move(self.position[0] + 740, self.position[1] + 480)

    @page_method_record("判断百宝箱快捷框是否存在")
    def is_baibaoxiang_pop_exist(self):
        if not utils.find_element_by_pic(
                self.get_page_shot("baibaoxiang_pop_tab.png"), sim=0.9, retry=3)[0]:
            return False
        return True

    # 判断是否存在指定配置项
    @page_method_record("判断是否存在指定配置项")
    def judge_setted_tools(self):
        if utils.find_element_by_pic(
            self.get_page_shot("computer_doctor_logo.png"), sim=0.6, retry=2)[0] and \
            utils.find_element_by_pic(
            self.get_page_shot("mycomputer_pro_logo.png"), sim=0.6, retry=2)[0] and \
                utils.find_element_by_pic(
            self.get_page_shot("open_menu_pro_logo.png"), sim=0.6, retry=2)[0] and \
                utils.find_element_by_pic(
            self.get_page_shot("rubbish_clean_logo.png"), sim=0.6, retry=2)[0]:
            return True
        else:
            log.log_info("hover 百宝箱后图标识别失败")
            if utils.find_element_by_pic(
            self.get_page_shot("computer_doctor_word.png"), sim=0.6, retry=2)[0] and \
            utils.find_element_by_pic(
            self.get_page_shot("mycomputer_pro_word.png"), sim=0.6, retry=2)[0] and \
                utils.find_element_by_pic(
            self.get_page_shot("open_menu_pro_word.png"), sim=0.6, retry=2)[0] and \
                utils.find_element_by_pic(
            self.get_page_shot("rubbish_clean_word.png"), sim=0.6, retry=2)[0]:
                return True
        log.log_info("hover 百宝箱后图标文案均识别失败")
        return False

    @page_method_record("判断当前主界面版本是否是新版本")
    def is_mainpage_version_new(self, except_version):
        uplive_file_path = os.path.join(find_dubapath_by_reg(), "ressrc", "chs", "uplive.svr")
        uplive_file = FileOperation(uplive_file_path)
        display_version = uplive_file.get_option("Common", "DisplayVersion")
        version = display_version.split(".")[0]
        if version == except_version:
            return True
        return False





if __name__ == '__main__':
    mp = main_page()
    mp.setting_center_menu_click()
