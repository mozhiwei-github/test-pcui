import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from duba.PageObjects.vip_page import vip_page

"""浏览器修复"""


class BrowserHomeProtectPage(BasePage):
    def pre_open(self):
        # 从会员页进入浏览器修复页
        self.vp = vip_page()
        self.vp.browser_mainpage_fix_click()

    @page_method_record("点击登录按钮")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("login_button1.png"),
                                            self.get_page_shot("login_button2.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击开始扫描按钮")
    def click_start_scanning_button(self):
        return utils.click_element_by_pic(self.get_page_shot("start_scanning.png"))

    @page_method_record("点击一键解锁按钮")
    def click_unlock_button(self):
        return utils.click_element_by_pic(self.get_page_shot("unlock_btn.png"))

    def check_sacn(self):
        """
        检查是否扫描结束
        :return:
        """
        for i in range(60):
            utils.perform_sleep(1)
            res = utils.find_element_by_pics([self.get_page_shot("scan_finished.png"),
                                              self.get_page_shot("scan_finished1.png")], retry=3,
                                             sim_no_reduce=True)[0]
            if res:
                log.log_info("扫描结束")
                return True
        log.log_info("扫描一分钟后仍未结束")
        return False



if __name__ == '__main__':
    page = BrowserHomeProtectPage()
    page.click_start_scanning_button()
    time.sleep(1)
