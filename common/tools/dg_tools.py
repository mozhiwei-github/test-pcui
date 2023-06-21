import ctypes
import sys
from enum import unique, Enum
import random



from common.tools import duba_tools
import os
from common import utils
from common.utils import try_import, is_admin

win32con = try_import('win32con')


dg_path = duba_tools.find_dgpath_by_reg()

def find_dgpath_by_reg():
    """
    获取中注册表驱动精灵的路径--选取workpath目录
    @return: 未找到时会返回 None
    """
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "WorkPath")
    else:
        regpath = r"SOFTWARE\MyDrivers\DriverGenius"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "WorkPath")
    return regvalue


def rename_file(file_name=None,file_path=None):
    """
    根据名称或者路径屏蔽指定文件
    @param file_name: 待屏蔽文件名
    @param file_path: 待屏蔽文件路径
    """
    re_file_path = r''
    file_name_test = str(random.randint(1,100))
    if file_name:
        re_file_name = file_name.split(".")[0] + "1." + file_name.split(".")[1]
    if file_path:
        re_path_list = file_path.split("\\")
        re_path_list[-1] = (file_path.split("\\")[-1]).split(".")[0] + file_name_test + "." +\
                           (file_path.split("\\")[-1]).split(".")[1]
        # 预防产生的随机数已存在
        for i in re_path_list:
            if i[-1] == ":":
                i += "\\"
            re_file_path = os.path.join(re_file_path,i)
    if os.path.exists(file_path):
        os.rename(file_path,re_file_path)


def get_dg_tryno():
    """获取驱动精灵版本号"""
    assert dg_path, "获取毒霸路径失败"
    with open(os.path.join(dg_path, "ressrc", "chs", "uplive.svr"), "r") as fr:
        while True:
            row_data = fr.readline()
            if row_data.find("TryNo") >= 0:
                return row_data.replace("TryNo=", "").replace("\n", "")
            if not row_data:
                return ""