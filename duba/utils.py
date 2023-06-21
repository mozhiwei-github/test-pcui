import os
import time

from common import utils
from common.log import log
from common.tools.duba_tools import find_dg_reg, find_duba_reg, get_duba_file_path, DubaFiles
from common.utils import create_server_id, win32con, perform_sleep
from duba.api.pay import pay_settings_api
from duba.contants import PaySettingsInfo
from duba.page_resource import page_resource


class DubaFilePath:
    popdata_file_path = get_duba_file_path(DubaFiles.POP_DATA_INI, folder="data")
    ksyscfg_file_path = get_duba_file_path(DubaFiles.KSYS_CFG_INI, folder="data")
    knewvip_file_path = get_duba_file_path(DubaFiles.KNEW_VIP_INI, folder="data")
    kplanetcache_file_path = get_duba_file_path(DubaFiles.KPLANET_CACHE_INI, folder="data")
    kvipapp_setting_path = get_duba_file_path(DubaFiles.KVIPAPP_SETTING_INI, folder="data")
    kpopcenter_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER_DLL)
    kpopcenter1_file_path = get_duba_file_path(DubaFiles.KPOP_CENTER1_DLL)
    kxetray_file_path = get_duba_file_path(DubaFiles.KXE_TRAY_EXE)
    kfixstar_file_path = get_duba_file_path(DubaFiles.KFIX_STAR_EXE)
    ksysslim_file_path = get_duba_file_path(DubaFiles.KSYSSLIM_EXE)
    knewvip_exe_file_path = get_duba_file_path(DubaFiles.KNEWVIP_EXE)
    ktrashud_root_file_path = get_duba_file_path(DubaFiles.KTRASHUD_DAT_ROOT)
    popcfg_file_path = get_duba_file_path(DubaFiles.POPCFG_INI, folder="data")
    kbigfile_file_path = get_duba_file_path(DubaFiles.KBIGFILE_DAT, folder="data")
    runtime_info_cache_file_path = get_duba_file_path(DubaFiles.RUNTIME_INFO_CACHE, folder=r"data\diskopt")

def get_tool_pay_settings(tool, open_id, token, tryno, server_id=None):
    """
    获取工具对应的会员套餐列表
    @param tool: 工具名称
    @param open_id: 用户open_id
    @param token: 用户token
    @param server_id: 客户端server id
    @param tryno: 渠道号
    @return:
    """
    if tool not in PaySettingsInfo:
        log.log_error(f"[Error]can not found tool: {tool}")
        return

    if not server_id:
        server_id = create_server_id()

    tool_pay_setting_info = PaySettingsInfo[tool]
    res = pay_settings_api(open_id, token, server_id, tryno, show=tool_pay_setting_info["show"])

    if res.status_code != 200:
        log.log_error(f"[Error]get_pay_setting status_code: {res.status_code}")
        return

    try:
        res_data = res.json()
        ret = res_data["resp_common"]["ret"]
        if ret != 0:
            log.log_error(f"[Error]get_pay_setting ret: {ret}")
            return

        return res_data["pay_price_settings"]
    except Exception as e:
        log.log_error("[Error] {e}")
        return


def kill_duba_page_process(excludeKislive=False):
    """杀掉毒霸页面进程"""
    for page in page_resource.values():
        process_name = page["process_name"]
        if process_name:
            if not (process_name == "kislive.exe" and excludeKislive):
                os.system("taskkill /f /im " + process_name)

    # kill掉pageresource以外的其它进程，防止升级数据替换失败
    os.system("taskkill /f /im kxecenter.exe")

    # kxetray与kxescore需要特殊处理
    pid_kxetray = utils.get_pid("kxetray.exe")
    pid_kxescore = utils.get_pid("kxescore.exe")
    os.system("taskkill /PID %s /PID %s /F /T" % (pid_kxetray, pid_kxescore))


def reset_duba_env():
    # 关闭毒霸自保护
    close_duba_self_protecting()
    # 杀掉毒霸页面进程
    kill_duba_page_process()


def close_duba_self_protecting():
    """关闭毒霸自保护"""
    from duba.PageObjects.setting_page import SettingPage
    sp = SettingPage()
    sp.self_protecting_close()
    sp.page_del()


def check_tools_login(obj, pic):
    """
    检查百宝箱工具是否有登录
    @pic: 百宝箱工具会员中心入口图片
    @obj: 百宝箱工具页面对象
    """
    if utils.find_element_by_pic(obj.get_page_shot(pic), retry=2, sim_no_reduce=True)[0]:
        islogin = False
    else:
        islogin = True
    return islogin


# 毒霸百宝箱工具登录超级会员
def login_super_vip(obj, username=None, password=None):
    from duba.PageObjects.vip_page import vip_page
    from duba.PageObjects.login_page import LoginPage
    obj.vip_center_click()
    vip_page_o = vip_page(do_pre_open=False)
    vip_page_o.user_login_click()  # 打开用户登录那个小窗体界面 （会判断是否已经登录，已经登录则退出）
    LoginPage_o = LoginPage(do_pre_open=False)
    LoginPage_o.super_vip_user_login(username, password)  # 登录一个超级会员
    if vip_page_o:
        vip_page_o.page_close()


# 毒霸百宝箱工具登录非会员
def login_normal_user(obj):
    from duba.PageObjects.vip_page import vip_page
    from duba.PageObjects.login_page import LoginPage
    obj.vip_center_click()
    vip_page_o = vip_page(do_pre_open=False)
    vip_page_o.user_login_click()  # 打开用户登录那个小窗体界面 （会判断是否已经登录，已经登录则退出）
    LoginPage_o = LoginPage(do_pre_open=False)
    LoginPage_o.normal_user_login()  # 登录一个非会员账号
    if vip_page_o:
        vip_page_o.page_close()


# 循环判断ksysslim.exe,ksyshelper64.exe，ksyshelper.exe是否存在
def check_ksysslim_exist_loop():
    for x in range(20):
        perform_sleep(1)
        ret = utils.is_process_exists("ksysslim.exe")  # 存在则返回True
        if not ret:
            log.log_info("ksysslim.exe已退出")
            return True
    log.log_info("点击关闭，20s后ksysslim.exe没退出")  # 循环结束仍未退出exe，则报错
    return False


# 会员卡点检查
def check_vip_block(self):
    from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
    from common.log import log
    if UnexpectedPopup.popup_process(UnexpectedPopupInfo.EXIT_VIP_UPDATE, hwnd=self.hwnd):
        log.log_info("出现卡点")
        # utils.keyboardInputAltF4()
        return True
    return False


def close_dg_protect_after_checkreg():
    from duba.PageObjects.dg_page import DgPage
    """判断精灵安装目录注册表后再关闭自保护"""
    res = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath=find_dg_reg(), keyname="AppPath")
    if res is not None:
        dg = DgPage()
        dg.self_protecting_close()
    else:
        log.log_info("此环境没有精灵安装目录注册表项")
        return


def close_duba_protect_after_checkreg():
    """判断毒霸安装目录注册表后再关闭自保护"""
    res = utils.query_reg_value(win32con.HKEY_LOCAL_MACHINE, regpath=find_duba_reg(), keyname="ProgramPath")
    if res is not None:
        close_duba_self_protecting()
    else:
        log.log_info("此环境没有毒霸安装目录注册表项")
        return


def add_log_reg():
    """添加毒霸日志注册表"""
    prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
    if os.path.exists(prg):
        log_reg_path = r"SOFTWARE\WOW6432Node\kingsoft\Antivirus\sysopt"
    else:
        log_reg_path = r"SOFTWARE\kingsoft\Antivirus\sysopt"
    utils.set_reg_value(regpath=log_reg_path,
                        keyname=r"LogLevel", value_type=win32con.REG_DWORD, value=0)
    utils.set_reg_value(regpath=log_reg_path,
                        keyname=r"needWriteLog", value_type=win32con.REG_DWORD, value=1)


def add_test_mode():
    """添加此注册表，毒霸就不会清host"""
    prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
    if os.path.exists(prg):
        reg_path = r"SOFTWARE\WOW6432Node\kingsoft\antivirus\testmode"
    else:
        reg_path = r"SOFTWARE\kingsoft\antivirus\testmode"
    utils.create_reg_key(regpath=reg_path)


def while_operation(product_path=None, photo_name=None, photo_name_list=[], sim=0.8, retry=3, try_max=30):
    try_num = 1
    result = False
    if len(photo_name_list) == 0:
        while try_num < try_max:
            if utils.find_element_by_pic(os.path.join(product_path, photo_name), sim=sim, retry=retry)[0]:
                result = True
                break
            else:
                time.sleep(0.8)
                try_num += 1
    else:
        while try_num < try_max:
            for i in photo_name_list:
                if utils.find_element_by_pic(os.path.join(product_path, i), sim=sim, retry=retry)[0]:
                    result = True
                    break
                else:
                    time.sleep(0.8)
                    try_num += 1
    return result
