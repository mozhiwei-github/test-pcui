from common.basepage import BasePage, page_method_record
from common import utils
import os
from office.contants import knstorePath
from office.utils import while_operation

class KnstoreUninstallPage(BasePage):
    def pre_open(self):
        utils.process_start(
            process_path=os.path.join(knstorePath.DEFAULTINSTALLPATH.value, "uninstall.exe"), async_start=True)

    @page_method_record("判断卸载界面是否存在")
    def is_uninstall_page_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("uninstall_page_logo.png"), sim=0.8, retry=3)[0]

    @page_method_record("点击卸载界面卸载按钮")
    def uninstall_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_page_uninstall_button.png"), sim=0.8, retry=3)

    @page_method_record("点击卸载界面取消按钮")
    def cancel_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_page_cancel_button.png"), sim=0.8, retry=3)

    @page_method_record("点击卸载界面再见按钮")
    def uninstall_finish_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_page_uninstall_finish_button.png"), sim=0.8, retry=3)

    @page_method_record("判断是否卸载完成")
    def is_uninstall_finished(self):
        return while_operation(self, photo_name="uninstall_page_uninstall_finish_button.png")

    @page_method_record("卸载可牛应用市场")
    def uninstall_knstore(self):
        self.uninstall_button_click()
        if not self.is_uninstall_finished():
            return False
        self.uninstall_finish_button_click()
        if not self.is_uninstall_page_exist():
            return False
        return True