from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
from common.contants import InputLan
import os
import platform
import win32gui


# 返回360安装目录
def get_360_path():
    if os.path.exists(r'C:\Program Files (x86)'):
        num_reg_path = r'SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\360安全卫士'
    else:
        num_reg_path = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\360安全卫士'
    num_install_path = utils.query_reg_value(regpath=num_reg_path, keyname='InstallLocation')
    if num_install_path:
        log.log_info("找到360安装路径", attach=False)
        return num_install_path
    else:
        log.log_error("没有找到360安装路径", attach=False)
        return "test"


# 传入一个值找到对应注册表位置
def get_360_regpath(key_name):
    if os.path.exists(r'C:\Program Files (x86)'):
        num_reg = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\WOW6432Node\\360Safe\\' + key_name
    else:
        num_reg = 'HKEY_LOCAL_MACHINE\\SOFTWARE\\360Safe\\' + key_name
    return num_reg


# 清理指定位置信息并拷贝信息进去
def clear_and_input(x, y, info):
    utils.mouse_click(x, y)
    utils.perform_sleep(0.2)
    utils.keyboardInputCtrlA()
    utils.keyboardInputByCode("backspace")
    utils.perform_sleep(0.2)
    utils.copy_to_clipboard(info)
    utils.perform_sleep(0.2)
    utils.key_paste()


class KsapiToolPage(BasePage):
    def __init__(self, fantasy_ksapi_dubapath):
        self.num_path = get_360_path()
        self.ksapi_path = fantasy_ksapi_dubapath
        super().__init__()

    def pre_open(self):
        # TODO：执行打开动作
        os.chdir(os.path.dirname(self.ksapi_path))
        utils.process_start("fantasy_ksapi", async_start=True)
        utils.perform_sleep(3)
        num_defend_hwnd = utils.get_hwnd_by_class('Q360HIPSClass', None)
        if num_defend_hwnd != None:
        # num_defend = utils.find_element_by_pic(self.get_page_shot("num_defend.png"), sim=0.9, hwnd=num_defend_hwnd)
        # if num_defend[0]:
            num_defend_pos = utils.get_pos_by_hwnd(num_defend_hwnd)
            log.log_info('数字阻止弹窗出现')
            utils.mouse_click(num_defend_pos[0] + 517, num_defend_pos[1] + 285)
            utils.perform_sleep(2)
            utils.mouse_click(num_defend_pos[0] + 517, num_defend_pos[1] + 372)
            utils.perform_sleep(2)
            num_control_center = utils.find_element_by_pic(self.get_page_shot("num_control_center.png"), sim=0.7)
            utils.perform_sleep(1)
            if num_control_center[0]:
                utils.mouse_click(num_control_center[1][0] + 700, num_control_center[1][1])
                utils.perform_sleep(1)
            if not utils.is_process_exists('fantasy_ksapi.exe'):
                utils.process_start("fantasy_ksapi", async_start=True)
                utils.perform_sleep(3)
        self.check_result('加载ksapi.dll')



    @page_method_record("执行结束进程操作")
    def click_kill_process(self):
        num_pid = utils.get_pid('360Tray.exe')
        if not num_pid:
            num_pid = utils.get_pid('360tray.exe')
            if not num_pid:
                num_pid = 999999999999
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("teminate_button.png"), sim=0.9)
        if is_find:
            utils.mouse_click(positions[0] - 200, positions[1])
            utils.change_input_lan(InputLan.EN)
            utils.key_input(str(num_pid))
            utils.click_element_by_pic(self.get_page_shot("teminate_button.png"))
            self.check_result("结束进程操作")
        else:
            log.log_info("没有找到对应图片")

    @page_method_record("执行删除文件1操作")
    def click_delete_file1(self):
        file_path = os.path.join(self.num_path, "360DeskAna.exe")
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("deleteFile1_button.png"), sim=0.9)
        if is_find:
            # file_path = "C:\\Users\\CF\\Desktop\\123\\123.txt"
            clear_and_input(positions[0] - 240, positions[1], file_path)
            utils.click_element_by_pic(self.get_page_shot("deleteFile1_button.png"))
            self.check_result("删除文件1操作")

    @page_method_record("执行删除文件2操作")
    def click_delete_file2(self):
        file_path = os.path.join(self.num_path, "360DeskAna64.exe")
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("deleteFile2_button.png"), sim=0.9)
        if is_find:
            # file_path = "C:\\Users\\CF\\Desktop\\123\\456.txt"
            clear_and_input(positions[0] - 240, positions[1], file_path)
            utils.click_element_by_pic(self.get_page_shot("deleteFile2_button.png"))
            self.check_result("删除文件2操作")

    @page_method_record("执行写入文件操作")
    def click_write_file(self):
        file_path = os.path.join(self.num_path, "updatecfg.ini")
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("writeFile_button.png"), sim=0.9)
        if is_find:
            # file_path = "C:\\Users\\CF\\Desktop\\123\\1231.txt"
            clear_and_input(positions[0] - 385, positions[1], file_path)
            utils.perform_sleep(1)
            clear_and_input(positions[0] - 205, positions[1], 'test')
            utils.click_element_by_pic(self.get_page_shot("writeFile_button.png"))
            self.check_result("写入文件操作")

    @page_method_record("执行读取文件操作")
    def click_read_file(self):
        file_path = os.path.join(self.num_path, "updatecfg.ini")
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("readFile_button.png"), sim=0.9)
        if is_find:
            # file_path = "C:\\Users\\CF\\Desktop\\123\\1231.txt"
            clear_and_input(positions[0] - 385, positions[1], file_path)
            utils.click_element_by_pic(self.get_page_shot("readFile_button.png"))
            self.check_result("读取文件操作")

    @page_method_record("执行删除key操作")
    def click_delete_key(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("deleteKey_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('360IA')
            # num_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\123'
            clear_and_input(positions[0], positions[1] - 30, num_reg)
            utils.click_element_by_pic(self.get_page_shot("deleteKey_button.png"))
            self.check_result("执行删除key操作")

    @page_method_record("执行EumValue操作")
    def click_eum_value(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("enumValue_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('360Scan')
            # num_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\CmGamebox'
            clear_and_input(positions[0], positions[1] - 30, num_reg)
            utils.click_element_by_pic(self.get_page_shot("enumValue_button.png"))
            self.check_result("执行EumValue操作")
            self.click_open_key()
            self.click_open_key_Ex()
            self.click_eum_key()
            self.click_eum_keyEx()

    @page_method_record("执行openKey操作")
    def click_open_key(self):
        utils.click_element_by_pic(self.get_page_shot("openKey_button.png"))
        self.check_result("执行openKey操作")

    @page_method_record("执行openKeyEx操作")
    def click_open_key_Ex(self):
        utils.click_element_by_pic(self.get_page_shot("openKeyEx_button.png"))
        self.check_result("执行openKeyEx操作")

    @page_method_record("执行enumKey操作")
    def click_eum_key(self):
        utils.click_element_by_pic(self.get_page_shot("enumKey_button.png"))
        utils.perform_sleep(2)
        self.check_result("执行enumKey操作")

    @page_method_record("执行enumKeyEx操作")
    def click_eum_keyEx(self):
        utils.click_element_by_pic(self.get_page_shot("enumKeyEx_button.png"))
        utils.perform_sleep(2)
        self.check_result("执行enumKeyEx操作")

    @page_method_record("执行创建key操作")
    def click_create_key(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("createKey_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('test')
            # num_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\456'
            clear_and_input(positions[0], positions[1] - 96, num_reg)
            utils.click_element_by_pic(self.get_page_shot("createKey_button.png"))
            self.check_result("执行创建key操作")

    @page_method_record("执行创建keyEx操作")
    def click_create_key_Ex(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("createKeyEx_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('test2')
            # num_inst_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\789'
            clear_and_input(positions[0], positions[1] - 96, num_reg)
            utils.click_element_by_pic(self.get_page_shot("createKeyEx_button.png"))
            self.check_result("执行创建keyEx操作")

    @page_method_record("执行删除value操作")
    def click_delete_value(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("deleteValue_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('Coop')
            # num_inst_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\789'
            clear_and_input(positions[0], positions[1] - 42, num_reg)
            utils.perform_sleep(1)
            clear_and_input(positions[0] + 246, positions[1] - 42, "insttime")
            utils.click_element_by_pic(self.get_page_shot("deleteValue_button.png"))
            self.check_result("执行删除value操作")

    @page_method_record("执行设置value操作")
    def click_set_value(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("setValueEx_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('Coop')
            # num_inst_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\78910'
            clear_and_input(positions[0] - 180, positions[1] - 42, num_reg)
            utils.perform_sleep(1)
            clear_and_input(positions[0], positions[1] - 42, "test")
            utils.perform_sleep(1)
            clear_and_input(positions[0] + 117, positions[1] - 42, "123")
            utils.click_element_by_pic(self.get_page_shot("setValueEx_button.png"))
            self.check_result("执行设置value操作")

    @page_method_record("执行查询value操作")
    def click_query_value(self):
        is_find, positions = utils.find_element_by_pic(self.get_page_shot("queryValueEx_button.png"), sim=0.9)
        if is_find:
            num_reg = get_360_regpath('Coop')
            # num_inst_reg = r'HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\7-Zip\78910'
            clear_and_input(positions[0], positions[1] - 70, num_reg)
            utils.perform_sleep(1)
            clear_and_input(positions[0] + 246, positions[1] - 70, "ipartner")
            utils.click_element_by_pic(self.get_page_shot("queryValueEx_button.png"))
            self.check_result("执行查询value操作")

    def check_result(self, case_name):
        utils.perform_sleep(2)
        hwnd = utils.get_hwnd_by_class(None, 'fantasy_ksapi')
        staticHwnd = win32gui.FindWindowEx(hwnd, None, 'Static', None)
        text = win32gui.GetWindowText(staticHwnd)
        if '成功' in text:
            utils.keyboardInputEnter()
            log.log_pass(case_name + '案例通过')
        elif hwnd is None:
            log.log_error(case_name + '找不到句柄', need_assert=False)
        else:
            utils.keyboardInputEnter()
            log.log_error(case_name + '案例失效', need_assert=False)
        utils.perform_sleep(2)