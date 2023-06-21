# --coding = 'utf-8' --
import os
from enum import Enum, unique
import win32con
from common import utils
from common.samba import Samba
from common.log import log
from common.unexpectwin_system import UnExpectWin_System
from common.utils import perform_sleep, Location
from common.basepage import BasePage, page_method_record
from common.tools.base_tools import get_page_shot
from common.tools.duba_tools import find_dgpath_by_reg
from duba.PageObjects.unexpected_popup import UnexpectedPopup, UnexpectedPopupInfo
from duba.PageObjects import vip_page, login_page
from duba.PageObjects.baibaoxiang_page import baibaoxiang_page
from duba.utils import DubaFilePath

"""C盘瘦身页"""


def error_to_kill_kxetray(fun):
    def wapper(fun_self):
        ret = fun(fun_self)
        if not ret:
            print("ready to kill!!!!!!!!")
            utils.kill_process_by_name("kxetray.exe")
        return ret

    return wapper


appdata = os.getenv("APPDATA")
programdata = os.getenv("ProgramData")

userpath = os.path.dirname(os.path.dirname(appdata))  # 回到上一级目录。。。因为os.getenv("APPDATA")打开的是C:\Users\CF\AppData\Roaming

# 微信专清模拟文件
WeChat_Log_Shared_Path = os.path.join("autotest", "微信日志")  # 共享目录
WeChat_Log = os.path.join(userpath, "AppData", "Roaming", "Tencent", "WeChat", "log")  # C盘瘦身能检出的目录

# 微信专清模拟文件
Applet_log_Shared_Path = os.path.join("autotest", "小程序日志")
Applet_log = os.path.join(userpath, "Documents", "WeChat Files", "wxid_0mcwz8yxcvg221",
                          "Applet",
                          "wx9074de28009e1111", "usr", "miniprogramLog")

# 微信专清模拟文件
WeChat_official_account_cache_Shared_Path = os.path.join("autotest", "微信公众号缓存")
WeChat_official_account_cache = os.path.join(userpath, "Documents", "WeChat Files", "wxid_0mcwz8yxcvg221",
                                             "FileStorage",
                                             "Cache", "2021-04")
# 用于判断是否下拉垃圾清理文件成功
Check_File_ksysslim = os.path.join(userpath, "Documents", "WeChat Files", "wxid_0mcwz8yxcvg221",
                                   "FileStorage",
                                   "Cache", "2021-04", "11.jpg")

# 大文件搬家模拟文件
Big_File_Moving_cache_Shared_Path = os.path.join("autotest", "大文件搬家_英伟达显卡升级安装包目录")
Big_File_Moving_cache = os.path.join(programdata, "NVIDIA Corporation", "Downloader",
                                     "f341c46583449ed64fb326a8bb114a02")

# 大文件搬家，模拟文件夹搬家文件
Big_File_Moving_folder_cache_Shared_Path = os.path.join("autotest", "test1")
Big_File_Moving_folder_cache = os.path.join("c:", "test1")

# 用于判断是否下拉大文件搬家文件成功
Check_File_bigfile = os.path.join(programdata, "NVIDIA Corporation", "Downloader",
                                  "f341c46583449ed64fb326a8bb114a02",
                                  "GeForce_Experience_Update_v3.22.0.32_Official_708F29.exe")

# 软件搬家模拟文件
SoftWare_Moving_cache_Shared_Path = os.path.join("autotest", "软件搬家", "winRAR")
SoftWare_Moving_cache = os.path.join("c:", "winRAR")

# 模拟的winRar存放本地目录   用于判断是否下拉软件搬家文件成功
Check_SoftWare = os.path.join("c:", "winRAR")
# 由于访问权限可能无法访问目录，故暂时屏蔽这些文件的下拉
# 诊断数据模拟文件
# Diagnostic_data_cache_Shared_Path = os.path.join("autotest", "诊断数据")
# Diagnostic_data_cache = os.path.join(r"C:\ProgramData\Microsoft\Windows Defender\Support")
#
# # Windows防御模拟文件
# Windows_Defense_cache_Shared_Path = os.path.join("autotest", "Windows防御")
# Windows_Defense_cache = os.path.join(r"C:\ProgramData\Microsoft\Diagnosis\EventTranscript")

# 进程占用模拟文件: CheckInfoc.exe
Occupy_process_Shared_Path = os.path.join("autotest", "test_exe")
Occupy_process_Path = os.path.join("c:", "test_exe")

# kbigfile.dat配置文件
kbigfile_Shared_Path = os.path.join("autotest", "bigfile_config")


@unique
class CleanAlertPromptCloseType(Enum):
    CLOSE_DIRECTLY = 0  # 直接关闭
    NOT_CLEAN_NOW = 1  # 点击暂不清理按钮关闭


class CreateGarbage:
    def create_garbage(self):
        # os.remove(CSlimmingGarbagePath.WeChat_Log.value)
        # os.remove(CSlimmingGarbagePath.Applet_log.value)
        # os.remove(CSlimmingGarbagePath.WeChat_official_account_cache.value)
        # os.remove(CSlimmingGarbagePath.Big_File_Moving_cache.value)

        samba_obj = Samba("10.12.36.203", "duba", "duba123")
        # 微信日志
        samba_obj.download_dir("TcSpace", WeChat_Log_Shared_Path,
                               WeChat_Log)

        # 小程序日志
        samba_obj.download_dir("TcSpace", Applet_log_Shared_Path,
                               Applet_log)

        # 微信公众号缓存
        samba_obj.download_dir("TcSpace", WeChat_official_account_cache_Shared_Path,
                               WeChat_official_account_cache)

        # 大文件搬家
        samba_obj.download_dir("TcSpace", Big_File_Moving_cache_Shared_Path,
                               Big_File_Moving_cache)

        # 大文件搬家---文件夹搬家
        samba_obj.download_dir("TcSpace", Big_File_Moving_folder_cache_Shared_Path,
                               Big_File_Moving_folder_cache)

        # 软件搬家
        samba_obj.download_dir("TcSpace", SoftWare_Moving_cache_Shared_Path,
                               SoftWare_Moving_cache)

        # # Windows防御
        # samba_obj.download_dir("TcSpace", Windows_Defense_cache_Shared_Path,
        #                        Windows_Defense_cache)
        #
        # # 诊断数据
        # samba_obj.download_dir("TcSpace", Diagnostic_data_cache_Shared_Path,
        #                        Diagnostic_data_cache)

        # 模拟进程占用的进程
        samba_obj.download_dir("TcSpace", Occupy_process_Shared_Path,
                               Occupy_process_Path)

        # kbigfile.dat
        samba_obj.download_dir("TcSpace", kbigfile_Shared_Path,
                               os.path.dirname(DubaFilePath.kbigfile_file_path), norm=False)

        # 构建软件（winRAR32）注册表
        winRAR_regpath = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\WinRAR archiver"
        utils.create_reg_key(regpath=winRAR_regpath)
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"DisplayIcon", value_type=win32con.REG_SZ, value=r"C:\winRAR\WinRAR.exe")
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"DisplayName", value_type=win32con.REG_SZ, value=r"WinRAR 6.01 (32-位)")
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"DisplayVersion", value_type=win32con.REG_SZ, value=r"6.01.0")
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"InstallLocation", value_type=win32con.REG_SZ, value=r'C:\winRAR"\"')
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"Language", value_type=win32con.REG_DWORD, value=0)
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"NoModify", value_type=win32con.REG_DWORD, value=1)
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"NoRepair", value_type=win32con.REG_DWORD, value=1)
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"Publisher", value_type=win32con.REG_SZ, value=r"win.rar GmbH")
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"UninstallString", value_type=win32con.REG_SZ, value=r"C:\winRAR\uninstall.exe")
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"VersionMajor", value_type=win32con.REG_DWORD, value=6)
        utils.set_reg_value(regpath=winRAR_regpath,
                            keyname=r"VersionMinor", value_type=win32con.REG_DWORD, value=1)

        while True:
            ret1 = os.path.exists(Check_File_ksysslim)  # 判断是否下拉垃圾清理文件成功
            ret2 = os.path.exists(Check_File_bigfile)  # 判断是否下拉大文件搬家文件成功
            ret3 = os.path.exists(Check_SoftWare)  # 判断是否下拉软件搬家文件成功
            if ret1 and ret2 and ret3:
                log.log_info("下拉文件成功，文件存在")
                break
        return ret1 and ret2


class CSlimmingPage(BasePage):
    def __init__(self, do_pre_open=True, page_desc=None, delay_sec=0, is_monitor_perf=True, from_bbx=False):
        self.from_bbx = from_bbx
        super().__init__(do_pre_open=do_pre_open, page_desc=page_desc, delay_sec=delay_sec,
                         is_monitor_perf=is_monitor_perf)

    def pre_open(self):
        # TODO：执行打开动作
        # 从vip页面打开
        if not self.from_bbx:
            self.vp = vip_page.vip_page()
            self.vp.c_slimming_click()
        # 从百宝箱打开
        else:
            self.bbx = baibaoxiang_page()
            self.bbx.c_slimming_click()

    @page_method_record("判断是否进入到C盘瘦身主界面")
    def is_C_slimming_main_page(self):
        try_max = 30
        try_num = 1
        result = True
        while not self.is_thin_button_exist():
            if not try_num < try_max:
                result = False
                log.log_info("30s内未完成C盘瘦身扫描")
                break
            perform_sleep(1)
            try_num += 1
        return result

    @page_method_record("判断一键瘦身按钮是否存在")
    def is_thin_button_exist(self):
        if not utils.find_element_by_pic(self.get_page_shot("thin_button.png"), sim=0.8, retry=2)[0]:
            return False
        return True

    @page_method_record("点击界面关闭按钮")
    def exit_button_click(self):
        return utils.click_element_by_pic(self.get_page_shot("exit.png"), sim=0.85, retry=3)

    @page_method_record("判断是否存在未清理点击关闭确认窗")
    def is_exit_sure_pop_exist(self):
        if not utils.find_element_by_pic(self.get_page_shot("exit_sure_pop.png"), sim=0.8, retry=2)[0]:
            return False
        return True

    @page_method_record("关闭退出确认窗")
    def close_exit_sure_pop(self):
        if utils.click_element_by_pic(self.get_page_shot("sure_button.png"), sim=0.8, retry=3):
            utils.perform_sleep(1)
            if not self.is_exit_sure_pop_exist():
                return True
            else:
                return False
        else:
            return False

    def page_confirm_close(self):
        # 首次关闭工具时，查找并关闭服务评分弹窗
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.SERVICE_SCORE, hwnd=self.hwnd):
            perform_sleep(1)
            return

        # 关闭创建桌面快捷方式提示
        if self.count_page_close < 1 and \
                UnexpectedPopup.popup_process(UnexpectedPopupInfo.QUICK_LINK, hwnd=self.hwnd):
            perform_sleep(1)
            return

        # 关闭页面的二次确认
        confirm_find_result, exit_confirm_position = utils.find_element_by_pic(self.get_page_shot("exit_ok.png"),
                                                                               sim=0.8,
                                                                               retry=2, hwnd=self.hwnd,
                                                                               sim_no_reduce=True)
        if not confirm_find_result:
            return
        utils.mouse_click(exit_confirm_position)
        utils.mouse_move(0, 0)

        log.log_info("点击关闭c盘瘦身二次确认按钮成功")
        perform_sleep(2)

    @page_method_record("执行垃圾清理")
    def click_to_slimming(self, check_user=True):
        # scan_result, position = utils.find_element_by_pic(self.get_page_shot("scan_successful.png"), sim=0.7,
        #                                                   sim_no_reduce=True, retry=15)
        # if not scan_result:
        #     return False
        # else:
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_slimming.png"))
        if result:
            log.log_pass("点击一键瘦身成功")
        self.close_clean_alert_prompt(CleanAlertPromptCloseType.NOT_CLEAN_NOW)
        if result and check_user:
            result = self.check_user()
        return result

    @page_method_record("执行大文件搬家")
    def click_to_slimming_bigfilemoving(self):
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_bigfiletab.png"), sim_no_reduce=True)
        if not result:
            log.log_info("没找到大文件搬家tab页！请检查是否只有一个本地磁盘或者是否存在tab图标")
            return False
        log.log_info("点击大文件搬家tab页成功", screenshot=True)
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_moving.png"))  # 点击一键搬家
        return result

    @page_method_record("执行软件搬家")
    def click_to_software_moving(self):
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_softwaretab.png"), sim_no_reduce=True)
        if not result:
            log.log_info("没找到软件搬家tab页！请检查是否只有一个本地磁盘或者是否存在tab图标")
            return False
        log.log_info("点击软件搬家tab页成功", screenshot=True)
        position = utils.find_element_by_pic(self.get_page_shot("software_moving_select_winrar.png"))  # 选择winRAR
        log.log_info("点击大文件搬家还原全选框")
        utils.mouse_click_int(position[1][0] - 90, position[1][1])
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_moving.png"))  # 点击一键搬家
        return result

    # c盘瘦身会员中心
    @page_method_record("点击会员中心")
    def vip_center_click(self):
        return utils.click_element_by_pics([self.get_page_shot("nor_center.png"), self.get_page_shot("vip_center.png"),
                                            self.get_page_shot("button_login.png")], retry=3,
                                           sim_no_reduce=True)

    @page_method_record("检查用户状态")
    def check_user(self):
        if UnexpectedPopup.popup_process(UnexpectedPopupInfo.EXIT_VIP_UPDATE, hwnd=self.hwnd):
            log.log_info("c盘瘦身页面：账号需要升级")
            perform_sleep(1)
            return False

        login_find_result, _ = utils.find_element_by_pic(get_page_shot("login_page", "tab_login_logo.png"), sim=0.9,
                                                         sim_no_reduce=True, retry=3)
        if login_find_result:
            log.log_info("c盘瘦身页面：发现快速登录弹窗")
            lp = login_page.LoginPage(False)
            # TODO 这里登录的是普通用户，还是无法使用瘦身，如果有VIP账号可以自行登录，或者等默认的VIP账号登录
            if lp.normal_user_login():
                log.log_info("c盘瘦身页面：登录账号成功")
            else:
                log.log_info("c盘瘦身页面：登录账号失败")
            return False

    @page_method_record("点击登录按钮")
    def click_login_button(self):
        return utils.click_element_by_pic(self.get_page_shot("login_button.png"))

    @page_method_record("点击升级会员按钮")
    def click_upgrade_vip_button(self):
        return utils.click_element_by_pic(self.get_page_shot("upgrade_vip_button.png"))

    @page_method_record("点击继续清理按钮")
    def click_continue_button(self):
        return utils.click_element_by_pic(self.get_page_shot("button_click_to_continue.png"))

    @page_method_record("点击开始扫描按钮")
    def click_scan_button(self):
        return utils.click_element_by_pic(self.get_page_shot("button_scan.png"))

    @page_method_record("判断是否在搬家中或者还原中")
    def judge_moving_and_recorving(self):
        finish = False
        for i in range(20):
            find_result, position = utils.find_element_by_pic(self.get_page_shot("moving_and_recovering_sign.png"),
                                                              sim_no_reduce=True, retry=3,
                                                              location=Location.LEFT_UP.value)
            if not find_result:  # 找不到元素，跳出循环
                finish = True
                break
            log.log_info("搬家或还原中..........")
            perform_sleep(5)
        assert finish, log.log_info("搬家/还原操作超时（100s）", need_assert=False)

    @page_method_record("查找并关闭清理风险提醒弹窗")
    def close_clean_alert_prompt(self, close_type=CleanAlertPromptCloseType.NOT_CLEAN_NOW):
        """
        查找并关闭清理风险提醒弹窗
        @param close_type: 弹窗关闭方式
        @return:
        """
        find_result, position = utils.find_element_by_pic(self.get_page_shot("clean_alert_prompt_tab_logo.png"),
                                                          sim_no_reduce=True, retry=3, location=Location.LEFT_UP.value)

        if find_result:
            if close_type == CleanAlertPromptCloseType.CLOSE_DIRECTLY:
                log.log_info("直接关闭清理风险提醒弹窗")
                utils.mouse_click(position[0] + 664, position[1] + 16)
            elif close_type == CleanAlertPromptCloseType.NOT_CLEAN_NOW:
                log.log_info("点击暂不清理按钮")
                utils.click_element_by_pic(self.get_page_shot("not_clean_now_button.png"), sim_no_reduce=True, retry=5)

    @page_method_record("检查系统盘瘦身(微信专清)功能是否有效")
    def ksysslim_check_clean(self):

        # 执行清理，结束后的界面判断
        # clean_result, position = utils.find_element_by_pic(self.get_page_shot("button_click_to_continue.png"),
        #                                                    sim_no_reduce=True, retry=10,
        #                                                    location=Location.LEFT_UP.value)
        res = self.check_clean_finished()  # 检查界面显示结束，是否清理超时
        if not res:
            log.log_info("扫描结束，界面显示不符合预期，请检查clean_finished.png")
            return False
        res = self.check_ksyshelper_exit()  # 检查界面显示结束后ksyshelper是否退出
        if not res:
            log.log_info("扫描结束，ksyshelper64.exe或者ksyshelper.exe无退出")
            return False
        find_result = os.path.exists(Check_File_ksysslim)
        if find_result:
            log.log_info("C盘瘦身清理(微信专清)失败!!，微信专清文件依旧存在")
            return False
            # 文件存在，证明清除失败
        log.log_info("微信专清模拟文件已被清除")
        return True

    @page_method_record("检查大文件搬家功能是否有效")
    def big_file_moving_check_clean(self):

        self.judge_moving_and_recorving()

        find_result, position = utils.find_element_by_pic(self.get_page_shot("end_of_moving.png"),  # 搬家成功标识
                                                          sim_no_reduce=True, retry=5, location=Location.LEFT_UP.value)
        find_result2 = utils.is_symlink_dir(Check_File_bigfile)  # 存在软链接(返回 True)就是搬家成功

        if not find_result:
            log.log_info("大文件搬家搬家失败！！无找到搬家成功标识")
            return find_result

        if not find_result2:
            log.log_info("大文件搬家搬家失败！！无找到创建的软链接")
            return find_result2

        print(find_result2)

        log.log_info("点击大文件搬家搬家记录")
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_moving_records.png"))
        if result:
            utils.perform_sleep(1)
            log.log_info("进入搬家记录成功", screenshot=True)
        position = utils.find_element_by_pic(self.get_page_shot("ksysslim_moving_icon.png"))
        log.log_info("点击大文件搬家还原全选框")

        utils.mouse_click_int(position[1][0] - 47, position[1][1] + 70)

        log.log_info("点击大文件搬家还原按钮")
        utils.click_element_by_pic(self.get_page_shot("button_click_to_reduction.png"))

        self.judge_moving_and_recorving()

        find_result = utils.find_element_by_pics([self.get_page_shot("recovery_was_successful.png"),
                                                  self.get_page_shot("recovery_was_successful2.png")],
                                                 sim_no_reduce=True, retry=5,
                                                 location=Location.LEFT_UP.value)[0]

        if not find_result:
            log.log_info("大文件搬家还原失败！！")
            return find_result
        else:
            log.log_info("大文件搬家还原成功")
            perform_sleep(3)
            utils.keyboardInputAltF4()
            perform_sleep(1)
            utils.keyboardInputAltF4()
            return find_result

    @page_method_record("检查进程占用提示是否弹出")
    def check_pop_occupy_tab(self):
        res = utils.find_element_by_pic(self.get_page_shot("occupy_tab.png"), sim_no_reduce=True, retry=3)
        if res:
            log.log_info("弹出进程占用提示")
            return res
        log.log_info("没有弹出进程占用提示")
        return res

    def click_occupy_btn(self, close_process=True):
        """
        操作进程占用提示弹窗，默认关闭进程
        :param close_process: 是否点击关闭进程，默认点击
        :return:
        """
        if not self.check_pop_occupy_tab():
            return
        if close_process:
            log.log_info("点击“关闭并搬家”")
            utils.click_element_by_pic(self.get_page_shot("close_occupy.png"), sim_no_reduce=False, retry=3)
        else:
            log.log_info("点击“关闭并搬家”")
            utils.click_element_by_pic(self.get_page_shot("no_close_occupy.png"), sim_no_reduce=False, retry=3)

    @page_method_record("检查软件搬家功能是否有效")
    def software_moving_check_clean(self):
        self.judge_moving_and_recorving()

        find_result, position = utils.find_element_by_pic(self.get_page_shot("end_of_moving.png"),  # 搬家成功标识
                                                          sim_no_reduce=True, retry=5, location=Location.LEFT_UP.value)
        if not find_result:
            log.log_info("软件搬家搬家失败！！没出现搬家成功标识，图片: end_of_moving.png")
            return find_result

        # res1 = utils.is_symlink_dir(Check_File_bigfile)
        # if res1:
        #     log.log_info("软件搬家成功，已创建软连接")
        # else:
        #     log.log_info("软件搬家搬家失败！！创建软连接失败！！")
        #     return False

        log.log_info("软件搬家成功")
        log.log_info("点击软件搬家搬家记录")
        result = utils.click_element_by_pic(self.get_page_shot("button_click_to_moving_records.png"))
        if result:
            utils.perform_sleep(1)
            log.log_info("进入搬家记录成功", screenshot=True)
        position = utils.find_element_by_pic(self.get_page_shot("software_recovering_select_winrar.png"))
        log.log_info("软件搬家还原页面勾选winRAR")
        utils.mouse_click_int(position[1][0] - 42, position[1][1])
        log.log_info("点击软件搬家还原按钮")
        utils.click_element_by_pic(self.get_page_shot("button_click_to_reduction.png"))

        self.judge_moving_and_recorving()

        find_result = utils.find_element_by_pics([self.get_page_shot("recovery_was_successful.png"),
                                                  self.get_page_shot("recovery_was_successful2.png")],
                                                 sim_no_reduce=True, retry=5,
                                                 location=Location.LEFT_UP.value)[0]

        if not find_result:
            log.log_info("软件搬家还原失败！！界面标识没有符合预期")
            return False

        res2 = utils.is_symlink_dir(SoftWare_Moving_cache)
        if not res2:
            log.log_info("软件搬家还原失败！！软链接没还原")
            return False

        log.log_info("软件搬家还原成功,软连接成功删除")
        perform_sleep(3)
        utils.keyboardInputAltF4()
        perform_sleep(1)
        utils.keyboardInputAltF4()
        return find_result

    @page_method_record("(反复)进行扫描和退出")
    def scan_check(self, manual_scanning=False):
        """
        :param manual_scanning: 是否手动启动进程并点击扫描
        :return:
        """
        if manual_scanning:
            utils.process_start(DubaFilePath.ksysslim_file_path, async_start=True)
            for i in range(20):
                perform_sleep(1)
                result = utils.click_element_by_pic(self.get_page_shot("button_scan.png"), retry=3, hwnd=None)
                if result:
                    break
        ret = self.is_C_slimming_main_page()
        if not ret:
            return False
        result = utils.click_element_by_pic(self.get_page_shot("exit.png"), retry=2)
        if not result:
            log.log_info("找不到关闭按钮")
        result = utils.click_element_by_pic(self.get_page_shot("exit_ok.png"), retry=2)
        if not result:
            log.log_info("弹出非预期弹窗，关闭该弹窗后，手动关闭ksysslim.exe进程")
            UnExpectWin_System().unexpectwin_detect_beta()
            utils.kill_process_by_name("ksysslim.exe")

    @page_method_record("点击扫描后杀ksysslim.exe")
    def scan_check_forced_exit(self, click_scan=False):
        """
        :param click_scan: 是否先点击扫描按钮，默认不点击
        :return:
        """
        if click_scan:
            utils.process_start(DubaFilePath.ksysslim_file_path, async_start=True)
            res = utils.click_element_by_pic(self.get_page_shot("button_scan.png"), sim=0.8, retry=3, hwnd=None)
            if not res:
                return
        utils.kill_process_by_name("ksysslim.exe")

    @page_method_record("点击关闭按钮")
    def click_exit_btn(self):
        return utils.click_element_by_pic(self.get_page_shot("exit.png"))

    @page_method_record("从界面判断是否清理结束")
    def check_clean_finished(self):
        for i in range(110):
            res = utils.find_element_by_pic(self.get_page_shot("clean_finished.png"), sim_no_reduce=True, retry=1)[0]
            if res:
                log.log_info("界面已显示清理结束")
                return True
        log.log_info("清理已超过2分钟，是否异常请检查")
        return False

    def check_ksyshelper_exit(self):
        """
        判断ksyshelper64.exe，ksyshelper.exe是否退出
        :return:
        """
        for i in range(60):
            utils.perform_sleep(1)
            res1 = utils.is_process_exists("ksyshelper.exe")
            res2 = utils.is_process_exists("ksyshelper64.exe")
            if not res2 and not res1:
                log.log_info("进程ksyshelper.exe，ksyshelper64.exe已退出")
                return True
        return False


class dgCSlimmingPage(CSlimmingPage):
    def pre_open(self):
        dgpath = find_dgpath_by_reg()
        dgdir = os.path.dirname(dgpath)
        ksysslim_path = os.path.join(dgdir, "ksysslim.exe")
        utils.process_start(ksysslim_path, async_start=True)


if __name__ == '__main__':
    ga = CreateGarbage()
    ga.create_garbage()
    utils.process_start(os.path.join(Occupy_process_Path, "npp.7.6.3.Installer.exe"), async_start=True)
    res = utils.is_process_exists("npp.7.6.3.Installer.exe")
    print(res)

    test = CSlimmingPage()
    test.click_to_slimming_bigfilemoving()
    test.click_occupy_btn()

    res = utils.is_process_exists("npp.7.6.3.Installer.exe")
    print(res)
