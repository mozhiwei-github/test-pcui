import os
import win32con
from common import utils


def find_duli_c_slimming_by_reg():
    prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
    reg_path_64 = r"SOFTWARE\WOW6432Node\cmpc"
    reg_path_32 = r"SOFTWARE\cmpc"
    reg_path = (reg_path_64, reg_path_32)
    if os.path.exists(prg):
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path[0], "ProgramPath")
    else:
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path[1], "ProgramPath")

    return reg_value
