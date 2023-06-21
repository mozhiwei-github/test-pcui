# --coding = 'utf-8' --
import atexit
import configparser
import importlib
import os
from common import utils
from common.log import log
from common.utils import perform_sleep
from common.basepage import BasePage
from common.tools.duba_tools import find_dubapath_by_reg
from duba.utils import DubaFilePath

"""C盘瘦身预扫泡页"""


def error_to_kill_kxetray(fun):
    def wapper(fun_self):
        ret = fun(fun_self)
        if not ret:
            print("ready to kill!!!!!!!!")
            utils.kill_process_by_name("kxetray.exe")
        return ret

    return wapper


class CSlimmingPreSweptPage(BasePage):
    # 去除页面初始化校验的初始化函数
    def __init__(self):
        super().__init__(check_open_result=False)
    
    # 使用命令行方式调起泡泡，方便检查泡泡的功能和界面
    def pop_by_commandline(self):
        assert utils.process_start(process_path=DubaFilePath.kfixstar_file_path, async_start=True,
                                   param="-app:pop -task:pure_vip_noad_pop -wait:0 -mask:0",
                                   run_path=find_dubapath_by_reg()), "启动kfixstar.exe进程失败"

    def check_red_bubble_style(self):
        """
        1、组件样式检查
        """
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_pic.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡图片中心图片错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_icon.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡icon文案错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_title.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡title文案错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_setting.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡设置按钮样式错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_close.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡关闭按钮样式错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_give_up.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡放弃释放按钮样式错误")
            return False
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_clean.png"), sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("红泡泡立即释放按钮样式错误")
            return False
        return True

    def check_white_bubble_style(self):
        """
        1、组件样式检查
        """
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_pic.png"),
                                          self.get_page_shot("white_light_bu_pic.png"),
                                          self.get_page_shot("white_bu_pic.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡图片中心图片错误")
            return False
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_icon.png"),
                                          self.get_page_shot("white_light_bu_icon.png"),
                                          self.get_page_shot("white_bu_icon.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡icon文案错误")
            return False
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_title.png"),
                                          self.get_page_shot("white_light_bu_title.png"),
                                          self.get_page_shot("white_bu_title.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡title文案错误")
            return False
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_setting.png"),
                                          self.get_page_shot("white_light_bu_setting.png"),
                                          self.get_page_shot("white_bu_setting.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡设置按钮样式错误")
            return False
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_close.png"),
                                          self.get_page_shot("white_light_bu_close.png"),
                                          self.get_page_shot("white_bu_close.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡关闭按钮样式错误")
            return False
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_clean.png"),
                                          self.get_page_shot("white_light_bu_clean.png"),
                                          self.get_page_shot("white_bu_clean.png")], sim_no_reduce=True, retry=3)[0]
        if not res:
            log.log_info("白泡泡立即释放按钮样式错误")
            return False
        return True

    def check_red_bubble_abandon_release(self):
        """红泡泡检查放弃释放按钮"""
        utils.click_element_by_pic(self.get_page_shot("red_bu_give_up.png"))
        utils.perform_sleep(2)
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_pic.png"), sim_no_reduce=True, retry=3)[0]
        if res:
            log.log_info("红泡泡放弃释放按钮失效")
            return False
        return True

    def check_red_bubble_close(self):
        """红泡泡检查关闭按钮"""
        utils.click_element_by_pic(self.get_page_shot("red_bu_close.png"))
        utils.perform_sleep(2)
        res = utils.find_element_by_pic(self.get_page_shot("red_bu_pic.png"), sim_no_reduce=True, retry=3)[0]
        if res:
            log.log_info("红泡泡关闭按钮失效")
            return False
        return True

    def check_white_bubble_close(self):
        """白泡泡检查关闭按钮"""
        utils.click_element_by_pics([self.get_page_shot("white_dark_bu_close.png"),
                                     self.get_page_shot("white_light_bu_close.png")])
        utils.perform_sleep(2)
        res = utils.find_element_by_pics([self.get_page_shot("white_dark_bu_pic.png"),
                                          self.get_page_shot("white_light_bu_pic.png")], sim_no_reduce=True, retry=3)[0]
        if res:
            log.log_info("白泡泡关闭按钮失效")
            return False
        return True

    def check_red_bubble_release(self):
        """红泡泡检查立即释放按钮"""
        utils.click_element_by_pic(self.get_page_shot("red_bu_clean.png"))
        utils.perform_sleep(2)
        res1 = utils.is_process_exists("ksysslim.exe")
        if not res1:
            log.log_info("点击立即释放按钮c盘瘦身没调起")
            return False
        log.log_info("点击立即释放按钮c盘瘦身主程序已调起", screenshot=True)
        utils.kill_process_by_id("ksysslim.exe")
        return True

    def check_white_bubble_release(self):
        """白泡泡检查立即释放按钮"""
        utils.click_element_by_pics([self.get_page_shot("white_dark_bu_clean.png"),
                                     self.get_page_shot("white_light_bu_clean.png")])
        utils.perform_sleep(2)
        res1 = utils.is_process_exists("ksysslim.exe")
        if not res1:
            log.log_info("点击立即释放按钮c盘瘦身没调起")
            return False
        log.log_info("点击立即释放按钮c盘瘦身主程序已调起", screenshot=True)
        utils.kill_process_by_id("ksysslim.exe")
        return True

    def check_red_bubble_never_notify(self):
        """红泡泡检查不再提醒"""
        """
        1、不在展示功能（1、检查写入配置）
        """
        assert utils.click_element_by_pic(self.get_page_shot("red_bu_setting.png")), "点击设置失败"  # 点击设置
        assert utils.click_element_by_pic(self.get_page_shot("red_bu_ban.png")), "点击不再提醒失败"  # 点击不再提醒
        perform_sleep(2)
        conf = configparser.ConfigParser()
        conf.read(DubaFilePath.popdata_file_path, encoding='utf-8')
        res = conf.get("no_show_anymore", "sys_slim_pop", fallback=False)
        if not res:
            log.log_info("点击不再弹出按钮，不再弹出标记位写入错误")
            return False
        return True

    def check_white_bubble_never_notify(self):
        """白泡泡检查不再提醒"""
        """
        1、不在展示功能（1、检查写入配置）
        """
        assert utils.click_element_by_pics([self.get_page_shot("white_dark_bu_setting.png"),
                                            self.get_page_shot("white_light_bu_setting.png")]), "点击设置失败"  # 点击设置
        assert utils.click_element_by_pic(self.get_page_shot("red_bu_ban.png")), "点击不再提醒失败"  # 点击不再提醒
        perform_sleep(2)
        conf = configparser.ConfigParser()
        conf.read(DubaFilePath.popdata_file_path, encoding='utf-8')
        res = conf.get("no_show_anymore", "sys_slim_pop_2", fallback=False)
        if not res:
            log.log_info("点击不再弹出按钮，不再弹出标记位写入错误")
            return False
        return True

    def check_bubble_auto_close(self):
        """检查泡泡三分钟自动关闭"""
        log.log_info("开始等待12分钟...等待泡泡自动关闭")
        perform_sleep(3)
        ret = utils.is_process_exists("kfixstar.exe")
        if ret:
            log.log_info("已等待12分钟，弹泡没自动关闭")
            return False
        return True


if __name__ == '__main__':
    print(os.path.dirname("E:/Read_File"))
