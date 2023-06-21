# --coding = 'utf-8' --
from common.basepage import BasePage, page_method_record
from common import utils
from common.log import log
from duba.PageObjects.main_page import main_page


class update_page(BasePage):
    def pre_open(self):
        # TODO：执行打开动作
        self.mp = main_page()
        self.mp.check_update_menu_click()

    @page_method_record("进行点击立即升级")
    def update_click(self, retry=60*10):
        """
        点击毒霸升级界面立即升级按钮
        @param retry: 识别升级成功界面重试次数，每次间隔1s
        @return:
        """
        # 有的时候进程起来已经在升级中,故此处没有点击到升级按钮也可以进行下一步
        utils.click_element_by_pic(self.get_page_shot("button_update.png"), sim=0.9, retry=3)
        utils.perform_sleep(3)

        # 匹配升级成功的图
        if utils.find_element_by_pic(self.get_page_shot("logo_update_success.png"), sim=0.95, retry=retry, hwnd=self.hwnd,
                                     sim_no_reduce=True)[0]:
            log.log_info("检测到升级完成界面", screenshot=True)

            utils.perform_sleep(1)

            # 需要立即重启的话就设置环境变量标记
            if self.check_need_reboot():
                with open("reboot.txt", "w") as fw:
                    fw.write("reboot")
                log.logger.info("重启文件已设定,准备重启系统")

            return True
        # 升级失败
        return False

    # 检查升级界面是否有立即重启按钮
    def check_need_reboot(self):
        return utils.find_element_by_pic(self.get_page_shot("button_reboot.png"), sim=0.9, retry=2, sim_no_reduce=True)[0]


if __name__ == '__main__':
    up = update_page()
    up.update_click()
