from common.basepage import BasePage, page_method_record
from common import utils
from office.utils import while_operation


class KnstoreInstallPage(BasePage):
    def __init__(self, package_path):
        self.package_path = package_path
        super().__init__()

    def pre_open(self):
        utils.process_start(process_path=self.package_path, async_start=True)

    @page_method_record("判断安装界面是否存在")
    def is_install_page_exist(self):
        return utils.find_element_by_pic(
            self.get_page_shot("install_page_logo.png"), sim=0.8, retry=3)[0]

    @page_method_record("点击安装界面同意并安装按钮")
    def install_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("install_page_install_button.png"), sim=0.8, retry=3)

    @page_method_record("点击安装界面安装完成按钮")
    def install_finish_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("install_page_install_finish_button.png"), sim=0.8, retry=3)

    @page_method_record("点击安装界面不同意按钮")
    def refuse_button_click(self):
        utils.click_element_by_pic(
            self.get_page_shot("install_page_refuse_button.png"), sim=0.8, retry=3)

    @page_method_record("判断是否安装完成")
    def is_install_finished(self):
        return while_operation(self, photo_name="install_page_install_finish_button.png")

    @page_method_record("安装应用市场")
    def install_knstore(self):
        self.install_button_click()
        if self.is_install_finished():
            self.install_finish_button_click()
            utils.perform_sleep(1)
            if not self.is_install_page_exist():
                return True
            return False
        else:
            return False

    @page_method_record("判断主界面是否存在")
    def is_mainpage_exist(self):
        return while_operation(self, photo_name="main_page_logo.png", try_max=10)



