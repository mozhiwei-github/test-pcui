import time

from common.unexpectwin_system import UnExpectWin_System
from common.utils import find_element_by_pic,click_element_by_pic,perform_sleep
from common import basepage
import os
from common.log import log
from duba.PageObjects.main_page import main_page
from common.basepage import BasePage,page_method_record
from common import utils
from duba.contants import Accelerate_module


def defend_pop_operation():
    tab_path = os.path.join(os.getcwd(), 'duba', 'PageShot', 'computer_accelerate_page','system_defend_pop_tab.png')
    more_operation_path = os.path.join(os.getcwd(), 'duba', 'PageShot', 'computer_accelerate_page','more_operation.png')
    pass_operation_path = os.path.join(os.getcwd(), 'duba', 'PageShot', 'computer_accelerate_page','pass_operation.png')
    perform_sleep(2)
    if find_element_by_pic(tab_path, sim=0.85, retry=2)[0]:
        log.log_info("查询到防御泡泡")
        log.log_info("点击更多操作按钮")
        click_element_by_pic(more_operation_path, sim=0.85, retry=2)
        time.sleep(1)
        log.log_info("点击允许操作按钮")
        click_element_by_pic(pass_operation_path, sim=0.85, retry=2)
    else:
        log.log_info("未识别到防御泡泡")

def get_enum_map(module_name):
    for i in range(len(Accelerate_module.module_dict.value)):
        if Accelerate_module.module_dict.value[i][0] == module_name:
            return i

    #find_element_by_pic(r"C:\project\dubatestpro\duba\PageShot\computer_accelerate_page\system_defend_pop_tab.png")

class ComputerAcceleratePage(BasePage):
    def pre_open(self):
        # 执行打开动作--打开电脑加速界面
        self.mp = main_page()
        self.mp.computer_accelerate_click()

    @page_method_record("检测电脑加速扫描状态")
    def check_accelerate_scan_status(self):
        accelerate_finished = False
        if utils.find_element_by_pic(self.get_page_shot("accelerate_button.png"), retry=1, sim=0.9)[0]:
            accelerate_finished = True
        return accelerate_finished

    @page_method_record("判断电脑加速是否完成")
    def is_accelerate_finished(self):
        if utils.find_element_by_pic(self.get_page_shot("accelerate_finished.png"), retry=2, sim=0.85)[0] and utils.find_element_by_pic(self.get_page_shot("return_mainpage_button.png"))[0]:
            return True
        return False

    @page_method_record("判断电脑加速扫描是否完成")
    def is_accelerate_scan_finished(self):
        if utils.find_element_by_pic(
                self.get_page_shot("accelerate_button.png"), retry=2, sim=0.85)[0]:
            return True
        return False

    @page_method_record("判断回首页按钮是否存在")
    def is_return_button_exist(self):
        if utils.find_element_by_pic(
                self.get_page_shot("return_mainpage_button.png"), retry=2, sim=0.85)[0]:
            return True
        return False

    @page_method_record("等待电脑加速完成")
    def wait_accelerate_finish(self):
        while not self.is_accelerate_finished():
            log.log_info("电脑加速进行中")
        if not self.is_return_button_exist():
            return False
        return True

    @page_method_record("等待电脑加速扫描完成")
    def wait_accelerate_scan_finish(self):
        while not self.check_accelerate_scan_status():
            log.log_info("电脑加速扫描进行中")
            utils.perform_sleep(2)
        if not self.is_accelerate_scan_finished():
            return False
        return True

    @page_method_record("判断电脑加速tab是否存在")
    def is_accelerate_tab_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("entry_computer_accelerate.png"), retry=2, sim=0.85)[0]

    @page_method_record("点击回首页按钮返回首页")
    def click_return_mainpage_button(self, reclick=False):
        utils.click_element_by_pic(self.get_page_shot("return_mainpage_button.png"), retry=2, sim=0.8)
        if utils.find_element_by_pic(self.get_page_shot("return_vip_pop.png"), sim=0.85)[0]:
            log.log_info("识别到会员泡泡")
            utils.click_element_by_pic(self.get_page_shot("giveup_clean_button.png"), sim=0.85, retry=3)
        if reclick:
            utils.perform_sleep(3)
            self.deal_satisfied_vippop()
            self.deal_secondary_sure_window()
            UnExpectWin_System().unexpectwin_detect()

    @page_method_record("点击一键加速按钮")
    def click_accelerate_button(self):
        utils.click_element_by_pic(self.get_page_shot("accelerate_button.png"),retry=2,sim=0.85)

    @page_method_record("判断指定tab列表中是否存在指定项")
    def is_module_exists(self,module_name):
        bcTester_exist_result = ()
        if not utils.find_element_by_pic(self.get_page_shot(Accelerate_module.module_dict.value[get_enum_map(module_name)][1]),retry=2,sim=0.85)[0]:
            self.list_scroll(module_name=module_name)
        log.log_info("当前处于指定列表中")
        result = utils.find_element_by_pic(self.get_page_shot(Accelerate_module.module_dict.value[get_enum_map(module_name)][1]), retry=2, sim=0.85)
        utils.mouse_move(result[1][0],result[1][1])
        exists_result = False
        if self.is_list_end(module_name=module_name):
            bcTester_exist_result = utils.find_element_by_pic(self.get_page_shot("bcTester.png"), retry=1, sim=0.85)
            if bcTester_exist_result[0]:
                exists_result = True
        else:
            while not (exists_result or self.is_list_end(module_name=module_name)):
                bcTester_exist_result = utils.find_element_by_pic(self.get_page_shot("bcTester.png"), retry=1, sim=0.85)
                if bcTester_exist_result[0]:
                    exists_result = True
                    break
                utils.mouse_scroll(200)
        return exists_result, bcTester_exist_result[1]

    @page_method_record("点击扫描结果中的bcTester勾选框")
    def click_bcTester_select(self, element_pic):
        utils.mouse_click(element_pic[0]+22, element_pic[1]+16)
        utils.perform_sleep(1)

    @page_method_record("控制列表中的滚动")
    def list_scroll(self, module_name):
        found_module_num = 0
        button_pos = utils.find_element_by_pic(self.get_page_shot("accelerate_button.png"), retry=2, sim=0.85)[1]
        while found_module_num < 4:
            if utils.find_element_by_pic(self.get_page_shot(Accelerate_module.module_dict.value[get_enum_map(module_name)][1]))[0]:
                log.log_info("已定位至目标列表处")
                found_module_num += 1
                break
            else:
                utils.mouse_move(button_pos[0], button_pos[1]+200)
                utils.mouse_scroll(100)

    @page_method_record("判断滚动后列表是否到达某tab底部")
    def is_list_end(self, module_name):
        should_stop = False
        list_len = len(Accelerate_module.module_dict.value)
        module_num = get_enum_map(module_name)
        for i in range(module_num,list_len):
            if i == (list_len-1):
                pass
            elif utils.find_element_by_pic(self.get_page_shot(Accelerate_module.module_dict.value[i+1][1]), retry=1, sim=0.85)[0]:
                should_stop = True
        return should_stop

    @page_method_record("点击深度加速确认框使其隐藏")
    def deal_secondary_sure_window(self):
        if utils.find_element_by_pic(self.get_page_shot("vip_pop_logo.png"), retry=5, sim=0.8)[0]:
            log.log_info("识别到深度加速确认泡")
            utils.click_element_by_pic(self.get_page_shot("giveup_release.png"), retry=2, sim=0.8)
        else:
            log.log_info("未识别到深度加速确认框")

    @page_method_record("点击电脑加速返回首页-电脑医生泡泡使其隐藏")
    def deal_doctor_pop(self):
        if utils.find_element_by_pic(self.get_page_shot("doctor_pop_logo.png"), retry=5, sim=0.85)[0]:
            log.log_info("识别到电脑医生泡泡")
            utils.click_element_by_pic(self.get_page_shot("doctor_pop_giveup_button.png"), retry=2, sim=0.8)
        else:
            log.log_info("未识别到电脑医生泡泡")

    @page_method_record("处理c盘瘦身弹窗")
    def deal_c_slim_vippop(self):
        if utils.find_element_by_pic(self.get_page_shot("c_slim_vippop.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("c_slim_pop_refuse_button.png"), retry=2, sim=0.85)
        else:
            log.log_info("未发现c盘瘦身vip弹窗")

    @page_method_record("处理碎片清理vip弹窗")
    def deal_suipian_vippop(self):
        if utils.find_element_by_pic(self.get_page_shot("suipian_vippop_logo.png"), sim=0.8, retry=3)[0]:
            utils.click_element_by_pic(self.get_page_shot("giveup_clean_button.png"), retry=2, sim=0.85)
        else:
            log.log_info("未发现碎片清理vip弹窗")

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

    @page_method_record("处理所有vippop")
    def deal_all_vippop(self):
        utils.perform_sleep(3)
        self.deal_c_slim_vippop()
        self.deal_suipian_vippop()
        self.deal_qudong_vippop()
        self.deal_satisfied_vippop()
        self.deal_doctor_pop()













