from common import utils
from common.log import log
from common.utils import win32con


def find_liebao_program_path_by_reg():
    """查找注册表中猎豹浏览器项目路径"""
    reg_path = r"SOFTWARE\WOW6432Node\liebao"
    reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "ProgramPath")
    assert reg_value, log.log_error("查找注册表中猎豹浏览器项目路径失败", attach=False, need_assert=False)
    return reg_value


def find_liebao_install_path_by_reg():
    """查找注册表中猎豹浏览器安装路径"""
    reg_path = r"SOFTWARE\WOW6432Node\liebao"
    reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "Install Path Dir")
    assert reg_value, log.log_error("查找注册表中猎豹浏览器安装路径失败", attach=False, need_assert=False)
    return reg_value