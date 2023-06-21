from common.basepage import BasePage, page_method_record
from duba.PageObjects.main_page import main_page
from common import utils

class DeviceInfoPage(BasePage):
    def pre_open(self):
        self.mp = main_page()
        self.mp.computer_doctor_click()

    @page_method_record("关闭电脑状态界面-点击关闭按钮")
    def click_close_button(self):
        return utils.click_element_by_pic(self.get_page_shot("device_info_close_button.png"), sim=0.85, retry=3)


    @page_method_record("判断是否存在满意度调查框")
    def is_satisfction_exist(self):
        # 规避前端加载时间
        utils.perform_sleep(5)
        return utils.find_element_by_pic(self.get_page_shot("satisfction_tab.png"), sim=0.8, retry=3)[0]

    @page_method_record("关闭满意度调查窗口")
    def close_satisfction_page(self):
        utils.click_element_by_pic(self.get_page_shot("satisfction_sure_button.png"), sim=0.8, retry=3)
        utils.perform_sleep(1)
        utils.click_element_by_pic(self.get_page_shot("satisfction_submit_button.png"), sim=0.8, retry=3)
        # 前端界面存在点击后动画时长
        utils.perform_sleep(5)
        if not self.is_satisfction_exist():
            return True
        return False