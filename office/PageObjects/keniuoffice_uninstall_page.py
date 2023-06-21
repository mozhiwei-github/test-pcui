import os

from common.basepage import BasePage, page_method_record
from common import utils
from office.contants import keniuofficePath
from office.utils import while_operation

class KeniuOfficeUninstallPage(BasePage):

    def pre_open(self):
        # TODO: 执行打开动作
        utils.process_start(
            process_path=os.path.join(keniuofficePath.DEFAULTINSTALLPATH.value, "uninstall.exe"), async_start=True)

    @page_method_record("判断卸载界面是否存在")
    def is_uninstall_page_exist(self):
        return while_operation(self, photo_name="uninstallpage_logo.png")

    @page_method_record("点击卸载界面的卸载按钮")
    def click_uninstall_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_button.png"), sim=0.8, retry=3)

    @page_method_record("判断卸载是否完成")
    def is_uninstall_finished(self):
        return while_operation(self, photo_name="uninstall_finished_button.png",try_max=60, sim=0.85)

    @page_method_record("点击卸载完成按钮")
    def click_uninstall_finished_button(self):
        utils.mouse_move(1,1)
        utils.click_element_by_pic(
            self.get_page_shot("uninstall_finished_button.png"), sim=0.8, retry=5)

    @page_method_record("判断可牛办公是否卸载成功")
    def is_keniuoffice_path_exist(self):
        file_path = os.path.join(keniuofficePath.DEFAULTINSTALLPATH.value, "ktemplate.exe")
        if os.path.exists(file_path):
            return False
        return True

