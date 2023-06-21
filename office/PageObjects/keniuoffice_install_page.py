from common.basepage import BasePage, page_method_record
from common import utils
from common.log import log


class KeniuOfficeInstallPage(BasePage):
    def __init__(self, package_path):
        self.package_path = package_path
        super().__init__()

    def pre_open(self):
        # TODO: 执行打开动作
        utils.process_start(process_path=self.package_path, async_start=True)

    @page_method_record("点击可牛办公安装界面的同意并安装按钮")
    def click_install_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_install_button.png"), sim=0.8, retry=3)

    @page_method_record("点击可牛办公安装界面的不同意按钮")
    def click_refuse_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_refuse_button.png"), sim=0.8, retry=3)

    @page_method_record("点击可牛办公安装界面的安装完成按钮")
    def click_finished_button(self):
        utils.mouse_move(0,0)
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_install_finished_button.png"), sim=0.8, retry=3)

    @page_method_record("点击可牛办公安装界面的自定义安装按钮")
    def click_custom_installation_button(self):
        utils.click_element_by_pic(
            self.get_page_shot("keniuoffice_custom_installation_button.png"), sim=0.8, retry=3)

    @page_method_record("选择自定义安装位置---带输入地址操作")
    def change_install_path(self, new_install_path=None):
        self.click_custom_installation_button()
        browse_button_result, browse_button_pos = utils.find_element_by_pic(
            self.get_page_shot("keniuoffice_browse_button.png"), sim=0.8, retry=3)
        utils.mouse_click(browse_button_pos[0]-100, browse_button_pos[1])
        if new_install_path:
            utils.keyboardInputAltA()
            utils.keyboardInputDel()
            for i in new_install_path:
                utils.keyboardInputByCode(i)
                utils.perform_sleep(0.5)
            log.log_info("新地址输入完成")

    @page_method_record("点击安装并判断可牛办公安装是否完成")
    def install_keniuoffice(self):
        self.click_install_button()
        try_num = 1
        while try_num < 60:
            if utils.find_element_by_pic(
                self.get_page_shot("keniuoffice_install_finished_button.png"), sim=0.8, retry=1)[0]:
                break
            try_num += 1
            utils.perform_sleep(1)
        if try_num >= 60:
            log.log_error("在1min内可牛办公没有安装完成--未匹配到安装完成按钮")
            return False
        self.click_finished_button()
        return True










