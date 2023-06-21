import os
from enum import unique, Enum
from common import utils
from common.log import log
from common.utils import try_import
from common.utils import win32con
from common.utils import perform_sleep, Location
from conew.page_resource import page_resource


class SoftwareRegistryLocation(Enum):
    """"软件注册表位置"""
    fastpdf = r"Software\fastpdf"  #PDF
    fastpic = r"Software\fastpic"  #看图
    k52zip = r"Software\k52zip\setup"  #压缩
    fastvc = r"Software\fastvc"  #视频转换
    kntemplate = r"Software\kntemplate\setup" #可牛办公


def kill_process(process_name):
    # kill进程
    if not utils.is_process_exists(process_name):
        log.log_error("%s 进程不存在" % process_name)
    os.system("taskkill /f /im %s" % process_name)
    perform_sleep(2)
    if utils.is_process_exists(process_name):
        process_id = utils.get_pid(process_name)
        os.system("taskkill /PID %s /F /T" % (process_id))
    log.log_info("kill进程 %s 成功" % process_name)
    return True

def kill_conew_page_process():
    """杀掉可牛产品相关页面进程"""
    for page in page_resource.values():
        process_name = page["process_name"]
        if process_name:
            os.system("taskkill /f /im " + process_name)

def restart_explorer():
    """重启explorer"""
    kill_process("explorer.exe")
    utils.process_start("start /b c:\windows\explorer.exe", True)
    perform_sleep(8)
    if utils.is_process_exists("explorer.exe"):
        log.log_info("重启explorer.exe成功")
    else:
        log.log_error("未找到explorer.exe")

def find_haoya_path_by_reg():
    """查找注册表中好压项目路径"""
    reg_path = r"Software\k52zip\setup"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    assert reg_value, log.log_error("查找注册表中好压路径失败", attach=False, need_assert=False)
    return reg_value


# 获取好压渠道号
def get_haoya_tryno():
    with open(os.path.join(find_haoya_path_by_reg(), "ressrc", "chs", "uplive.svr"), "r") as fr:
        while True:
            row_data = fr.readline()
            if row_data.find("TryNo") >= 0:
                return row_data.replace("TryNo=", "").replace("\n", "")
            if not row_data:
                return ""


def find_kantu_path_by_reg():
    """查找注册表中看图项目路径"""
    reg_path = r"Software\fastpic"
    reg_value = utils.query_reg_value(win32con.HKEY_CURRENT_USER, reg_path, "installpath")
    assert reg_value, log.log_error("查找注册表中看图路径失败", attach=False, need_assert=False)
    return reg_value


# 获取看图渠道号
def get_kantu_tryno():
    with open(os.path.join(find_kantu_path_by_reg(), "ressrc", "chs", "uplive.svr"), "r", encoding="utf-8") as fr:
        while True:
            row_data = fr.readline()
            if row_data.find("TryNo") >= 0:
                return row_data.replace("TryNo=", "").replace("\n", "")
            if not row_data:
                return ""


def find_knmgr_path_by_reg():
    """查找注册表中可牛电脑助手项目路径"""
    if os.path.exists(r"C:\Program Files (x86)"):
        reg_path = r"SOFTWARE\WOW6432Node\knoptasst\ascommon"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "installpath")
    else:
        reg_path = r"SOFTWARE\knoptasst\ascommon"
        reg_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, reg_path, "installpath")
    assert reg_value, log.log_error("查找注册表中可牛电脑助手项目路径失败", attach=False, need_assert=False)
    return reg_value



# 获取可牛电脑助手渠道号
def get_knmgr_tryno():
    with open(os.path.join(find_knmgr_path_by_reg(), "ressrc", "chs", "uplive.svr"), "r") as fr:
        while True:
            row_data = fr.readline()
            if row_data.find("TryNo") >= 0:
                return row_data.replace("TryNo=", "").replace("\n", "")
            if not row_data:
                return ""


def file_exist(file,folder="haoyatool"):
    """
    判定桌面目录中文件是否存在
    @param folder: 桌面的文件夹，默认为haoyatool
    @param file：文件夹中文件或目录
    @return:
                    """
    path = os.path.join(os.getenv("USERPROFILE"), "desktop", folder, file)
    if not os.path.exists(path):
        log.log_error("目录不存在")
    log.log_info("文件%s存在" % file)
    return path, True






if __name__=="__main__":
    restart_explorer()