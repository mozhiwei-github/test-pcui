import os
import time
import shutil

import pytest
import win32con
from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
from common.samba import Samba
import win32com.client
import win32con, winreg
from common.utils import Location, perform_sleep, is_process_exists

unins_time_64 = r"SOFTWARE\WOW6432Node\cmpc"
unins_time_keyname = "UninstallTime"
ProgramPath_value = ""
duba_reg = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus"


# def getSign():
#     s = win32com.client.gencache.EnsureDispatch('capicom.signedcode', 0)
#     Package_loacl_path = os.path.join(Download_Package_path().Package_loacl_path,
#                                       file_name(Download_Package_path().Package_loacl_path))
#     Package_loacl_path = r'c:\cleanMaster_package\kclean_master_20210819_10038_1003_8.exe'
#     s.FileName = Package_loacl_path
#     signer = s.Signer
#     print(signer.Certificate.IssuerName, signer.Certificate.SerialNumber)


def get_file_name(num=0):
    file_name = os.listdir(DownloadPackage().Package_loacl_path)[num]
    return file_name


def find_duli_c_slimming_by_reg():
    reg_path_64 = r"SOFTWARE\WOW6432Node\cmpc"
    reg_path_32 = r"SOFTWARE\cmpc"
    reg_root = win32con.HKEY_LOCAL_MACHINE
    prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
    if os.path.exists(prg):
        reg_value = utils.query_reg_value(reg_root, reg_path_64, "ProgramPath")
    else:
        reg_value = utils.query_reg_value(reg_root, reg_path_32, "ProgramPath")
    return reg_value


def pytest_generate_tests(metafunc):
    tod_param = metafunc.config.getoption("--tod")
    print(tod_param)
    return tod_param


def get_tod(request):
    tod = request.param
    return tod


def print_tid_tod():
    reg_path_64 = r"SOFTWARE\WOW6432Node\cmpc\Setup"
    reg_path_32 = r"SOFTWARE\cmpc\Setup"
    prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
    reg_root = win32con.HKEY_LOCAL_MACHINE
    if os.path.exists(prg):
        tid1 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_64, keyname="tid1")
        tid2 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_64, keyname="tid2")
        tod1 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_64, keyname="tod1")
        tod2 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_64, keyname="tod2")
    else:
        tid1 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_32, keyname="tid1")
        tid2 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_32, keyname="tid2")
        tod1 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_32, keyname="tod1")
        tod2 = utils.query_reg_value(regroot=reg_root, regpath=reg_path_32, keyname="tod2")

    log.log_info("tid1 = " + tid1)
    log.log_info("tid2 = " + tid2)
    log.log_info("tod1 = " + tod1)
    log.log_info("tod2 = " + tod2)


def check_package_name():
    tod = get_tod()
    tod = str(tod)
    package_name = get_file_name()
    if tod in package_name:
        log.log_info("tod检查成功，tod与输出参数结果一致")
        return True
    else:
        log.log_info("tod与输出参数结果不一致！！！")
        return False


# 静默安装包执行
def check_package_slience_installing():
    duba_reg = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus"
    ProgramPath_value = utils.query_reg_value(regpath=duba_reg, keyname="ProgramPath")
    utils.remove_reg_value(regpath=duba_reg, value="ProgramPath")
    utils.remove_reg_value(regpath=unins_time_64, value=unins_time_keyname)  # 删除上次卸载时间
    execute_file = os.path.join(DownloadPackage().Package_loacl_path, get_file_name(num=0))
    star_res = utils.process_start(execute_file, async_start=True)
    if star_res:
        package_exists = is_process_exists(get_file_name(num=0))  # 判断安装包进程是否存在
        count = 1
        while package_exists:  # 安装包进程存在则证明还在安装
            perform_sleep(1)
            count = 1 + count
            package_exists = is_process_exists(get_file_name(num=0))
            if not package_exists:
                set_duba_reg(value=ProgramPath_value)
                log.log_info("安装进程已退出")
                print(count)
                return True
                break
            if count == 30:
                set_duba_reg(value=ProgramPath_value)
                log.log_info("安装进程等待30s左右还未退出")
                return False
                break
    else:
        set_duba_reg(value=ProgramPath_value)
        log.log_error("安装进程未能启动")
        return False


def set_duba_reg(value):
    utils.set_reg_value(regpath=duba_reg, keyname="ProgramPath", value=value)


class DownloadPackage:
    Package_Path = os.path.join("autotest", "清理大师安装包验证")  # 共享目录
    Package_loacl_path = os.path.join("c:", "cleanMaster_package")  # 本地存放目录

    def download_package(self):
        cr = Samba("10.12.36.203", "duba", "duba123")

        # 下拉安装包
        cr.download_dir("TcSpace", DownloadPackage().Package_Path,
                        DownloadPackage().Package_loacl_path)
        while True:
            ret1 = os.path.exists(DownloadPackage().Package_loacl_path)  # 判断是否下拉安装包成功
            if ret1:
                log.log_info("下拉文件成功，文件存在")
                break
        return ret1


class KcleanMasterInstall(BasePage):

    def pre_open(self):
        execute_file = os.path.join(DownloadPackage().Package_loacl_path, get_file_name())
        utils.process_start(execute_file, async_start=True)

    # 非静默安装包执行
    @page_method_record("非静默安装包执行")
    def check_package_interface_installing(self):
        # execute_file = os.path.join(Download_Package_path().Package_loacl_path, get_file_name())
        # utils.process_start(execute_file, async_start=True)
        perform_sleep(1)
        find_result = utils.find_element_by_pic(self.get_page_shot("re_install.png"),  # 重新安装标识
                                                sim_no_reduce=False, retry=3)
        if find_result[0]:
            utils.click_element_by_pic(self.get_page_shot("confirm_re_install.png"))
        else:
            find_result = utils.find_element_by_pic(self.get_page_shot("tab_logo.png"),  # 安装标识
                                                    sim_no_reduce=True, retry=5)
        if find_result[0]:
            utils.click_element_by_pic(self.get_page_shot("install_button.png"))  # 执行安装包
            package_exists = is_process_exists(get_file_name())  # 判断安装包进程是否存在
            # count = 1
            while package_exists:  # 安装包进程存在则证明还在安装
                perform_sleep(1)
                # count = 1 + count
                package_exists = is_process_exists(get_file_name(num=0))
                if not package_exists:
                    log.log_info("安装进程已退出")
                    return True
                    break
                # if count == 30:
                #     log.log_info("安装进程等待30s左右还未退出")
                #     return False
                #     break
            find_result = utils.find_element_by_pic(self.get_page_shot("clean_master_identification.png"),
                                                    # 清理大师是否打开标识
                                                    sim_no_reduce=False, retry=5)
            if find_result:
                log.log_pass("安装成功，已打开界面")
                return True
            else:
                log.log_error("安装后，主界面没打开！！")
                return False

        else:
            log.log_error("找不到安装界面标识（安装界面可能已更新）")
            return False


class InstallCheck:

    # 判断托盘进程是否存在
    def check_clean_master_process(self):
        result = is_process_exists("cmtray.exe")
        if result:
            # log.log_info("托盘已启动")
            return True
        else:
            # log.log_info("托盘未启动")
            return False

    # 判断开始菜单项是否存在
    def check_start_menu(self):
        start_menu = r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Clean Master\C盘清理大师.lnk"
        res = os.path.exists(start_menu)
        if res:
            # log.log_info("开始菜单项存在")
            return True
        else:
            # log.log_info("开始菜单项不存在")
            return False

    # 判断桌面快捷方式是否存在
    def check_desktop_lnk(self):
        start_menu = r"c:\Users\Public\Desktop\C盘清理大师.lnk"
        res = os.path.exists(start_menu)
        if res:
            # log.log_info("桌面快捷方式存在")
            return True
        else:
            # log.log_info("桌面快捷方式不存在")
            return False

    # 判断控制面板卸载项（uninstall注册表）是否存在
    def check_control_panel(self):
        reg_root = win32con.HKEY_LOCAL_MACHINE
        reg_path_64 = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\cmpc"
        regpath_32 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\cmpc"
        keyname = "DisplayName"
        prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
        if os.path.exists(prg):
            res = utils.query_reg_value(regroot=reg_root, regpath=reg_path_64, keyname=keyname)
        else:
            res = utils.query_reg_value(regroot=reg_root, regpath=regpath_32, keyname=keyname)
        if res:
            # log.log_info("控制面板卸载项存在")
            return True
        else:
            # log.log_info("控制面板卸载项不存在")
            return False

    # 判断安装目录文件是否存在
    def check_file(self):
        prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
        install_path_64 = r"C:\Program Files (x86)\cmcm\Clean Master"
        install_path_32 = r"C:\Program Files\cmcm\Clean Master"
        install_path = (install_path_64, install_path_32)
        file1 = "cmtray.exe"
        file2 = "kismain.exe"
        if os.path.exists(prg):
            check1 = os.path.join(install_path[0], file1)
            check2 = os.path.join(install_path[0], file2)
        else:
            check1 = os.path.join(install_path[1], file1)
            check2 = os.path.join(install_path[1], file2)

        res = (os.path.exists(check1), os.path.exists(check2))
        if not res[0] and not res[1]:
            log.log_info("文件已卸载: " + file1 + " , " + file2)
            return True
        else:
            log.log_info("文件未卸载成功: " + file1 + " , " + file2)
            return False


if __name__ == '__main__':
    ...
    # pytest.main(["-v", "-s", __file__])
    # allure_attach_path = os.path.join("Outputs", "allure")
    # pytest.main(["-v", "-s", __file__, '--alluredir=%s' % allure_attach_path])
    # os.system("allure serve %s" % allure_attach_path)
    # Download_Package().download_package()

    #
    print_tid_tod()
