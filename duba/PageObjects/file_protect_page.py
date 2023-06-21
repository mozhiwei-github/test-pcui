#!/usr/bin/evn python
# --coding = 'utf-8' --
import time
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from duba.PageObjects.vip_page import vip_page

"""文件夹加密"""


class FileProtectPage(BasePage):
    def pre_open(self):
        # 从会员页进入文件夹加密页
        self.vp = vip_page()
        self.vp.file_encode_click()

    @page_method_record("点击登录按钮")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("login_button1.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("点击添加文件夹按钮")
    def click_add_folder(self):
        return utils.click_element_by_pic(self.get_page_shot("add_folder.png"))

    def check_vip_block(self):
        """
        检查会员卡点
        注意：文件夹加密的会员卡点样式是独立的
        :return:
        """
        self.click_add_folder()
        utils.perform_sleep(1)
        log.log_info("点击""添加文件夹""之后截图", screenshot=True)
        ret = utils.find_element_by_pic(self.get_page_shot("add_folder.png"))[0]
        if not ret:
            return False
        utils.click_element_by_pic(self.get_page_shot("vip_block_cancel_btn.png"))
        return True


if __name__ == '__main__':
    page = FileProtectPage()
    page.vip_center_click()
    time.sleep(2)
