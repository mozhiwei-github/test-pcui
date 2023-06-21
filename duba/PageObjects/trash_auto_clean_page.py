import atexit
import importlib
import os
import shutil

import duba
from common import utils
from common.basepage import BasePage, page_method_record
from common.file_process import FileOperation
from common.log import log
from common.tools import duba_tools
from common.tools.duba_tools import find_dubapath_by_reg
from common.utils import perform_sleep, check_charset
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects.vip_page import vip_page
import xml.etree.ElementTree as ET

from duba.utils import DubaFilePath

"""自动清理垃圾"""

ktaskcfg_path = r"c:\datmaker\ktaskcfg.dat"

AutoSpeedUpPop_lsit = [["interval_days", "0"], ["min_size_mb", "0"], ["event_interval_minute", "0"]]

common_lsit = ["pop_time_h", "pop_time_l", "pop_count"]


def set_xml_attribute_value(file_path):
    """
    修改ktaskcfg.dat解密后，delaytime=1
    :param file_path: 解密后文件的路径
    :param attribute_value:
    :return:
    """
    tree = ET.parse(file_path)  # 读取文件
    root = tree.getroot()
    # 遍历xml文档
    for child in root:
        if child.attrib.get("name") is not None and child.attrib["name"] == 'trashmon':
            for x in child:
                if x.attrib["id"] == '{1B82D49B-8220-4787-A44C-53BAE449CDC9}':
                    x.set("delaytime", "1")  # 修改属性
                    tree.write(r"c:\datmaker\ktaskcfg.dat", encoding='UTF-8')


def modify_kvipapp_setting():
    """
    修改kvipapp_setting.ini
    :return:
    """
    file = FileOperation(DubaFilePath.kvipapp_setting_path)
    file.del_section("AutoSpeedUpPop")
    file.add_section("AutoSpeedUpPop")
    file.set_options("AutoSpeedUpPop", AutoSpeedUpPop_lsit)


def delete_popdata():
    """
    删除popdata.ini中不需要的option
    :return:
    """
    file = FileOperation(DubaFilePath.popdata_file_path)
    file.del_option_by_list("common", common_lsit)
    file.del_option("last_show_time", "autocleanpop")
    file.del_option("min_limit_size", "autocleanpop")


def delete_ktrashud():
    """
    删除ktrashud.dat中不需要的option
    :return:
    """
    file = FileOperation(DubaFilePath.ktrashud_root_file_path)
    file.del_option("common", "mainshow")


def delete_popcfg():
    """
    删除popcfg.ini中不需要的option
    :return:
    """
    file = FileOperation(DubaFilePath.popcfg_file_path, encoding=check_charset(DubaFilePath.popcfg_file_path))
    file.del_option("min_limit_size_ver2", "autocleanpop")


class TrashAutoCleanPage(BasePage):

    def pre_open(self):
        # 从会员页进入自动清理垃圾页
        self.vp = vip_page()
        self.vp.auto_clean_crash_click()

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

    @page_method_record("点击登录按钮")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("login_button.png"),
                                            self.get_page_shot("login_button1.png"),
                                            self.get_page_shot("login_button2.png")], retry=3,
                                           sim_no_reduce=True)

    def check_auto_trash_clean_pop(self):
        """
        检查自动垃圾清理泡泡是否弹出
        :return:
        """
        for i in range(360):
            utils.perform_sleep(1)
            res = utils.find_element_by_pics([self.get_page_shot("auto_clean_pop_tab.png"),
                                              self.get_page_shot("auto_clean_pop_tab2.png")], retry=1,
                                             sim_no_reduce=True)[0]
            if res:
                log.log_info("已经弹出自动垃圾清理泡泡")
                self.click_pop_close()
                return True
        log.log_info("经过6分钟后，无弹出自动垃圾清理泡泡")
        return False

    def click_pop_close(self):
        """
        点击自动垃圾清理泡泡关闭按钮
        :return:
        """
        return utils.click_element_by_pic(self.get_page_shot("pop_close_btn.png"))

    def open_auto_clean(self):
        """
        打开自动清理功能
        :return:
        """
        return utils.click_element_by_pic(self.get_page_shot("open_btn.png"), sim=0.8, retry=5, sim_no_reduce=True)


if __name__ == '__main__':

    duba.utils.delete_user_cache()


    # duba_tools.rename_kpopcenter()
    #
    # delete_popcfg()
    # delete_ktrashud()
    # delete_popdata()
    # modify_kvipapp_setting()
    #
    # Datmaker_local = os.path.join("c:", "datmaker", "datmaker.exe")
    # file_local = os.path.join("c:", "datmaker", "ktaskcfg.dat")
    # file_local2 = os.path.join("c:", "datmaker")
    # duba_file = os.path.join(find_dubapath_by_reg(), "data", "ktaskcfg.dat")
    # duba_file2 = os.path.join(find_dubapath_by_reg(), "data")
    # print(duba_file)
    # utils.pull_datmaker()
    # shutil.copy(duba_file, file_local2)  # 复制毒霸的文件到file_local2目录下
    # utils.decrypt_dat(Datmaker_local, file_local, op="-d")
    # set_xml_attribute_value(file_local)
    # utils.decrypt_dat(Datmaker_local, file_local, op="-e")
    # shutil.copy(file_local, duba_file2)
    #
    # duba_tools.restart_kxetray()
    #
    # test = TrashAutoCleanPage(do_pre_open=False, check_open_result=False)
    # test.check_auto_trash_clean_pop()
    # test.click_pop_close()

    # os.chdir(r"C:\Users\CF\jiemi解密工具\datmaker")
    # os.system("datmaker.exe -e ktaskcfg.dat")
    # utils.keyboardInputEnter()
