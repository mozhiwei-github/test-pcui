#!/usr/bin/evn python
# --coding = 'utf-8' --
from common.log import log
from duba.PageObjects.main_page import main_page
from common import utils
from common.basepage import BasePage, page_method_record
from duba.PageObjects.setting_page import SettingPage


class baibaoxiang_page(BasePage):
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
            self.mp.baibaoxiang_click()
        else:
            self.mp = main_page()
            self.mp.baibaoxiang_click()

    # 点击会员特权
    @page_method_record("点击会员特权")
    def huiyuantequan_click(self):
        return utils.click_element_by_pic(self.get_page_shot("button_huiyuantequan.png"), retry=3)

    @page_method_record("点击精选工具按钮")
    def special_tools_button_click(self):
        return utils.click_element_by_pic(self.get_page_shot("special_tools_button.png"), retry=3)

    # 点击打开文件粉碎
    @page_method_record("点击打开文件粉碎")
    def filedestroy_click(self):
        self.huiyuantequan_click()
        utils.mouse_move(self.position[0] + 400, self.position[1] + 300)
        while not utils.click_element_by_pic(self.get_page_shot("file_destroy_logo.png"), sim=0.85, retry=1):
            log.log_info("滚动页面以寻找指定图标")
            utils.mouse_scroll(200)
            utils.perform_sleep(2)
            result = utils.find_element_by_pic(self.get_page_shot("computer_safe_selected.png"), retry=3)[0]
            if result:
                log.log_info("未查找到文件粉碎功能tab")
                break
    # 点击实用工具
    @page_method_record("点击实用工具")
    def shiyongtool_click(self):
        return utils.click_element_by_pic(self.get_page_shot("button_shiyongtool.png"), retry=3)

    # 点击C盘瘦身
    @page_method_record("点击C盘瘦身tab")
    def c_slimming_click(self):
        return utils.click_element_by_pic(self.get_page_shot("c_slimming_logo.png"), retry=3)

    # 点击其它产品
    @page_method_record("点击其它产品")
    def otherproduct_click(self):
        return utils.click_element_by_pic(self.get_page_shot("button_otherproduct.png"), retry=3)

    # 打开工具
    @page_method_record("打开工具")
    def tools_button_click(self, tool_button, sim=0.8, retry=3):
        return utils.click_element_by_pic(tool_button, sim=sim, retry=retry)

    # 点击打开主界面快捷入口设置tab
    @page_method_record("点击打开主界面快捷入口设置tab")
    def tools_tab_click(self):
        return utils.click_element_by_pic(self.get_page_shot("tools_tab.png"), retry=3)

    @page_method_record("点击打开常用工具编辑按钮")
    def tools_update_button_click(self):
        return utils.click_element_by_pic(self.get_page_shot("tools_update_button.png"), retry=3)

    # 删除快捷入口中的所有已配置项
    @page_method_record("删除快捷入口中的所有已配置项")
    def delete_setted_tools(self):
        deleted_num = 0
        while utils.click_element_by_pic(self.get_page_shot("tools_delete_button.png"), sim=0.85, retry=2):
            deleted_num += 1
            log.log_info(f"删除第 {deleted_num} 个已配置项")
            if deleted_num >= 7:
                break
            utils.perform_sleep(1)

    @page_method_record("判断是否存在空工具编辑框")
    def is_tools_null_exist(self):
        return utils.find_element_by_pic(self.get_page_shot("actually_tools_null.png"), retry=3)[0]

    # 增加固定四个快捷入口配置项
    @page_method_record("增加固定四个快捷入口配置项")
    def set_tools(self):
        self.huiyuantequan_click()
        result = utils.find_elements_by_pic(self.get_page_shot("add_tools_button.png"), retry=3)
        if not result[0]:
            return False
        for i in range(7):
            utils.mouse_click(result[1][i])
        utils.perform_sleep(1)
        self.special_tools_button_click()
        utils.mouse_move(self.position[0]+400, self.position[1]+300)
        utils.perform_sleep(2)
        while not self.is_tools_finish_button_exist():
            utils.mouse_scroll(-250)
            log.log_info("滚动页面返回至百宝箱界面顶部")
        if not self.tools_finish_button_click():
            return False
        return True

    @page_method_record("判断常用工具栏tab是否存在")
    def is_actually_tools_tab_exist(self):
        return utils.find_element_by_pic(self.get_page_shot("actually_tools_tab.png"), retry=3)[0]

    # 点击快捷入口配置完成按钮
    @page_method_record("点击快捷入口配置完成按钮")
    def tools_finish_button_click(self):
        return utils.click_element_by_pic(
            self.get_page_shot("tools_finish_button.png"), sim=0.85, retry=3)

    # 判断点击快捷入口配置完成按钮是否存在
    @page_method_record("判断快捷入口配置完成按钮是否存在")
    def is_tools_finish_button_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("tools_finish_button.png"), sim=0.85, retry=3)[0]

    # 从百宝箱返回首页
    @page_method_record("从百宝箱返回首页")
    def return_homepage(self):
        utils.click_element_by_pic(
            self.get_page_shot("exit_baibaoxiang_new.png"), sim=0.85, retry=3)
        utils.perform_sleep(2)
        return utils.find_element_by_pic(
            self.get_page_shot("entry_baibaoxiang_new.png"), sim=0.85, retry=3)[0]



if __name__ == '__main__':
    import time

    bp = baibaoxiang_page()
    # bp.page_open()
    bp.huiyuantequan_click()
    x, y = utils.get_mouse_point()
    utils.mouse_move(x + 200, y)
    time.sleep(5)
    utils.mouse_scroll(300)
    time.sleep(2)
    utils.mouse_scroll(300)
    time.sleep(10)
