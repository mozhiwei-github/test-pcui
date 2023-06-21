import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from duba.PageObjects.vip_page import vip_page
from duba.utils import check_vip_block

"""隐私无痕模式"""


class PrivacyNoTracePage(BasePage):
    def pre_open(self):
        # 从会员页进入隐私无痕模式页
        self.vp = vip_page()
        self.vp.privacy_notrace_click()

    @page_method_record("打开会员中心")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("login_button1.png"),
                                            self.get_page_shot("login_button2.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击一键开启")
    def click_all_open(self):
        return utils.click_element_by_pic(self.get_page_shot("all_open_btn.png"))

    @page_method_record("点击一键关闭")
    def click_all_close(self):
        return utils.click_element_by_pic(self.get_page_shot("all_close_btn.png"))

    @page_method_record("检查功能开关是否都开启")
    def check_all_open(self):
        ret1 = utils.find_element_by_pic(self.get_page_shot("all_open_tab1.png"), retry=3,
                                         sim_no_reduce=True)[0]
        ret2 = utils.find_element_by_pic(self.get_page_shot("all_open_tab2.png"), retry=3,
                                         sim_no_reduce=True)[0]

        if ret1 and ret2:
            log.log_info("所有功能已开启")
            return True
        return False

    @page_method_record("检查功能开关是否都关闭")
    def check_all_close(self):
        ret1 = utils.find_element_by_pic(self.get_page_shot("all_close_tab.png"), retry=3,
                                         sim_no_reduce=True)[0]
        if ret1:
            log.log_info("所有功能已关闭")
            return True
        return False


if __name__ == '__main__':
    page = PrivacyNoTracePage()
    page.click_all_open()
    page.check_all_open()
    page.click_all_close()
    page.check_all_close()
    time.sleep(1)
