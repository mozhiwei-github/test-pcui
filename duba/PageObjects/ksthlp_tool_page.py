import configparser
from common.log import log
from common import utils
from common.basepage import BasePage, page_method_record
import os
import win32gui
from common.tools.pop_tools import BasePop
from common.utils import Location


def start_get_WriteMemoryTest():
    os.popen('start ' + os.path.join(os.getcwd(), 'defendtool', 'WriteMemoryTest.exe'))
    utils.perform_sleep(5)
    isFind, position = utils.find_element_by_pic(
        pic=os.path.join(os.getcwd(), "duba", "PageShot", 'ksthlp_tool_page', 'current_address.png'),
        location=Location.RIGHT_UP.value)
    print(isFind)
    utils.mouse_drag((position[0] + 20, position[1] + 5), (position[0] + 60, position[1] + 5))
    utils.key_copy()
    utils.mouse_click((position[0] + 741, position[1] - 16))


def kill_test_exe():
    if utils.is_process_exists('ProcessHollowing.exe'):
        process_id = utils.get_pid('ProcessHollowing.exe')
        os.system("taskkill /PID %s /F /T" % (process_id))


def retry_start_test(test_path):
    for i in range(10):
        print('重新打开第' + str(i + 1) + '次')
        utils.process_start('start ' + test_path, async_start=True)
        utils.perform_sleep(2)
        text_hwnd = utils.get_hwnd_by_class(None, 'Hello World')
        if text_hwnd is not None:
            print('成功打开')
            utils.perform_sleep(5)
            break
        else:
            kill_test_exe()
            utils.perform_sleep(2)


class KsthlpToolPage(BasePage):
    def __init__(self, TestDlg_self_sign_dubapath):
        self.left = 0
        self.top = 0
        self.ksthlp_path = TestDlg_self_sign_dubapath
        super().__init__()

    def pre_open(self):
        # TODO：执行打开动作
        utils.process_start(os.path.join(os.path.dirname(self.ksthlp_path), "TestDlg_self_sign.exe"), async_start=True)

    @page_method_record("获取TestDlg坐标")
    def get_TestDlg_positions(self):
        TestDlg_hwnd = utils.get_hwnd_by_class(None, 'TestDlg')
        if TestDlg_hwnd is not None:
            self.left = win32gui.GetWindowRect(TestDlg_hwnd)[0]
            print(self.left)
            self.top = win32gui.GetWindowRect(TestDlg_hwnd)[1]
            print(self.top)
        else:
            log.log_error('找不到TestDlg界面')

    # 获取控件内容
    @page_method_record("获取控件内容")
    def get_edit_text(self):
        utils.mouse_dclick(self.left + 340, self.top + 500)
        utils.keyboardInputCtrlA()
        utils.perform_sleep(0.1)
        utils.key_copy()
        utils.perform_sleep(0.1)
        text = utils.get_clipboard_text()
        return text

    @page_method_record("点击初始化按钮操作")
    def click_init_button(self):
        utils.mouse_click(self.left + 26, self.top + 43)
        utils.perform_sleep(1)
        utils.mouse_click(self.left + 26, self.top + 58)
        utils.perform_sleep(2)
        TestDlg_self_sign_tips_hwnd = utils.get_hwnd_by_class(None, 'TestDlg_self_sign')
        Static_hwnd = win32gui.FindWindowEx(TestDlg_self_sign_tips_hwnd, None, 'Static', None)
        text = win32gui.GetWindowText(Static_hwnd)
        print(text)
        if 'success' in text:
            log.log_pass('TestDlg初始化成功')
            utils.keyboardInputEnter()
        else:
            log.log_error('TestDlg初始化失败')
            utils.keyboardInputEnter()

    @page_method_record("点击检测所有进程shellcode操作")
    def click_all_proc_shellcode(self):
        utils.mouse_click(self.left + 585, self.top + 140)
        utils.perform_sleep(3)
        text = self.get_edit_text()
        print(text)
        if text != '':
            log.log_pass('检测所有进程shellcode操作成功')
        else:
            log.log_error('检测所有进程shellcode操作失败', need_assert=False)

    @page_method_record("点击检测进程shellcode操作")
    def click_proc_shellcode(self):
        test_pid = utils.get_pid('TestDlg_self_sign.exe')
        utils.copy_to_clipboard(str(test_pid))
        utils.mouse_click(self.left + 160, self.top + 85)
        utils.perform_sleep(1)
        utils.key_paste()
        utils.perform_sleep(1)
        utils.mouse_click(self.left + 584, self.top + 78)
        utils.perform_sleep(2)
        text = self.get_edit_text()
        print(text)
        if text != '':
            log.log_pass('检测进程shellcode操作成功')
        else:
            log.log_error('检测进程shellcode操作失败', need_assert=False)

    @page_method_record("点击获取进程句柄操作")
    def click_get_proc_handle(self):
        utils.mouse_click(self.left + 350, self.top + 180)
        utils.perform_sleep(1)
        text = self.get_edit_text()
        print(text)
        log.log_info('获取进程句柄' + text)
        if 'success' in text:
            log.log_pass('获取进程句柄操作成功')
        else:
            log.log_error('获取进程句柄操作失败', need_assert=False)

    @page_method_record("点击打开进程操作")
    def click_open_proc(self):
        utils.mouse_click(self.left + 505, self.top + 178)
        utils.perform_sleep(1)
        text = self.get_edit_text()
        print(text)
        log.log_info('打开进程' + text)
        if 'success' in text:
            log.log_pass('获取打开进程操作成功')
        else:
            log.log_error('获取打开进程操作失败', need_assert=False)

    @page_method_record("点击关闭进程操作")
    def click_close_proc(self):
        utils.mouse_click(self.left + 666, self.top + 180)
        utils.perform_sleep(1)
        text = self.get_edit_text()
        print(text)
        log.log_info('关闭进程' + text)
        if 'success' in text:
            log.log_pass('关闭进程操作成功')
        else:
            log.log_error('关闭进程操作失败', need_assert=False)

    @page_method_record("点击读内存操作")
    def click_read(self):
        start_get_WriteMemoryTest()
        utils.perform_sleep(2)
        utils.mouse_click(self.left + 168, self.top + 134)
        utils.key_paste()
        utils.perform_sleep(0.5)
        writememory_pid = utils.get_pid('WriteMemoryTest.exe')
        print('writememory_pid:' + str(writememory_pid))
        utils.copy_to_clipboard(str(writememory_pid))
        utils.mouse_click(self.left + 168, self.top + 90)
        utils.keyboardInputCtrlA()
        utils.perform_sleep(0.5)
        utils.keyboardInputDel()
        utils.perform_sleep(0.5)
        utils.key_paste()
        utils.perform_sleep(1)
        utils.copy_to_clipboard('10')
        utils.mouse_click(self.left + 168, self.top + 180)
        utils.key_paste()
        utils.perform_sleep(1)
        utils.mouse_click(self.left + 387, self.top + 80)
        text = self.get_edit_text()
        print(text)
        if 'Hello World!' in text:
            log.log_pass('读内存操作成功')
        else:
            log.log_error('读内存操作失败', need_assert=False)

    @page_method_record('点击写内存操作')
    def click_write(self):
        utils.copy_to_clipboard('test')
        utils.mouse_click(self.left + 400, self.top + 300)
        utils.perform_sleep(0.5)
        utils.key_paste()
        utils.perform_sleep(0.5)
        utils.mouse_click(self.left + 388, self.top + 135)
        text = self.get_edit_text()
        if 'success' in text:
            log.log_pass('写内存点击操作成功')
        else:
            log.log_error('写内存点击操作失败', need_assert=False)
        utils.mouse_click(self.left + 387, self.top + 80)
        utils.perform_sleep(0.5)
        text2 = self.get_edit_text()
        if 'test' in text2:
            log.log_pass('写内存操作成功')
        else:
            log.log_error('写内存操作失败', need_assert=False)
        utils.kill_process_by_name('WriteMemoryTest.exe')

    @page_method_record('检查捕风功能')
    def check_bufeng(self, path):
        duba_path = path
        a = os.walk(os.path.join(duba_path, 'ks_dump', 'dll_dump'))
        for folder in a:
            for file in folder[2]:
                if file.startswith('s01598'):
                    os.remove(os.path.join(folder[0], file))
                    print('删除dump成功')
                else:
                    print('没有dump可删除')
        config = configparser.ConfigParser()
        config.read(os.path.join(duba_path, 'windhunter.cfg'), 'utf-8')
        if config.has_section('Sign'):
            print('存在')
            config.remove_section('Sign')
            config.write(open(os.path.join(duba_path, 'windhunter.cfg'), 'w'))
        else:
            print('不存在')
        test_path = os.path.join(os.getcwd(), 'defendtool', 'hollow', 'ProcessHollowing.exe')
        utils.process_start('start ' + test_path, async_start=True)
        utils.perform_sleep(2)
        defendpop = BasePop()
        if defendpop.pop_init:
            defendpop.click_func(520, 168)
            utils.perform_sleep(2)
            retry_start_test(test_path)
        elif utils.get_hwnd_by_class(None, 'Hello World') is None:
            kill_test_exe()
            retry_start_test(test_path)
        else:
            utils.perform_sleep(5)
        kill_test_exe()

        isEffect = False
        a = os.walk(os.path.join(duba_path, 'ks_dump', 'dll_dump'))
        for folder in a:
            for file in folder[2]:
                if file.startswith('s01598'):
                    log.log_pass('捕风功能正常')
                    isEffect = True
                    break
        if not isEffect:
            log.log_error('捕风功能失效', need_assert=False)
