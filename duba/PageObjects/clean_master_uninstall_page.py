import os

from common import utils
from common.basepage import BasePage, page_method_record
from common.log import log
import win32con


class KcleanMasterUnInstall(BasePage):
    regroot = win32con.HKEY_LOCAL_MACHINE
    regpath_64 = r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\cmpc"
    regpath_32 = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\cmpc"
    unin_str_keyname = "UninstallString"

    def pre_open(self):
        prg = r'C:\Program Files (x86)'  # 64位系统专有文件夹
        if os.path.exists(prg):
            res = utils.query_reg_value(regroot=self.regroot, regpath=self.regpath_64, keyname=self.unin_str_keyname)
        else:
            res = utils.query_reg_value(regroot=self.regroot, regpath=self.regpath_32, keyname=self.unin_str_keyname)
        start_result = utils.process_start(res, async_start=True)
        print(start_result)
        if start_result:
            log.log_pass("执行卸载exe成功")
        else:
            log.log_error("卸载执行exe失败！！")

    @page_method_record("执行清理大师执行卸载")
    def uninstall(self):
        find_result, pos = utils.find_element_by_pic(self.get_page_shot("tab_logo.png"),
                                                     sim_no_reduce=False, retry=3)
        if find_result:
            click_result = utils.click_element_by_pic(self.get_page_shot("uninstall_confirm.png"),
                                                      sim_no_reduce=False, retry=5)
            log.log_info("点击确认卸载")
            if click_result:
                utils.perform_sleep(5)
                utils.click_element_by_pic(self.get_page_shot("finish.png"),
                                           sim_no_reduce=True, retry=15)
                log.log_info("卸载已完成")
                utils.perform_sleep(3)
                proc = utils.is_process_exists("uni0nst.exe")
                if proc:
                    log.log_error("卸载后3秒，卸载进程没退出")
                    # utils.set_reg_value(regpath=duba_reg,keyname="ProgramPath", value=ProgramPath_value)
                    return False
                else:
                    log.log_info("卸载进程已退出")
                    # utils.set_reg_value(regpath=duba_reg,keyname="ProgramPath", value=ProgramPath_value)
                    return True
            else:
                log.log_error("没找到确认卸载按钮")
                # utils.set_reg_value(regpath=duba_reg,keyname="ProgramPath", value=ProgramPath_value)
                return False
        else:
            log.log_error("没找到卸载界面")
            # utils.set_reg_value(regpath=duba_reg,keyname="ProgramPath", value=ProgramPath_value)
            return False


if __name__ == '__main__':
    ProgramPath_value = r"C:\program files (x86)\kingsoft\kingsoft antivirus\""
    utils.set_reg_value(regpath=duba_reg, keyname="ProgramPath", value=ProgramPath_value)

    # ProgramPath_value = utils.query_reg_value(regpath=duba_reg, keyname="ProgramPath")

    # utils.remove_reg_value(regpath=duba_reg, value="ProgramPath")

    # process = utils.is_process_exists("uni0nst.exe")
    # print(process)
