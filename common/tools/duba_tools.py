import configparser
import os
from enum import unique, Enum
from common import utils
from common.file_process import FileOperation
from common.log import log
from common.utils import try_import

win32con = try_import('win32con')

scriptpath = os.getcwd()
# 请设置项目跟目录为运行路径
# scriptpath = scriptpath[:scriptpath.index("dubatestpro") + 11]
# scriptpath = scriptpath[:os.path.dirname(scriptpath).rindex(os.path.sep)]
dubapath = r"C:\Program Files (x86)\kingsoft\kingsoft antivirus"

COMMONPATH = os.path.join(scriptpath, "common")


def find_dubapath_by_reg():
    """
    获取中注册表毒霸的ProgramPath值
    @return: 未找到时会返回 None
    """
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\kingsoft\antivirus"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "ProgramPath")
    else:
        regpath = r"SOFTWARE\kingsoft\antivirus"
        regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "ProgramPath")
    return regvalue


def find_duba_reg():
    """
    获取毒霸注册表的路径
    @return: 未找到时会返回 None
    """
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\kingsoft\antivirus"
    else:
        regpath = r"SOFTWARE\kingsoft\antivirus"
    return regpath


def find_dg_reg():
    """
    获取精灵注册表的路径
    @return: 未找到时会返回 None
    """
    if os.path.exists(r"C:\Program Files (x86)"):
        regpath = r"SOFTWARE\WOW6432Node\MyDrivers\DriverGenius"
    else:
        regpath = r"SOFTWARE\MyDrivers\DriverGenius"
    return regpath


def find_dgpath_by_reg():
    """
    获取中注册表驱动精灵的路径
    @return: 未找到时会返回 None
    """
    regpath = r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\dg.exe"
    regvalue = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath, "")
    return regvalue


def clean_vipinfo():
    try:
        cmd1 = r"reg delete HKCU\Software\kingsoft\KVip /v user_info /f"
        cmd2 = r"reg delete HKCU\Software\kingsoft\KVip\10001 /va /f"
        cmd3 = r"rd /s /q  %LocalAppData%\Kingsoft\kvip"
        cmd4 = r"reg delete HKCU\Software\kingsoft\KVip /v user_info_json /f"

        os.system(cmd1)
        os.system(cmd2)
        os.system(cmd3)
        os.system(cmd4)
        # appdata_path = os.environ.get("appdata")
        # vip_data_path = os.path.join(appdata_path, "kingsoft\\kvip")
        # utils.remove_path(vip_data_path)
        # utils.remove_reg_key(regroot=win32con.HKEY_CURRENT_USER, regpath=r"Software\kingsoft\KVip")
        # return utils.set_reg_value(win32con.HKEY_CLASSES_ROOT,
        #                            regpath=r"WOW6432Node\CLSID\{9B7A98EC-7EF9-468c-ACC8-37C793DBD7E0}\Implemented Categories\{9B4EEDF7-FC98-4fa0-8440-9D1BC57B5F2F}",
        #                            keyname="uid", value=str(uuid.uuid4()).replace("-", ""))
        return True
    except:
        return False


def get_duba_tryno():
    """获取毒霸版本号"""
    duba_path = find_dubapath_by_reg()
    assert duba_path, "获取毒霸路径失败"
    with open(os.path.join(duba_path, "ressrc", "chs", "uplive.svr"), "r") as fr:
        while True:
            row_data = fr.readline()
            if row_data.find("TryNo") >= 0:
                return row_data.replace("TryNo=", "").replace("\n", "")
            if not row_data:
                return ""


def get_duba_file_path(filename, folder=None):
    """
    获取毒霸目录下文件路径
    @param filename: 文件名
    @param folder: 文件所在路径（相对毒霸根目录）
    @return:
    """
    product_path = find_dubapath_by_reg()
    assert product_path, "未找到毒霸安装路径"

    folder_file_path = os.path.join(folder, filename.value) if folder else filename.value

    file_path = os.path.join(product_path, folder_file_path)

    return file_path


def set_reg(repa, kname, val):
    """判断注册表是否存在，若不存在则创建
    @param repa: 注册表地址 （duba_tools.py  find_duba_reg()、find_dg_reg()）
    @param kname: 注册表键名
    @param val: 注册表键值
    """
    if val is not None:
        utils.set_reg_value(regpath=repa, keyname=kname, value=val)


def get_dg_install_reg():
    """获取精灵的文件目录，便于删除后恢复"""
    ProgramPath_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath=find_dg_reg(), keyname="AppPath")
    return ProgramPath_value


def get_duba_install_reg():
    """获取毒霸的文件目录，便于删除后恢复"""
    ProgramPath_value = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath=find_duba_reg(),
                                              keyname="ProgramPath")
    return ProgramPath_value


def duba_install_reg_remove():
    """屏蔽毒霸的文件目录，模拟毒霸未安装"""
    utils.remove_reg_value(regpath=find_duba_reg(), value="ProgramPath")


def dg_install_reg_remove():
    """ 屏蔽精灵的文件目录，模拟精灵未安装"""
    utils.remove_reg_value(regpath=find_dg_reg(), value="AppPath")


def restart_cmcore():
    """重启cmcore进行预扫逻辑"""
    utils.kill_process_by_name("cmcore.exe")
    utils.process_start(process_path="net start cmcore", async_start=True)


def install_reg_remove():
    """删除毒霸和精灵的注册表安装标识
    建议删除完之后恢复：set_reg()  get_dg_install_reg()   get_duba_install_reg()
    """
    log.log_info("弹泡前检查精灵和毒霸的安装注册表是否被重写，有则删除")
    duba_reg_value = get_duba_install_reg()
    dg_reg_value = get_dg_install_reg()
    if duba_reg_value:
        duba_install_reg_remove()
    if dg_reg_value:
        dg_install_reg_remove()


@unique
class DubaFiles(Enum):
    """毒霸目录下的文件"""
    POP_DATA_INI = "popdata.ini"
    KSYS_CFG_INI = "ksyscfg.ini"
    KNEW_VIP_INI = "knewvip.ini"
    KPLANET_CACHE_INI = "kplanetcache.ini"
    KPOP_CENTER_DLL = "kpopcenter.dll"
    KPOP_CENTER1_DLL = "kpopcenter1.dll"
    KXE_TRAY_EXE = "kxetray.exe"
    KFIX_STAR_EXE = "kfixstar.exe"
    KL_SOFT_MGR_EXE = "klsoftmgr.exe"
    KSYSSLIM_EXE = "ksysslim.exe"
    KNEWVIP_EXE = "knewvip.exe"
    KVIPAPP_SETTING_INI = "kvipapp_setting.ini"
    KTRASHUD_DAT_ROOT = "ktrashud.dat"
    POPCFG_INI = "popcfg.ini"
    KBIGFILE_DAT = "kbigfile.dat"
    RUNTIME_INFO_CACHE = "runtime_info_cache.ini"

    """"popdata.ini文件的section项"""
    LAST_SHOW_TIME = "last_show_time"  # 弹出时间记录
    NO_SHOW_ANYMORE = "no_show_anymore"  # 不再弹出

    """ksyscfg.ini文件的section项"""
    SCAN = "scan"  # 工具扫描（使用）时间

    """kvipapp_setting.ini文件的section项和key值"""
    SOFT_UNINS_MGR_NORMAL_POP = "SoftUninstallMgr_NormalPop"  # 软件卸载王，右下角泡泡相关配置
    SOFT_UNINS_MGR_WIN10_TOAST = "SoftUninstallMgr_WinToastPop"  # 软件卸载王，win10 toast 相关配置
    TOOL_USE_INTERVAL_DAYS = "tool_use_interval_days"
    DIFF_POP_SAME_PRODUCT_AVOID_DAYS = "diff_pop_same_product_avoid_days"
    LOOP_MINUTES = "loop_minutes"
    START_MINUTES = "start_minutes"
    MIN_SIZE = "min_size"
    SWITCH_ON = "switch_on "

    """kplanetcache.ini文件的section项和key值"""
    PURE_VIP_NOAD_POP = "pure_vip_noad_pop"  # kfixstar.exe 弹泡的命令行中pram的值
    PARAM = "param"

    """kplanetcache.ini文件命令行值"""
    RED_PARAM_VALUE = "{\"popname\":\"sys_slim_clean_pop_old\",\"poptime\":\"2\"}"  # 红泡泡命令行
    WHITE_PARAM_VALUE = "{\"popname\":\"sys_slim_clean_pop_new\",\"poptime\":\"2\"}"  # 白泡泡命令行


# 屏蔽泡泡中心，并且删除多余的kpopcenter1.dll
def rename_kpopcenter():
    kpopcenter_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER_DLL)
    kpopcenter1_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER1_DLL)

    res = os.path.exists(kpopcenter1_file_path)
    if res:
        os.remove(kpopcenter1_file_path)
    res = os.path.exists(kpopcenter_file_path)
    if res:
        os.rename(kpopcenter_file_path, kpopcenter1_file_path)


# 恢复泡泡中心
def recover_kpopcenter():
    kpopcenter_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER_DLL)
    kpopcenter1_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER1_DLL)

    res = os.path.exists(kpopcenter1_file_path)
    if res:
        os.rename(kpopcenter1_file_path, kpopcenter_file_path)


# 修改并还原泡泡中心
def rename_and_recover_kpopcenter(do_fun):
    def fun1(self):
        """屏蔽泡泡中心"""
        rename_kpopcenter()
        res = do_fun(self)
        """还原泡泡中心"""
        recover_kpopcenter()
        if not res:
            return False
        return True

    return fun1


# 重命名泡泡中心之后需要重启托盘
def restart_kxetray():
    kxetray_file_path = get_duba_file_path(DubaFiles.KXE_TRAY_EXE)
    utils.kill_process_by_name("kxetray.exe")
    utils.perform_sleep(5)
    utils.process_start(process_path=kxetray_file_path, async_start=True)


# 关闭主功能使用完成后关闭界面推广泡---C盘瘦身泡
def close_C_slim_pop():
    duba_path = find_dubapath_by_reg()
    knewvip_path = os.path.join(duba_path, "data", "knewvip.ini")
    C_file = FileOperation(knewvip_path)
    set_value_close = ["close", "1"]
    C_section_list = ["kcleanr_msgbox_c_slim", "kbootopt_msgbox_c_slim", "kswscxex_msgbox_c_slim"]
    for sec in C_section_list:
        try:
            C_file.get_options(sec)
        except configparser.NoSectionError as e:
            C_file.add_section(sec)
        C_file.set_option(sec, set_value_close[0], set_value_close[1])


# 关闭主功能使用完成后关闭界面推广泡---大文件专清泡
def close_kdisk_pop():
    duba_path = find_dubapath_by_reg()
    kvipapp_setting_path = os.path.join(duba_path, "data", "kvipapp_setting.ini")
    set_value_switch = ["switch_on", "0"]
    kdisk_file = FileOperation(kvipapp_setting_path)
    kdisk_section_list = ["kbootopt_msgbox_klargeclean", "kcleaner_msgbox_klargeclean", "kswscxex_msgbox_klargeclean"]
    for sec in kdisk_section_list:
        try:
            kdisk_file.get_options(sec)
        except configparser.NoSectionError as e:
            kdisk_file.add_section(sec)
        kdisk_file.set_option(sec, set_value_switch[0], set_value_switch[1])


# 关闭主功能使用完成后关闭界面推广泡---猎豹浏览器推广泡
def close_liebao_pop():
    duba_path = find_dubapath_by_reg()
    kvipapp_setting_path = os.path.join(duba_path, "data", "kvipapp_setting.ini")
    set_value_switch = ["switch_on", "0"]
    liebao_file = FileOperation(kvipapp_setting_path)
    liebao_section_list = ["kcleaner_msgbox_instliebao", "kbootopt_msgbox_instliebao", "kswscxex_msgbox_instliebao"]
    for sec in liebao_section_list:
        try:
            liebao_file.get_options(sec)
        except configparser.NoSectionError as e:
            liebao_file.add_section(sec)
        liebao_file.set_option(sec, set_value_switch[0], set_value_switch[1])


# 关闭主功能使用完成后关闭界面推广泡---电脑医生推广泡
def close_doct_pop():
    duba_path = find_dubapath_by_reg()
    kvipapp_setting_path = os.path.join(duba_path, "data", "kvipapp_setting.ini")
    set_value_switch = ["switch_on", "0"]
    doct_file = FileOperation(kvipapp_setting_path)
    doct_section_list = ["kcleaner_msgbox_sysdoc", "kbootopt_msgbox_sysdoc", "kswscxex_msgbox_sysdoc"]
    for sec in doct_section_list:
        try:
            doct_file.get_options(sec)
        except configparser.NoSectionError as e:
            doct_file.add_section(sec)
        doct_file.set_option(sec, set_value_switch[0], set_value_switch[1])


# 关闭主功能使用完成后关闭界面推广泡---碎片清理推广泡
def close_defrag_pop():
    duba_path = find_dubapath_by_reg()
    kvipapp_setting_path = os.path.join(duba_path, "data", "kvipapp_setting.ini")
    set_value_close = ["close", "1"]
    defrag_file = FileOperation(kvipapp_setting_path)
    defrag_section_list = ["kcleaner_msgbox_defrag", "kbootopt_msgbox_defrag", "kswscxex_msgbox_defrag"]
    for sec in defrag_section_list:
        try:
            defrag_file.get_options(sec)
        except configparser.NoSectionError as e:
            defrag_file.add_section(sec)
        defrag_file.set_option(sec, set_value_close[0], set_value_close[1])


# 关闭主功能使用完成后关闭界面推广泡---隐私清理推广泡
def close_prcycl_pop():
    duba_path = find_dubapath_by_reg()
    prcycl_cfg_path = os.path.join(duba_path, "data", "prcycl_cfg.ini")
    prcycl_file = FileOperation(prcycl_cfg_path)
    prcycl_section = "setting_remind"
    set_value_prcycl = ["KCleanerNoShowMsgbox", "1"]
    try:
        prcycl_file.get_options(prcycl_section)
    except configparser.NoSectionError as e:
        prcycl_file.add_section(prcycl_section)
    prcycl_file.set_option(prcycl_section, set_value_prcycl[0], set_value_prcycl[1])


# 关闭主功能使用完成后关闭界面推广泡---驱动管理王推广泡
def close_driver_pop():
    duba_path = find_dubapath_by_reg()
    kvipapp_setting_path = os.path.join(duba_path, "data", "kvipapp_setting.ini")
    set_value_close = ["close", "1"]
    driver_file = FileOperation(kvipapp_setting_path)
    driver_section_list = ["kcleaner_msg_drivermanager", "kbootopt_msg_drivermanager", "kswscxex_msg_drivermanager"]
    for sec in driver_section_list:
        try:
            driver_file.get_options(sec)
        except configparser.NoSectionError as e:
            driver_file.add_section(sec)
        driver_file.set_option(sec, set_value_close[0], set_value_close[1])


# 关闭主功能使用完成后关闭界面推广泡
def deal_mainpage_close_pop():
    close_driver_pop()
    close_kdisk_pop()
    close_prcycl_pop()
    close_liebao_pop()
    close_doct_pop()
    close_C_slim_pop()
    close_defrag_pop()
