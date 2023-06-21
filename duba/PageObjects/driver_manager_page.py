import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from duba.PageObjects.vip_page import vip_page

"""驱动管理王"""


class DriverManagerPage(BasePage):
    def pre_open(self):
        # 从会员页进入驱动管理王页
        self.vp = vip_page()
        self.vp.drive_download_click()

    @page_method_record("点击备份/还原按钮")
    def click_backup_revert_button(self):
        return utils.click_element_by_pic(self.get_page_shot("backup_revert_button.png"), sim=0.8, sim_no_reduce=True)

    @page_method_record("点击会员中心按钮")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("vip_center.png"), self.get_page_shot("vip_center2.png")]
                                           , retry=3,
                                           sim_no_reduce=True)

    @page_method_record("检查是否扫描驱动结束")
    def check_finish_scan_driver(self):
        res = utils.find_element_by_pic(self.get_page_shot("finish_scan_tab.png"))[0]
        if res:
            log.log_info("自动扫描结束，且有驱动需要安装")
            return res
        res = utils.find_element_by_pic(self.get_page_shot("finish_scan_tab2.png"))[0]
        if res:
            log.log_info("自动扫描结束，无驱动需要安装")
            return res

    @page_method_record("关闭异常提示框")
    def close_exception_prompt_box(self):
        utils.click_element_by_pic(self.get_page_shot("remind_tab.png"))
        utils.keyboardInputAltF4()

    @page_method_record("点击扫描键")
    def click_scan_btn(self):
        utils.click_element_by_pic(self.get_page_shot("scan_btn.png"), retry=4, sim_no_reduce=True)

    @page_method_record("检查是否正在扫描")
    def check_scan_driver(self, close_box=True):
        for i in range(40):
            res = utils.find_element_by_pic(self.get_page_shot("checking_driver_tab.png"), retry=1)[0]
            if not res:
                self.check_finish_scan_driver()
                if close_box:
                    self.close_exception_prompt_box()
                return True
            utils.perform_sleep(1)
        log.log_info("扫描超时, 扫描超过40s")
        return False

    @page_method_record("点击界面一键修复")
    def click_fix_btn(self):
        utils.click_element_by_pic(self.get_page_shot("fix_btn.png"), retry=4)

    @page_method_record("点击提示中的一键修复")
    def click_remind_fix_btn(self):
        utils.click_element_by_pic(self.get_page_shot("remind_fix_btn.png"), retry=4)


if __name__ == '__main__':
    page = DriverManagerPage()
    page.click_scan_btn()
    page.check_scan_driver()
    # page.click_backup_revert_button()
    page.click_vip_center_button()
    # time.sleep(2)
