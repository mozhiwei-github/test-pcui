# --coding = 'utf-8' --
from enum import Enum
from common import utils
from common.log import log
from common.basepage import BasePage
from common.file_process import *
from duba.utils import DubaFilePath

"""磁盘管理预扫泡页"""

# runtime_info_cache.ini 扫描结果的section
runtime_se_list = [
    "largeclean",
    "repeatclean",
    "wechatclean",
    "QQclean"
]

# kvipapp_setting.ini 预扫设置section
kvipapp_se_list = [
    "kdisk_mgr_pop",
    "kdiskopt_dupclean",
    "kdiskopt_wechatclean",
    "kdiskopt_qqclean"
]

# popdata.ini 弹泡记录
popdata_se_list = [
    "kdisk_mgr_pop",
    "kdisk_mgr_pop_win_toast",

    "kdiskopt_dupclean",
    "kdiskopt_dupclean_win_toast",
    "kdisk_mgr_repeat_pop",

    "kdiskopt_wechatclean",
    "kdiskopt_wechatclean_win_toast",
    "kdisk_mgr_wechat_pop",

    "kdiskopt_qqclean",
    "kdisk_mgr_qq_pop"
]


def check_pre_scan_process_up(process_name, section):
    """
    检查一段时间内预扫进程是否被调起,
    预扫进程不存在（预扫结束太快），则检查预扫结果
    :param process_name: 预扫进程名
    :param section: 预扫结果section
    :return: 存在返回 True，不存在返回 False
    """
    for i in range(1, 6):
        utils.perform_sleep(1)
        ret = utils.is_process_exists(process_name)
        if ret:
            log.log_info("已调起预扫：" + process_name)
            return True
    ret = utils.is_process_exists(process_name)
    if not ret:
        return check_pre_scan_result(section)


def check_pre_scan_result(section):
    """
    检查预扫结果
    :param section: 目标预扫结果项
    :return:
    """
    f = FileOperation(DubaFilePath.runtime_info_cache_file_path)
    re = f.get_sessions()
    if section in re:
        log.log_info("已经有预扫结果：" + section)
        return True
    return False


def set_kvipapp_setting():
    """
    设置kvipapp_setting的弹泡阈值，初始扫描等待时间
    :return:
    """

    f = FileOperation(DubaFilePath.kvipapp_setting_path)
    for i in kvipapp_se_list:
        f.set_option(i, "min_size", "1")
    f.set_options("kdisk_public_time", [["start_minutes", "1"], ["loop_minutes", "1"]])


def del_popdata():
    """
    删除泡泡弹出记录
    :return:
    """
    f = FileOperation(DubaFilePath.popdata_file_path)
    f.del_section_by_list(popdata_se_list)


def set_pop_time_to_yesterday(pop_section):
    """
    设置指定泡泡弹出时间为昨天
    :param pop_section: 泡泡section项
    :return:
    """
    f = FileOperation(DubaFilePath.popdata_file_path)
    now = int(utils.get_time())
    yesterday = now - 86400
    f.set_option(pop_section, "last_show_time", str(yesterday))


def del_runtime_info_cache():
    """
    删除磁盘清理的扫描结果
    :return:
    """
    f = FileOperation(DubaFilePath.runtime_info_cache_file_path)
    f.del_section_by_list(runtime_se_list)


class DiskManagePreSweptPage(BasePage):
    # 去除页面初始化校验的初始化函数
    def __init__(self):
        super().__init__(check_open_result=False)

    def click_pop_close_btn(self):
        log.log_info("操作泡泡前截图", screenshot=True)
        return utils.click_element_by_pic(self.get_page_shot("pop_close_btn.png"), sim=0.8, sim_no_reduce=True)

    def check_pre_sacn_exit(self, process_name):
        """
        检查5分钟内是否结束预扫进程，若期间预扫进程结束，则点击泡泡关闭按钮
        :return:
        """
        for i in range(1, 300):
            utils.perform_sleep(1)
            if not utils.is_process_exists(process_name):
                return True
        return False


if __name__ == "__main__":
    # set_pop_time_to_yesterday("kdisk_mgr_pop")
    # test = DiskManagePreSweptPage()
    # test.click_pop_close_btn()
    #
    set_kvipapp_setting()
    # del_popdata()
    # del_runtime_info_cache()
    #
    # utils.kill_process_by_name("kxetray.exe")
    # utils.process_start(DubaFilePath.kxetray_file_path, async_start=True)
    #
    # utils.perform_sleep(55)
    # res = check_pre_scan_process_up("klargecleanup.exe")
    #
    # test.check_pop_and_close("klargecleanup.exe")
    #
