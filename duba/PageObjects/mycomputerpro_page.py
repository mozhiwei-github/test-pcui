import time
from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page

"""我的电脑pro"""


class mycomputerpro_page(BasePage):
    def pre_open(self):
        # 从百宝箱进入
        baibaoxiang_page_o = baibaoxiang_page()
        baibaoxiang_page_o.tools_button_click(baibaoxiang_page_o.get_page_shot("button_mycomputerpro.png"))
        utils.perform_sleep(3)
        # 检查是否有新手指引
        find_tip_iknow, pos_tip_iknow = utils.find_element_by_pic(self.get_page_shot("tip_iknow.png"), retry=3,
                                                                  sim_no_reduce=True)
        if find_tip_iknow:
            log.log_info("点击新手指引")
            for i in range(1, 4, 1):
                utils.mouse_click(pos_tip_iknow)
                utils.perform_sleep(1)

    @page_method_record("打开本地磁盘C")
    def open_patten_c(self):
        utils.click_element_by_pic(self.get_page_shot("left_tab_thiscomputer.png"), retry=3, hwnd=self.hwnd)
        find_c, pos_c = utils.find_element_by_pic(self.get_page_shot("button_bendicipanC.png"), retry=3, hwnd=self.hwnd)
        if find_c:
            utils.mouse_dclick(pos_c[0], pos_c[1])
            utils.perform_sleep(5)
            find_c_tab, pos_c_tab = utils.find_element_by_pic(self.get_page_shot("tab_patten_c.png"), retry=3,
                                                              hwnd=self.hwnd)
            return find_c_tab
        return False

    @page_method_record("返回上一级目录")
    def back_upper_folder(self):
        return utils.click_element_by_pic(self.get_page_shot("button_upper_folder.png"), retry=3, hwnd=self.hwnd)

    @page_method_record("新增tab页")
    def add_tab_page(self):
        if utils.click_element_by_pic(self.get_page_shot("button_tab_add.png"), retry=3, hwnd=self.hwnd):
            return utils.find_element_by_pic(self.get_page_shot("tab_thiscomputer.png"), retry=3, hwnd=self.hwnd)[0]
        return False


if __name__ == '__main__':
    mycomputerpro_page_o = mycomputerpro_page()
    if mycomputerpro_page_o.open_patten_c():
        log.log_info("打开本地磁盘C成功")
    else:
        log.log_info("打开本地磁盘C失败")

    utils.perform_sleep(3)

    if mycomputerpro_page_o.add_tab_page():
        log.log_info("新增tab页成功")
    else:
        log.log_info("新增tab页失败")

    utils.perform_sleep(3)

    if mycomputerpro_page_o.back_upper_folder():
        log.log_info("返回上一级目录成功")
    else:
        log.log_info("返回上一级目录失败")

    utils.perform_sleep(3)
