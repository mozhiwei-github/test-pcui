import os
import win32con
from common import utils

scriptpath = os.getcwd()

COMMONPATH = os.path.join(scriptpath, "common")


def find_wallpaper_path_by_reg():
    regpath = r"SOFTWARE\WOW6432Node\cmcm\kdesk"
    regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "ProgramPath")
    return regvalue
